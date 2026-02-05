import httpx
from lxml import etree
import asyncio
import polars as pl
import pprint
from gen_calendars import gen_calendar
from unidecode import unidecode
import os
import posixpath

pl.Config.set_tbl_width_chars(1000)
pl.Config.set_fmt_str_lengths(1000)

async def get_calendars_info(a_client: httpx.AsyncClient, url:str):
    print(f"processing link {url}")
    data = await a_client.get(url)
    data.raise_for_status()

    r_processed = await asyncio.to_thread(process_calendar_data, etree.HTML(data.text))
    return {'DATA':{'URL': url, 'process_result': r_processed}}

def process_calendar_data(r_html: etree.HTML):
    col_process = {
        0: {'NAME': 'DATA', 'PROCESS':True}
        , 1: {'NAME': 'GODZ', 'PROCESS': True}
        , 2: { 'NAME': 'GOSPODARZE', 'PROCESS':True}
        , 3: {'NAME': 'GOSPODARZ', 'PROCESS': True}
        , 4: {'NAME': 'WYNIK', 'PROCESS': False}
        , 5: {'NAME': 'GOŚCIE', 'PROCESS': True}
        , 6: {'NAME': 'GOŚĆ', 'PROCESS': True}
    }

    f_data = list()
    for item in r_html.xpath('//table[not(@class)]/tbody/tr[not(@class="bg_blau_20")]'):
        row_dict = dict()
        num_processed = 0
        for col in item.xpath('./td'):
            if not col_process.get(num_processed, {}).get('PROCESS'):
                num_processed += 1
                continue
            col_n = col_process.get(num_processed, {}).get('NAME')
            r_data = col.text.strip() if col.text else str()

            a_text = str()
            img_text = str()
            if col.xpath('./a/text()'):
                a_text = col.xpath('./a/text()')[0].strip()
            if col.xpath('./a/img/@src'):
                img_text = col.xpath('./a/img/@src')[0].strip()

            t_to_fill = '|'.join(filter(lambda r: r.strip(), [r_data, a_text, img_text])) or None
            row_dict.update({col_n: t_to_fill})
            num_processed += 1
        f_data.append(row_dict)
    return f_data

async def main():
    calendar_links = [
        #'https://www.transfermarkt.pl/laliga/gesamtspielplan/wettbewerb/ES1/saison_id/2025'
        # 'https://www.transfermarkt.pl/premier-league/gesamtspielplan/wettbewerb/GB1/saison_id/2025'
        # 'https://www.transfermarkt.pl/serie-a/gesamtspielplan/wettbewerb/IT1/saison_id/2025'
        'https://www.transfermarkt.pl/bundesliga/gesamtspielplan/wettbewerb/L1/saison_id/2025'
    ]
    tasks = list()

    async with httpx.AsyncClient(timeout=10) as a_client:
        for calendar in calendar_links:
            tasks.append(
                asyncio.create_task(get_calendars_info(a_client, calendar))
            )
        f_data = await asyncio.gather(*tasks)
    pl_df = pl.DataFrame(f_data).unnest('DATA').explode('process_result').unnest('process_result') \
    .with_columns(
        pl.col('DATA').fill_null(strategy="forward").over('URL').alias('DATA')
        , pl.col('GOSPODARZ').str.replace('tiny', 'head')
        , pl.col('GOŚCIE').str.replace('tiny', 'head')
    ).with_columns(
        pl.col('DATA').str.split('|').list.get(1).str.to_date('%d.%m.%Y').alias('DATE')
    ).with_columns(
        pl.col('DATE').dt.day().alias('DAY')
        , pl.col('DATE').dt.month().alias('MONTH')
        , pl.col('DATE').dt.year().alias('YEAR')
        , pl.col('DATE').dt.strftime('%B').str.to_uppercase().alias('MONTH_NAME')
        , pl.concat_list(['GOSPODARZE', 'GOŚĆ']).alias('TEAMS_PLAYING_LIST')
        , pl.col('URL').str.extract(r'wettbewerb\/(.*?)\/', 1).alias('LEAGUE_ID')
    ).drop("GODZ")
    teams_l = pl_df.select('GOSPODARZE').unique().to_series().to_list()
    pprint.pprint(teams_l)
    for team in teams_l:
        inner_df = pl_df.filter(pl.col('TEAMS_PLAYING_LIST').list.contains(team)) \
        .with_columns(
            pl.when(pl.col('TEAMS_PLAYING_LIST').list.first() == team).then(pl.lit('H')).otherwise(pl.lit('A')).alias("HOME_AWAY")
        ).with_columns(
            pl.struct([
                pl.col('DAY')
                , pl.lit('Bundesliga').alias('LEAGUE_NAME')
                , pl.when(pl.col('HOME_AWAY') == "H").then(pl.col("GOŚCIE")).otherwise(pl.col("GOSPODARZ")).alias("TEAM_AGAINST_LOGO")
                , pl.col('HOME_AWAY')
            ]).map_elements(lambda r: {r.get('DAY'): (r.get('TEAM_AGAINST_LOGO') ,r.get('LEAGUE_NAME'), r.get('HOME_AWAY'))}, return_dtype=pl.Object).alias('OBJ_PROCESS')
            , pl.when(pl.col('HOME_AWAY') == "H").then(pl.col("GOSPODARZ")).otherwise(pl.col("GOŚCIE")).alias("TEAM_LOGO")
        ).select('MONTH_NAME','MONTH','YEAR','TEAM_LOGO','OBJ_PROCESS', 'LEAGUE_ID').group_by(['MONTH_NAME', 'MONTH', 'YEAR','TEAM_LOGO', 'LEAGUE_ID']).agg( pl.col("OBJ_PROCESS").map_elements(
            lambda dicts: {k: v for d in dicts for k, v in d.items()}, return_dtype=pl.Object
            ))

        team_normalize = unidecode(team).upper().replace(" ", "_").replace(".", "")
        season_t = f"{inner_df.select(pl.col('YEAR').min()).item()}/{inner_df.select(pl.col('YEAR').max()).item()}"
        print(f"processing {team_normalize} and {team}")
        if team_normalize == "BAYERN":
            for row in inner_df.rows(named=True):
                path_img = f"{team_normalize}_{row.get("MONTH_NAME").upper()}_C.png"
                path_full = posixpath.join(F'http://localhost:8000/gen_calendars/images/TEAM_IMAGES/{row.get("LEAGUE_ID")}/{team_normalize}', path_img)
                print(f"processing team with row {row} and team {team} and path_full {path_full}")
                gen_calendar(row.get('YEAR')
                             , row.get('MONTH')
                             , f'http://localhost:8000/gen_calendars/images/MONTHS_IMAGES/{row.get("MONTH_NAME")}.png'
                             , row.get('OBJ_PROCESS')
                             , team
                             , row.get("MONTH_NAME")
                             , path_full#'http://localhost:8000/gen_calendars/images/d5.png'
                             , row.get("TEAM_LOGO")
                             , season_t
                            )


if __name__ == "__main__":
    asyncio.run(main())