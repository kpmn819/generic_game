#! /bin/sh

# attempt to do a generic game format with classes

# IMPORTS START --------------------------------------------------
# makes extensive use of pygame to blit the screen

from random import randrange, shuffle, random, sample

# pull stuff from config file
from config import white, black, green, red, blue
from config import game_names, game_types, nt_path, pi_path
from config import small_prize, big_prize, web_server, lists_path
import db_module
use_db = True
from datetime import datetime



#from random import sample
from time import sleep, time
import sys, pygame, os
import multiprocessing
import timeout_decorator
times_out = 300

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
    def __init__(self, name, background, qu_ans, score,  reward= None):
        self.name = name
        self.background = background
        self.qu_ans = qu_ans # all of the questions and answers
        self.score = score
        self.reward = reward

        # make two lists of questions and answers
        self.just_a = []
        self.just_q = []
        for q_plus_a in self.qu_ans:
            self.just_q.append(q_plus_a[0])
            temp = []
            for i in range(1, len(q_plus_a)):
                temp.append(q_plus_a[i])
            self.just_a.append(temp)
            
            
            
        # leaving here our Game has the questions and answers
        # and a background
    # ============= end of Game class initialization ================   

    def take_turn(self):
        pass       
    
 # ============ end of Game class methods =============== 
 # ============ start PictGame class =========================
class PictGame():
    def __init__(self, name, background, qu_ans, score,  reward= None): 
        self.name = name
        self.background = background
        self.qu_ans = qu_ans # a list of tuples
        # like this (image 1a, image 1b)
        #           (image 2a, image 2b)
        self.score = score
        self.reward = reward
        # see if we can load them into pygame
        all_files = []
        count = 0
        self.all_picts = []
        for pair in range(0, len(self.qu_ans)):
            temp = []
            temp_surface = []
            temp.append(self.qu_ans[count][0])
            temp.append(self.qu_ans[count][1])
            temp_surface.append(pygame.image.load('graphics/'+ self.qu_ans[count][0]).convert_alpha())
            temp_surface.append(pygame.image.load('graphics/'+ self.qu_ans[count][1]).convert_alpha())
                
            count += 1
            self.all_picts.append(temp_surface)
            all_files.append(temp)
        # we now have a list of pairs of surfaces ready to be blitted
        
            

# ----------- Buttons ---------------
class Button():
    def __init__(self, in_port, in_stat, out_port, out_stat):
        self.in_port = in_port
        self.in_stat = in_stat
        self.out_port = out_port
        self.out_stat = out_stat
    def setup_port(self):
        #initialize ports
        GPIO.setup(self.out_port, GPIO.OUT)
        GPIO.setup(self.in_port, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    def read_status(self):
        # read the input port here
        if GPIO.input(self.in_port) == GPIO.LOW:
            self.in_stat = False
            return self
        else:
            self.in_stat = True
            return self
    def set_status(self):
        # set the output port here
        if self.out_stat == True:
            GPIO.output(self.out_port, True)
        else:
            GPIO.output(self.out_port, False)
        return self
    
# !!!!!!!!!!!!!
class ScreenObject():
    def __init__(self, location):
        self.location = location
    def blit_scr_obj(self, location, image):
        display.blit(image, location)

class GraphicObject(ScreenObject):
    def __init__(self, location, file_name):
        self.file_name = file_name
        super().__init__(location)
    # load into pygame 
        self.surface = pygame.image.load(file_name).convert_alpha()

class TextObject(ScreenObject):
    def __init__(self, text, location, size, color, width=None, font='FreeSans'):
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.width = width
        super().__init__(location)

    def parse_string(self):    
        # this handy util breaks up long lines for us

        lines_list = textwrap.wrap(self.text, self.width)        
	# will return any number of lines of final_length
        return lines_list 
    #----------- font process
    def font_process(self):
        global display
        x = self.location[0]
        y = self.location[1]
        # attempt to combine all font operations into one call that
        # renders and blits the text
        black = (0,0,0)
        d_shadow = 3
        # create a font object from a system font
        font = pygame.font.SysFont(self.font, self.size, True, False)
        # render font on a new surface font.render(text, antialias, bkgnd = none)
        render_message = font.render(self.text, True, self.color)
        # render drop shadow in black
        if d_shadow:
            render_ds = font.render(self.text, True, black)
            render_ds_rect = render_message.get_rect()
        # attempt to center works
        # create a rectangular object for the text surface object
        render_msg_rect = render_message.get_rect()
        # center in x, use y from call
        render_msg_rect.center = self.location # (x,y) x = screen center
        # blit drop shadow then text to image
        if d_shadow:
            #render_ds_rect.center = (image_centerx + d_shadow, y + d_shadow)
            render_ds_rect.center = (x + d_shadow, y + d_shadow)
            display.blit(render_ds, render_ds_rect)
        display.blit(render_message, render_msg_rect)
        # no flip here up to the caller
        
class SoundObject():
    def __init__(self, file, volume):
        self.file = file
        self.volume = volume
    def play_sound(self):
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.load(gpath + self.file)
        pygame.mixer.music.play()    
# \\\\\\\\\\\\\\\\\\\\ END CLASSES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# /////////////// INITIALIZE RUN ONCE ////////////////////////////
def init():
    # set up the ports port#, input T/F, state T/F (optional)
    global image_centerx
    global image_centery
    image_centerx = 960
    image_centery = 540
    global small_index
    small_index = 0
    global big_index
    big_index = 0
    # button(in port, in stat, out port, out stat)
    if os.name == 'nt':
        pass
    else:
        # Initialize i/o ports and flash lights
        light_list = [0] * 7
        buttons_lights(light_list, 0, 0)
        light_list = [1] * 7
        buttons_lights(light_list, 1, 0)
        sleep(1)
        light_list = [0] * 7
        buttons_lights(light_list, 1, 0)
        # Start the web server if on the pi
        process = multiprocessing.Process(target = task)
        process.start()



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

    # ======== pygame setup ===========
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    clock = pygame.time.Clock()
    screen_width = 1920
    screen_height = 1080
    bgColor = (0,0,0)
    size = (screen_width, screen_height)
    global display
    display = pygame.display.set_mode((1920,1080))
    # ^^^^^^^^^^^^ end pygame setup ^^^^^^^^^^^

    global gpath
    if os.name == 'nt':
        gpath = nt_path
    else:
        gpath = pi_path

    # arrows
    b_arro = gpath + 'blue_arrow.png'
    # glows
    g_gl = gpath + 'g-glow.png'
    r_gl = gpath + 'r-glow.png'
    gr_gl = gpath + 'gray-glow.png'
    # path to sounds
    awefile = gpath + 'Awe.mp3'
    yayfile = gpath + 'Yay.mp3'
    global yay
    yay = SoundObject('Yay.mp3', .3)
    
    # these guys are shared by all games
    global blue_arrow
    blue_arrow = pygame.image.load(b_arro).convert_alpha()
    global green_glow
    green_glow = pygame.image.load(g_gl).convert_alpha()
    global red_glow
    red_glow = pygame.image.load(r_gl).convert_alpha()
    global gray_glow
    gray_glow = pygame.image.load(gr_gl).convert_alpha()
    # text responses to right and wrong answers
    global correct
    correct = get_file('right_resp.csv', 1)[0]
    global wrong
    wrong = get_file('wrong_resp.csv', 1)[0]
#\\\\\\\\\\\\\\\\\\\ INITIALIZE \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# /////////////////// START UTILITY METHODS ////////////////////////
def task():
    # Used to start web server
    try:
        print('Attempting to start server')
        os.system(web_server)
    except:
        print('could not start server')

def get_file(list_file, col_count):
    # now a more generic reader that can take any number of columns
    if os.name == 'nt':
        pass
    else:
        list_file = lists_path + list_file
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
            row_count = line_count - 1
            # returns lists within lists acces via [list of items][items]
            return [cvs_list]
    except FileNotFoundError:
        print('file not found')
        # print message on screen
        file_error = True
        
def light_proc(light_list):
    if os.name == 'nt':
        pass
    else:
        buttons_lights(light_list,1,0)

def btn_proc(btn_list):
    if os.name == 'nt':
        resp = key_press(btn_list)
        return resp
    else:
        buttons = buttons_lights(btn_list, 0, 1)
        for i, button in enumerate(buttons):
            # exit from anywhere if you hold down mouse and press button

            if not button.in_stat:
                # reset for the next time
                button.in_stat = True
                return i
 
                
            


def buttons_lights(light_list, lgt_set, btn_mon):
    # 0, 0 initializes the ports
    if not lgt_set and not btn_mon:
        #             in, in stat, out, out stat
        btn_free = Button(13, True, 16, True)
        button1 = Button(4, True, 24, True)
        button2 = Button(17, True, 25, True)
        button3 = Button(27, True, 12, True)
        button4 = Button(22, True, 18, True)
        button5 = Button(5, True, 14, True)
        btn_pay = Button(26, True, 16, True)
        button_list = [btn_free, button1, button2, button3, button4,
                   button5, btn_pay]
        # this makes it persistant for use below
        global button_obj
        button_obj = button_list
        for i, button in enumerate(button_list):
            Button.setup_port(button)
        print('PORTS INITIALIZED')

    if lgt_set:
        # uses active_list to set outputs
        for i, button in enumerate(button_obj):
            if light_list[i]:
                # set the port False = low light on
                GPIO.output(button.out_port, False)
                # call Button to set port gpio
                button.out_stat = False
            else:
                button.out_stat = True
                GPIO.output(button.out_port, True)


    if btn_mon:
        loop = True
        count = 0
        while loop == True:
            count += 1
            for i, button in enumerate(button_obj):
                # special code to shutdown goes here
                if GPIO.input(13) == GPIO.LOW and GPIO.input(5) == GPIO.LOW:
                    GPIO.cleanup()
                    # Shutdown the web server
                    os.system('sudo fuser -k 8000/tcp')
                    os.system("sudo shutdown -h now")
                event = pygame.event.poll()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print('got the mouse')
                    GPIO.cleanup()
                    # Shutdown the web server
                    os.system('sudo fuser -k 8000/tcp')
                    sys.exit()
                # ===== end shutdown code ======

                # only check the flagged ports
                if light_list[i]:
                    # go check the physical port if it comes back False
                    if GPIO.input(button.in_port) == GPIO.LOW:
                        button.in_stat = False
                        return button_obj
                        # loop = False
                        # set our status and get out
                        count += 1
                    sleep(.01)
                else:
                    pass
        # returns button objects to btn_proc to scan
        return    button_obj


def key_press(key_list):
    # list looks like [0, 1, 1, 1, 1, 1, 0]
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
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('got the mouse')
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
                
                if event.key == pygame.K_q:
                    raise Exception(KeyboardInterrupt)
            
                    
    return x


# Place arrows and blit
def place_arrows(style):
    if  '1' in style:
        ScreenObject.blit_scr_obj(arrow1, arrow1.location, blue_arrow)
    if  '2' in style:
        ScreenObject.blit_scr_obj(arrow2, arrow2.location, blue_arrow)
    if  '3' in style:
        ScreenObject.blit_scr_obj(arrow3, arrow3.location, blue_arrow)
    if  '4' in style:
        ScreenObject.blit_scr_obj(arrow4, arrow4.location, blue_arrow)
    if  '5' in style:
        ScreenObject.blit_scr_obj(arrow5, arrow5.location, blue_arrow)

# gets a list of intro statements and puts them on screen
def picture_intro(curr_game):
    button_list = [0,0,0,0,0,0,0]
    light_proc(button_list)

    # put up the game intro
    # splice the name of the game to _intro.csv to load file
    intro = get_file(curr_game.name + '_intro.csv', 1)[0]
    bkg = ScreenObject([0,0])
    ScreenObject.blit_scr_obj(bkg, bkg.location, curr_game.background)
    text_y = 400
    for i in range(0, len(intro)):
        intro_display(intro[i], text_y)
        text_y += 70
        pygame.display.flip()
        sleep(1)
    sleep(4)

def intro_display(intro_line, y):
    message = TextObject(str(intro_line[0]), [image_centerx, y], 60, white )
    TextObject.font_process(message)


def score_process(curr_game, right):
    f_size = 80
    if right:
        curr_game.score[0] += 1
        turn_resp = str(correct[randrange(len(correct))][0])
        resp_msg = TextObject(turn_resp, (900, 700), f_size, white)
    else:
        curr_game.score[1] += 1
        turn_resp = str(wrong[randrange(len(wrong))][0])
        resp_msg = TextObject(turn_resp, (900, 700), f_size, white)
    ScreenObject.blit_scr_obj(curr_game, [0,0], curr_game.background)
    # display response and score
    if curr_game.score[0] + curr_game.score[1] < 5:
        message = f'Your score is {curr_game.score[0]} Right {curr_game.score[1]} Wrong'
        score_msg = TextObject(message,(900,500), f_size, white)
        ScreenObject.blit_scr_obj(curr_game,(0,0),curr_game.background)
        TextObject.font_process(score_msg)
        TextObject.font_process(resp_msg)
        pygame.display.flip()
        sleep(3)
    
def make_surface(file):
    surface = pygame.image.load(file).convert_alpha()
    return surface

def blit_formatted(file):
    global image_centerx
    # reads text formatted as [[Text, Size, X Postion or 'center', Y Position, Color]]
    lines = get_file('free_cash.csv',5)[0]
    for index, line in enumerate(lines):
        line[2].strip
        line[3].strip
        line[4].strip
        if line[2] == 'center':
            line[2] = image_centerx
        if line[4] == 'white':
            line[4] = white
        elif line[4] == 'blue':
            line[4] = blue
        elif line[4] == 'red':
            line[4] = red
        else:
            line[4] = white
        greeting = line[0]
        greet = TextObject(greeting, ( int(line[2]), int(line[3])), int(line[1]), line[4] )
        TextObject.font_process(greet)

# \\\\\\\\\\\\\\\\\\\ END UTILITY METHODS \\\\\\\\\\\\\\\\\\\\\\\\\\

#////////////////// START METHODS /////////////////////////


def free_cash():
    ''' called by both games selects if it is a free game or
    if they put in some money sets global variables'''
    button_list = [1, 0, 0, 0, 0, 0, 1]
    # setup lights
    light_proc(button_list)

    # display rules and wait for input
    global free
    
    global display
    free_ch_bkg = make_surface(gpath + 'free_donate.jpg')
    bakgnd = ScreenObject((0,0))
    ScreenObject.blit_scr_obj(bakgnd, bakgnd.location, free_ch_bkg)
    #create the object first can reuse object since blit stores it
    blit_formatted('free_cash.csv')
    pygame.display.flip()
    # Select if this is a paid or free play
    while True:
        sleep(.05)
        selection = btn_proc(button_list)
        if selection == 0:
            SoundObject.play_sound(yay)
            free = False
        else:
            free = True
 
        break
 

        



#================ CHOOSE GAME ====================

def choose_game():
    button_list = [0, 1, 0, 0, 0, 1, 0]
    light_proc(button_list)
    choice_bkg = make_surface(gpath + 'game_choice.jpg')
    global curr_game
    bakgnd = ScreenObject((0,0))
    ScreenObject.blit_scr_obj(bakgnd, bakgnd.location, choice_bkg)
    greeting = 'Please select a game to play'
    greet = TextObject(greeting, (image_centerx, 100), 80, white)
    TextObject.font_process(greet)
    # first the left side
    x = 430
    y = 400
    name = game_names[1]
    file = name + '_dscr.csv'
    dscr = get_file(file, 1)
    greeting = dscr[0][0][0]
    greet = TextObject(greeting, (x, y), 70, white)
    TextObject.font_process(greet)
    y = y + 90
    greeting = dscr[0][1][0]
    greet = TextObject(greeting, (image_centerx, 300), 80, white, 30)
    parsed_lines = TextObject.parse_string(greet)
    for item in parsed_lines:
        greet = TextObject(item, (x, y), 60, white)
        TextObject.font_process(greet)
        y = y + 70

    # now the right side
    x = 1430
    y = 400

    name = game_names[5]
    file = name + '_dscr.csv'
    dscr = get_file(file, 1)
    greeting = dscr[0][0][0]
    greet = TextObject(greeting, (x, y), 80, white)
    TextObject.font_process(greet)
    y = y + 90
    greeting = dscr[0][1][0]
    greet = TextObject(greeting, (x, y), 80, white, 30)
    parsed_lines = TextObject.parse_string(greet)
    for item in parsed_lines:
        greet = TextObject(item, (x, y), 60, white)
        TextObject.font_process(greet)
        y = y + 70
    place_arrows('1and5')
    pygame.display.flip()

    light_proc(button_list)
    game_to_play = btn_proc(button_list)
    name = game_names[game_to_play]
    type = game_types[name]
    # make the game object and call it curr_game
    # the goal is to generalize the commands below to just two picture and text
    if type == 'picture':
        background = make_surface(gpath + name + '_bkg.jpg')
        curr_game = PictGame( name, background, get_file(name + '_picture.csv', 2)[0], [0,0])
    if type == 'text':
        background = make_surface(gpath + name + '_bkg.jpg')
        curr_game = TextGame( name, background, get_file(name + '_qna.csv', 4)[0], [0,0])
    if game_to_play == 3:
        curr_game = TextGame( name, g2_bkg, get_file('another_text.csv', 4)[0], [0,0])
    curr_game.free = free # True for free False for donation this is an add on
    pinball = SoundObject('pinball-start.mp3', .3)
    SoundObject.play_sound(pinball)
    sleep(2.5)
    return curr_game  
# ^^^^^^^^^^^^^^^^^^^^ CHOOSE GAME ^^^^^^^^^^^^^^^^^^^

#==================== TEXT GAME =====================
def text_game():
    button_list = [0, 1, 0, 1, 0, 1, 0]
    light_proc(button_list)
    wrong_sound = SoundObject('Downer.mp3', .2)
    right_sound = SoundObject('Quick-win.mp3', .3)
    # get 5 (number of turns)
    turn_picks = sample(range( 0, len(curr_game.just_q)), 5)
    curr_game.score = [0,0]
    turn_no = 0 #used by database
    # take turns
    # ||||||||| 5 TURNS ||||||||||||||||||||||||
    for index in turn_picks:
        display.blit(curr_game.background, (0,0))
        turn_no += 1
        turn_ans = (curr_game.just_a[index])
        # need to go through questions and randomize answers
        display_list = turn_ans[:] # make a copy
        shuffle(display_list)
        # for each turn need to blit question and answers on screen
        # display the question
        qx_offset = 990
        qy_offset = 100
        question = TextObject(curr_game.just_q[index], [qx_offset,qy_offset], 80, white, 30)
        q_db = question.text # whole question before parse
        q_parsed = TextObject.parse_string(question)
        for item in q_parsed:
            question.location = [qx_offset,qy_offset]
            question.text = item
            TextObject.font_process(question)
            qy_offset += 70
        # place answers
        ax_offset = 320
        ay_offset = 500
        ans_font = 60
        blit_x = []
        for i in range(0,3):
            blit_x.append(ax_offset) # for use in later lookup
            ay_offset = 500
            answer = TextObject(display_list[i], [ax_offset,ay_offset], ans_font, white, 20)
            q_parsed = TextObject.parse_string(answer)
            for item in q_parsed:
                answer.location = [ax_offset,ay_offset]
                answer.text = item
                TextObject.font_process(answer)
                ay_offset += 70
            ax_offset += 640
        place_arrows('135')
        
        pygame.display.flip()

        # go and get the button pressed and convert it to an index
        btn_dict = {1:1, 3:2, 5:3}
        resp = btn_dict[btn_proc(button_list)]
        # need to highlight correct in green
        
        r_indx = display_list.index(turn_ans[0]) #gives index of right ans
        highlight_ans = TextObject(turn_ans[0], [blit_x[r_indx], 500],ans_font,green, 20)
        h_parsed = TextObject.parse_string(highlight_ans)
        ay_offset = 500
        for item in h_parsed:
            highlight_ans.location = [blit_x[r_indx],ay_offset]
            highlight_ans.text = item
            TextObject.font_process(highlight_ans)
            ay_offset += 70

        # Right and Wrong answer processing
        if display_list[resp -1] == turn_ans[0]:
            print('got it')
            resp_ans = True
            SoundObject.play_sound(right_sound)
        else:
            print('wrong')
            resp_ans = False
            SoundObject.play_sound(wrong_sound)
            # need to blit wrong in red
            ax_offset = 320
            ay_offset = 500
            highlight_ans = TextObject(display_list[resp - 1],(blit_x[resp - 1],ay_offset),ans_font,red,20)
            h_parsed = TextObject.parse_string(highlight_ans)
            for item in h_parsed:
                highlight_ans.location = [blit_x[resp-1],ay_offset]
                highlight_ans.text = item
                TextObject.font_process(highlight_ans)
                ay_offset += 70
        if use_db:
            # turn by turn data put in db
            game_no = db_module.get_game()
            turn_data = (game_no, turn_no, q_db, display_list[resp -1], resp_ans)
            db_module.turn_write(turn_data)
        pygame.display.flip()
        sleep(1)
        score_process(curr_game, resp_ans)

#^^^^^^^^^^^^^^^^^^ TEXT GAME ^^^^^^^^^^^^^^^^^^^^

#================== PICTURE GAME =================
def picture_game():
    wrong_sound = SoundObject('Downer.mp3', .2)
    right_sound = SoundObject('Quick-win.mp3', .3)
    picture_intro(curr_game)
    button_list = [0, 1, 1, 1, 1, 1, 0]
    light_proc(button_list)
    # get 5 indexes for our turns
    turn_picks = sample(range( 0, len(curr_game.all_picts)), 5)
    for q in range(0,5):
        question_picture = curr_game.all_picts[turn_picks[q]][0]
        answer_picture = curr_game.all_picts[turn_picks[q]][1]
        # need to get a random set of 2 other indexes the don't equal hero
        wrong_a = answer_picture
        shuffle_answers = []
        shuffle_answers.append(answer_picture)
        # pick something other than the hero
        for i in range(0,4):
            #     don't duplicate right answer   don't repeat any
            while (answer_picture == wrong_a) or (wrong_a in shuffle_answers):
                index = sample(range( 0, len(curr_game.all_picts)), 1)[0]
                wrong_a = curr_game.all_picts[index][1]
            shuffle_answers.append(wrong_a)
        
        ScreenObject.blit_scr_obj(curr_game,[0,0], curr_game.background)
        #shuffle_answer order
        shuffle(shuffle_answers)
        display.blit(gray_glow, (770, 2))
        display.blit(question_picture, (810, 40))

        blit_index = []
        x = 50
        blit_index.append(x)
        # put answers on screen
        ay = 600
        for i in range(0,5):
            display.blit(shuffle_answers[i], (x,ay)) 
            x += 380
            blit_index.append(x)

        place_arrows('12345')
        pygame.display.flip()
        #resp = key_press(button_list)
        resp = btn_proc(button_list)
        # correct answer highlited green nomatter what
        glo_offset = 20
        c_index = shuffle_answers.index(answer_picture)
        c_glow = ScreenObject([blit_index[c_index]- glo_offset, ay-glo_offset])
        ScreenObject.blit_scr_obj(c_glow, c_glow.location, green_glow)
        pygame.display.flip()

        if answer_picture == shuffle_answers[int(resp -1)]:
            resp_ans = True
            SoundObject.play_sound(right_sound)

        else:
            # user answer highligted red if wrong
            resp_ans = False
            SoundObject.play_sound(wrong_sound)
            c_index = resp - 1
            c_glow = ScreenObject([blit_index[c_index]- glo_offset, ay-glo_offset])
            ScreenObject.blit_scr_obj(c_glow, c_glow.location, red_glow)
            sleep(.01)
            pygame.display.flip()
        if use_db:
                game_no = db_module.get_game()
                _qpic = curr_game.qu_ans[turn_picks[q]][0]
                # have to work backward to find the response
                for location, item in enumerate(curr_game.all_picts):
                    if shuffle_answers[resp-1] == item[1]:
                        a_file = curr_game.qu_ans[location][1]
                turn_data = (game_no, q + 1, _qpic, a_file, resp_ans)
                db_module.turn_write(turn_data)
        sleep(1.5)   
            
        score_process(curr_game, resp_ans)
    
        
# ^^^^^^^^^^^^^^^  PICTURE GAME ^^^^^^^^^^^^^^^^^^       

#================= FINAL SCORE ===================
def final_score(score):
    button_list = [0, 0, 0, 0, 0, 0, 0]
    light_proc(button_list)

    # play game final sound
    f_score_sounds = ['0_right.wav','1_right.wav','2_right.mp3','3_right.wav',
                       '4_right.mp3', '5_right.wav']
    f_score_vol = [.3, 1, 1, .5, 1, 1]
    final_sound = SoundObject(f_score_sounds[score[0]], f_score_vol[score[1]])
    SoundObject.play_sound(final_sound)

    # put up background and text
    final_bkg = make_surface(gpath + 'finalscore.jpg')
    bkg = ScreenObject([0,0])
    ScreenObject.blit_scr_obj(bkg, [0,0], final_bkg)
    msg_y = 400
    message = 'Final Score'
    msg = TextObject(message, [image_centerx, msg_y], 80, white)
    TextObject.font_process(msg)
    message = f'{score[0]} Right {score[1]} Wrong'
    msg = TextObject(message, [image_centerx, msg_y + 90], 80, white)
    TextObject.font_process(msg)
    pygame.display.flip()
    sleep(4)

    # process winners
    global small_index
    global big_index
    if score[0] > 3 and not free:
        if small_index == len(small_prize) - 1:
            small_index = 0
            small_word = small_prize[small_index]
        else:
            small_index += 1
            small_word = small_prize[small_index]
        
        if big_index == len(big_prize) - 1:
            big_index = 0
            big_word = big_prize[big_index]
        else:
            big_index += 1
            big_word = big_prize[big_index]

        if score[0] == 5:
            win_word = big_word
        else:
            win_word = small_word
        
        msg_y = 700
        message = TextObject('You are a WINNER!!',(image_centerx, msg_y),75,red )
        TextObject.font_process(message)
        msg_y += 100
        message = TextObject('Please see one of our Staff for your prize', (image_centerx, msg_y),75,red)
        TextObject.font_process(message)
        msg_y += 100
        message = TextObject('Tell them your winner code is '+ '"'+ win_word+ '"', (image_centerx, msg_y),75,red)
        TextObject.font_process(message)
        pygame.display.flip()
        fanfare = SoundObject('fanfare.mp3', .5)   
        SoundObject.play_sound(fanfare)
        sleep(5)


           
    elif score[0] < 4 and not free:
        msg_y = 700
        message = TextObject('Sorry you did not win this time',(image_centerx, msg_y),75,blue )
        TextObject.font_process(message)
        pygame.display.flip()
        sleep(2)

    
#^^^^^^^^^^^^^^^^^ FINAL SCORE ^^^^^^^^^^^^^^^^^^^


# GAME LOOP -------
#@timeout_decorator.timeout(times_out, use_signals=True)
def game_loop():
    global curr_game
    
    # free_cash and curr_game calls include background images
    free_cash()
    # game must be created first
    
    curr_game = choose_game()
    if use_db:
        # make an entry in the game field -1 score means game isn't finished
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y,%H,%M,%S")
        db_module.db_start()
        game_data = (curr_game.name, date_time, -1, free)
        this_game = db_module.game_write(game_data)
        db_module.db_close
    
    if type(curr_game).__name__ == 'PictGame':
        picture_game()
        type(curr_game).__name__
        
    else:
        text_game()
    # we have gone and played the game so we can now finish
    if use_db:
        # add the ending score
        db_score = (curr_game.score[0], this_game)
        db_module.db_start()
        db_module.game_over(db_score)
        db_module.db_close


    final_score(curr_game.score)       

#\\\\\\\\\\\\\\\\\\\\\\ END METHODS \\\\\\\\\\\\\\\\\\\\\\\\




def main():
    
    try:
        init()
        while 1 == 1:
            global curr_game
        
            try:
                curr_game
            except NameError:
                    print('no curr_game defined')
            else:
                print('previus game deleted')
                del curr_game
            try:
                game_loop()
            except timeout_decorator.TimeoutError:
                continue

        
    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        if os.name != 'nt':
            GPIO.cleanup()
            os.system('sudo fuser -k 8000/tcp')

if __name__ == '__main__':
    main()