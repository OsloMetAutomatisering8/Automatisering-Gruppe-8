import utime
from time import sleep
import machine
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

BUTTON = Pin(14, Pin.IN, Pin.PULL_UP)
TERMINATION = Pin(20, Pin.IN, Pin.PULL_DOWN)
BA_SHORT = Pin(22, Pin.IN, Pin.PULL_DOWN) 
B_BREAK = Pin(17, Pin.IN, Pin.PULL_DOWN)
BA_BREAK = Pin(21, Pin.IN, Pin.PULL_DOWN)
BA_SWITCH = Pin(18, Pin.IN, Pin.PULL_DOWN)
NO_GND = Pin(19, Pin.IN, Pin.PULL_DOWN)

STATE = 0
ANSWER = 100
i2c = I2C(0, sda=machine.Pin(8), scl=machine.Pin(9), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)    

while True:
    if (BUTTON.value() == 0):
        ANSWER = 1
        if (TERMINATION() == 1):
            if (STATE != 1):
                lcd.clear()
                lcd.putstr("Termination     fault!")
            STATE = 1
        elif (BA_SHORT() == 1):
            if (STATE != 2):
                lcd.clear()
                lcd.putstr("BA shortcircuit")
            STATE = 2
        elif (B_BREAK() == 1):
            if (STATE != 3):
                lcd.clear()
                lcd.putstr("B wirebreak")
            STATE = 3
        elif (BA_BREAK() == 1):
            if (STATE != 4):
                lcd.clear()
                lcd.putstr("BA wirebreak")
            STATE = 4
        elif (BA_SWITCH() == 1):
            if (STATE != 5):
                lcd.clear()
                lcd.putstr("BA switched")
            STATE = 5
        elif (NO_GND() == 1):
            if (STATE != 6):
                lcd.clear()
                lcd.putstr("Improper grounding")
            STATE = 6
        else:
            if (STATE != 7):
                lcd.clear()
                lcd.putstr("No fault running")
            STATE = 7
            
    else:
        if (ANSWER != 0):
            lcd.clear()
            lcd.putstr("Press button to reveal answer")
        ANSWER = 0
        STATE = 0