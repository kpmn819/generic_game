import os
if os.name == 'nt':
    pass
else:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

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

def buttons_lights(active_list, lgt_set, btn_mon):
    try:button1
    except NameError: button1 = None
    # figure if one is missing they all are
    if button1 is None:
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
        for i, button in enumerate(button_list):
            pass
            #Button.setup_port(button)

    if lgt_set:
        # uses active_list to set outputs
        for i, button in enumerate(button_list):
            if active_list[i]:
                # set the port False = low light on
                # call Button to set port gpio
                button.out_port = False
            else:
                button.out_port = True

    if btn_mon:
        loop = True
        while loop == True:
            for i, button in enumerate(button_list):
                if active_list[i]: 
                    # go check the physical port if it comes back False
                    # set our status and get out
                    button.in_port = False
                    loop = False
                else:
                    button.in_port = True
                    pass

    return    button_list


# 0=free, 1=btn1, 2=btn2, 3=btn3, 4=btn4, 5=btn5, 6=pay
active_list = [0, 1, 1, 1, 1, 1, 0]
# last two items in buttons_lights call lgt_set, btn_mon
button_list = buttons_lights(active_list, 1, 0)
print(button_list[1].out_port)

