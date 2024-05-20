import threading
import requests
import sys
import Adafruit_ADS1x15


from bs4 import BeautifulSoup
from rpi_lcd import LCD
from time import sleep
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

from Webinfo import WebSongInfo

# GPIO pin numbers
BUTTON_PIN = 11

# Menu options
OPTIONS = {'fm4': 'Current FM4 Song', 'oe1liveradio': 'Current OE1 Song', "temperature": "Temperatur in Linz"}

# Global flag to control the main loop execution
pause_flag = False

# Function to read ADC value
def read_adc(channel):
    value = adc.read_adc(0, gain=GAIN)
    return value

# Function to determine selected option based on potentiometer value
def get_selected_option():
    adc_value = read_adc(0)
    max_value = 26404
    if adc_value < max_value/3:
        return "fm4"
    elif adc_value < 2*(max_value/3):
        return "oe1liveradio"
    else:
        return "temperature"


# Function to execute for each option
def execute_option(channel):
    global pause_flag
    pause_flag = True
    GPIO.remove_event_detect(BUTTON_PIN)
    reset_display()
    option = get_selected_option()
    if option == "fm4":
        print("Getting FM4 Song")
         # Create an instance of RequestSongName with the radio name "fm4"
        request = WebSongInfo("fm4")
    elif option == "oe1liveradio":
        print("Playing Ö1 Song")
        request = WebSongInfo("oe1liveradio")
        # Your Ö1 song playing code here
    elif option == "temperature":
        print("Displaying temperature in Linz")
        # Your temperature display code here
        #request = RequestTemperature("linz")
        request = WebSongInfo("linz")

    lcd.text("Loading...", 1)
    try:
        content = request.fetch_content()
        song = request.parse_content(content)
    except requests.RequestException as e:
        song = "Error fetching song"
        print(f"Error: {e}")

    print(song)
    lcd.text(song, 1)
    sleep(5)
    # setup_gpio()
    reset_display()
    pause_flag = False

# Function to reset the display
def reset_display():
    lcd.clear()

# Function to setup GPIO event detection
def setup_gpio():
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=execute_option, bouncetime=500)


# Setup GPIO
GPIO.setmode(GPIO.BOARD)

# Setup GPIO BUTTON
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup ADC
adc = Adafruit_ADS1x15.ADS1115() # Create an ADS1115 ADC (16-bit) instance
GAIN = 1

# Setup LCD
lcd = LCD()

# Reset_display()
setup_gpio()
print("Initializing done")

while True:
    if pause_flag:
        sleep(0.1)
    else:
    # Display menu based on potentiometer value
        lcd.text("Menu: ", 1)
        lcd.text(OPTIONS.get(get_selected_option()), 2)
        sleep(1)

