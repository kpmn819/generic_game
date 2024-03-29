#!/usr/bin/python


import sqlite3
import os
from datetime import datetime
from config import pi_db, nt_db

def db_start():
    if os.name == 'nt':
        db_path = nt_db
    else:
        db_path = pi_db

    global curs
    global conn
    #conn = sqlite3.connect('game_db.db')
    #conn = sqlite3.connect('/home/pi/game_web/game/db.sqlite3')
    conn = sqlite3.connect(db_path)


    curs = conn.cursor()

def db_close():
    curs.close()
    conn.close()    

def game_write(data):
    global curs
    global conn
    try:
        curs.execute("INSERT INTO game_code_game(name,dtime,score,free) VALUES(?,?,?,?);", data)
        conn.commit()
        curs.execute("SELECT MAX(id) FROM game_code_game;")
        this_game = curs.fetchone()
        #return this game's number for use in turns
        return this_game[0]
    except sqlite3.OperationalError as e:
        print(e)

def get_game():
    try:
        curs.execute("SELECT MAX(id) FROM game_code_game;")
        this_game = curs.fetchone()
        #return this game's number for use in turns
        return this_game[0]
    except sqlite3.OperationalError as e:
        print(e)
     
def turn_write(data):
    try:
        curs.execute("INSERT INTO game_code_qna(game_id,q_number,question,answer,correct) VALUES(?,?,?,?,?);", data)
        conn.commit() 
    except sqlite3.OperationalError as e:
        print(e)
def game_over(final_score):
    try:
        curs.execute("UPDATE game_code_game SET score=? WHERE id=?;", final_score)
        conn.commit() 
    except sqlite3.OperationalError as e:
        print(e)


# db_start()
'''now = datetime.now()
date_time = now.strftime("%m/%d/%Y,%H,%M,%S")

game_stuff =('jjjjjj', date_time, 0)
this_game = game_write(game_stuff)
print(this_game)
turn_stuff =(this_game,1,'a question','wronga',False)
turn_write(turn_stuff)
turn_stuff =(this_game,2,'another','correct',True)
turn_write(turn_stuff)
#conn.close()
#db_start()
final_score = (555555, this_game)
game_over(final_score)
curs.close()
conn.close() '''









'''import sqlite3
from datetime import datetime

class DataBase():
    def __init__(self, conn, curs):
        self.conn = conn
        self.curs = curs
 
    def start_game(self, data):
        self.curs.execute("INSERT INTO game(name,dtime,score) VALUES(?,?,?);", data)
        self.conn.commit()
        # need to get current game_no
    def end_game(self, score):
        pass
    def write_turn(self, data):
        pass
    def db_close(self):
        self.conn.close()
def start_db():
    conn = sqlite3.connect('game_db.db')
    curs = conn.cursor()
    return (conn, curs)


db_conn_curs = start_db()
db = DataBase(db_conn_curs[0], db_conn_curs[1])
data = ('frobozz', datetime.now, 0)
DataBase.start_game(db, data)
DataBase.db_close(db)'''
