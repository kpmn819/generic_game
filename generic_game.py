# attempt to do a generic game format with classes

# IMPORTS START --------------------------------------------------
# makes extensive use of pygame to blit the screen

from genericpath import exists
from http.client import PROXY_AUTHENTICATION_REQUIRED
from lib2to3.pgen2.token import NUMBER
from random import randrange, shuffle, random, sample
#from random import sample
from time import sleep, time
import sys, pygame, os
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

# //////////////////  CLASSES ////////////////////////////////////////////
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
        # leaving here our Game has the questions and answers a passed in score of (0,0)
        # and a background
    # ============= end of Game class initialization ================   

        
    def take_turn(self):
        pass    
        
            
            

        


class Port():
    def __init__(self, p_num, input, state= None):
        self.p_num = p_num
        self.input = input
        self.state = state
        # need to setup gpio port here
        if self.input:
            print('Port ' + str(self.p_num) + ' is an input')
            if os.name != 'nt':
                GPIO.setup(p_num, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        else:
            print('Port ' + str(self.p_num) + ' is an output')
            if os.name != 'nt':
                GPIO.setup(p_num, GPIO.OUT)
    def change_state(self):
        if not self.input:
            if self.state:
                self.state = False
            else:
                self.state = True
        else:
            pass
    def read_state(self):
        if self.input:
            # read the port
            print('reading port')
            return self.state
        else:
            pass

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
    # set up the ports
    light_1 = Port(14, False, True)
    light_2 = Port(15, False, True)
    butn_1 = Port(23, True, False)
 
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
    display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
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
MASTER_TIMEOUT = 300
#@timeout_decorator.timeout(MASTER_TIMEOUT,use_signals=True)
def game_loop():
    global dolphin
    dolphin.take_turn()
    print('took a turn')    
    print('This is dolphin.q_thisgame')
    print(dolphin.q_thisgame)
    print('these are the answers')
    print(dolphin.a_thisgame)
    




def main():
    try:
        init()
        global dolphin # so it can be seen everywhere
        global bonehenge
        global humpback
        global another_game
    
        home_screen = Screen('nice picture.jpeg', 'Welcome to the game')
        print(home_screen.fs_text) 
        #print(qna)
        #print(len(qna))
        #print(qna[1])
        #print(qna[1][0])
        # this little construct will see if the game exists already
        # if it does delete it and make another this is for the loop 
        try:
            dolphin
        except NameError:
                print('no dolphin defined')
        else:
            del dolphin
        dolphin = Game('water.jpeg', picture, (0,0), 5)
        #print(dolphin.qu_ans)
    
     
        #print(dolphin.just_a)
        game_loop()

        ''' BASIC PROGRAM
        init() initialize variables, screen settings and setup ports
        LOOP START
        Show home screen
        Show game selection if any
        Show donation screen if any
        Enter game loop w/timeout
        Show final score award prize if any
        
         LOOP END '''   


    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        #
        # GPIO.cleanup()

if __name__ == '__main__':
    main()