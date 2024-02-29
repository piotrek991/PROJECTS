import cx_Oracle as oracledb
import sys

lib_dir = r"D:\oracle_client_instance\instantclient_21_12"
oracledb.init_oracle_client(lib_dir=lib_dir)
connection = oracledb.connect(dsn='localhost:1521/ORCLCDB', user='dummy', password='dummy')

cursor = connection.cursor()
sql = """
    TRUNCATE TABLE RAW_FOOTBALLERS_DATA
"""
cursor.execute(sql)

with open('insert.sql',mode='r', encoding='utf-8') as file:
    sql_raw = file.readlines()

for i in range(1, len(sql_raw)-1):
    sql = sql_raw[i]
    sql = 'INSERT ALL \n' + sql + ' SELECT 1 FROM DUAL'
    print(sql)
    cursor.execute(sql)

connection.commit()





