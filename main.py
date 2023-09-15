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
import data



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

"""
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
"""
    
# main function    
def main(): 
    collected_data = data.game_data_collect()
    df = g.to_pandas_df(collected_data)
    print("data is converted into pandas")
    g.upload_df("2023fall", df, '1YbU3GZq58mWu5Kl4l4gPhq96aohmk8gFxbzGr6cpA7o')
    
if __name__ == "__main__":
    main()

