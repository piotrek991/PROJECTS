import asyncio
import os
import unicodedata
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_result
)
from urllib.parse import urlparse
from pathlib import Path
from itertools import islice 
import pprint
import json
import aiofiles as aiof

request_semaphore = asyncio.Semaphore(10)

def is_http_error_to_retry(response):
    if isinstance(response, httpx.Response):
        return response and not (response.status_code == 429 or response.status_code >= 500)
    elif isinstance(response, list):
        return response is None
    else:
        return False

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=(
        retry_if_exception_type(httpx.RequestError) | # Catches network issues, timeouts, generic errors
        retry_if_result(is_http_error_to_retry)       # Catches specific HTTP status codes like 429, 5xx
    ),
    reraise=True
)
async def fetch_json(session: httpx.AsyncClient, url:str, outside_d:dict = None, outside_d_key:str = None):
    print(f"fetching {url}")
    async with request_semaphore:
        response = await session.get(url)
        if response.status_code >= 400 and not is_http_error_to_retry(response):
            response.raise_for_status()
        elif 200 <= response.status_code < 300:
            if outside_d is not None:
                if outside_d_key is not None:
                    outside_d.update({outside_d_key: response.json()})
                else:
                    outside_d.update({'fetch_data': response.json()})
                return outside_d
            else:
                return response.json()
        else:
            return response

async def fetch_json_team_players(session: httpx.AsyncClient, url:str, outside_d:dict):
    players_info_base = f"https://www.transfermarkt.com/quickselect/players/{{num}}"
    l_teams = await fetch_json(session, url)
    l_teams_ids = {
        item.get('id'): {**item} for item in l_teams
    }

    l_task_inner = list()
    for p_id, p_s in l_teams_ids.items():
        l_task_inner.append(asyncio.create_task(fetch_json(session, players_info_base.format(num=p_id), p_s, 'players')))
    data_r = await asyncio.gather(*l_task_inner)
    outside_d.update({'teams_info': data_r})
    return outside_d

async def main():
    headers_page = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    base_link_goto = f"ttps://www.transfermarkt.com{{part_of_the_link}}"
    league_data_base = f"https://www.transfermarkt.com/quickselect/competitions/{{comp_num}}"
    countries_link = f"https://www.transfermarkt.com/quickselect/countries"

    async with httpx.AsyncClient(headers=headers_page) as client:
        countries_data = await fetch_json(client, countries_link)
        countries_ids = {item.get("id"): item.get("name") for item in countries_data}

        #countries_ids = dict(islice(countries_ids.items(), 2))

        tasks = list()
        for c_id, c_name in countries_ids.items():
            tasks.append(asyncio.create_task(fetch_leagues_teams(client, league_data_base.format(comp_num=c_id), {"country_name": c_name, "country_id": c_id})))
        await asyncio.gather(*tasks)

async def fetch_leagues_teams(session: httpx.AsyncClient, url:str, outside_d:dict):
    team_base = f"https://www.transfermarkt.com/quickselect/teams/{{team_id}}"

    comp_id = Path(urlparse(url).path).name
    data_l = (await fetch_json(session, url, {'comp_id': comp_id}))
    data_l = data_l.get('fetch_data')

    f_name_base = f"data_{outside_d.get("country_name").replace(" ", "_").lower()}"

    if not data_l:
        outside_d.update({'fetch_data': data_l})
        return outside_d
    league_d = {
        item.get('id'): (item.get('name'), item.get('link')) for item in data_l
    }
    tasks_inner = list()
    for t_id, (t_name, t_link) in league_d.items():
        tasks_inner.append(asyncio.create_task(fetch_json_team_players(session, team_base.format(team_id=t_id), {'league_id': t_id, 'league_name': t_name, 'league_link':t_link})))

    data_t = await asyncio.gather(*tasks_inner)
    outside_d.update({'fetch_data': data_t})

    os.makedirs('countries_data', exist_ok=True)
    async with aiof.open(os.path.join('countries_data', f_name_base + '.json'), 'w',encoding='utf-8') as out:
        await out.write(json.dumps(outside_d))
        await out.flush()

    # with open(os.path.join('countries_data', f_name_base + '.json'), 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(outside_d))
    return outside_d


if __name__ == '__main__':
    asyncio.run(main())