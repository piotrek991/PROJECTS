import re
import requests
from lxml import etree
import pandas as pd
from pathlib import Path
import os
from operator import itemgetter


def encode_decode(str_data:str) -> str:
    f_string = str_data.encode().decode('unicode-escape').encode('latin-1').decode()
    return f_string


def save_get_data(data_dict: dict = None, org_df: pd.DataFrame = pd.DataFrame()) -> None | pd.DataFrame:
    data_path = os.path.abspath(os.path.join(Path(__file__).parent, './data/comb_data.csv'))
    Path(data_path).parent.mkdir(parents=True, exist_ok=True)

    if not data_dict:
        if Path(data_path).is_file():
            pd_df = pd.read_csv(data_path, header=0)
            return pd_df
        return pd.DataFrame()
    else:
        pd_df = pd.DataFrame([[key, *list(values)] for key, values in data_dict.items()]
                             , columns=['el_id', 'engine_capacity', 'engine_power', 'ds1_rest', 'price_str'])
        pd_df = pd.concat([pd_df.reset_index(drop=True), org_df.reset_index(drop=True)], axis=0)
        print(pd_df)
        pd_df.to_csv(data_path, index=False)
        return


if __name__ == "__main__":
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'}
    data = requests.get("https://www.otomoto.pl/osobowe?search%5Border%5D=created_at_first%3Adesc&page=3", headers=headers)
    dom = etree.HTML(str(data.content))

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
        notice_name = encode_decode(
            el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')][2]/*/a[@target='_self']")[0] \
            .text)
        describe_str_1 = encode_decode(
            el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')][2]/p")[0].text
        )
        price_str = int(encode_decode(
            el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/h3")[0].text.replace(" ", "")
        ))
        engine_capacity = re.match("(^[0-9\\s]+cm3\\s+)•", describe_str_1).group(1) \
                if re.match("(^[0-9\\s]+cm3\\s+)•", describe_str_1) else "NOT SPECIFIED"
        engine_power = re.search("•([0-9\\s]*KM\\s+)•", describe_str_1).group(1) \
                if re.search("•([0-9\\s]*KM\\s+)•", describe_str_1) else "NOT SPECIFIED"
        ds1_rest = re.search("(•\\s+)([^•]+$)", describe_str_1).group(2)

        data_dict_o[int(el_id)] = [
            engine_capacity
            , engine_power
            , ds1_rest
            , price_str
        ]
    diff_el_id = list(set(data_dict_o.keys()).difference(set(current_ids)))
    if diff_el_id:
        data_list_o = list(itemgetter(*diff_el_id)(data_dict_o))
        data_dict_o = {val: data_list_o[num] for num, val in enumerate(diff_el_id)}
        print(f"before save")
        print(data_dict_o)
        save_get_data(data_dict_o, data_current_pd)
    else:
        print("nothing to save")




####match cases
# pojemność silnik (^[0-9\s]+cm3\s+)(?:•
# moc silnika (?:•)([0-9\s]*KM\s+)(?:•)
# reszta (?:•)([^•]+$)
