
import requests
import Adafruit_ADS1x15
import datetime

from rpi_lcd import LCD
from time import sleep, time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

from Webinfo import WebSongInfo, WebWeatherInfo, WebTagesschauInfo, WebSchneehoehenInfo

from GardenMoonInfo import GardenMoonInfo
from HafasOebb import OebbHafasClient

# GPIO pin numbers
BUTTON_PIN = 11

# Menu options
OPTIONS = {
    'fm4': 'FM4 Song',
    'oe1liveradio': 'ö1 Song',
    "train": "Nächster Zug",
    "tagesschau": "Aktuelle Nachrichten",
    "schneehoehe_soelden": "Schneehöhe in Sölden",
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

def lcd_u(text: str, line: int):
    # Create a mapping of German umlauts and special characters to their LCD cod                                                                                                                                                                                                                                             es
    umlaut_mapping = {
        'ä': "\xE1",  # ä
        'ö': "\xEF",  # ö
        'ü': "\xF5",  # ü
        'ß': "\xE2",  # ß
        '°': "\xDF",  # °
        'µ': "\xE4",  # µ
        'Ω': "\xF4"   # Ω
    }

    # Replace umlauts in the text with the corresponding codes
    for char, code in umlaut_mapping.items():
        text = text.replace(char, code)

    # Call the original lcd.text function
    lcd.text(text, line)

def display_scrolling_text(txt, seconds: int = 5):
    txt = txt.strip() + ' '
    words = txt.split()  # Split text into individual words
    # Calculate the number of words the text needs to scroll
    scroll_length = len(words)

    # If the text is less than or equal to 32 characters, display it without scr                                                                                                                                                                                                                                             olling
    if len(txt) <= 32:
        lcd_u(txt, 1)
        sleep(seconds)
        return

    # Calculate the total number of scrolls needed to show the entire text at le                                                                                                                                                                                                                                             ast once
    total_scrolls = max((seconds * 2) - 2, scroll_length)
    print(total_scrolls)
    i = 0
    while i < total_scrolls + 1:
        # Extract the words to display in the current scroll
        display_words = ' '.join(words)
        lcd_u(display_words[:32], 1)

        # Initial delay only for the first scroll
        if i == 0:
            sleep(1)
        else:
            sleep(0.5)

        # Rotate words for scrolling effect
        words = words[1:] + words[:1]
        i += 1
# Function to read ADC value
def read_adc(channel):
    value = adc.read_adc(channel, gain=GAIN)
    return value

# Function to determine selected option based on potentiometer value
def get_selected_option():
    adc_value = read_adc(0)
    max_value = 26404
    thresholds = [max_value / len(OPTIONS) * i for i in range(1, len(OPTIONS))]
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

    elif option == "train":
        print("Nächster Zug")
        request = OebbHafasClient()

    elif option == "tagesschau":
        print("Tagesschau")
        request = WebTagesschauInfo()

    elif option == "schneehoehe_soelden":
        print("Schneehöhe in Sölden")
        request = WebSchneehoehenInfo("oetztal-arena-soelden")

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



    lcd_u("Loading...", 1)
    try:
        content = request.fetch_content()
        text = request.parse_content(content)
    except requests.RequestException as e:
        text = "Error fetching text"
        print(f"Error: {e}")

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

def get_menu_text():
    key = get_selected_option()
    index = list(OPTIONS.keys()).index(key)
    option = OPTIONS.get(get_selected_option())
    return str(index+1) + ". " + option
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
        sleep(1)
    else:
    # Display menu based on potentiometer value
        lcd_u(get_menu_text(), 1)
        sleep(1)
