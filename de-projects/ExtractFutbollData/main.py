import requests
from lxml import etree
import pandas as pd
import re
import os
import unicodedata

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0.2; SM-A300FU Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.138 Mobile Safari/537.36'}

req = requests.get('https://www.transfermarkt.pl/laliga/gesamtspielplan/wettbewerb/ES1?saison_id=2024&spieltagVon=1&spieltagBis=38', headers=headers)
req.raise_for_status()

html_raw = etree.HTML(req.text)

t_data = list()
df_cols = list()
for d_raw in html_raw.xpath('//div[@class="box"]'):
    if not df_cols and d_raw.xpath('./table/thead/tr[not(contains(@class,"bg_blau_20"))]/th/text()'):
        cols = d_raw.xpath('./table/thead/tr[not(contains(@class,"bg_blau_20"))]/th/text()')
        print(cols)
        for col in cols:
            col_str = '|'.join(df_cols)
            if not re.search(rf'{col}', col_str):
                df_cols.append(col)
        df_cols.remove('Goście')
        df_cols.append('Kolejka')

    rows = d_raw.xpath('./table/tbody/tr[not(contains(@class,"bg_blau_20"))]')
    nr_kolejka = d_raw.xpath('./div/text()')[0]
    l_date = str()
    l_time = str()
    for row in rows:
        data_td = row.xpath('./td')
        data_td_t = [col.xpath('./a/text()')[0] if col.xpath('./a/text()') else None if not col.xpath('./text()') else col.xpath('./text()')[0].strip() for col in data_td]
        if not data_td_t[0]:
            data_td_t[0] = l_date
        else:
            l_date = data_td_t[0]

        if not data_td_t[1]:
            data_td_t[1] = l_time
        else:
            l_time = data_td_t[1]
        data_td_t.pop(3)
        data_td_t.pop(4)

        data_td_t.append(nr_kolejka)
        t_data.append(data_td_t)

df = pd.DataFrame(t_data, columns=df_cols)
print(df)