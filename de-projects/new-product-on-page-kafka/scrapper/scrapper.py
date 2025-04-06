import json
from concurrent.futures import ProcessPoolExecutor
from functools import cached_property
from nltk.sem.logic import AnyType
from fingerprint import generate_fingerprint, encode_to_url_format
import requests
import re
import http.client
import aiohttp
import asyncio
from playwright.async_api import async_playwright
from typing import List, Dict
from lxml import etree, html
from urllib.parse import unquote
from dataclasses import dataclass, field, asdict
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import uuid
from http.cookies import SimpleCookie
import hashlib
import os
##get data_dome

@dataclass
class AllegroProduct:
  product_id: str
  product_name: str
  product_url: str
  product_price:str = field(default_factory=str)
  product_sku: str = field(default_factory=str)
  product_availability: str = field(default_factory=str)
  product_attributes: Dict[str, str] = field(default_factory=dict)
  product_offer_attributes: Dict[str, str] = field(default_factory=dict)
  product_category_path: str = field(default_factory=str)
  product_category: str = field(default_factory=str)
  #last_checked: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
  @property
  def product_category_hash(self) -> int:
    init_md5 =  int(hashlib.md5(self.product_category.encode()).hexdigest(),16)
    return init_md5 % (10 ** 10)

  def as_dist(self):
    d_own = asdict(self)
    d_own['product_category_hash'] = self.product_category_hash
    return d_own


class aioHTTPClient:
  def __init__(self, static_headers=None):
    self.static_headers = static_headers or {}
    self.http_client = http.client.HTTPSConnection("allegro.pl")

  def request_http(self, url, extra_headers=None):
    print(self.static_headers)
    payload = ''
    headers = {**self.static_headers, **(extra_headers or {})}
    self.http_client.request("GET", url,
                 payload, headers)
    res = self.http_client.getresponse()
    data = res.read()
    return data

  async def request(self, url, datadome_cookie:str, extra_headers=None, ):
    headers = {**self.static_headers, **(extra_headers or {})}
    del headers['Cookie']

    datadome_cookie = re.search(r'datadome=([^;]+)', datadome_cookie).group(1)
    cookie = SimpleCookie()
    cookie['_cmuid'] = str(uuid.uuid4())
    cookie['_cmuid']['domain'] = 'allegro.pl'
    cookie['datadome'] = datadome_cookie
    cookie['datadome']['domain'] = 'allegro.pl'

    async with aiohttp.ClientSession(headers=headers) as session:
      session.cookie_jar.update_cookies(cookie)
      try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as response:
          response.raise_for_status()

          return await response.text()
      except Exception as e:
        for val in session.cookie_jar._cookies.values():
          if n_cookie_v := re.search(r'wdctx=([^;]+)' , str(val)):
            cookie['wdctx'] = n_cookie_v.group(1)
            cookie['wdctx']['domain'] = 'allegro.pl'
            break
        session.cookie_jar.clear()
        session.cookie_jar.update_cookies(cookie)
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as response:
          response.raise_for_status()
          return await response.text()

  @staticmethod
  async def request_no_ses(session, url):
    try:
      async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
        response.raise_for_status()
        return await response.text()
    except aiohttp.ClientError as e:
      print(f"durring resquest for url {url} got error {e}")
      raise e

  async def request_multiple_urls(self, urls: List[str], extra_headers=None):
    tasks = []
    headers = {**self.static_headers, **(extra_headers or {})}
    async with aiohttp.ClientSession(headers=headers) as session:
      for url in urls:
        tasks.append(self.request_no_ses(session, url))
      return await asyncio.gather(*tasks, return_exceptions=True)

class AllegroScrapper:
  load_dotenv()
  def __init__(self):
    self.pg_conn = psycopg2.connect(
      host=os.getenv("POSTGRES_HOST"),
      dbname=os.getenv("POSTGRES_DB"),
      user=os.getenv("POSTGRES_USER"),
      password=os.getenv("POSTGRES_PASSWORD"),
      port=os.getenv("POSTGRES_PORT"),
      cursor_factory=RealDictCursor
     )
    self.db_cursor = self.pg_conn.cursor()
    self.async_executor = ProcessPoolExecutor()

  @property
  def cookie_datadome(self):
    headers = {
      'sec-ch-ua-platform': '"Windows"',
      'Referer': 'https://allegro.pl/',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
      'sec-ch-ua-mobile': '?0',
    }
    url = "https://js-data.allegro.pl/js/"
    payload_raw = generate_fingerprint()
    payload = encode_to_url_format(payload_raw)
    r = requests.post(url, data=payload, headers=headers)
    r_raw_datadome = r.json()['cookie']
    return r_raw_datadome

  @cached_property
  def session(self):
    custom_headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
      'cache-control': 'no-cache',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
      'viewport-width': '2560',
      'Cookie': self.cookie_datadome
    }
    conn = aioHTTPClient(static_headers=custom_headers)
    return conn

  async def extract_product_details(self, product: AllegroProduct):
    product_url = product.product_url
    raw_html = await self.session.request(product_url, self.cookie_datadome)
    loop = asyncio.get_running_loop()
    product_processed = await loop.run_in_executor(self.async_executor, self.process_html, raw_html, product)
    return product_processed

  @staticmethod
  def process_html(raw_html_inner: str, product_inner: AllegroProduct):
    print(f"processing product {product_inner.product_url}")
    data_html_etree = etree.HTML(str(raw_html_inner))
    curr_price = data_html_etree.xpath('.//meta[@itemprop="price"]/@content')[0]
    curr_availability = re.search(r'\/(\w+)$', data_html_etree.xpath('.//link[@itemprop="availability"]/@href')[0])
    product_sku = data_html_etree.xpath('.//meta[@itemprop="sku"]/@content')[0]

    features_dict = dict()
    for item_feature in data_html_etree.xpath("//div[@data-box-name='Parameters']/div//tr"):
      column_vales = item_feature.xpath('.//td')
      if not len(column_vales) > 0:
        continue
      if feature_va := column_vales[1].xpath('.//a/text()'):
        features_dict[column_vales[0].text] = feature_va[0]
      else:
        features_dict[column_vales[0].text] = column_vales[1].text

    categories = list()
    for category_part in data_html_etree.xpath(".//ol[@data-role='breadcrumbs-list']/li"):
      category_name = category_part.xpath('.//a/span//text()')[0].strip().lower()
      categories.append(category_name)
    try:
      categories.pop()
      l_category = categories.pop() + " " + categories.pop()
    except IndexError as e:
      print(f"error processing product {product_inner.product_url} - categorues values: {categories}")
      l_category = "non determined"

    product_inner.product_category = l_category
    product_inner.product_category_path = '->'.join(categories)
    product_inner.product_price = curr_price
    product_inner.product_availability = curr_availability.group(1)
    product_inner.product_sku = product_sku
    product_inner.product_attributes = features_dict
    return product_inner

  async def process_multiple_products(self, product_list: List[AllegroProduct]):
    tasks_l = [self.extract_product_details(product) for product in product_list]
    return await asyncio.gather(*tasks_l, return_exceptions=False)

  async def page_rendered_data(self, url:str, custom_headers:dict = None):
    headers = {**self.session.static_headers, **(custom_headers or {})}
    async with async_playwright() as p:
      browser = await p.chromium.launch(headless=False, args=[
                    "--disable-blink-features=AutomationControlled",  # Hide automation flags
                    "--enable-logging",  # Enable verbose logging
                    "--v=1"  # Logging level
                ],
                slow_mo=100)

      # Create a new browser context with custom headers
      context = await browser.new_context(
            user_agent=headers['user-agent'],  # Must match headers
            viewport={"width": 2560, "height": 1279},  # Matches sec-ch-viewport-height and viewport-width
            extra_http_headers=headers,
            locale="pl-PL",  # Matches accept-language
            timezone_id="Europe/Warsaw",  # Poland timezone
            java_script_enabled=True,
            bypass_csp=True
            )
      await context.add_init_script(script="""
                      Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                      Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
                      Object.defineProperty(navigator, 'languages', { get: () => ['pl-PL', 'pl', 'en-US', 'en'] });
                  """)
      page = await context.new_page()
      await page.wait_for_timeout(1000)  # Wait 1s
      await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
      await page.goto(url, wait_until="networkidle")
      print("Browser is open. Inspect it manually. Press Enter here to close...")
      input()
      html_content = await page.content()
      # Clean up
      await browser.close()
      return html_content

  def insert_data(self, products_l: List[AllegroProduct]):
    def normalize_field(val: AnyType) -> str:
      field_format = f"'{{field_value}}'"
      if isinstance(val, dict):
        raw_str = json.dumps(val, ensure_ascii=False).replace("'", "''")
        return field_format.format(field_value=raw_str)
      raw_str = str(val).replace("'", "''")
      return field_format.format(field_value=raw_str)

    ins_statements = list()
    for product in products_l:
      d_product = product.as_dist()
      d_product_ins = ', '.join(list(map(normalize_field,list(d_product.values())))).join(['(', '),'])
      ins_statements.append(d_product_ins)

    ins_statements[-1] = ins_statements[-1][:-1]
    on_conflict_statement = """
      ON CONFLICT (id)
      DO UPDATE
        SET allegro_url=EXCLUDED.allegro_url,
          availability=EXCLUDED.availability,
          category=EXCLUDED.category,
          category_hash=EXCLUDED.category_hash,
          category_path=EXCLUDED.category_path,
          name=EXCLUDED.name,
          offer_attributes=EXCLUDED.offer_attributes,
          price=EXCLUDED.price,
          product_attributes=EXCLUDED.product_attributes,
          sku=EXCLUDED.sku;
    """
    ins_statement_f = '\n'.join(ins_statements).join(["INSERT INTO product_details.products VALUES \n", on_conflict_statement])
    print(f"generated ins statment {ins_statement_f}")
    self.db_cursor.execute(ins_statement_f)
    self.pg_conn.commit()



async def main(s_obj:AllegroScrapper):
  res_html = await s_obj.session.request("https://allegro.pl/kategoria/do-kuchni-frytkownice-67439", s_obj.cookie_datadome)
  html_etree_inner = etree.HTML(res_html)
  if html_etree_inner is not None:
    return html_etree_inner

def get_products():
  scrap_obj = AllegroScrapper()

  html_etree = asyncio.run(main(scrap_obj))
  p_list = list()
  p_list_ids = set()
  for article in html_etree.xpath('//article[not(@data-analytics-view-label)]'):
    t_a = article.xpath('.//a/text()')[0]
    offer_link = unquote(article.xpath('.//a/@href')[0])
    if re.search(r'allegrolokalnie', offer_link):
      continue
    if offer_redirect := re.search(r'redirect=([\w\/\.\-:]+)\?', offer_link):
      offer_link = offer_redirect.group(1)
    print(f"processing link : {offer_link}")
    offer_id_raw = re.search(r'-([0-9]+)(?:$|\?)|rep=([0-9]+)$', offer_link).group()
    offer_id = re.search(r'([0-9]+)', offer_id_raw).group(1)
    if offer_id in p_list_ids:
      continue
    p_list_ids.add(offer_id)

    attributes_l = article.xpath(
      './/div[h2]/div[2]//span[not(@aria-label) and not(parent::span) and not(@style)]/text()')
    attributes_d = {attributes_l[i]: attributes_l[i + 1] for i in range(0, len(attributes_l), 2)}

    p_list.append(AllegroProduct(
      product_id=offer_id
      , product_name=t_a.lower()
      , product_url=offer_link
      , product_offer_attributes=attributes_d
    )
    )
  p_list = p_list[:5]
  print("before")
  for value in p_list:
    print(value)
  p_list_processed = asyncio.run(scrap_obj.process_multiple_products(p_list))
  print("after")
  for value in p_list_processed:
    print(value)
  scrap_obj.insert_data(p_list_processed)

if __name__ == "__main__":
  get_products()