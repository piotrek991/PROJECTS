import pandas as pd
import numpy as np
import sqlite3
from attributes import *
import os


def process_clients() -> pd.DataFrame():
    f_path = PATH_CLIENTS if PATH_CLIENTS.endswith('/') else PATH_CLIENTS+'/' + 'client.csv'
    if os.path.exists(f_path):
        d_client = pd.read_csv(f_path, header=0)
    else:
        return pd.DataFrame()

    org_columns = list(d_client.columns)
    org_columns.append('err_msg')
    # UNIQUELLY IDENTIFY EACH ROW
    d_client['row_id'] = d_client.index

    # UNIQUNESS KEY
    check_prep_u = d_client.groupby(['CUSTOMER_ID','REPORTING_DATE']) \
                .agg(count=('BUCKET', 'count'), rows=('row_id', lambda x: x.tolist()[1:]))
    check_prep_u = check_prep_u.loc[check_prep_u['count'] > 1].reset_index().explode('rows')
    check_prep_u['uniquness_check'] = check_prep_u.apply(lambda x: f"row with key "
                                                         f"[{x['CUSTOMER_ID']},{x['REPORTING_DATE']}] is duplicated", axis=1)
    # NULL CHECK
    err_msg = list(map(lambda x: x + f' is empty, but mandatory {chr(10)}', d_client.columns))
    d_client['null_check'] = d_client.isna().apply(lambda x:
                                                    [a*b for a, b in zip(x.tolist(), err_msg)], axis=1)
    # POSITIVE INTEGER CUSTOMER_ID, BUCKET CHECK
    err_msg = list(map(lambda x: x + f'is not positive or not in INT type', ['CUSTOMER_ID', 'BUCKET']))
    d_client['positive_int_check'] = d_client.loc[:, ['CUSTOMER_ID', 'BUCKET']]\
        .map(lambda x:(isinstance(x,int) and x <= 0 if isinstance(x,(int,float)) else x <= 0 if x.isnumeric() else False))\
        .apply(lambda x: [a*b for a, b in zip(x.tolist(), err_msg)], axis=1)

    # AGE RANGE CHECK
    err_msg = ['Age is not in range <18,100>']
    d_client['age_range_check'] = d_client.loc[:,['AGE']]\
        .map(lambda x: 18 > x > 100 if isinstance(x,(int,float)) else 18 > int(x) > 100 if is_float_try(x) else False)\
        .apply(lambda x: [a*b for a, b in zip(x.to_list(), err_msg)], axis=1)

    # EDUCATION CHECK
    err_msg = ['Education is out of specified set']
    d_client['education_check'] = d_client.loc[:,['EDUCATION']]\
        .map(lambda x: str.upper(x) not in ['SECONDARY','ELEMENTARY','HIGHER EDUCATION'])\
        .apply(lambda x: [a*b for a, b in zip(x.tolist(), err_msg)], axis=1)

    # MERGE ERRORS MSG
    d_client = d_client.merge(check_prep_u.loc[:,['rows','uniquness_check']], left_on='row_id'
                              , right_on='rows', how='left')\
        .fillna(value={'uniquness_check': ''})
    d_client['err_msg'] = d_client.loc[:, ['null_check','positive_int_check', 'age_range_check'
                                        ,'education_check','uniquness_check']]\
        .map(lambda x: ''.join(x))\
        .apply(lambda x: ''.join(x.tolist()), axis=1)

    return d_client.loc[:,org_columns]


def process_households() -> pd.DataFrame():
    f_path = PATH_HOUSEHOLD if PATH_HOUSEHOLD.endswith('/') else PATH_HOUSEHOLD + '/' + 'household.csv'
    if os.path.exists(f_path):
        d_household = pd.read_csv(f_path, header=0)
    else:
        return pd.DataFrame()
    org_columns = list(d_household.columns)
    org_columns.append('err_msg')

    ignore_columns = org_columns.copy()
    ignore_columns.append(['row_id', 'rows'])

    d_household['row_id'] = d_household.index
    # UNIQUNESS KEY
    check_prep_u = d_household.groupby(['HOUSEHOLD_ID','REPORTING_DATE']) \
        .agg(count=('REPORTING_DATE', 'count'), rows=('row_id', lambda x: x.tolist()[1:]))
    check_prep_u = check_prep_u.loc[check_prep_u['count'] > 1].reset_index().explode('rows')
    check_prep_u['uniquness_check'] = check_prep_u.apply(lambda x: f"row with key "
                                                                   f"[{x['HOUSEHOLD_ID']}] is duplicated",axis=1)
    # NULL CHECK
    err_msg = list(map(lambda x: x + f' is empty, but mandatory {chr(10)}', d_household.columns))
    d_household['null_check'] = d_household.isna().apply(lambda x:
                                                   [a * b for a, b in zip(x.tolist(), err_msg)], axis=1)
    # POSITIVE INTEGER
    err_msg = list(map(lambda x: x + f'is not positive or not in INT type', ['HOUSEHOLD_ID', 'INCOME_ID','BUCKET']))
    d_household['positive_int_check'] = d_household.loc[:, ['HOUSEHOLD_ID', 'INCOME_ID', 'BUCKET']] \
        .map(lambda x:(isinstance(x,int) and x <= 0 if isinstance(x,(int,float)) else x <= 0 if x.isnumeric() else False))\
        .apply(lambda x: [a * b for a, b in zip(x.tolist(), err_msg)],
                                                                axis=1)
    # CHILD_NO RANGE CHECK
    err_msg = ['CHILD_NO is not in <0,10> range']
    d_household['child_no_range_check'] = d_household.loc[:, ['CHILD_NO']] \
        .map(lambda x: 0 > x > 10 if isinstance(x,(int,float)) else 0 > int(x) > 10 if is_float_try(x) else False) \
        .apply(lambda x: [a * b for a, b in zip(x.to_list(), err_msg)], axis=1)

    # HH_MEMBERS RANGE CHECK
    err_msg = ['HH_MEMBERS is not in <1,10> range']
    d_household['hh_members_range_check'] = d_household.loc[:, ['HH_MEMBERS']] \
        .map(lambda x: 1 > x > 10 if isinstance(x,(int,float)) else 1 > int(x) > 10 if is_float_try(x) else False) \
        .apply(lambda x: [a * b for a, b in zip(x.to_list(), err_msg)], axis=1)

    # Y,N RANGE SET CHECK
    err_msg = ['MARRIED is not in Y,N', 'HOUSE_OWNER is not in Y,N']
    d_household['ho_m_check'] = d_household.loc[:,['MARRIED', 'HOUSE_OWNER']]\
        .map(lambda x: str.upper(x) not in ['Y','N'] if not is_float_try(x) else False)\
        .apply(lambda x: [a*b for a, b in zip(x.tolist(), err_msg)], axis=1)

    # MERGE ERRORS MSG
    d_household = d_household.merge(check_prep_u.loc[:, ['rows', 'uniquness_check']], left_on='row_id'
                              , right_on='rows', how='left') \
        .fillna(value={'uniquness_check': ''})
    d_household['err_msg'] = d_household.loc[:, ['null_check', 'positive_int_check', 'child_no_range_check'
                                              , 'hh_members_range_check','ho_m_check','uniquness_check']] \
        .map(lambda x: ''.join(x)) \
        .apply(lambda x: ''.join(x.tolist()), axis=1)

    return d_household.loc[:, org_columns]


def process_income() -> pd.DataFrame():
    f_path = INCOME_PATH if INCOME_PATH.endswith('/') else INCOME_PATH + '/' + 'income.csv'
    if os.path.exists(f_path):
        d_income = pd.read_csv(f_path, header=0)
    else:
        return pd.DataFrame()
    org_columns = list(d_income.columns)
    org_columns.append('err_msg')

    ignore_columns = org_columns.copy()
    ignore_columns.extend(['row_id', 'rows'])

    d_income['row_id'] = d_income.index
    # UNIQUNESS KEY
    check_prep_u = d_income.groupby(['INCOME_ID','CUSTOMER_ID','REPORTING_DATE']) \
        .agg(count=('FIRST_JOB', 'count'), rows=('row_id', lambda x: x.tolist()[1:]))
    check_prep_u = check_prep_u.loc[check_prep_u['count'] > 1].reset_index().explode('rows')
    check_prep_u['uniquness_check'] = check_prep_u\
        .apply(lambda x: f"row with key [{x['INCOME_ID']},{x['CUSTOMER_ID']},{x['REPORTING_DATE']}] is duplicated", axis=1)

    # NULL CHECK
    err_msg = list(map(lambda x: x + f' is empty, but mandatory {chr(10)}', d_income.columns))
    d_income['null_check'] = d_income.isna().apply(lambda x:
                                                    [a*b for a, b in zip(x.tolist(), err_msg)], axis=1)
    # POSITIVE INTEGER
    err_msg = list(map(lambda x: x + f'is not positive or not in INT type', ['INCOME_ID', 'CUSTOMER_ID', 'INCOME','BUCKET']))
    d_income['positive_int_check'] = d_income.loc[:, ['INCOME_ID', 'CUSTOMER_ID', 'INCOME', 'BUCKET']] \
        .map(lambda x:(isinstance(x,int) and x <= 0 if isinstance(x,(int,float)) else x <= 0 if x.isnumeric() else False))\
        .apply(lambda x: [a * b for a, b in zip(x.tolist(), err_msg)],axis=1)
    # INCOME RANGE CHECK
    err_msg = ['INCOME is not in <1K,30K> range']
    d_income['income_range_check'] = d_income.loc[:, ['INCOME']] \
        .map(lambda x: 10**3 > x > 30*10**3 if isinstance(x,(int,float)) else 10**3 > int(x) > 30*10**3 if is_float_try(x) else False) \
        .apply(lambda x: [a * b for a, b in zip(x.to_list(), err_msg)], axis=1)

    # Y,N RANGE SET CHECK
    err_msg = ['FIRST_JOB is not in Y,N']
    d_income['first_job_check'] = d_income.loc[:, ['FIRST_JOB']] \
        .map(lambda x: str.upper(x) not in ['Y', 'N'] if not is_float_try(x) else False) \
        .apply(lambda x: [a * b for a, b in zip(x.tolist(), err_msg)], axis=1)

    # MERGE ERRORS MSG
    d_income = d_income.merge(check_prep_u.loc[:, ['rows', 'uniquness_check']], left_on='row_id'
                              , right_on='rows', how='left') \
        .fillna(value={'uniquness_check': ''})
    d_income['err_msg'] = d_income.loc[:, list(set(list(d_income.columns)).difference(set(ignore_columns)))] \
        .map(lambda x: ''.join(x)) \
        .apply(lambda x: ''.join(x.tolist()), axis=1)

    return d_income.loc[:, org_columns]


def process_loan() -> pd.DataFrame():
    f_path = LOAN_PATH if LOAN_PATH.endswith('/') else LOAN_PATH + '/' + 'loan.csv'
    if os.path.exists(f_path):
        d_loan = pd.read_csv(f_path, header=0)
    else:
        return pd.DataFrame()
    org_columns = list(d_loan.columns)
    org_columns.append('err_msg')

    ignore_columns = org_columns.copy()
    ignore_columns.extend(['row_id', 'rows'])

    d_loan['row_id'] = d_loan.index
    # UNIQUNESS KEY
    check_prep_u = d_loan.groupby(['LOAN_ID', 'REPORTING_DATE']) \
        .agg(count=('INTODEFAULT', 'count'), rows=('row_id', lambda x: x.tolist()[1:]))
    check_prep_u = check_prep_u.loc[check_prep_u['count'] > 1].reset_index().explode('rows')
    check_prep_u['uniquness_check'] = check_prep_u.apply(lambda x: f"row with key "
                                                                   f"[{x['LOAN_ID']},{x['REPORTING_DATE']}] is duplicated",axis=1)
    # NULL CHECK
    err_msg = list(map(lambda x: x + f' is empty, but mandatory', d_loan.columns))
    d_loan['null_check'] = d_loan.isna().apply(lambda x:
                                                   [a * b for a, b in zip(x.tolist(), err_msg)], axis=1)

    # POSITIVE INTEGER
    err_msg = list(
        map(lambda x: x + f'is not positive or not in INT type', ['LOAN_ID', 'CUSTOMER_ID', 'BUCKET']))
    d_loan['positive_int_check'] = d_loan.loc[:, ['LOAN_ID', 'CUSTOMER_ID', 'BUCKET']] \
        .map(lambda x:(isinstance(x,int) and x <= 0 if isinstance(x,(int,float)) else x <= 0 if x.isnumeric() else False))\
        .apply(lambda x: [a * b for a, b in zip(x.tolist(), err_msg)],axis=1)

    # POSITIVE DECIMAL
    err_msg = list(
        map(lambda x: x + f'is not positive or not in DECIMAL type', ['LOAN_AMT', 'INSTALLMENT_AMT']))
    d_loan['positive_float_check'] = d_loan.loc[:, ['LOAN_AMT', 'INSTALLMENT_AMT']] \
        .map(lambda x:(isinstance(x,int) and x <= 0 if isinstance(x,(int,float)) else x <= 0 if is_float_try(x) else False))\
        .apply(lambda x: [a * b for a, b in zip(x.tolist(), err_msg)],axis=1)

    # Y,N RANGE SET CHECK
    err_msg = ['INTODEFAULT is not in Y,N']
    d_loan['default_check'] = d_loan.loc[:, ['INTODEFAULT']] \
        .map(lambda x: str.upper(x) not in ['Y', 'N'] if not is_float_try(x) else False) \
        .apply(lambda x: [a * b for a, b in zip(x.tolist(), err_msg)], axis=1)

    # LOAN_AMT RANGE CHECK
    err_msg = ['LOAN_AMT is not in <0.5K,100K> range']
    d_loan['loan_amt_check'] = d_loan.loc[:, ['LOAN_AMT']] \
        .map(lambda x: 0.5 * 10 ** 3 > x > 100 * 10 ** 3 if isinstance(x,(int,float))
                    else 10.5 * 10 ** 3 > int(x) > 100 * 10 ** 3 if is_float_try(x) else False) \
        .apply(lambda x: [a * b for a, b in zip(x.to_list(), err_msg)], axis=1)

    # INSTALLMENT_AMT RANGE CHECK
    err_msg = ['INSTALLMENT_AMT is not in <10K,100K> range']
    d_loan['installment_amt'] = d_loan.loc[:, ['INSTALLMENT_AMT']] \
        .map(lambda x: 10 > x > 100 * 10 ** 3 if isinstance(x,(int,float))
                    else 10 > int(x) > 100 * 10 ** 3 if is_float_try(x) else False) \
        .apply(lambda x: [a * b for a, b in zip(x.to_list(), err_msg)], axis=1)

    # PAST_DUE_AMT RANGE CHECK
    err_msg = ["PAST_DUE_AMT is not '>=0' range"]
    d_loan['installment_amt'] = d_loan.loc[:, ['INSTALLMENT_AMT']] \
        .map(lambda x: x < 0 if isinstance(x,(int,float))
                    else int(x) < 0 if is_float_try(x) else False) \
        .apply(lambda x: [a * b for a, b in zip(x.to_list(), err_msg)], axis=1)

    # MERGE ERRORS MSG
    d_loan = d_loan.merge(check_prep_u.loc[:, ['rows', 'uniquness_check']], left_on='row_id'
                              , right_on='rows', how='left') \
        .fillna(value={'uniquness_check': ''})
    d_loan['err_msg'] = d_loan.loc[:, list(set(list(d_loan.columns)).difference(set(ignore_columns)))] \
        .map(lambda x: ''.join(x)) \
        .apply(lambda x: ''.join(x.tolist()), axis=1)

    return d_loan.loc[:, org_columns]


def calculate_metrics(data:pd.DataFrame,table:str, key_field:list) -> list:

    metric_text = np.array([
        ['NULLS %', table]
        , ['DUPLICATES %', table]
        , ['DATE CONSISTENCY %', table]
    ])
    # NULLS PERCENTAGE
    metric_null = sum(data.isna().sum()) / sum(data.count())

    # DUPLICATE PERCENTAGE
    metric_duplicates = data.duplicated().sum() / len(data)

    # DATE CONSISTENCY CHECK
    prep_df = data.copy()
    grouped_df = prep_df.groupby(key_field).agg(min_d=('REPORTING_DATE','min'), max_d=('REPORTING_DATE','max'), count_r=('REPORTING_DATE','count')).reset_index()
    grouped_df['diff'] = (grouped_df['max_d'].dt.to_period('M') - grouped_df['min_d'].dt.to_period('M')).apply(lambda x: x.n)
    metric_consistency_dates = grouped_df.apply(lambda x: x['count_r'] - x['diff'] - 1 == 0, axis=1).sum() / len(grouped_df)

    np_metrics = np.array([metric_null, metric_duplicates, metric_consistency_dates])[:,None]
    np_metrics = np.hstack((metric_text, np_metrics))

    return list(np_metrics)


if __name__ == '__main__':
    # PROCESS ALL DATA
    data_income = process_income()
    data_household = process_households()
    data_loan = process_loan()
    data_client = process_clients()

    data_metrics = pd.DataFrame(columns=['METRIC','TABLE', 'VALUE'])
    data_income['REPORTING_DATE'] = data_income['REPORTING_DATE'].apply(pd.to_datetime,format='%d.%m.%Y'
                                                                        ,errors='coerce')
    data_household['REPORTING_DATE'] = data_household['REPORTING_DATE'].apply(pd.to_datetime, format='%d.%m.%Y',
                                                                        errors='coerce')
    data_loan['REPORTING_DATE'] = data_loan['REPORTING_DATE'].apply(pd.to_datetime, format='%Y-%m-%d',
                                                                        errors='coerce')
    data_client['REPORTING_DATE'] = data_client['REPORTING_DATE'].apply(pd.to_datetime, format='%d.%m.%Y',
                                                                        errors='coerce')

    concat_df = pd.DataFrame(
        calculate_metrics(data_income, key_field=['CUSTOMER_ID','INCOME_ID'], table='INCOME'),
        columns=['METRIC','TABLE', 'VALUE'])
    data_metrics = pd.concat([data_metrics, concat_df], axis=0)

    concat_df = pd.DataFrame(
        calculate_metrics(data_household, key_field=['HOUSEHOLD_ID','INCOME_ID'], table='HOUSEHOLD'),
        columns=['METRIC','TABLE', 'VALUE'])
    data_metrics = pd.concat([data_metrics, concat_df], axis=0)

    concat_df = pd.DataFrame(
        calculate_metrics(data_client, key_field=['CUSTOMER_ID'], table='CLIENT'),
        columns=['METRIC', 'TABLE', 'VALUE'])
    data_metrics = pd.concat([data_metrics, concat_df], axis=0)

    concat_df = pd.DataFrame(
        calculate_metrics(data_loan, key_field=['LOAN_ID','CUSTOMER_ID'], table='LOAN'),
        columns=['METRIC', 'TABLE', 'VALUE'])
    data_metrics = pd.concat([data_metrics, concat_df], axis=0)

    f_path = PROCESSED_PATH if PROCESSED_PATH.endswith('/') else PROCESSED_PATH + '/'
    with pd.ExcelWriter(f_path + 'data_err_metrics') as writer:
        data_income[data_income['err_msg'] != ''].to_excel(writer, sheet_name='INCOME', index=False)
        data_household[data_income['err_msg'] != ''].to_excel(writer, sheet_name='HOUSEHOLD', index=False)
        data_loan[data_income['err_msg'] != ''].to_excel(writer, sheet_name='LOAN', index=False)
        data_client[data_income['err_msg'] != ''].to_excel(writer, sheet_name='CLIENT', index=False)

        data_metrics.to_excel(writer, sheet_name='METRICS', index=False)

    data_income.loc[data_income['err_msg'] == '', list(data_income.columns)[:-1]].to_csv(
        f_path + 'income_processed.csv', index=False)
    data_household.loc[data_household['err_msg'] == '', list(data_household.columns)[:-1]].to_csv(
        f_path + 'household_processed.csv', index=False)
    data_loan.loc[data_loan['err_msg'] == '', list(data_loan.columns)[:-1]].to_csv(
        f_path + 'loan_processed.csv', index=False)
    data_client.loc[data_client['err_msg'] == '', list(data_client.columns)[:-1]].to_csv(
        f_path + 'client_processed.csv', index=False)




