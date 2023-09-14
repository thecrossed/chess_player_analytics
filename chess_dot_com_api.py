import requests
from datetime import date
from datetime import datetime
import json

def last_n_month(n):
    """
    purpose:
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

def get_user_archives(username, 
                      nr_months,
                     user_agent = {'User-Agent': 'username: tianminlyu, email: tianminlyu@gmail.com'}):
    """
    purpose:
    get archive monthly files of specific chess.com player
    
    input:
    username - username of the chess.com player
    nr_months - integer, nummber of past months that we want to get the archives
    # to request chess.com API
       user_agent = {'User-Agent': 'username: tianminlyu, email: tianminlyu@gmail.com'}
    
    output:
    target_month - files of archives according to months parameter
    """
    url = "https://api.chess.com/pub/player/{username}/games/archives".format(username = username)
    archive_request = requests.get(url, headers = user_agent)
    archives = archive_request.json()['archives']
    past_months = last_n_month(nr_months)
    target_month = []
    for archive in archives:
        if archive[-7:] in past_months:
            target_month.append(archive)
    return target_month
    
def get_archive_games(filename,
                     user_agent = {'User-Agent': 'username: tianminlyu, email: tianminlyu@gmail.com'}):
    """
    purpose:
    
    return games in one archive file
    
    input:
    filename - filename that contains game urls
    
    output: 
    """
    games = requests.get(filename,headers = user_agent).json()['games']
    return games