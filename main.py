import logging
import logging.handlers
import os
import io
import pandas as pd
import numpy as np
import requests
import json
# from chessdotcom import get_player_profile, get_player_stats, get_player_game_archives  (not working)
import chess.pgn
from converter.pgn_data import PGNData
import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import sys
import chess_dot_com_api as capi
import googlesheet as g


"""
input for logger

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
"""

""" SECRET
try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    logger.info("Token not available!")
    #raise
    
# load data from student json
with open('./students.json') as user_file:
    file_contents = user_file.read()

parsed_json = json.loads(json.loads(file_contents))

print(parsed_json)
"""


# student data - will be transferred to database
students_username = ['yaohengli',
           'chessloverma',
           'chengliam',
           'emmaxli',
           'akfunchess66',
           
           'willhanzhu',
           'TLPAWN',
           'Jasminezhao777',
           'Justinzhao777',
           'Milkmilkok',
           'zlicyigloo',
           'Zora_zhu',
           'dogwater1012000',
           
           'AJLinVH',
           'charliezienyang',
           'whatwhywhywhat',
           'ZhouYuanLi',
           'Logicalcheetah26',
           'Nolan330',
           'antleo0314']

def lowercase_student(student_list):
    """
    to lowercase all the username
    
    input - list, list of student username, regardless upper or lower case
    
    output - list, list of student username, lower case
    """
    
    lower_students = [x.lower() for x in student_list]
    
    return lower_students


def student_df(student_data):
    """
    purpose:
    transform student_data dictionary data into a pandas dataframe
    
    input:
    student_data - dictionary, where key is the class and value is a list of username of each student
    
    output:
    a dataframe having two columns - class, student class; username, student username
    """
    df = pd.DataFrame({'Keys': list(student_data.keys()), 'Values': list(student_data.values())})
    df = df.explode(column='Values').reset_index(drop=True)
    df.rename(columns = {'Keys':'class', 'Values':'username'}, inplace = True)
    return df


def game_data_collect():
    """
    collect game data for each student from the json raw data -
    end_times
    white_players
    black_players
    time_controls
    urls
    """
    end_times = []
    white_players = []
    black_players = []
    time_controls = []
    urls = []
    students = lowercase_student(students_username)
    for student in students:
        print(student.upper())
        archives = capi.get_user_archives(student,2)
        #print(archives)
        for archive in archives[::-1]:
            games = capi.get_archive_games(archive)
            for game in games[::-1]:
                #print(game)
                if (game['white']['username'].lower() == student.lower() and game['black']['username'].lower() in students):
                    end_time = datetime.utcfromtimestamp(game['end_time']).strftime('%Y-%m-%d %H:%M:%S')
                    print(end_time)
                    print("[w]" + student)
                    print("[b]" + game['black']['username'])
                    print("time control: " + game['time_control'])
                    print("          ")
                    
                    end_times.append(end_time)
                    white_players.append(student.lower())
                    black_players.append(game['black']['username'].lower())
                    time_controls.append(game['time_control'])
                    urls.append(game['url'])
                    
                elif (game['black']['username'].lower() == student.lower() and game['white']['username'].lower() in students):
                    end_time = datetime.utcfromtimestamp(game['end_time']).strftime('%Y-%m-%d %H:%M:%S')
                    print(end_time)
                    print("[w]" + game['white']['username'])
                    print("[b]" + student)
                    print("time control: " + game['time_control'])
                    print("          ")
                    
                    end_times.append(end_time)
                    white_players.append(game['white']['username'].lower())
                    black_players.append(student.lower())
                    time_controls.append(game['time_control'])
                    urls.append(game['url'])
    print("---------")
    return end_times, white_players, black_players, time_controls, urls

def to_pandas_df(fetched_data):
    """
    Import fetched game data into a pandas dataframe
    
    and then sort and drop duplicates
    """
    df = pd.DataFrame()
    df['end_time'] = fetched_data[0]
    df['white_player'] = fetched_data[1]
    df['black_player'] = fetched_data[2]
    df['time_control'] = fetched_data[3]
    df['url'] = fetched_data[4]
    df = df.sort_values(by = 'end_time', ascending = False)
    df = df.drop_duplicates()
    
    return df

def rp_nan_empty(df):
    """
    purpose:
    replace null value in the df with "" string so that in google sheet it will turn out to be empty space, rather than 'nan'
    """
    df = df.fillna("")

    return df

def upload_df(name, df, sheet_url):
    """
    purpose:
    upload df to google sheet RCC_chess_game_result
    each class/csv/file represent one sheet
    
    input - 
    name: class name, sheet tab
    df: df that will be uploaded for each tab
    """
    #spreadsheet_key = '12R6hwzKys_DQE6vFpuOLGpe68hGHktSzd65AkR0nOsA' # sheet url from RCC_chess_game_result
    scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("./creds.json", scope)
    wks_name = name
    df = rp_nan_empty(df)
    d2g.upload(df, sheet_url, wks_name, credentials=creds)  
    
# main function    
def main(): 
    collected_data = game_data_collect()
    df = g.to_pandas_df(collected_data)
    g.upload_df("2023fall", df, '1YbU3GZq58mWu5Kl4l4gPhq96aohmk8gFxbzGr6cpA7o')
    
if __name__ == "__main__":
    main()

