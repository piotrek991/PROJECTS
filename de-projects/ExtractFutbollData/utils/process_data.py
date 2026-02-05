import pathlib
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import concurrent
import json
import pprint
import polars as pl
import xlsxwriter
from functools import reduce
from typing import List

def get_f_list(d_path: pathlib.Path) -> list | None:
    if d_path.is_dir():
        f_list = list(d_path.glob('*.json'))
        return f_list
    else:
        return None

def process_m_files(f_path: pathlib.Path) -> dict:
    print(f"Processing {f_path}")
    f_data = json.loads(f_path.read_text())
    f_path_base = f"./data_countries_e/data_{{country_n}}.xlsx"

    os.makedirs('./data_countries_e', exist_ok=True)
    try:
        pl_d = pl.DataFrame(f_data).lazy()
        pl_d = (pl_d.unnest("fetch_data").collect())

        col_t = pl_d.schema['teams_info']

        if isinstance(col_t, pl.List) and not isinstance(col_t.inner, pl.Struct):
            return {
                'file': f_path
                , 'status': 'error'
                , 'error_message': 'teams info is not a struct column'
            }
        pl_d_t = (pl_d.explode("teams_info")
            .unnest("teams_info").rename({'id':'team_id', 'name':'team_name', 'link':'team_link'})
             ).lazy()
        pl_d_t = (pl_d_t.explode("players").unnest("players").rename({'id':'player_id', 'name':'player_name', 'link':'player_link'})
                .with_columns(pl.col("shirtNumber").cast(pl.Int64, strict=False).alias("shirtNumber"))
                ).collect()

        replace_map = {
            ',':''
            ,' ':'_'
        }
        u_country_name = pl_d_t.select('country_name').unique().get_column('country_name').to_list().pop().lower()
        u_country_name = reduce(lambda a, rp: a.replace(*rp), replace_map.items(), u_country_name)

        pl_d_t.write_excel(
            f_path_base.format(country_n=u_country_name),
            u_country_name
        )
        return {
            'status': 'success'
            , 'file': f_path_base.format(country_n=u_country_name)
            , 'data': pl_d_t
            , 'country_name': u_country_name
            }
    except Exception as e:
        return {'status': 'error'
            , 'file':f_path
            , 'error_message': str(e)
        }

def result_to_e(pl_list: List):
    with xlsxwriter.Workbook('data_countries_e/_data_BULK.xlsx') as wb:
        for pl_df, country_nm in pl_list:
            print("Processing '{}'".format(country_nm))
            pl_df.write_excel(
                wb,
                country_nm
            )

def concat_pl_dfs(pl_list: List):
    pl_l_inner = [pl_df for pl_df, country_name in pl_list]
    concat_df = pl.concat(pl_l_inner)
    return concat_df

def get_pld_json():
    f_l = get_f_list(pathlib.Path('countries_data'))
    pl_dfs_r = list()
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures_to_file = {executor.submit(process_m_files, f): f for f in f_l}

        for future in concurrent.futures.as_completed(futures_to_file):
            original_file = futures_to_file[future]
            try:
                result_info = future.result()

                if result_info["status"] == "success":
                    print(
                        f"SUCCESS: Processed '{result_info['file']}'")
                    pl_dfs_r.append((result_info.get('data'), result_info.get('country_name')))
                else:
                    print(
                        f"ERROR: Failed to process '{result_info['file']}'.{result_info['error_message']}")
            except Exception as exc:
                print(
                    f"Main thread exception while getting result for '{original_file.name}': {type(exc).__name__} - {exc}")
    return pl_dfs_r





