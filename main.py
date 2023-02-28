import logging
import logging.handlers
import os
import io
import pandas as pd
import requests
from chessdotcom import get_player_profile, get_player_stats, get_player_game_archives
import chess.pgn
from converter.pgn_data import PGNData
from datetime import date
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
            'Oinkoinkw'],
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
    games = class_games(3)
    students = student_df(tianmin_players)
    
    games_white = games.merge(students.rename({'username': 'white_username_class'}, axis=1),
               left_on='white_username', right_on='white_username_class', how='left')

    games_white_black = games_white.merge(students.rename({'username': 'black_username_class'}, axis=1),
               left_on='black_username', right_on='black_username_class', how='left')

    df = games_white_black[['username', 'uuid', 'url', 'initial_setup', 'time_class',
       'time_control', 'end_time', 'white_username', 'black_username',
       'Result', 'StartTime', 'UTCDate', 'class_x','class_y']]

    df = df.rename(columns={"class_x": "white_user_class", "class_y": "black_user_class"})
    
    return df

def filter_game(df):
    """
    return a dataframe that contains only relevant games
    """
    new_df = df.loc[df['time_control'] == '900+10']
    new_df = new_df.loc[new_df['initial_setup'] == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1']
    return new_df
    
def main():
    # df = class_games(3)
    # df.to_csv("game_result.csv")
    #student_data = student_df(tianmin_players)
    # student_data.to_csv("student_data.csv")
    df = game_class()
    new_df = same_class(df)
    filter_df = filter_game(new_df)
    filter_df.to_csv("game_class.csv")
    nr_user = filter_df['username'].nunique()
    logger.info(f'{nr_user} of users have been fetched.')
    logger.info(f'{df['username'].nunique()} of users have been fetched - before filtered.')

if __name__ == "__main__":
    main()
