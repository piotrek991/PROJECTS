import requests
import json
import pandas as pd
import time
import os
import re
from datetime import datetime
import os.path


key = "6ff16a0f18614751d07cc33f7bb498d5"
headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }


def log_runs(endpoint: str, parameters: dict, errors_info: dict = dict(), finished:bool = True, predefined_status:int = 0, **kwargs):
    global current_requests
    date_d = datetime.today()
    file_name = 'logs_' + datetime.strftime(date_d, '%Y_%m_%d')
    if predefined_status:
        current_requests_inner = current_requests
    else:
        current_requests_inner = current_requests

    columns = ['time', 'endpoint', 'parameters', 'finished', 'errors_info','current_requests']
    data = list(map(str,[datetime.strftime(date_d,'%H:%M:%S'), endpoint, parameters
        ,finished, errors_info, current_requests_inner]))
    for key_inner,value_inner in kwargs.items():
        columns.append(str(key_inner))
        data.append(str(value_inner))
    write_list = [columns[i] + ' ? ' + data[i] for i in range(len(data))]
    with open(file_name, mode = 'a') as file:
        file.write('|'.join(write_list))
        file.write("\n")

    write_list.insert(0,'date ? ' + datetime.strftime(date_d,'%Y_%m_%d'))
    with open('logs_concat.txt', mode = 'a') as file:
        file.write('|'.join(write_list))
        file.write("\n")


def read_logs(endpoint: str, *args, daily:bool = False) -> dict:
    date_d = datetime.today()
    file_name = 'logs_' + datetime.strftime(date_d, '%Y_%m_%d')
    available_endpoints = ['teams', 'players', 'leagues']

    if endpoint not in available_endpoints:
        print('wrong endpoint please provide a correct one')
    else:
        endpoint_inner = "https://v3.football.api-sports.io/" + endpoint
        if daily:
            if os.path.isfile(file_name):
                with open(file_name, mode='r') as file:
                    data = file.readlines()
                key_values = list()
                for item_inner in range(len(data)-1,-1,-1):
                    key_values = list(map(str.strip, re.split('[?|]', data[item_inner])))
                    if endpoint_inner in key_values:
                        break
                if args:
                    logs_dict = {key_values[i]: key_values[i+1] for i in range(0,len(key_values), 2)
                                 if key_values[i] in args}
                else:
                    logs_dict = {key_values[i]: key_values[i+1] for i in range(0,len(key_values), 2)}
                return logs_dict
            else:
                print("Theres no file for today in logs - api were not used")
        else:
            if os.path.isfile('logs_concat.txt'):
                with open('logs_concat.txt', mode='r') as file:
                    data = file.readlines()
                key_values = list()
                for item_inner in range(len(data) - 1, -1, -1):
                    key_values = list(map(str.strip, re.split('[?|]', data[item_inner])))
                    if endpoint_inner in key_values:
                        break
                if args:
                    logs_dict = {key_values[i]: key_values[i + 1] for i in range(0, len(key_values), 2)
                                 if key_values[i] in args}
                else:
                    logs_dict = {key_values[i]: key_values[i + 1] for i in range(0, len(key_values), 2)}
                return logs_dict
            else:
                print("Theres no log file at all")


def call_api(endpoint: str, parameters_v: dict=dict(), headers_v: dict=dict(), final_data: list=list(), log_run: bool=False):
    global t_s
    global current_requests
    current_requests += 1

    data = requests.get(endpoint, params=parameters_v, headers = headers_v)
    j_d = json.loads(data.content)
    if isinstance(j_d['errors'],dict):
        if j_d['errors'].get('requests') is not None:
            print(f"Requests limit is reached, currently on page "
                  f"{parameters_v['page'] if parameters_v.get('page') else 1} "
                  f"returning gathered data until this moment ....")
            log_runs(endpoint, parameters_v, j_d['errors'], False, current_requests - 1)
            return final_data
        elif j_d['errors'].get('rateLimit') is not None:
            print(f"Rate Limit for subscription plan exceeded gotta wait {60 - (datetime.now() - t_s).seconds % 60} seconds")
            time.sleep(60 - ((datetime.now() - t_s).seconds % 60))
            t_s = datetime.now()
            call_api(endpoint, parameters_v, headers, final_data,log_run)
        else:
            print("Other errors occurred :")
            for key,value in j_d['errors'].items():
                print(f"{key} : {value}")
            return final_data
    elif j_d['paging']['current'] < j_d['paging']['total']:
        final_data.append(j_d['response'])
        if parameters_v.get('page') is None:
            parameters_v.update({'page':j_d['paging']['current']+1})
        else:
            parameters_v['page'] += 1
        call_api(endpoint,parameters_v,headers,final_data,log_run)
    else:
        if j_d['response']:
            final_data.append(j_d['response'])
        if log_run:
            log_runs(endpoint,parameters_v)
    return final_data


def create_dict(keys:[]) -> dict:
    final_dict = dict()
    for item in keys:
        final_dict[item] = str()
    return final_dict


def create_sql_insert(data : pd.DataFrame, table_name: str, columns :list = list(), table_columns: list = list(), save_file:bool = True):
    if not columns:
        columns = data.columns.to_list()
    data_c = data.copy()

    data_c = data_c.apply(lambda x: ['null' if pd.isna(el) else el for el in x])
    data_c = data_c.apply(lambda x: ["q'|" + str(el) + "|'" if not isinstance(el, (int,float)) and el != 'null' else el for el in x])

    print(data_c)
    sql_text = pd.DataFrame()
    if table_columns:
        sql_text['inserts'] = data_c.loc[:,columns].apply(lambda x: ", ".join(list(map(str, x.values.tolist()))).join(
            (f"INTO {table_name}({','.join(table_columns)}) VALUES("
             ,f")\n\t log errors into err$_{table_name} ('load failed') reject limit unlimited \n")), axis =1).values.tolist()
    else:
        sql_text['inserts'] = data_c.loc[:, columns].apply(lambda x: ", ".join(list(map(str, x.values.tolist()))).join(
            (f"INTO {table_name} ("
             , f")\n log errors into err$_{table_name} ('load failed') reject limit unlimited")), axis=1).values.tolist()
    if save_file:
        with open('insert.sql', mode='w', encoding='utf-8') as file:
            file.write(f"INSERT ALL\n")
            file.write(''.join(sql_text['inserts'].values.tolist()))
            file.write('SELECT 1 FROM DUAL;')
    else:
        r_text = ''.join(sql_text['inserts'].values.tolist())
        r_text = f"INSERT ALL\n" + r_text + 'SELECT 1 FROM DUAL;';
        return r_text


def get_all_leagues(get_new_data:bool = True,**kwargs) -> list:
    available_parameters = {'id':int, 'name':str, 'code': int,
                            'search': str, 'country': str, 'season': int,
                            'current': str, 'team': int, 'type':str, 'last':str}
    parameters_dict = dict()
    filename_check = 'leagues_'
    for key, value in kwargs.items():
        if available_parameters.get(key) and isinstance(value, available_parameters.get(key)):
            parameters_dict[key] = value
            if not isinstance(value, str):
                filename_check += key + str(value) + '_'
            else:
                filename_check += key + value + '_'
    filename_check += '.csv'
    if not get_new_data:
        if os.path.exists(filename_check):
            raw_league_data = pd.read_csv(filename_check).values.tolist()
            return raw_league_data

    league_data = call_api("https://v3.football.api-sports.io/leagues", parameters_v=parameters_dict,
                           headers_v=headers,final_data=list(),log_run=True)
    cleaned_data_inner = list()
    for item_inner in league_data:
        for _item_inner in item_inner:
            row_list = list()
            row_list.append(_item_inner['league']['id'])
            row_list.append(_item_inner['league']['name'])
            row_list.append(_item_inner['country']['name'])
            cleaned_data_inner.append(row_list)
    raw_df = pd.DataFrame(data=cleaned_data_inner,columns=['id','league_name','country_name'])
    save_retrieved_data(raw_df,'leagues',parameters_dict)
    return cleaned_data_inner


def get_players_seasoned_data(get_logs_data:bool = True, get_new_data:bool=True) -> list:
    global t_s
    cleaned_data = list()

    parameters_to_call = {'season': 2023, 'league': 39}
    if not get_new_data:
        if get_logs_data:
            data_logs = read_logs('players', 'parameters', 'finished')
            if data_logs.get('finished') is not None and os.path.exists("player_season2023_league39_.csv"):
                cleaned_data = pd.read_csv("players_season2023_league39_.csv").values.tolist()
                parameters_to_call = {'season': 2023, 'league': 39, 'page': data_logs.get('page')}
        elif os.path.exists("players_season2023_league39_.csv"):
            cleaned_data = pd.read_csv("players_season2023_league39_.csv").values.tolist()
            return cleaned_data

    t_s = datetime.now()
    merged_data = call_api("https://v3.football.api-sports.io/players",
                           parameters_to_call, headers, list(),log_run=True)
    if merged_data:
        for item in merged_data:
            for item_ in item:
                row_list = list()
                row_list.append(item_['player']['id'])
                row_list.append(item_['player']['name'])
                row_list.append(item_['player']['firstname'])
                row_list.append(item_['player']['lastname'])
                row_list.append(item_['player']['age'])
                dummy_dict = create_dict(['team_id','league_id'])
                for stats in item_['statistics']:
                    dummy_dict['team_id'] = dummy_dict['team_id'] + ', ' + str(stats['team']['id'])
                    if not len(dummy_dict['league_id']):
                        dummy_dict['league_id'] = dummy_dict['league_id'] + ', ' + str(stats['league']['id'])
                    elif stats['league']['id'] not in list(map(int,dummy_dict['league_id'].lstrip(', ').split(', '))):
                        dummy_dict['league_id'] = dummy_dict['league_id'] + ', ' + str(stats['league']['id'])

                row_list.append(dummy_dict['team_id'].lstrip(', '))
                row_list.append(int(dummy_dict['league_id'].lstrip(', ')))
                cleaned_data.append(row_list)
        raw_df =pd.DataFrame(data = cleaned_data, columns=['player_id','full_name', 'firstname','lastname'
                ,'age','team_id','league_id'])
        save_retrieved_data(raw_df,'players',parameters_to_call)
        return cleaned_data
    else:
        return list()


def get_act_squads(only_main_leagues: bool=True, get_new_data:bool=True, temp:bool=True)->list:
    global t_s
    if datetime.now().month // 7 >= 1:
        season_to_call = datetime.now().year
    else:
        season_to_call = datetime.now().year - 1
    filename_check = 'players_season' + str(season_to_call) + '_.csv'
    print(f'here with act squad and filename {filename_check}')

    if not get_new_data:
        if os.path.exists(filename_check):
            print('returning data from act_squads')
            raw_teams = pd.read_csv(filename_check).values.tolist()
            return raw_teams

    raw_teams_data = get_teams_data(only_main_leagues=only_main_leagues, get_new_data=False, season=season_to_call)
    df_raw_team_data = pd.DataFrame(data=raw_teams_data, columns=['id_team', 'id_league', 'team_name', 'code'])

    squad_data = list()
    for team_inner in df_raw_team_data.loc[:,'id_team'].unique():
        print(f'calling for team {team_inner}')
        raw_squad_data = call_api('https://v3.football.api-sports.io/players',parameters_v={'season': season_to_call,'team': team_inner}
                                        ,headers_v=headers, final_data=list(), log_run=False)
        for squad_inner in raw_squad_data:
            for squad_inner_ in squad_inner:
                row_list = list()
                row_list.append(team_inner)
                row_list.append(squad_inner_['player']['id'])
                row_list.append(squad_inner_['player']['firstname'])
                row_list.append(squad_inner_['player']['lastname'])
                row_list.append(squad_inner_['player']['age'])
                row_list.append(squad_inner_['player']['nationality'])
                row_list.append(season_to_call)
                squad_data.append(row_list)

    raw_df = pd.DataFrame(data = squad_data, columns = ['team_id','player_id','p_firstname'
        ,'p_lastname','p_age','p_nationality','season'])
    raw_df_grouped = raw_df.groupby(['player_id']).size().reset_index(name='how_many')
    raw_df.set_index('player_id',inplace=True)

    print(raw_df_grouped.loc[raw_df_grouped.how_many > 1, :].size)
    for row_item in raw_df_grouped.loc[raw_df_grouped.how_many > 1, :].itertuples():
        raw_data = call_api('https://v3.football.api-sports.io/transfers',parameters_v={'player':row_item.player_id}
                                        ,headers_v=headers, final_data=list(), log_run=False)
        transfer_dates = dict()
        for item_inner in raw_data:
            for transfer in item_inner[0]['transfers']:
                transfer_dates[transfer['date']] = transfer['teams']['in']['id']

        if transfer_dates:
            dates = list(map(lambda x: datetime.strptime(x,'%Y-%m-%d'),transfer_dates.keys()))
            raw_df.loc[row_item.player_id, 'team_id'] = transfer_dates[str(max(dates).date())]

    raw_df.reset_index(inplace=True)
    raw_df.drop_duplicates(inplace=True, subset=['player_id','team_id'])

    save_retrieved_data(raw_df,'players',{'season':season_to_call})

    return squad_data


def get_all_players_data(only_main_league: bool = True, get_new_data:bool=True) -> list:
    global t_s

    if not get_new_data:
        if os.path.exists('players_.csv'):
            print('return data from all players')
            raw_data_final = pd.read_csv('players_.csv').values.tolist()
            return raw_data_final

    data_inner = get_teams_data(only_main_leagues=only_main_league,get_new_data=False, season=2023)
    if data_inner:
        df_inner = pd.DataFrame(data=data_inner, columns=['id_team', 'id_league', 'team_name', 'code'])
        final_list = list()
        for team_id_inner in df_inner.loc[:,'id_team'].unique()[:2]:
            data_inner = call_api('https://v3.football.api-sports.io/transfers', parameters_v={'team': team_id_inner}
                                  , headers_v=headers, final_data=list())
            for item in data_inner:
                for item_ in item:
                    row_list = list()
                    row_list.append(item_['player']['id'])
                    row_list.append(item_['transfers'][0]['date'])
                    if item_['transfers'][0]['teams']['in']['id']:
                        row_list.append(item_['transfers'][0]['teams']['in']['id'])
                    else:
                        row_list.append(item_['transfers'][0]['teams']['out']['id'])
                    final_list.append(row_list)
        raw_df = pd.DataFrame(data=final_list,columns=['player_id','reference_date','reference_team_id'])
        raw_df = raw_df.drop_duplicates()

        raw_data_final_prep = raw_df.groupby(['player_id']).agg({'reference_date':"max"}).reset_index()
        raw_data_final = raw_df.merge(raw_data_final_prep, on=['player_id','reference_date'], how='inner').loc[:
                                    ,['player_id','reference_team_id','reference_date']]

        save_retrieved_data(raw_data_final,'players')
        return raw_data_final.values.tolist()
    else:
        print('no data was returned from get_teams_data function')
    return list()


def get_teams_data(only_main_leagues: bool = True,get_new_data:bool=True, **kwargs) -> list:
    global t_s
    available_parameters = {'id': int, 'name': str, 'code': int,
                            'search': str, 'country': str, 'season': int,
                            'league': int, 'venue': str}

    parameters_dict = dict()
    filename_check = 'teams_'
    for key, value in kwargs.items():
        if available_parameters.get(key) and isinstance(value, available_parameters.get(key)):
            parameters_dict[key] = value
            if not isinstance(value,str):
                filename_check += key + str(value) + '_'
            else:
                filename_check += key + value + '_'

    filename_check += '.csv'
    if not get_new_data:
        if os.path.exists(filename_check):
            print('returning_act_data')
            raw_teams = pd.read_csv(filename_check).values.tolist()
            return raw_teams

    if not parameters_dict:
        print('At least one paramater is required')
    elif parameters_dict.get('season'):
        raw_data_leagues = get_all_leagues(get_new_data=False, season=2023)
        data_leagues = pd.DataFrame(data=raw_data_leagues, columns=['id','league_name','country_name'])
        if only_main_leagues:
            data_leagues = data_leagues.loc[data_leagues.country_name != 'World'].groupby('country_name').agg(
                {'id': 'min'}).merge(data_leagues, how='inner', on='id')

        id_series = data_leagues.id.to_list()
        teams_data = list()
        for item in id_series:
            raw_inner_data = call_api('https://v3.football.api-sports.io/teams',parameters_v={'season': 2023,'league': item}
                                        ,headers_v=headers, final_data=list(), log_run=True)
            for team_inner in raw_inner_data:
                for team_inner_ in team_inner:
                    row_list = list()
                    row_list.append(team_inner_['team']['id'])
                    row_list.append(item)
                    row_list.append(team_inner_['team']['name'])
                    row_list.append(team_inner_['team']['code'])
                    teams_data.append(row_list)
        raw_df = pd.DataFrame(data = teams_data,columns=['id_team', 'id_league', 'team_name', 'code'])
        save_retrieved_data(raw_df,'teams',{'season':parameters_dict.get('season')})

        return teams_data
    else:
        print(f'current version only handle request with season parameter')
    return list()


def save_retrieved_data(data_to_s: pd.DataFrame, endpoint: str, parameters: dict = {}, *args):
    filename_inner = endpoint + '_'
    if parameters.get('page'):
        del parameters['page']
    for key, value in parameters.items():
        if isinstance(value,int):
            filename_inner += key + str(value) + '_'
        else:
            filename_inner += key + str(value) + '_'
    for value in args:
        filename_inner += value + '_'
    filename_inner += '.csv'
    data_to_s.to_csv(filename_inner, index=False)


def collect_players_data(get_new_data:bool = True) -> list:
    global t_s

    if not get_new_data:
        if os.path.exists('players_details_.csv'):
            raw_players_data = pd.read_csv('players_details_.csv').values.tolist()
            return raw_players_data

    raw_all_players_data = get_all_players_data(only_main_league=True, get_new_data=False)
    raw_act_squads_data = get_act_squads(only_main_leagues=True,get_new_data=False)

    df_players_data = pd.DataFrame(data = raw_all_players_data,
                                   columns=['player_id','reference_team','reference_date'])
    df_squads_data = pd.DataFrame(data = raw_act_squads_data, columns=['team_id','player_id','p_firstname'
        ,'p_lastname','p_age','p_nationality','season'])

    df_merged = df_players_data.merge(df_squads_data, on='player_id', how='left')
    df_data_to_fill = df_merged.loc[df_merged.isna().any(axis=1),:]
    df_data_filled = df_merged.loc[~df_merged.isna().any(axis=1),:]

    df_data_to_fill.loc[:,'reference_date'] = pd.to_datetime(df_data_to_fill.reference_date,format='%Y-%m-%d',errors='coerce').dt.date
    df_data_to_fill = df_data_to_fill.dropna(subset=['reference_date'])

    df_data_to_fill.loc[:,'season'] = df_data_to_fill.reference_date.apply(
            lambda x : x.year if x.month // 7 >= 1 else x.year - 1)

    calc_groups = df_data_to_fill.groupby(['reference_team','season'])['player_id'].size().reset_index(name='count')
    calc_groups_merged = df_data_to_fill.merge(calc_groups, on=['reference_team','season'], how='inner')

    teams_seasoned_data = dict()
    for item_row in calc_groups_merged.itertuples():
        collected = False
        print(f'here with player_id {item_row.player_id}')
        if not teams_seasoned_data.get(item_row.player_id):
            raw_data = call_api('https://v3.football.api-sports.io/players',
                                parameters_v={'season':int(item_row.season),'team': item_row.reference_team}
                                , headers_v=headers
                                , final_data = list())
            for item_inner in raw_data:
                for item_inner_ in item_inner:
                    row_list = list()
                    row_list.append(item_inner_['player']['firstname'])
                    row_list.append(item_inner_['player']['lastname'])
                    row_list.append(item_inner_['player']['age'])
                    row_list.append(item_inner_['player']['nationality'])

                    if item_inner_['player']['id'] == item_row.player_id:
                        collected = True
                    teams_seasoned_data[item_inner_['player']['id']] = row_list

        season_to_age = int(item_row.season)
        if not collected:
            tries = 2
            while not collected and tries:
                raw_data = call_api('https://v3.football.api-sports.io/players',
                                    parameters_v={'season': season_to_age, 'id': item_row.player_id}
                                    , headers_v=headers
                                    , final_data=list())
                if raw_data:
                    collected = True
                else:
                    season_to_age -= 1
                    tries -= 1
            if collected:
                for item_inner in raw_data:
                    for item_inner_ in item_inner:
                        row_list = list()
                        row_list.append(item_inner_['player']['firstname'])
                        row_list.append(item_inner_['player']['lastname'])
                        row_list.append(item_inner_['player']['age'])
                        row_list.append(item_inner_['player']['nationality'])

                        teams_seasoned_data[item_row.player_id] = row_list
            else:
                continue

        calc_groups_merged.loc[item_row.Index,'p_firstname'] = teams_seasoned_data[item_row.player_id][0]
        calc_groups_merged.loc[item_row.Index, 'p_lastname'] = teams_seasoned_data[item_row.player_id][1]

        age_insert = teams_seasoned_data[item_row.player_id][2] + int(datetime.now().year - season_to_age)
        calc_groups_merged.loc[item_row.Index, 'p_age'] = age_insert
        calc_groups_merged.loc[item_row.Index, 'p_nationality'] = teams_seasoned_data[item_row.player_id][3]

    concat_df = pd.concat([calc_groups_merged,df_data_filled]).reset_index(drop=True)
    save_retrieved_data(concat_df,'players_details')

    return concat_df.values.tolist()


def build_players_history(seasoned : bool = True) -> pd.DataFrame:
    global t_s

    transfer_window_inner = pd.read_excel('okna_trans_dane.xlsx', sheet_name='concat_data')
    data_leagues_inner = pd.read_csv('data_leagues.csv')
    merged_data = transfer_window_inner.merge(data_leagues_inner, left_on = 'Country', right_on = 'country_name', how='inner')

    if seasoned:
        players_data_inner = get_players_seasoned_data(get_logs_data=False, get_new_data=False)
        if players_data_inner:
            df_inner = pd.DataFrame(data = players_data_inner, columns=['player_id','full_name', 'firstname','lastname'
                ,'age','team_id','league_id'])
            df_inner.loc[:,'team_id'] = df_inner.apply(lambda x: x.team_id.split(','), axis=1)
            df_inner = df_inner.explode('team_id')
            df_inner.loc[:,'valid_since'] = pd.NA
            players_history_in = dict()
            t_s = datetime.now()
            for item in [54,178]:#df_inner.player_id.unique():
                player_history_inner = dict()
                data_transfers_inner = call_api('https://v3.football.api-sports.io/transfers',
                                                parameters_v={'player': item}, headers_v=headers, final_data=list())
                if data_transfers_inner:
                    for item_ in data_transfers_inner[0][0]['transfers']:
                        team_id = item_['teams']['in']['id']
                        if not player_history_inner.get(team_id):
                            player_history_inner[team_id] = item_['date']
                        else:
                            if isinstance(player_history_inner[team_id],list):
                                player_history_inner[team_id].append(item_['date'])
                            else:
                                current_value = player_history_inner[team_id]
                                player_history_inner[team_id] = [current_value, item_['date']]
                    players_history_in[item] = player_history_inner
                else:
                    return pd.DataFrame()
            for item in df_inner.itertuples():
                if players_history_in.get(item.player_id):
                    team_id_inner = int(item.team_id)
                    if players_history_in[item.player_id].get(int(team_id_inner)):
                        if isinstance(players_history_in[item.player_id],list):
                            df_inner.loc[item.Index,'valid_since'] = players_history_in[item.player_id][team_id_inner].pop(0)
                        else:
                            df_inner.loc[item.Index,'valid_since'] = players_history_in[item.player_id][team_id_inner]
                    else:
                        seasoned_player_history = list()
                        keep_check = True
                        season_to_call = 2023
                        data_player = call_api('https://v3.football.api-sports.io/players',parameters_v={'season': season_to_call,'id': item.player_id}
                                            ,headers_v=headers, final_data=list(), log_run=False)
                        while keep_check:
                            for item_inner in data_player[0][0]['statistics']:
                                seasoned_player_history.append(item_inner['team']['id'])
                            seasoned_player_history = list(set(seasoned_player_history))
                            if team_id_inner not in seasoned_player_history:
                                keep_check = False
                            else:
                                l_count = len(seasoned_player_history)
                                season_to_call -= 1
                                seasoned_player_history = list()
                                data_player = call_api('https://v3.football.api-sports.io/players',
                                                       parameters_v={'season': season_to_call, 'id': item.player_id}
                                                       , headers_v=headers, final_data=list(), log_run=False)
                        if l_count > 2:
                            data_transfer = merged_data.loc[merged_data[
                                merged_data.id == item.league_id].index[0], 'Open_winter']
                            data_to_write = f"{season_to_call + 1 if data_transfer.month % 6 > 1 else season_to_call}" \
                                            f"-{data_transfer.month:0>2}-{data_transfer.day:0>2}"
                        else:
                            data_transfer = merged_data.loc[
                                merged_data[merged_data.id == item.league_id].index[0], 'Open_summer']
                            data_to_write = f"{season_to_call + 1}-{data_transfer.month:0>2}-{data_transfer.day:0>2}."
                        df_inner.loc[item.Index,'valid_since'] = data_to_write

            return df_inner
        else:
            return pd.DataFrame()
    # --------------------------------
    #other option to call in function
    # --------------------------------
    elif not seasoned:
        final_list = list()
        final_list_duplicates=list()
        teams_raw = get_teams_data(only_main_leagues=True,get_new_data=False,season=2023)
        teams_inner = pd.DataFrame(data = teams_raw, columns=['team_id', 'league_id','team_name','team_code'])

        last_season_history = list()
        func_season = lambda x: x+ [season_inner]

        for season_inner in [2021,2022,2023]:
            actual_season = list()
            for item_inner in [1062,39,120]:#teams_inner.loc[:,'team_id'].unique()[:2]:
                raw_squad_data = call_api('https://v3.football.api-sports.io/players',
                                          parameters_v={'season': season_inner, 'team': item_inner}, headers_v=headers, final_data=list())
                for r_item in raw_squad_data:
                    for r_item_ in r_item:
                        actual_season.append([item_inner, r_item_['player']['id']])

            final_list_duplicates.extend(list(map(func_season,actual_season)))

            temp_season = actual_season
            actual_season = [hist for hist in actual_season if hist not in last_season_history]
            actual_season = list(map(func_season, actual_season))

            last_season_history = temp_season
            final_list.extend(actual_season)
        df_prep_org = pd.DataFrame(data=final_list, columns = ['team_id', 'player_id', 'season'])
        df_prep_org_dup = pd.DataFrame(data=final_list_duplicates,columns = ['team_id', 'player_id', 'season'])
        df_prep_gr = df_prep_org.groupby(['player_id'])['team_id'].apply(list).reset_index()

        final_list = list()

        for player_inner in df_prep_gr.itertuples():
            raw_data_transfers = call_api('https://v3.football.api-sports.io/transfers',
                                          parameters_v={'player': player_inner.player_id}, headers_v=headers, final_data=list())
            temp_teams = player_inner.team_id
            for t_item in raw_data_transfers:
                for t_item_ in t_item:
                    for transfer in t_item_['transfers']:
                        final_list.append([player_inner.player_id
                                           , transfer['teams']['in']['id']
                                           , transfer['date']])
                        if transfer['teams']['in']['id'] in temp_teams:
                            temp_teams.remove(transfer['teams']['in']['id'])

        df_prep_gr = df_prep_gr.explode('team_id')
        df_prep_gr_season = df_prep_org_dup.groupby(['player_id','season']).agg({'team_id':'count'})\
            .reset_index().set_index(['player_id','season']).rename(columns={'team_id':'how_many'})
        df_merged = df_prep_gr.merge(df_prep_org, on=['player_id','team_id'])
        merged_transfer_windows = teams_inner.merge(merged_data,left_on=['league_id'], right_on=['id'],how='inner')

        for player_inner in df_merged.itertuples():
            if df_prep_gr_season.loc[(player_inner.player_id,player_inner.season),'how_many'] > 1:
                ind_transfer = merged_transfer_windows.loc[teams_inner.team_id == player_inner.team_id,'Open_winter'].index[0]
                data_transfer = merged_transfer_windows.loc[ind_transfer,'Open_winter']
                final_list.append(
                    [player_inner.player_id,
                     player_inner.team_id,
                     f"{player_inner.season + 1 if data_transfer.month // 6 > 1 else player_inner.season}"
                     f"-{data_transfer.month:0>2}-{data_transfer.day:0>2}."]
                )
            else:
                ind_transfer = merged_transfer_windows.loc[teams_inner.team_id == player_inner.team_id, 'Open_summer'].index[0]
                data_transfer = merged_transfer_windows.loc[ind_transfer, 'Open_summer']
                final_list.append(
                    [player_inner.player_id,
                     player_inner.team_id,
                     f"{player_inner.season}-{data_transfer.month:0>2}-{data_transfer.day:0>2}"]
                )
        return pd.DataFrame(data=final_list, columns=['player_id','team_id','valid_since'])

    return pd.DataFrame()


t_s = datetime.now()

status_data = requests.get("https://v3.football.api-sports.io/status", headers = headers)
j_d_status = json.loads(status_data.content)

current_requests = j_d_status['response']['requests']['current']


data = collect_players_data(get_new_data=False)


