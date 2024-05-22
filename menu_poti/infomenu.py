import requests
import Adafruit_ADS1x15
import datetime

from rpi_lcd import LCD
from time import sleep, time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

from Webinfo import WebSongInfo, WebWeatherInfo

from GardenMoonInfo import GardenMoonInfo
from HafasOebb import OebbHafasClient

# GPIO pin numbers
BUTTON_PIN = 11

# Menu options
OPTIONS = {
    'fm4': 'FM4 Song',
    'oe1liveradio': 'OE1 Song',
    "train": "Nächster zuch",
    "temperature_linz": "Temperatur in Linz",
    "temperature_vienna": "Temperatur in Wien",
    "temperature_bremen": "Temperatur in Bremen",
    "temperature_lissabon": "Temperatur in Lissabon",
    "garden_moon_info": "Garten Mondkalender"
}

# Global flag to control the main loop execution
pause_flag = False
stay_duration = 5

# helper

def display_scrolling_text(txt, seconds: int = 5):
    txt = txt.strip() + '. '
    # Calculate the number of positions the text needs to scroll
    scroll_length = len(txt) if len(txt) > 32 else 32
    # If the text is less than 32 characters, pad it with spaces to make it 32 characters long
    if len(txt) < 33:
        txt = txt + (32 - len(txt)) * ' '
        lcd.text(txt, 1)
        sleep(seconds)
        return
    # Calculate the total number of scrolls needed to show the entire text at least once
    total_scrolls = max((seconds * 5) + 0.8, scroll_length)

    i = 0
    while i < total_scrolls + 1:
        lcd.text(txt[:32], 1)
        if i == 0:
            sleep(0.8)
        sleep(0.2)
        txt = txt[1:] + txt[0]
        i += 1


# Function to read ADC value
def read_adc(channel):
    value = adc.read_adc(0, gain=GAIN)
    return value

# Function to determine selected option based on potentiometer value
def get_selected_option():
    adc_value = read_adc(0)
    max_value = 26404
    thresholds = [max_value / len(OPTIONS) * i for i in range(1, 5)]
    stations = list(OPTIONS.keys())
    for i, threshold in enumerate(thresholds):
        if adc_value < threshold:
            return stations[i]
    return stations[-1]


# Function to execute for each option
def execute_option(channel):
    global pause_flag
    pause_flag = True
    GPIO.remove_event_detect(BUTTON_PIN)
    reset_display()
    option = get_selected_option()
    if option == "fm4":
        print("Getting FM4 Song")
        request = WebSongInfo("fm4")

    elif option == "oe1liveradio":
        print("Playing Ö1 Song")
        request = WebSongInfo("oe1liveradio")

    elif option == "temperature_linz":
        print("Displaying temperature for Linz")
        request = WebWeatherInfo("48.3064", "14.2861")

    elif option == "temperature_vienna":
        print("Displaying temperature for Wien")
        request = WebWeatherInfo("48.2085", "16.3721")

    elif option == "temperature_bremen":
        print("Displaying temperature for Bremen")
        request = WebWeatherInfo("53.075", "8.808")

    elif option == "temperature_lissabon":
        print("Displaying temperature for Lissabon")
        request = WebWeatherInfo("38.717", "-9.133")

    elif option == "garden_moon_info":
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%B %d")
        print("Garten Mondkalendar fuer " + formatted_date)
        request = GardenMoonInfo(formatted_date)

    elif option == "train":
        print("Nächster Zug")
        request = OebbHafasClient()

    lcd.text("Loading...", 1)
    try:
        content = request.fetch_content()
        text = request.parse_content(content)
    except requests.RequestException as e:
        text = "Error fetching text"
        print(f"Error: {e}")

    print(text)
    display_scrolling_text(text, stay_duration)
    setup_gpio()
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
        option = "Menu: " + OPTIONS.get(get_selected_option())
        lcd.text(option, 1)
        sleep(1)