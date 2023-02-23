import logging
import logging.handlers
import os
import io
import pandas as pd
import requests
from chessdotcom import get_player_profile, get_player_stats, get_player_game_archives
import chess.pgn
from converter.pgn_data import PGNData

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
    start_time = []
    end_time = []
    white_username = [] 
    black_username = []
    result = []
    
    games = get_archive_games(file)
    
    for game in games:
        try:
            usernames.append(username)
            logger.info(f'Username is : {username}')
            white_username.append(game.get('white',None)['username'])
            black_username.append(game.get('black',None)['username'])
            pgn_written = io.StringIO(game['pgn'])
            game_data = chess.pgn.read_game(pgn_written)
            result.append(game_data.headers['Result'])
            start_time.append(game_data.headers['StartTime'])
            end_time.append(game_data.headers['EndTime'])
        except Exception as e:
            print(e)
    df = pd.DataFrame(list(zip(usernames,                               
                          end_time,
                           white_username,
                           black_username,
                          result,
                          start_time
                              )),
               columns =['username',
                        'end_time',
                        'white_username',
                        'black_username',
                           'Result',
                          'StartTime'
                        ])
    return df

def class_games():
    result_df = []
    for classes in tianmin_players.keys():
        for player in tianmin_players[classes]:
            try:
                files = get_user_archives(player,["2023/02"])
                file = files[-1]
                result = game_result(player,file)
                result_df.append(result)
            except:
                pass
    df = pd.concat(df_players)
    return df
        

def main():
    df = class_games()
    df.to_csv("game_result.csv")
    

if __name__ == "__main__":
    main()
