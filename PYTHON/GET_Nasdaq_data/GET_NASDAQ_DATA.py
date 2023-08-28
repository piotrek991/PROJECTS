import nasdaqdatalink
import pandas as pd

nasdaqdatalink.ApiConfig.api_key = "s7hewK6KLG9Zs4LR_kBw"
df = pd.read_csv('economist_country_codes.csv',delimiter = ";")
df_country_codes = {}

for index,row in df.iterrows():
    text = row["COUNTRY|CODE"]
    df_country_codes[text] = text[text.find("|") + 1:len(text)]

with open("data.sql",'w') as file1:
    file1.write("CREATE TABLE COUNTRY_TIME_DATA (\n")
    file1.write("COUNTRY VARCHAR2(100),\n")
    file1.write("RAPORT_DATE VARCHAR2(100),\n")
    file1.write("LOCAL_PRICE NUMBER,\n")
    file1.write("DOLAR_PRICE NUMBER,\n")
    file1.write("DOLLAR_PPP NUMBER);\n")

    sql_line =  "INSERT INTO COUNTRY_TIME_DATA VALUES("
    for key in df_country_codes:
        nasdaq_data_link = "ECONOMIST/BIGMAC_" + df_country_codes[key]
        mydata = nasdaqdatalink.get(nasdaq_data_link).reset_index()

        for index,row in mydata.iterrows():
            local_price = str(row['local_price'])
            dollar_ppp = str(row['dollar_ppp'])
            dollar_price = str(row['dollar_price'])
            merge_text = sql_line + "'" + key + "', '" + str(row['Date'])[0:10] + "'," + local_price + "," + dollar_price + "," + dollar_ppp + ");\n"
            file1.write(merge_text)





