
#!/usr/bin/python
import sqlite3
from datetime import datetime


from generic_game import final_score

def db_start():
    
    global curs
    global conn
    conn = sqlite3.connect('game_db.db')
    curs = conn.cursor()
    

def game_write(data):
    global curs
    global conn
    try:
        curs.execute("INSERT INTO game(name,dtime,score) VALUES(?,?,?);", data)
        conn.commit()
        curs.execute("SELECT MAX(game_no) FROM game;")
        this_game = curs.fetchone()
        #return this game's number for use in turns
        return this_game[0]
    except sqlite3.OperationalError:
        pass
def turn_write(data):
    try:
        curs.execute("INSERT INTO qna(game_no,q_number,question,answer,correct) VALUES(?,?,?,?,?);", data)
        conn.commit() 
    except sqlite3.OperationalError:
        pass
def game_over(final_score):
    try:
        curs.execute("UPDATE game SET score=? WHERE game_no=?;", final_score)
        conn.commit() 
    except sqlite3.OperationalError as e:
        print(e)


db_start()
now = datetime.now()
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
final_score = (777, this_game)
game_over(final_score)

conn.close()   
