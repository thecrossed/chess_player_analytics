import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

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
    df['result'] = fetched_data[5]
    df['white_rating'] = fetched_data[6]
    df['black_rating'] = fetched_data[7]
    df['white_accuracy'] = fetched_data[8]
    df['black_accuracy'] = fetched_data[9]
    df = df.sort_values(by = 'end_time', ascending = False)
    df = df.drop_duplicates()
    
    return df

def to_pandas_move(fetched_data):
    """
    Import fetched game data into a pandas dataframe
    
    and then sort and drop duplicates
    """
    df = pd.DataFrame()
    df['move_num'] = fetched_data[0]
    df['move'] = fetched_data[1]
    df['clk'] = fetched_data[2]
    df['urls'] = fetched_data[3]
    df['end_time'] = fetched_data[4]
    df = df.astype('str')
    df['move_num'] = df['move_num'].astype('int')
    df = df.drop_duplicates()
    df = df.sort_values(by = ['end_time','move_num'], ascending = [False,True])
    
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
    # info about credential 
    # https://developers.google.com/workspace/guides/create-credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name("./creds.json", scope)
    wks_name = name
    df = rp_nan_empty(df)
    d2g.upload(df, sheet_url, wks_name, credentials=creds)  
