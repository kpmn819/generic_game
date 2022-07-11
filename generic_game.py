# attempt to do a generic game format with classes

# IMPORTS START --------------------------------------------------
# makes extensive use of pygame to blit the screen
from typing import final

from cv2 import QT_FONT_BLACK
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
class TextGame():
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
 # ============ start PictGame class =========================
class PictGame():
    def __init__(self, background, qu_ans, score, num_ans, reward= None): 
        self.background = background
        self.qu_ans = qu_ans # a list of tuples
        self.score = score
        self.reward = reward
        print('picture is')
        print(qu_ans)
        # see if we can load them into pygame
        loaded = []
        for x in range(0, len(self.qu_ans)-1):
            file_name = 'graphics/' + self.qu_ans[x][0]
            loaded.append(pygame.image.load(file_name).convert_alpha())
            file_name = 'graphics/' + self.qu_ans[x][1]
            loaded.append(pygame.image.load(file_name).convert_alpha())
        print('length of q_ans')
        print(self.qu_ans[0][1])
            
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
class ScreenObject():
    def __init__(self, location):
        self.location = location
    def blit_scr_obj(self, location, image):
        display.blit(image, location)   
class TextObject(ScreenObject):
    def __init__(self, text, location, size, color, width=None, font=None):
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.width = width
        super().__init__(location)

    def parse_string(self, text, width):    
        # this handy util breaks up long lines for us

        lines_list = textwrap.wrap(text, width)        
	# will return any number of lines of final_length
        return lines_list 
    #----------- font process
    def font_process(self, text, location, size, color):
        global display
        x = location[0]
        y = location[1]
        # attempt to combine all font operations into one call that
        # renders and blits the text
        black = (0,0,0)
        d_shadow = 3
        # create a font object from a system font
        font = pygame.font.SysFont('FreeSans', size, True, False)
        # render font on a new surface font.render(text, antialias, bkgnd = none)
        render_message = font.render(text, True, color)
        
        # render drop shadow in black
        if d_shadow:
            render_ds = font.render(text, True, black)
            render_ds_rect = render_message.get_rect()
        # attempt to center works
        # create a rectangular object for the text surface object
        render_msg_rect = render_message.get_rect()
        
        # center in x, use y from call
        #render_msg_rect.center = (image_centerx, y) # (x,y) x = screen center
        render_msg_rect.center = location # (x,y) x = screen center
        # blit drop shadow then text to image
        if d_shadow:
            #render_ds_rect.center = (image_centerx + d_shadow, y + d_shadow)
            render_ds_rect.center = (x + d_shadow, y + d_shadow)
            display.blit(render_ds, render_ds_rect)
        display.blit(render_message, render_msg_rect)
        # no flip here up to the caller
    
# \\\\\\\\\\\\\\\\\\\\ END CLASSES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def init():
    # set up the ports port#, input T/F, state T/F (optional)
    global image_centerx
    global image_centery
    image_centerx = 960
    image_centery = 540
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
    # make some arrow objects
    global arrow1
    arrow1 = ScreenObject((15, 890))
    global arrow2
    arrow2 = ScreenObject((452, 890))
    global arrow3
    arrow3 = ScreenObject((895, 890))
    global arrow4
    arrow4 = ScreenObject((1337, 890))
    global arrow5
    arrow5 = ScreenObject((1775, 890))
    
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
    
    global display
    #display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    display = pygame.display.set_mode((1920,1080))
    # assign I/O ports here ////////////
    gpath = 'graphics/'
    udol1 = gpath + '25b.jpg'
    udol2 = gpath + '26b.jpg'
    udol3 = gpath + '75a.jpg'
    udol4 = gpath + '86a.jpg'
    udol5 = gpath + '100b.jpg'
    udol6 = gpath + '126b.jpg'

    udol7 = gpath + '271c.jpg'
    udol8 = gpath + '454b.jpg'
    udol9 = gpath + '618a.jpg'
    udol10 = gpath + '706b.jpg'
    udol11 = gpath + '1142b.jpg'
    udol12 = gpath + '1726a.jpg'

    # now set pointers to computer picks
    cdol1 = gpath + '25a.jpg'
    cdol2 = gpath + '26a.jpg'
    cdol3 = gpath + '75b.jpg'
    cdol4 = gpath + '86c.jpg'
    cdol5 = gpath + '100a.jpg'
    cdol6 = gpath + '126a.jpg'

    cdol7 = gpath + '271b.jpg'
    cdol8 = gpath + '454a.jpg'
    cdol9 = gpath + '618b.jpg'
    cdol10 = gpath + '706a.jpg'
    cdol11 = gpath + '1142a.jpg'
    cdol12 = gpath + '1726b.jpg'

    g1_open_pict = gpath + 'game_1.jpg'
    g2_open_pict = gpath + 'game_2.jpg'
    #free_donate_pict = gpath + 'free_donate.jpg' #(not used)
    game_choice_pict = gpath + 'game_choice.jpg'
    finalscore_pict = gpath + 'finalscore.jpg'
    # arrows
    r_arro = gpath + 'red_arrow.png'
    y_arro = gpath + 'yellow_arrow.png'
    b_arro = gpath + 'blue_arrow.png'
    # glows
    g_gl = gpath + 'g-glow.png'
    r_gl = gpath + 'r-glow.png'
    gr_gl = gpath + 'gray-glow.png'
    # path to sounds
    awefile = gpath + 'Awe.mp3'
    yayfile = gpath + 'Yay.mp3'
    # audio files for final score
    # had to convert a couple to mp3, pygame didn't like the wav version
    final_audio = ('0_right.wav','1_right.wav','2_right.mp3','3_right.wav',
                '4_right.mp3','5_right.wav')
    final_vol = (.3,1,1,.5,1,1)
    # now to actually load them same letters this has to be done in two steps
    # first the user pictures
    uw1 = pygame.image.load(udol1).convert_alpha()
    uw2 = pygame.image.load(udol2).convert_alpha()
    uw3 = pygame.image.load(udol3).convert_alpha()
    uw4 = pygame.image.load(udol4).convert_alpha()
    uw5 = pygame.image.load(udol5).convert_alpha()
    uw6 = pygame.image.load(udol6).convert_alpha()
    uw7 = pygame.image.load(udol7).convert_alpha()
    uw8 = pygame.image.load(udol8).convert_alpha()
    uw9 = pygame.image.load(udol9).convert_alpha()
    uw10 = pygame.image.load(udol10).convert_alpha()
    uw11 = pygame.image.load(udol11).convert_alpha()
    uw12 = pygame.image.load(udol12).convert_alpha()
    # now the computer pictures
    cw1 = pygame.image.load(cdol1).convert_alpha()
    cw2 = pygame.image.load(cdol2).convert_alpha()
    cw3 = pygame.image.load(cdol3).convert_alpha()
    cw4 = pygame.image.load(cdol4).convert_alpha()
    cw5 = pygame.image.load(cdol5).convert_alpha()
    cw6 = pygame.image.load(cdol6).convert_alpha()
    cw7 = pygame.image.load(cdol7).convert_alpha()
    cw8 = pygame.image.load(cdol8).convert_alpha()
    cw9 = pygame.image.load(cdol9).convert_alpha()
    cw10 = pygame.image.load(cdol10).convert_alpha()
    cw11 = pygame.image.load(cdol11).convert_alpha()
    cw12 = pygame.image.load(cdol12).convert_alpha()
    # full 1920 x 1080 images for backgrounds
    g1_bkg = pygame.image.load(g1_open_pict).convert_alpha()
    g2_bkg = pygame.image.load(g2_open_pict).convert_alpha()
    #free_donate = pygame.image.load(free_donate_pict).convert_alpha() # not used
    global game_choice
    game_choice = pygame.image.load(game_choice_pict).convert_alpha()
    global finalscore
    finalscore = pygame.image.load(finalscore_pict).convert_alpha()
    # small arrow with alpha
    global blue_arrow
    blue_arrow = pygame.image.load(b_arro).convert_alpha()
    global green_glow
    green_glow = pygame.image.load(g_gl).convert_alpha()
    global red_glow
    red_glow = pygame.image.load(r_gl).convert_alpha()
    global gray_glow
    gray_glow = pygame.image.load(gr_gl).convert_alpha()
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
    picture = get_file('picture.csv', 2)[0]
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
        
def key_press():
    x = ''
    loop = True
    while x == '':
        # simulate button polling
        # creating a loop to check events that
        # are occurring
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # checking if keydown event happened or not
            if event.type == pygame.KEYDOWN:
                
                # checking if key "A" was pressed
                if event.key == pygame.K_1:
                    x = 1
                    
                if event.key == pygame.K_2:
                    x = 2
                    
                if event.key == pygame.K_3:
                    x = 3
                    
                if event.key == pygame.K_4:
                    x = 4
                    
                if event.key == pygame.K_5:
                    x = 5
                    
    return x
# Place arrows and blit
def place_arrows(style):
    if style == 'outer2':
        ScreenObject.blit_scr_obj(arrow1, arrow1.location, blue_arrow)
        ScreenObject.blit_scr_obj(arrow5, arrow5.location, blue_arrow)
    if style == 'all5':
        ScreenObject.blit_scr_obj(arrow1, arrow1.location, blue_arrow)
        ScreenObject.blit_scr_obj(arrow2, arrow2.location, blue_arrow)
        ScreenObject.blit_scr_obj(arrow3, arrow3.location, blue_arrow)
        ScreenObject.blit_scr_obj(arrow4, arrow4.location, blue_arrow)
        ScreenObject.blit_scr_obj(arrow5, arrow5.location, blue_arrow)
    if style == '2and4':
        ScreenObject.blit_scr_obj(arrow2, arrow2.location, blue_arrow)
        ScreenObject.blit_scr_obj(arrow4, arrow4.location, blue_arrow)

# \\\\\\\\\\\\\\\\\\\ END UTILITY METHODS \\\\\\\\\\\\\\\\\\\\\\\\\\

#////////////////// START METHODS /////////////////////////


def free_cash(background):
    ''' called by both games selects if it is a free game or
    if they put in some money sets global variables'''
    # display rules and wait for input
    global free
    global win
    global display
    bakgnd = ScreenObject((0,0))
    ScreenObject.blit_scr_obj(bakgnd, bakgnd.location, background)
    #create the object first can reuse object since blit stores it
    greeting = 'Press Free Play'
    greet = TextObject(greeting, (image_centerx, 200), 60, white )
    TextObject.font_process(greet, greet.text, greet.location,greet.size, greet.color)
    greeting = 'or'
    greet = TextObject('or',(image_centerx, 280), 60, white)
    TextObject.font_process(greet, greet.text, greet.location,greet.size, greet.color)
    greeting = 'Make a Donation and get a chance to win a Bonehenge Prize'
    greet = TextObject(greeting, (image_centerx, 360), 60, white )
    TextObject.font_process(greet, greet.text, greet.location,greet.size, greet.color)
    greeting = 'Prizes are awarded for 5 of 5 or 4 of 5 correct answers'
    greet = TextObject(greeting, (image_centerx,800), 30, white )
    TextObject.font_process(greet, greet.text, greet.location,greet.size, greet.color)
    greeting = 'If you win you will see your winner code word'
    greet = TextObject(greeting, (image_centerx,850), 30, white )
    TextObject.font_process(greet, greet.text, greet.location,greet.size, greet.color)
    pygame.display.flip()
    
    # Select if this is a paid or free play
    # make a quick change to this file
    
    while True:
        sleep(.05)
        selection = key_press()
        print(selection)
        break
        #print('in pay detection')
        '''if GPIO.input(portList2[1]) == GPIO.LOW:
            sleep(.08)
            free = True
            win = False
            print('Free Play')
            break
                
        if GPIO.input(portList2[2]) == GPIO.LOW:
            #print('PLAYBACK SHOULD HAPPEN')
            sleep(.08)
            free = False
            win = False # set it false for now
            Rnd_Chance = int(random() * 100 )
            play_sound('Yay.mp3', .3)
            
            
            if Rnd_Chance <= payout:
                win = True
                print('A Winner')
                
            else:
                win = False
                print('A Loser')
            break'''
# CHOOSE GAME ------
def choose_game(background):
    global curr_game
    bakgnd = ScreenObject((0,0))
    ScreenObject.blit_scr_obj(bakgnd, bakgnd.location, background)
    greeting = 'Please select a game to play'
    greet = TextObject(greeting, (image_centerx, 300), 80, white)
    TextObject.font_process(greet, greet.text, greet.location, greet.size, greet.color)
    # first the left side
    greeting = 'Photo-ID Challenge'
    greet = TextObject(greeting, (430, 600), 70, white)
    TextObject.font_process(greet, greet.text, greet.location, greet.size, greet.color)
    x = 430
    y = 600
    # chop these up
    y = y + 90
    greeting = 'See if you can match dolphin dorsal fins'
    greet = TextObject(greeting, (image_centerx, 300), 80, white, 30)
    parsed_lines = TextObject.parse_string(greet,greet.text,greet.width)
    for item in parsed_lines:
        greet = TextObject(item, (x, y), 60, white)
        TextObject.font_process(greet, greet.text, greet.location, greet.size, greet.color)
        y = y + 70
    # now the right side
    x = 1430
    y = 600
    greeting = 'Bonehenge Tour Quiz'
    greet = TextObject(greeting, (x, y), 80, white)
    TextObject.font_process(greet, greet.text, greet.location, greet.size, greet.color)
    y = y + 90
    greeting = 'Answer some questions about what you learned on your tour'
    greet = TextObject(greeting, (x, y), 80, white, 30)
    parsed_lines = TextObject.parse_string(greet,greet.text,greet.width)
    for item in parsed_lines:
        greet = TextObject(item, (x, y), 60, white)
        TextObject.font_process(greet, greet.text, greet.location, greet.size, greet.color)
        y = y + 70
    place_arrows('2and4')
    pygame.display.flip()
    game_to_play = key_press()
    # make the game object and call it curr_game
    if game_to_play == 1:
        curr_game = TextGame('water.jpeg', qna, (0,0), 5)
        print('dolphin selected')
    if game_to_play == 2:
        curr_game = PictGame('somepic.jpg', picture, (0,0), 2)
    return curr_game    
# GAME LOOP -------
def game_loop():
    global curr_game
    free_cash(game_choice)
    # game must be created first
    curr_game = choose_game(finalscore)
    #print(curr_game.num_ans)
    # curr_game returns a Game object with it's backround, 
    # question/answer file, (0,0)location, number of questions


    #curr_game.take_turn()
    print('took a turn')    

#\\\\\\\\\\\\\\\\\\\\\\ END METHODS \\\\\\\\\\\\\\\\\\\\\\\\




def main():
    try:
        init()
        stuff ='here is a really long line that will have to be compressed by our formatter'
        zow = TextObject(stuff, (200,300), 50, red)
        print(zow.color)
        zow.text =TextObject.parse_string(zow, stuff, 10)
        print(zow.text)
        global curr_game
    
        try:
            curr_game
        except NameError:
                print('no curr_game defined')
        else:
            del curr_game
        
        game_loop()

        
    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        #
        # GPIO.cleanup()

if __name__ == '__main__':
    main()