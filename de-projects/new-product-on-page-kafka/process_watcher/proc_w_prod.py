import random
from http.cookies import SimpleCookie

from scrapper import AllegroScrapper, KafkaOperations
from dataclasses import dataclass, fields
from operator import itemgetter
from functools import reduce
from typing import List, Dict, Tuple
from decimal import Decimal
from lxml import etree, html
import re
import copy
import asyncio
from datetime import datetime
import json
from concurrent.futures import ProcessPoolExecutor

@dataclass
class AllegroProductDB:
    price: str
    id: str
    sku: str
    availability: str
    offer_attributes: Dict[str, str]
    category: str
    category_hash: str
    category_path: str
    allegro_url: str
    name: str
    product_attributes: Dict[str, str]

@dataclass
class watchObj:
    watch_id: int
    watch_attr_name: str
    attr_storage:str
    product_d: AllegroProductDB


class ProcessWatcher(AllegroScrapper):
    def __init__(self):
        super().__init__()
        self.w_details = list()
        self.w_fields = {f.name for f in fields(watchObj)}

    def get_watched_products(self):
        sql_t = """
           SELECT w.watch_id
            , w_d.watch_attr_name
            , w_d.attr_storage
            , p.*
            FROM product_details.watch_list w
                JOIN product_details.products p ON w.product_id = p.id
                JOIN product_details.watch_attr_dict w_d ON w_d.watch_attr_id = w.watch_attr_id
                ;
        """
        self.db_cursor.execute(sql_t)
        rows = self.db_cursor.fetchall()
        all_p_cols = {f.name for f in fields(AllegroProductDB)}
        for row in rows:
            d_row = dict(row)
            print(d_row)
            p_product_d =list(itemgetter(*all_p_cols)(d_row))
            l_string = reduce(lambda acc, pair: acc + (f"{pair[0]}='{pair[1]}',\n" if isinstance(pair[1], (str, int, float, Decimal))
                                                        else f"{pair[0]}={pair[1]},\n")
                              , zip(all_p_cols, p_product_d), "" )
            l_p = eval("AllegroProductDB(" + l_string[:-2] + ")")
            watch_obj_t = watchObj(
                watch_id=d_row["watch_id"],
                watch_attr_name=d_row["watch_attr_name"],
                attr_storage=d_row["attr_storage"],
                product_d=l_p
            )
            self.w_details.append(watch_obj_t)

    async def process_multiple_watches(self):
        tasks_l = [self.extract_product_details(product) for product in self.w_details]
        return await asyncio.gather(*tasks_l, return_exceptions=False)

    async def extract_product_details(self, product: watchObj):
        product_url = product.product_d.allegro_url
        raw_html = await self.session.request(product_url, self.cookie_datadome)
        loop = asyncio.get_running_loop()
        watch_info = await loop.run_in_executor(self.async_executor, self.process_html_w, raw_html, product)
        return watch_info

    @staticmethod
    def process_html_w(raw_html_inner: str, product_inner: watchObj):
        print(f"processing product {product_inner.product_d.allegro_url}")
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
            print(f"error processing product {product_inner.product_d.allegro_url} - categorues values: {categories}")
            l_category = "non determined"

        product_inner_c = copy.deepcopy(product_inner.product_d)

        product_inner_c.category = l_category
        product_inner_c.category_path = '->'.join(categories)
        product_inner_c.price = curr_price
        product_inner_c.availability = curr_availability.group(1)
        product_inner_c.sku = product_sku
        product_inner_c.offer_attributes = features_dict

        check_p = '.' + product_inner.watch_attr_name.lower()
        product_inner.product_d.price = str(random.randint(50, 100))
        comp_1 = eval('product_inner.product_d' + check_p)
        comp_2 = eval('product_inner_c' + check_p)
        comp_r = (comp_1 != comp_2)
        return product_inner, comp_r, product_inner_c

    async def update_watch_data(self, query_str:str):
        success = False
        print(f"processing query {query_str}")
        try:
            self.db_cursor.execute(query_str)
            success = True
        except Exception as e:
            print(f"during execution of query {query_str} error occured: {e}")
        finally:
            return query_str, success

    async def update_watch_data_multi(self, w_list: List[Tuple[watchObj, bool, watchObj]]):
        kafka_operator = KafkaOperations()
        await kafka_operator.producer.start()

        r_func = lambda d: 'ACTION' if d else 'NO ACTION'
        d_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        query_update_w = f"""
            UPDATE product_details.watch_list w 
                SET last_check = '{{check_date}}'
                , watch_action = '{{w_action}}'
                WHERE watch_id = {{watch_id}}
                ;
        """
        query_update_p = f"""
            UPDATE product_details.products p
                {{changes_statement}}
                WHERE id = {{product_id}}
                ;
        """
        t_list = list()
        for w_obj, act, product_n in w_list:
            query_f = query_update_w.format(check_date=d_date, w_action=r_func(act), watch_id=w_obj.watch_id)
            if act:
                d_changes = dict()
                if w_obj.attr_storage == 'DEFAULT':
                    print("DEFAULT")
                    set_st = 'SET ' + w_obj.watch_attr_name.lower() + "='" + eval('product_n.' + w_obj.watch_attr_name.lower()) + "'"
                    d_changes[w_obj.watch_attr_name.lower()] = {'old': eval('w_obj.product_d.' + w_obj.watch_attr_name.lower())
                                                                , 'new': eval('product_n.' + w_obj.watch_attr_name.lower())
                                                                , 'product_url': w_obj.product_d.allegro_url
                                                                }
                else:
                    set_st = w_obj.attr_storage.lower() + f"= jsonb_set({w_obj.attr_storage.lower()}, '{{ {w_obj.watch_attr_name.lower()} }}', '\"" + eval(
                        'product_n.' + w_obj.watch_attr_name.lower()) + "\"'::jsonb)"
                    d_changes[w_obj.attr_storage.lower()] = {
                            w_obj.watch_attr_name.lower():{
                                'old': eval('w_obj.product_d.' + w_obj.watch_attr_name.lower())
                                , 'new': eval('product_n.' + w_obj.watch_attr_name.lower())
                                , 'product_url': w_obj.product_d.allegro_url
                        }
                    }
                print(f"d_changes produced: {d_changes}")
                t_list.append(self.update_watch_data(f"{query_f} \n {query_update_p.format(changes_statement=set_st, product_id=w_obj.product_d.id)}"))
                await kafka_operator.producer.send(kafka_operator.TOPIC,json.dumps(d_changes).encode('utf-8'))
                continue
            t_list.append(self.update_watch_data(query_f))

        await asyncio.gather(*t_list, return_exceptions=False)

        await kafka_operator.producer.stop()
        await kafka_operator.consumer.stop()
        return


if __name__ == '__main__':
    w = ProcessWatcher()
    w.get_watched_products()
    p_after = asyncio.run(w.process_multiple_watches())
    print(p_after)
    p_processed = asyncio.run(w.update_watch_data_multi(p_after))
    w.pg_conn.commit()
    w.pg_conn.close()