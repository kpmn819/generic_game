# attempt to do a generic game format with classes

# IMPORTS START --------------------------------------------------
# makes extensive use of pygame to blit the screen
import game_util as gu
from genericpath import exists
from http.client import PROXY_AUTHENTICATION_REQUIRED
from lib2to3.pgen2.token import NUMBER
from random import randrange, shuffle, random, sample
#from random import sample
from time import sleep, time
import sys, pygame, os
from tkinter import FALSE
#from xml.dom import WrongDocumentErr
#from xml.etree.ElementTree import QName
from pygame.locals import *
if os.name == 'nt':
    pass
else:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
import pygame.font
import os
# code to use comma seperated values
import csv
# code to break up long strings
import textwrap
''' this decorater wraps the major functions and methods
to allow resetting the game if they walk away'''
import timeout_decorator


# /////////////////  VARIABLES AND CONSTANTS ///////////////////////////

# \\\\\\\\\\\\\\\\\ END VARIABLES AND CONSTANTS \\\\\\\\\\\\\\\\\\\\\\\\

# //////////////////  CLASSES ///////////////////////////////////////////
# !!!!!!!!!!!
class Game():
    def __init__(self, background, qu_ans, score, num_ans, reward= None):
        self.background = background
        self.qu_ans = qu_ans # all of the questions and answers
        self.score = score
        self.reward = reward
        self.num_ans = num_ans # how many answers per question

        # how many q and a are there, how many do we need assume 5?
        q_count = len(qu_ans)
        q_random = sample(range( 0, q_count), 5)
        self.q_random = q_random
        self.q_thisgame = []
        self.a_thisgame = []
         # make a list of just the questions for this game
        for q in self.q_random:
            self.q_thisgame.append(self.qu_ans[q][0]) # now we have our game q & a
            # now let's get the list of the answers
            for x in range(self.num_ans):
                self.a_thisgame.append(self.qu_ans[q][x + 1])
        # make a temp list to group the answers per question
        temp_list = []
        for i in range(0, len(self.a_thisgame), num_ans):
            temp_list.append(self.a_thisgame[i:i+num_ans])
        self.a_thisgame = temp_list # all cleaned up and ready
        # leaving here our Game has the questions and answers a passed in score of (0,0)
        # and a background
    # ============= end of Game class initialization ================   

    def take_turn(self):
        pass       
    
 # ============ end of Game class methods ===============       
            
# !!!!!!!!!!!!
class Port():
    def __init__(self, p_num, input, state= None):
        self.p_num = p_num
        self.input = input
  
        # need to setup gpio port here
        if self.input:
            if os.name != 'nt':
                GPIO.setup(p_num, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            else:
                #print('input port not set')
                pass
        else:
            if os.name != 'nt':
                GPIO.setup(p_num, GPIO.OUT)
            else:
                #print('output port not set')
                pass
    def change_state(self):
        if not self.input:
            if self.state:
                self.state = False
            else:
                self.state = True
        else:
            pass
    def out_high(self):
        if not self.input:
            self.state = True
        else:
            pass
    def out_low(self):
        if not self.input:
            self.state = False
        else:
            pass
    def read_state(self):
        if self.input:
            # read the port
            print('reading port')
            return self.state
        else:
            pass
    def change_config(config):
        if config == 'free_and_pay':
            pass
        if config == 'five_on':
            pass
        if config == 'three_on':
            pass


# !!!!!!!!!!!!!
class Screen():
    def __init__(self, background, fs_text= None, questions= None, 
                 answers= None,  score= None, arrows= None, highlights= None):
        
        self.questions = questions
        self.fs_text = fs_text
        self.answers = answers
        self.background = background
        self.score = score
        self.arrows = arrows
        self.highlights = highlights
      

# \\\\\\\\\\\\\\\\\\\\ END CLASSES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def init():
    # set up the ports port#, input T/F, state T/F (optional)
    light_1 = Port(24, False, True)
    light_2 = Port(25, False, True)
    light_3 = Port(12, False, False)
    light_4 = Port(18, False, False)
    light_5 = Port(14, False, False)
    light_fp = Port(16,False, False)

    butn_1 = Port(4, True, False)
    butn_2 = Port(17, True, False)
    butn_3 = Port(27, True, False)
    butn_4 = Port(22, True, False)
    butn_5 = Port(5, True, False)
    butn_free = Port(13, True, False)
    butn_pay = Port(26, True, False)
    
 
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    clock = pygame.time.Clock()
    screen_width = 1920
    screen_height = 1080
    bgColor = (0,0,0)
    size = (screen_width, screen_height)
    global white 
    white = (255, 255, 255)
    global black
    black = (0, 0, 0)
    global red
    red = (255, 0, 0)
    global blue
    blue = (0, 0, 255)
    # for autostart to work properly uncomment the line below
    #display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    #display = pygame.display.set_mode((1920,1080))
    # assign I/O ports here ////////////

    # set path name to graphics and sound files here ///////

    # make picture files objects for pygame here ////////

    # load picture objects into pygame here ///////
    # get file data
    global correct
    correct = get_file('right_resp.csv', 1)[0]
    #correct = correct[0]
    global qna
    qna = get_file('qna_pool.csv', 4)[0]
    global wrong
    wrong = get_file('wrong_resp.csv', 1)[0]
    global picture
    picture = get_file('picture.csv', 6)[0]
# /////////////////// START UTILITY METHODS ////////////////////////
def get_file(list_file, col_count):
    # now a more generic reader that can take any number of columns
    global row_count
    global file_error
    try:
        ''' call with file and get back list of lists'''
        with open(list_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            rowlist = []
            cvs_list = []
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    # avoids the header line
                    rowlist = [row[0]] # initalizes the list first item
                    if col_count > 1:
                        for x in range(1,col_count):
                            rowlist.append(row[x])
                        
                    cvs_list.append(rowlist)
                    # this is a 0 based list of lists
                    # access questions_list[q# - 1][column]
                line_count += 1
            #print(f'Processed {line_count} lines.')
            row_count = line_count - 1
            # returns lists within lists acces via [list of items][items]
            return [cvs_list]
    except FileNotFoundError:
        print('file not found')
        # print message on screen
        file_error = True
        

# \\\\\\\\\\\\\\\\\\\ END UTILITY METHODS \\\\\\\\\\\\\\\\\\\\\\\\\\

#////////////////// START METHODS /////////////////////////
# CHOOSE GAME ------
def choose_game():
    global curr_game
    print('1= dolphin, 2= Bonehenge, 3= humpback')
    #game_to_play = input('A number please  ')
    game_to_play = '1'
    # make the game object and call it curr_game
    if game_to_play == '1':
        curr_game = Game('water.jpeg', picture, (0,0), 5)
        print('dolphin selected')
    if game_to_play == '2':
        curr_game = Game('bonehenge.jpeg', qna, (0,0), 3)
    print('Here are the questions for curr_game')
    print(curr_game.q_thisgame)
    print('And the answers')
    print(curr_game.a_thisgame)

def pay_free():
    # put up screen
    # change lights
    pass

    
# GAME LOOP -------
def game_loop():
    choose_game()
    # game must be created first
    global curr_game
    pay_free()


    curr_game.take_turn()
    print('took a turn')    

#\\\\\\\\\\\\\\\\\\\\\\ END METHODS \\\\\\\\\\\\\\\\\\\\\\\\




def main():
    try:
        init()
        got = gu.something('here we are')
        print(got)
        global curr_game
    
        try:
            curr_game
        except NameError:
                print('no dolphin defined')
        else:
            del dolphin
        
        game_loop()

        
    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        #
        # GPIO.cleanup()

if __name__ == '__main__':
    main()