# attempt to do a generic game format with classes

# IMPORTS START --------------------------------------------------
# makes extensive use of pygame to blit the screen

from random import randrange, shuffle, random, sample

#from random import sample
from time import sleep, time
import sys, pygame, os

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
    def __init__(self, background, qu_ans, score, num_ans, reward= None): 
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

class GraphicObject(ScreenObject):
    def __init__(self, location, file_name):
        self.file_name = file_name
        super().__init__(location)
    # load into pygame 
        self.surface = pygame.image.load(file_name).convert_alpha()

class TextObject(ScreenObject):
    def __init__(self, text, location, size, color, width=None, font=None):
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
        #x = location[0]
        #y = location[1]
        x = self.location[0]
        y = self.location[1]
        # attempt to combine all font operations into one call that
        # renders and blits the text
        black = (0,0,0)
        d_shadow = 3
        # create a font object from a system font
        font = pygame.font.SysFont('FreeSans', self.size, True, False)
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
        #render_msg_rect.center = (image_centerx, y) # (x,y) x = screen center
        render_msg_rect.center = self.location # (x,y) x = screen center
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
    global gpath
    gpath = 'graphics/'

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
    
    # full 1920 x 1080 images for backgrounds
    global g1_bkg
    g1_bkg = pygame.image.load(g1_open_pict).convert_alpha()
    #g1_bkg = GraphicObject([0,0], gpath + 'game_1.jpg')
    global g2_bkg
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

def score_process(curr_game, right):
    if right:
        curr_game.score[0] += 1
        turn_resp = str(correct[randrange(len(correct))][0])
        resp_msg = TextObject(turn_resp, (900, 700), 60, white)
    else:
        curr_game.score[1] += 1
        turn_resp = str(wrong[randrange(len(wrong))][0])
        resp_msg = TextObject(turn_resp, (900, 700), 60, white)
    ScreenObject.blit_scr_obj(curr_game, [0,0], curr_game.background)
    # display response and score
    if curr_game.score[0] + curr_game.score[1] < 5:
        message = 'Your score is ' + str(curr_game.score[0]) + ' Right '+ str(curr_game.score[1]) + ' Wrong'
        score_msg = TextObject(message,(900,500), 60, white)
        ScreenObject.blit_scr_obj(curr_game,(0,0),curr_game.background)
        TextObject.font_process(score_msg)
        TextObject.font_process(resp_msg)
        pygame.display.flip()
        sleep(3)
    

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
    TextObject.font_process(greet)
    greeting = 'or'
    greet = TextObject('or',(image_centerx, 280), 60, white)
    TextObject.font_process(greet)
    greeting = 'Make a Donation and get a chance to win a Bonehenge Prize'
    greet = TextObject(greeting, (image_centerx, 360), 60, white )
    TextObject.font_process(greet)
    greeting = 'Prizes are awarded for 5 of 5 or 4 of 5 correct answers'
    greet = TextObject(greeting, (image_centerx,800), 30, white )
    TextObject.font_process(greet)
    greeting = 'If you win you will see your winner code word'
    greet = TextObject(greeting, (image_centerx,850), 30, white )
    TextObject.font_process(greet)
    pygame.display.flip()
    
    
    # Select if this is a paid or free play
    # make a quick change to this file
    
    while True:
        sleep(.05)
        selection = key_press()
        print(selection)
        break
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



#================ CHOOSE GAME ====================
def choose_game(background):
    global curr_game
    bakgnd = ScreenObject((0,0))
    ScreenObject.blit_scr_obj(bakgnd, bakgnd.location, background)
    greeting = 'Please select a game to play'
    greet = TextObject(greeting, (image_centerx, 300), 80, white)
    TextObject.font_process(greet)
    # first the left side
    greeting = 'Photo-ID Challenge'
    greet = TextObject(greeting, (430, 600), 70, white)
    TextObject.font_process(greet)
    x = 430
    y = 600
    # chop these up
    y = y + 90
    greeting = 'See if you can match dolphin dorsal fins'
    greet = TextObject(greeting, (image_centerx, 300), 80, white, 30)
    parsed_lines = TextObject.parse_string(greet)
    for item in parsed_lines:
        greet = TextObject(item, (x, y), 60, white)
        TextObject.font_process(greet)
        y = y + 70
    # now the right side
    x = 1430
    y = 600
    greeting = 'Bonehenge Tour Quiz'
    greet = TextObject(greeting, (x, y), 80, white)
    TextObject.font_process(greet)
    y = y + 90
    greeting = 'Answer some questions about what you learned on your tour'
    greet = TextObject(greeting, (x, y), 80, white, 30)
    parsed_lines = TextObject.parse_string(greet)
    for item in parsed_lines:
        greet = TextObject(item, (x, y), 60, white)
        TextObject.font_process(greet)
        y = y + 70
    place_arrows('2and4')
    pygame.display.flip()
    game_to_play = key_press()
    # make the game object and call it curr_game
    if game_to_play == 1:
        curr_game = TextGame(g2_bkg, qna, [0,0], 5)
        print('dolphin selected')
    if game_to_play == 2:
        curr_game = PictGame(g1_bkg, picture, [0,0], 2)
    return curr_game  
# ^^^^^^^^^^^^^^^^^^^^ CHOOSE GAME ^^^^^^^^^^^^^^^^^^^

#==================== TEXT GAME =====================
def text_game():
        # get 5 (number of turns) 
    turn_picks = sample(range( 0, len(curr_game.just_q)), 5)
    print(turn_picks)# a list of index numbers for q & a
    curr_game.score = [0,0]

    # take turns
    # ||||||||| 5 TURNS ||||||||||||||||||||||||
    for index in turn_picks:
        display.blit(curr_game.background, (0,0))
        
        #print(curr_game.just_q[index])
        turn_ans = (curr_game.just_a[index])
        #print(turn_ans[0])
        # need to go through questions and randomize answers
        display_list = turn_ans[:] # make a copy
        shuffle(display_list)
        print(display_list)
        # for each turn need to blit question and answers on screen
        # display the question
        x = 990
        y = 100
        question = TextObject(curr_game.just_q[index], [990,100], 80, white, 30)
        q_parsed = TextObject.parse_string(question)
        for item in q_parsed:
            question.location = [x,y]
            question.text = item
            TextObject.font_process(question)
            y += 70
        # left answer
        x = 320
        y = 500
        for i in range(0,3):
            y = 500
            answer = TextObject(display_list[i], [x,y], 50, white, 30)
            q_parsed = TextObject.parse_string(answer)
            print(q_parsed)
            for item in q_parsed:
                question.location = [x,y]
                question.text = item
                TextObject.font_process(answer)
                y += 70
            x += 640

        # mid answer

        #right answer

        pygame.display.flip()
        # have the lights right and wait for a response
        #resp = input('Select 1 2 or 3 ')
        resp = str(key_press())
        if display_list[int(resp)-1] == turn_ans[0]:
            print('got it')
            score_process(curr_game, True)
            #curr_game.score[0] = curr_game.score[0] + 1
        else:
            print('wrong')
            score_process(curr_game, False)
            #curr_game.score[1] = curr_game.score[1] + 1
        print('Score is now ',str(curr_game.score[0]), ' Right ', str(curr_game.score[1]), ' wrong' )
#^^^^^^^^^^^^^^^^^^ TEXT GAME ^^^^^^^^^^^^^^^^^^^^

#================== PICTURE GAME =================
def picture_game():
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
        display.blit(question_picture, (810,40))
        x = 190
        # put answers on screen
        for i in range(0,5):
            display.blit(shuffle_answers[i], (x,600)) 
            x += 310
        place_arrows('12345')
        pygame.display.flip()
        resp = key_press()
        if answer_picture == shuffle_answers[resp -1]:
            score_process(curr_game, True)
        else:
            score_process(curr_game, False)
        print(resp)
        
# ^^^^^^^^^^^^^^^  PICTURE GAME ^^^^^^^^^^^^^^^^^^       

#================= FINAL SCORE ===================
def final_score():
    pass
#^^^^^^^^^^^^^^^^^ FINAL SCORE ^^^^^^^^^^^^^^^^^^^


# GAME LOOP -------
def game_loop():
    global curr_game
    free_cash(game_choice)
    # game must be created first
    curr_game = choose_game(finalscore)
    
    if type(curr_game).__name__ == 'PictGame':
        picture_game()
     
        
        print(type(curr_game).__name__)
        print(curr_game.all_picts)
    else:
        print(curr_game.just_a)
        print(curr_game.just_q)
        text_game()
    #display.blit(curr_game.all_picts[0], (100,100))  
    #pygame.display.flip()
    
    #print(curr_game.num_ans)
    # curr_game returns a Game object with it's backround, 
    # question/answer file, (0,0)location, number of questions


    #curr_game.take_turn()
    print('took a turn')    

#\\\\\\\\\\\\\\\\\\\\\\ END METHODS \\\\\\\\\\\\\\\\\\\\\\\\




def main():
    try:
        init()
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