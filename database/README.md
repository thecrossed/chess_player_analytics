schema 

* Class

class_id, int, Primary key/ foreign key, not null;

class_name, str, not null;

start_year, int, not null;

term_no, int, not null;

level, str;

* Student

student_id, int, Primary key; foreign key, not null;

class_id, int, foreign key, not null;

student_name, str, not null;

chessdotcom_account_name, str;


* Game

game_id, int, Primary key; foreign key, not null;

white_student_id,

white_player_username,

black_student_id,

black_player_username,

time_start,

time_control,

game_url,

game_result



* Move

game_id,

move_id,

move_nr,

is_white_move,

png,

move_play_time








