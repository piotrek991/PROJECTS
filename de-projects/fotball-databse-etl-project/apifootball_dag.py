from airflow.decorators import dag, task
import api_operations
import pandas as pd
import cx_Oracle as oracledb
from datetime import datetime

@dag(
    schedule=None
    , start_date = datetime(2021,1,1)
    , catchup = False
    , tags = ['getdetails']
)
def load_players_details():

    @task
    def extract_transform():
        raw_data = api_operations.collect_players_data(get_new_data=False)
        raw_df = pd.DataFrame(data = raw_data, columns = ['player_id','reference_team','reference_date','team_id'
            ,'p_firstname','p_lastname','p_age','p_nationality','season','count'])

        raw_df.dropna(axis=0, subset=['p_nationality'], inplace=True)
        raw_sql_text = api_operations.create_sql_insert(data=raw_df,
                                     table_name='RAW_FOOTBALLERS_DATA',
                                     columns = ['player_id, p_firstname', 'p_lastname', 'p_age', 'p_nationality'],
                                     table_columns = ['FOOT_ID', 'NAME', 'SURNAME','AGE', 'NATIONALITY'],
                                     save_file=False)
        return raw_sql_text

    @task
    def run_insert(sql_text:str):
        #do poprawy
        lib_dir = r"D:\oracle_client_instance\instantclient_21_12"
        oracledb.init_oracle_client(lib_dir=lib_dir)
        connection = oracledb.connect(dsn='localhost:1521/ORCLCDB', user='dummy', password='dummy')

        cursor = connection.cursor()
        cursor.execute(sql_text)

        connection.commit()

    data_sql = extract_transform()
    run_insert(data_sql)


load_players_details()

