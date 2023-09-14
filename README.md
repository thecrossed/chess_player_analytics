# chess_analytics_pipeline

## Purpose

This repo aims at automating the analytics work of the RCC chess club.

## Description

1. .github/workflows

It stores the schedule and workflow of github actions. One can adjust the time for the automated pipeline to work.

2. .ipython_checkpoints

It stores the status of the chess_game_result.ipynb file

3. test notebooks

It is used to store ipynb for testing purpose

4. main.py

It is python file storing the code in production.

5. requirements.txt

It stores the python package that need to be installed

6. status.log

Log the message when the workflow runs.

7. output data

Storing output data

8. chess_dot_com_api.py

Module dealing with chess.com api

9. googlesheet.py

Module dealing with google sheet

10. stuudents.py

Module dealing with student data

11. games.py

Module dealing with game data



## Project
1. Generate game results for BO, BP and talented 2023 fall classes

RCC club have weekly round-robin chess games for each class. Currently, teaching assistants need to visit the profile page of chess.com of each player to record the game result into a google spreadsheet. This project aims to automate the work by calling chess.com API to get the games data and log it into a csv file which teaching assistants can download from this repo and upload to the google spreadsheet. Sending game and result dataframe to [RCC_tianmin_students_games](https://docs.google.com/spreadsheets/d/1YbU3GZq58mWu5Kl4l4gPhq96aohmk8gFxbzGr6cpA7o/edit#gid=1280403112) 

## Contact person

tianminlyu@gmail.com
