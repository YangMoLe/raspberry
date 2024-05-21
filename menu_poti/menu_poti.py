import requests
import Adafruit_ADS1x15
import datetime

from systemd import journal
from rpi_lcd import LCD
from time import sleep
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

from Webinfo import WebSongInfo, WebWeatherInfo

from GardenMoonInfo import GardenMoonInfo
# GPIO pin numbers
BUTTON_PIN = 11

# Menu options
OPTIONS = {
    'fm4': 'Current FM4 Song',
    'oe1liveradio': 'Current OE1 Song',
    "temperature_linz": "Temperatur in Linz",
    "temperature_bremen": "Temperatur in Bremen",
    "temperature_lissabon": "Temperatur in Lissabon",
    "garden_moon_info": "Garten Mondkalender"
}

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
    thresholds = [max_value / 5 * i for i in range(1, 5)]
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
        journal.send("Getting FM4 Song")
        request = WebSongInfo("fm4")

    elif option == "oe1liveradio":
        journal.send("Playing Ö1 Song")
        request = WebSongInfo("oe1liveradio")

    elif option == "temperature_linz":
        journal.send("Displaying temperature for Linz")
        request = WebWeatherInfo("48.3064", "14.2861")

    elif option == "temperature_bremen":
        journal.send("Displaying temperature for Bremen")
        request = WebWeatherInfo("53.075", "8.808")

    elif option == "temperature_lissabon":
        journal.send("Displaying temperature for Lissabon")
        request = WebWeatherInfo("38.717", "-9.133")

    elif option == "garden_moon_info":
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%B %d")
        journal.send("Garten Mondkalendar fuer " + formatted_date)
        request = GardenMoonInfo(formatted_date)


    lcd.text("Loading...", 1)
    try:
        content = request.fetch_content()
        text = request.parse_content(content)
    except requests.RequestException as e:
        text = "Error fetching text"
        journal.send(f"Error: {e}")

    print(text)
    lcd.text(text, 1)
    sleep(5)
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
journal.send("Initializing done")

while True:
    if pause_flag:
        sleep(0.1)
    else:
    # Display menu based on potentiometer value
        option = "Menu: " + OPTIONS.get(get_selected_option())
        lcd.text(option, 1)
        sleep(1)
