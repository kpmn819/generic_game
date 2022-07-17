




class GameScreen:
    def __init__(self, buttons, text, background, highlights,
    question, answers, qpicture, apictures, score ):
        self.buttons = buttons # which buttons are active
        self.text = text # full screen text
        self.background = background
        self.highlights = highlights
        self.question = question
        self.answers = answers # list of three
        self.qpicture = qpicture
        self.apictures = apictures # list of five
        self.score = score
    def qna(self):
        return self.question
    def blitter(self):
        # this would send stuff to the blitter
        # but how would it know?
        # test for no content -1 and don't pass on
        print(self.question, self.answers,) 
    @classmethod
    def game1_scr(cls):
        pass

# create screen objects
home_screen = GameScreen(1,2,3,'','QString',['Ra','W1','W2'],-1,-1,(2,3))
#donate_screen = GameScreen()
#game1_screen = GameScreen()
home_screen.background = 'somepicture.jpeg'

#print(home_screen.background)
#print(home_screen.score)
#print(home_screen.question)
#print(home_screen.answers)
ques_ans = home_screen.qna()
print(ques_ans)
home_screen.blitter()

        


