import logging
import logging.handlers
import os
import io
import pandas as pd
import numpy as np
import requests
from chessdotcom import get_player_profile, get_player_stats, get_player_game_archives
import chess.pgn
from converter.pgn_data import PGNData
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise
    
# students from Tianmin's classes - BO, BP, AN
tianmin_players = {
    "Teacher" : ['tianminlyu'],
    "BO" : ['AGcuber19',
            'TLPAWN',
            'xiaoanwu',
            'EmmaXLi',
            'akfunchess66',
            'Marsboom', 
            'Claraqiu',
            'Ravenclawfairy', 
            'Zora_zhu',
            'BurleyWalrus'],
    "BP" : ['taionemm',
            'augustinewz',
            'oscarzhang818',
            'yaohengli',
            'Wallacewang1214',
            'SophiaZ2022',
            'AliceCLi',
            'yumitang',
            'james2945',
            'Oinkoinkw',
           'DDisawesome'], # this is the new username for Oinkoinkw (Winston Rao)
    "AN" : ['Cathye1',
            'lunathekitsune',
            'ArthurRocket',
            'vivianwwww20',
            'ChloeWang16',
            'Tyzalex',
            'ZhichengW',
            'Haochen1123',
            'jaydenlan0118',
            'ImRacoonie']
}

def student_df(student_data):
    """
    input:
    student_data - dictionary, where key is the class and value is a list of username of each student
    
    output:
    a dataframe having two columns - class, student class; username, student username
    """
    df = pd.DataFrame({'Keys': list(student_data.keys()), 'Values': list(student_data.values())})
    df = df.explode(column='Values').reset_index(drop=True)
    df.rename(columns = {'Keys':'class', 'Values':'username'}, inplace = True)
    return df

def last_n_month(n):
    """
    return the month as yyyy/mm format of the past n months from now
    input -
    n: number of months from past
    
    output -
    a list of month with yyyy/mm format
    """
    months_lst = []
    for num in range(n):
        months = date.today() + relativedelta(months=-num)
        if months.month <= 9:
            months_lst.append(str(months.year) + "/"+ "0" + str(months.month))
        else:
            months_lst.append(str(months.year) + "/"+ str(months.month))
    return months_lst

def get_user_archives(username, months):
    """
    get archive monthly files of specific chess.com player
    input:
    username - username of the chess.com player
    months - target months that we want to get the archives
    
    output:
    target_month - files of archives according to months parameter
    """
    archives = get_player_game_archives(username).json['archives']
    target_month = []
    for archive in archives:
        if archive[-7:] in months:
            target_month.append(archive)
    return target_month

def get_archive_games(filename):
    """
    return games in one archive file
    
    input:
    filename - filename that contains game urls
    
    output: 
    """
    games = requests.get(filename).json()['games']
    return games

def game_result(username,file):
    """
    get username, game_starttime, game_endtime, white_username, black_username, Result from game data
    input -
    username: of the player
    file: the file stored games data
    
    output -
    a dataframe that contains username, game_starttime, game_endtime, white_username, black_username, Result
    """
    usernames = []
    uuid = []
    url = []
    initial_setup = []
    time_class = []
    time_control = []
    start_time = []
    end_time = []
    white_username = [] 
    black_username = []
    result = []
    UTCDate = []
    
    games = get_archive_games(file)
    
    for game in games:
        try:
            usernames.append(username)
            uuid.append(game.get('uuid',None))
            url.append(game.get('url',None)) # game.get('url', None)
            initial_setup.append(game.get('initial_setup',None))
            time_class.append(game.get('time_class',None))
            time_control.append(game.get('time_control',None))
            white_username.append(game.get('white',None)['username'])
            black_username.append(game.get('black',None)['username'])
            pgn_written = io.StringIO(game['pgn'])
            game_data = chess.pgn.read_game(pgn_written)
            result.append(game_data.headers['Result'])
            start_time.append(game_data.headers['StartTime'])
            end_time.append(game_data.headers['EndTime'])
            UTCDate.append(game_data.headers['UTCDate'])
        except Exception as e:
            print(e)
    df = pd.DataFrame(list(zip(usernames,  
                           uuid,
                           url,
                           initial_setup,
                           time_class,
                           time_control,
                           end_time,
                           white_username,
                           black_username,
                           result,
                           start_time,
                           UTCDate
                              )),
               columns =['username',
                         'uuid',
                         'url',
                         'initial_setup',
                         'time_class',
                         'time_control',
                         'end_time',
                         'white_username',
                         'black_username',
                         'Result',
                         'StartTime',
                         'UTCDate'
                        ])
    return df

def class_games(n):
    """
    input:
    n- number of past months thee data set has retrieved
    output
    return a dataframe that contains what game_result function returns for each player in the classes
    """
    result_df = []
    for classes in tianmin_players.keys():
        for player in tianmin_players[classes]:
            try:
                logger.info(f'The game of this : {player} is being proccessed...')
                months = last_n_month(n)
                files = get_user_archives(player,months)
                for file in files: 
                    result = game_result(player,file)
                    result_df.append(result)
            except:
                pass
    df = pd.concat(result_df)
    return df

def same_class(df):
    """
    ensure that the players are from the same class
    
    input:
    df - the targeted dataframe
    
    output:
    a new dataframe where rows containing only white user class equals to black user class
    """
    new_df = df.loc[df['white_user_class'] == df['black_user_class']]
    return new_df
        

def game_class():
    """
    output - a dataframe that have column white_user_class indicate the class of the white username and black_user_class for black
    """
    games = class_games(5)
    students = student_df(tianmin_players)
    
    students['username_lower'] = students['username'].str.lower()
    games['white_username_lower'] = games['white_username'].str.lower()
    games['black_username_lower'] = games['black_username'].str.lower()

    games_white = games.merge(students.rename({'username_lower': 'white_username_class_lower'}, axis=1),
               left_on='white_username_lower', right_on='white_username_class_lower', how='left')

    games_white_black = games_white.merge(students.rename({'username_lower': 'black_username_class_lower'}, axis=1),
               left_on='black_username_lower', right_on='black_username_class_lower', how='left')
    
    df = games_white_black.rename(columns={"class_x": "white_user_class", "class_y": "black_user_class"})
    df['start_date_time'] = pd.to_datetime(df['UTCDate'] + ' ' + df['StartTime'])
    df = df[['username', 'uuid', 'url', 'initial_setup', 'time_class',
       'time_control', 'end_time', 'white_username', 'black_username',
       'Result', 'StartTime', 'UTCDate', 'white_user_class','black_user_class','start_date_time']]    
    return df

def filter_game(df):
    """
    return a dataframe that contains only relevant games
    """
    new_df = df.loc[df['time_control'].isin(['900+10','600+5','600'])]
    new_df = new_df.loc[new_df['start_date_time'] >= '2023-02-17']
    new_df = new_df.loc[new_df['initial_setup'] == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1']
    new_df = new_df.drop_duplicates(subset=['uuid'])
    
    return new_df

def replace_username(df, old_name, new_name):
    """
    input 
    df - target df
    old_name - old username that is to be replaced
    new_name - new username that is replacing the old one
    
    output -
    return a dataframe that the old username has been replaced
    """
    
    df = df.replace({old_name: new_name})
    return df

def class_select(df, classname):
    """
    input:
    df - targeted df
    classname - str, class name
    """
    class_df = df.loc[df['white_user_class'] == classname]
    
    return class_df

def first_game(df):
    """
    only remain the first game played between each pair of players, regardless white or black
    """
    df[['white_result', 'black_result']] = df["Result"].apply(lambda x: pd.Series(str(x).split("-")))

    players = pd.DataFrame(np.sort(df[['white_username','black_username']].values, axis=1), columns=df[['white_username','black_username']].columns)
    
    df['players'] = players.values.tolist()
    df['players'] = df['players'].astype(str)
    
    df["rank"] = df.groupby("players")["start_date_time"].rank(method="dense", ascending=True)
    df_first_game = df.loc[df['rank'] == 1]
    return df_first_game

def class_pivot(df):
    """
    Return a pivoted table where row/column representing each player and each cell storing the game result
    """
    df = df.replace({'1/2': 0.5})
    df['white_result'] = df['white_result'].astype(float)
    df['black_result'] = df['black_result'].astype(float)
    white_username_index = df.pivot(index='white_username', columns='black_username', values='white_result').reset_index()
    white_username_index = white_username_index.rename(columns={"white_username": "player"})
    
    black_username_index = df.pivot(index='black_username', columns='white_username', values='black_result').reset_index()
    black_username_index = black_username_index.rename(columns={"black_username": "player"})
    
    merge = white_username_index.append(black_username_index)
    
    merge_aggr = merge.groupby(['player']).max().reset_index()
    
    return merge_aggr

    
def main():
    df = game_class()
    df_newname = replace_username(df, "Oinkoinkw","DDisawesome")
    new_df = same_class(df_newname)
    filter_df = filter_game(new_df)
    filter_df_cols = filter_df[['white_username', 'black_username', 'url','UTCDate', 
       'StartTime', 'end_time','Result', 'white_user_class','black_user_class','start_date_time']]   
    filter_df_cols = filter_df_cols.sort_values(by = ['white_user_class','UTCDate','white_username','black_username'], ascending = False)
    filter_df_cols.to_csv("game_class.csv")
    now = datetime.now()
    for classname in filter_df_cols['white_user_class'].unique():
        class_df = class_select(filter_df_cols, classname)
        first_game_df = first_game(class_df)
        class_result = class_pivot(first_game_df)
        class_result.to_csv("game_result/{}_class_result_{}.csv".format(classname, now))
        

if __name__ == "__main__":
    main()
