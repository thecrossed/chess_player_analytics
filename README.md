# chess_analytics_pipeline

## Purpose

This repo aims at automating the analytics work of the rcc chess club.

## Description

1. .github/workflows

It stores the schedule and workflow of github actions. One can adjust the time for the automated pipeline to work.

2. .ipython_checkpoints

It stores the status of the chess_game_result.ipynb file

3. chess_game_result.ipynb

It is used to test our code before implementing into main.py

4. main.py

It is python file storing the code in production.

5. requirements.txt

It stores the python package that need to be installed

6. status.log

Log the message when the workflow runs.

## Project
1. Generate game results for BO, BP and AN 2023 spring classes

RCC club have weekly round-robin chess games for each class. Currently, teaching assistants need to visit the profile page of chess.com of each player to record the game result into a google spreadsheet per class. This project aims to automate the work by calling chess.com API to get the games data and log it into a csv file which teaching assistants can download from this repo and upload to the google spreadsheet.

Main steps -

a. Get a collection of student username and the class they are in (json format)

b. Calling the chess.com API for each student for their game archives of the past three months

c. Extracting the username, game_starttime, game_endtime, white_username, black_username, Result from data in step b.

d. Filtering out the games that don't have both players are in the same class

e. calculate how many seconds of each game (TA might need this info to exclude games that don't count)

f. generate a csv file with a file name indicating the time when the work is done

g. push the change into the repo

h. Automately run the job every day

i. Sending emails to relevant people that this work is done successfully or not

## Contact person

tianminlyu@gmail.com
