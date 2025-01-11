import re
import requests
from lxml import etree
import pandas as pd
from pathlib import Path
import os
from operator import itemgetter
from datetime import datetime, timedelta
from pyppeteer import launch
from requests_html import HTML
import asyncio
import traceback


class HtmlContent:
    def __init__(self, def_ua:str, main_url:str, pagination_add:str):
        self.def_ua = def_ua
        try:
            requests.get(main_url, headers={'user-agent':self.def_ua}).raise_for_status()
            self.main_url = main_url
        except Exception as e:
            print(f"provided url does not exists or not in proper format")
            raise e
        self.temp_url = str()
        self.pagination_add = {pagination_add: int()}

    @staticmethod
    def check_url(url:str, headers: dict) -> None | str:
        try:
            requests.get(url, headers=headers).raise_for_status()
            return None
        except Exception as e:
            return url

    def assign_temp_url(self, params:dict, temp_url:str = None, use_main:bool = True):
        try:
            url_inner = self.main_url if use_main else self.check_url(temp_url, headers={'user-agent':self.def_ua})
            assert url_inner
        except AssertionError as e:
            print()

    async def fetch(self, url, browser, ua: str = None):
        page = await browser.newPage()
        ua_inner = ua if ua else self.def_ua
        await page.setUserAgent(ua_inner)

        try:
            await page.goto(url, {'waitUntil': 'load'})
        except Exception as e:
            traceback.print_exc()
        else:
            return await page.content()
        finally:
            await page.close()

    async def main(self, use_temp: bool = False):
        browser = await launch(headless=True, args=['--no-sandbox'])
        page_url = self.temp_url if use_temp else self.main_url

        doc = await self.fetch(page_url, browser)
        await browser.close()

        html = HTML(html=doc)
        return html.html


class OtoMotoData(HtmlContent):
    def encode_decode(self, str_data:str) -> str:
        f_string = str_data.encode().decode('unicode-escape').encode('latin-1').decode()
        return f_string


    def save_get_data(self, data_dict: dict = None, org_df: pd.DataFrame = pd.DataFrame()) -> None | pd.DataFrame:
        data_path = os.path.abspath(os.path.join(Path(__file__).parent, './data/comb_data.csv'))
        Path(data_path).parent.mkdir(parents=True, exist_ok=True)

        if not data_dict:
            if Path(data_path).is_file():
                pd_df = pd.read_csv(data_path, header=0)
                return pd_df
            return pd.DataFrame()
        else:
            pd_df = pd.DataFrame([[key, *list(values)] for key, values in data_dict.items()]
                                 , columns=['el_id', 'notice_name','engine_capacity', 'engine_power', 'price_str',
                                            'mileage', 'fuel_type', 'gearbox', 'production_year', 'when_added', 'ds1_rest']
                                 )
            pd_df = pd.concat([pd_df.reset_index(drop=True), org_df.reset_index(drop=True)], axis=0)
            print(pd_df)
            pd_df.to_csv(data_path, index=False)
            return


    def resolve_time(self, start_time: datetime, data_string:str) -> None | datetime:
        data_string = data_string.replace("wczoraj", "1 dni temu")
        if str_val := re.search('([0-9]+)\\s+(minut[ęy]?)', data_string):
            f_time = start_time - timedelta(minutes=int(str_val.group(1)))
        elif str_val:= re.search('([0-9]+)\\s+(godzin[ęy]?)', data_string):
            f_time = start_time - timedelta(hours=int(str_val.group(1)))
        elif str_val := re.search('([0-9]+)\\s+(dni)', data_string):
            f_time = start_time - timedelta(days=int(str_val.group(1)))
        else:
            print(f"currently {data_string} could not be resolved")
            return
        return f_time


if __name__ == "__main__":
    execution_start = datetime.now()
    URL = 'https://www.otomoto.pl/osobowe?search%5Border%5D=created_at_first%3Adesc&page=3'
    UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    data = asyncio.run(main(URL, UA))
    print(f"html content retrieved after {datetime.now() - execution_start}")
    t1 = datetime.now()
    dom = etree.HTML(str(data))

    data_dict_o = dict()
    data_current_pd = save_get_data()
    try:
        assert not data_current_pd.empty
        current_ids = pd.Series(data_current_pd.el_id).to_list()
    except AssertionError:
        current_ids = []

    for num, el in enumerate(dom.xpath("//div[@data-testid='search-results']/div/article")):
        dom_inner = etree.HTML(str(el.text))
        el_id = el.get('data-id')
        ###dimensions###
        notice_name = encode_decode(
            el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')][2]/*/a[@target='_self']")[0] \
            .text)
        describe_str_1 = encode_decode(
            el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')][2]/p")[0].text
        )
        price_str = int(encode_decode(
            el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/h3")[0].text.replace(" ", "")
        ))
        mile_age = int(re.sub(r'\s|km','',encode_decode(
            el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/dd[@data-parameter='mileage']/text()")[0]
            )
        ))
        fuel_type = encode_decode(
            el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/dd[@data-parameter='fuel_type']/text()")[0]
        )
        gearbox = encode_decode(
            el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/dd[@data-parameter='gearbox']/text()")[0]
        )
        production_year = int(encode_decode(
            el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/dd[@data-parameter='year']/text()")[0]
        ))
        when_added = resolve_time(execution_start, encode_decode(
            el.xpath(
                ".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/dd[2]/p")[0].text
        )).strftime("%d-%m-%Y %H:%M:%S")
        engine_capacity = re.match("(^[0-9\\s]+cm3\\s+)•", describe_str_1).group(1) \
                if re.match("(^[0-9\\s]+cm3\\s+)•", describe_str_1) else "NOT SPECIFIED"
        engine_power = re.search("•([0-9\\s]*KM\\s+)•", describe_str_1).group(1) \
                if re.search("•([0-9\\s]*KM\\s+)•", describe_str_1) else "NOT SPECIFIED"
        ds1_rest = re.search("(•\\s+)([^•]+$)", describe_str_1).group(2)
        ###dimensions###

        data_dict_o[int(el_id)] = [
            notice_name
            , engine_capacity
            , engine_power
            , price_str
            , mile_age
            , fuel_type
            , gearbox
            , production_year
            , when_added
            , ds1_rest
        ]
    print(f"dimensions processed after {datetime.now() - t1}")
    t1 = datetime.now()
    diff_el_id = list(set(data_dict_o.keys()).difference(set(current_ids)))
    if diff_el_id:
        data_list_o = list(itemgetter(*diff_el_id)(data_dict_o))
        data_dict_o = {val: data_list_o[num] for num, val in enumerate(diff_el_id)}
        save_get_data(data_dict_o, data_current_pd)
    else:
        print("nothing to save")
    print(f"data saved after {datetime.now() - t1}")




### match case
## minut ([0-9]+)\s+(minut[ęy]?)
