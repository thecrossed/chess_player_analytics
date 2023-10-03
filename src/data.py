import chess_dot_com_api as capi
import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
           'antleo0314',
           'AntLeoChess']

def lowercase_student(student_list):
    """
    to lowercase all the username
    
    input - list, list of student username, regardless upper or lower case
    
    output - list, list of student username, lower case
    """
    
    lower_students = [x.lower() for x in student_list]
    
    return lower_students


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
    results = []
    students = lowercase_student(students_username)
    for student in students:
        print(student.upper())
        archives = get_user_archives(student,2)
        #print(archives)
        for archive in archives[::-1]:
            games = get_archive_games(archive)
            for game in games[::-1]:
                #print(game)
                if (game['white']['username'].lower() == student.lower() and game['black']['username'].lower() in students):
                    end_time = datetime.utcfromtimestamp(game['end_time']).strftime('%Y-%m-%d %H:%M:%S')
                    print(end_time)
                    print("[w]" + student)
                    print("[b]" + game['black']['username'])
                    print("time control: " + game['time_control'])
                    print(game['pgn'].split("\n")[-2].split(" ")[-1]) # result
                    print("          ")
                    
                    end_times.append(end_time)
                    white_players.append(student.lower())
                    black_players.append(game['black']['username'].lower())
                    time_controls.append(game['time_control'])
                    urls.append(game['url'])
                    results.append(game['pgn'].split("\n"))
                    
                elif (game['black']['username'].lower() == student.lower() and game['white']['username'].lower() in students):
                    end_time = datetime.utcfromtimestamp(game['end_time']).strftime('%Y-%m-%d %H:%M:%S')
                    print(end_time)
                    print("[w]" + game['white']['username'])
                    print("[b]" + student)
                    print("time control: " + game['time_control'])
                    print(game['pgn'].split("\n")[-2].split(" ")[-1])
                    print("          ")
                    
                    end_times.append(end_time)
                    white_players.append(game['white']['username'].lower())
                    black_players.append(student.lower())
                    time_controls.append(game['time_control'])
                    urls.append(game['url'])
                    results.append(game['pgn'].split("\n")[-2].split(" ")[-1])

    print("---------")
    return end_times, white_players, black_players, time_controls, urls, results
