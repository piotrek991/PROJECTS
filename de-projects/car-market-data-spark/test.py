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
from urllib.parse import urlencode, urlparse, parse_qs


class HtmlContent:
    def __init__(self, def_ua: str, main_url:str):
        self.def_ua = def_ua
        try:
            requests.get(main_url, headers={'user-agent': self.def_ua}).raise_for_status()
            self.main_url = main_url
        except Exception as e:
            print(f"provided url does not exists or not in proper format")
            raise e
        self.temp_url = str()
        self.html_data = str()

    @staticmethod
    def check_url(url: str, headers: dict) -> None | str:
        try:
            requests.get(url, headers=headers).raise_for_status()
            return url
        except:
            return

    @staticmethod
    def add_url_params(org_url: str, add_params: dict) -> str:
        url_components = urlparse(org_url)
        original_params = parse_qs(url_components.query)

        merged_params = {**original_params, **add_params}
        updated_query = urlencode(merged_params, doseq=True)

        return url_components._replace(query=updated_query).geturl()

    def edit_url_param(self, url: str, param_name: str, param_new_val: any):
        url_components = urlparse(url)
        params = parse_qs(url_components.query)
        try:
            assert params.get(param_name)
        except AssertionError as e:
            url_inner = self.add_url_params(self.main_url, {param_name:param_new_val})
            print(f"url does not contain specified param - ADDING.")
            return url_inner
        params[param_name] = param_new_val
        updated_query = urlencode(params, doseq=True)
        return url_components._replace(query=updated_query).geturl()

    def assign_temp_url(self, params: dict = None, temp_url: str = None, use_main: bool = True):
        try:
            url_tmp = self.main_url if use_main else self.check_url(temp_url, headers={'user-agent': self.def_ua})
            self.temp_url = self.add_url_params(url_tmp, params) if params else url_tmp
            assert self.temp_url
        except AssertionError as e:
            print(f"Url provided is not in proper format/does not exists")
            raise e

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
        self.html_data = html.html


class OtoMotoData(HtmlContent):
    allowed_fields = {
        'el_id',
        'notice_name',
        'engine_capacity',
        'engine_power',
        'price_str',
        'mileage',
        'fuel_type',
        'gearbox',
        'production_year',
        'when_added',
        'ds1_rest'
    }

    def __init__(self, main_url: str, def_ua: str, fields: set, data_path:str, def_file_name:str):
        super().__init__(def_ua, main_url)
        try:
            assert not fields.difference(self.allowed_fields)
            self.fields = fields
        except AssertionError as e:
            print(f"not allowed field/s : {fields.difference(self.allowed_fields)}")
            raise e
        self.new_data = dict()
        self.stored_data = pd.DataFrame()
        self.data_path = os.path.abspath(data_path)
        self.def_file_name = def_file_name

    @staticmethod
    def encode_decode(str_data: str) -> str:
        f_string = str_data.encode().decode('unicode-escape').encode('latin-1').decode()
        return f_string

    @staticmethod
    def resolve_time(start_time: datetime, data_string:str) -> None | datetime:
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

    def get_stored_data(self, alt_path: str = None):
        try:
            inner_path = os.path.join(self.data_path, self.def_file_name) if not alt_path \
                else os.path.join(os.path.abspath(alt_path), self.def_file_name)
            assert os.path.isfile(inner_path)
        except AssertionError as e:
            print(f"Provided path is not file.")
            raise e
        self.stored_data = pd.read_csv(inner_path, header=0)

    def save_data(self, alt_path: str = None):
        inner_path = self.data_path if not alt_path else os.path.abspath(alt_path)
        Path(inner_path).parent.mkdir(parents=True, exist_ok=True)
        try:
            stored_columns = set(self.stored_data.columns)
            assert not stored_columns.difference(self.fields)
            assert self.new_data
        except AssertionError as e:
            print(f"stored data contains columns to used in collected data/ new data dict are empty.")
            raise e
        data_inner = [[key, *list(val_out.values())] for key, val_out in self.new_data.items()]

        pd_inner = pd.DataFrame(data_inner, columns = list(self.fields))
        pd_inner = pd.concat([pd_inner.reset_index(drop=True), self.stored_data.reset_index(drop=True)], axis=0)
        pd_inner.to_csv(os.path.join(inner_path, self.def_file_name), index=False)

    def diff_data(self, key_field: str):
        try:
            assert self.stored_data
            inner_ids = pd.Series(self.stored_data[key_field]).to_list()
            diff_ids = list(set(self.new_data.keys()).difference(set(inner_ids)))
        except AssertionError as e:
            print(f"Empty stored data - returning object new data.")
            return self.new_data
        except Exception as e:
            print(f"Error occurred during checking diff")
            raise e
        inner_diff_items = list(itemgetter(*diff_ids)(self.new_data))
        inner_diff_dict = {inner_val: inner_diff_items[inner_num] for inner_num, inner_val in enumerate(diff_ids)}
        return inner_diff_dict

    def extract_fields(self):
        self.html_data = asyncio.run(self.main(use_temp=False))
        html_etree = etree.HTML(str(self.html_data))

        for num, el in enumerate(html_etree.xpath("//div[@data-testid='search-results']/div/article")):
            el_id = el.get('data-id')
            ###dimensions###
            notice_name = self.self.encode_decode(
                el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')][2]/*/a[@target='_self']")[0] \
                    .text)
            describe_str_1 = self.encode_decode(
                el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')][2]/p")[0].text
            )
            price_str = int(self.encode_decode(
                el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/h3")[0].text.replace(" ", "")
            ))
            mile_age = int(re.sub(r'\s|km', '', self.encode_decode(
                el.xpath(
                    ".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/dd[@data-parameter='mileage']/text()")[
                    0]
            )
                                  ))
            fuel_type = self.encode_decode(
                el.xpath(
                    ".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/dd[@data-parameter='fuel_type']/text()")[
                    0]
            )
            gearbox = self.encode_decode(
                el.xpath(
                    ".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/dd[@data-parameter='gearbox']/text()")[
                    0]
            )
            production_year = int(self.encode_decode(
                el.xpath(
                    ".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/dd[@data-parameter='year']/text()")[
                    0]
            ))
            when_added = self.resolve_time(execution_start, self.encode_decode(
                el.xpath(
                    ".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/dd[2]/p")[0].text
            )).strftime("%d-%m-%Y %H:%M:%S")
            engine_capacity = re.match("(^[0-9\\s]+cm3\\s+)•", describe_str_1).group(1) \
                if re.match("(^[0-9\\s]+cm3\\s+)•", describe_str_1) else "NOT SPECIFIED"
            engine_power = re.search("•([0-9\\s]*KM\\s+)•", describe_str_1).group(1) \
                if re.search("•([0-9\\s]*KM\\s+)•", describe_str_1) else "NOT SPECIFIED"
            ds1_rest = re.search("(•\\s+)([^•]+$)", describe_str_1).group(2)

            inner_dict = {
                'notice_name': notice_name
                , 'engine_capacity': engine_capacity
                , 'engine_power': engine_power
                , 'price_str': price_str
                , 'mile_age': mile_age
                , 'fuel_type': fuel_type
                , 'gearbox': gearbox
                , 'production_year': production_year
                , 'when_added': when_added
                , 'ds1_rest': ds1_rest
            }
            self.new_data[int(el_id)] = itemgetter(*list(self.fields))(inner_dict)

    def next_page(self):
        pass
if __name__ == "__main__":
    execution_start = datetime.now()
    URL = 'https://www.otomoto.pl/osobowe?search%5Border%5D=created_at_first%3Adesc&page=3'
    UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'





### match case
## minut ([0-9]+)\s+(minut[ęy]?)
