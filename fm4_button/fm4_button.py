import requests
import sys

from bs4 import BeautifulSoup
from rpi_lcd import LCD
from time import sleep
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 11 to be an input pin and set initial value to be pulled low (off)


def get_current_song():

    # FM4 website URL
    # [oe1liveradio, fm4]
    url = "https://onlineradiobox.com/at/fm4/playlist/?lang=en"

    # Fetch webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting the song and artist information
    song = soup.find("td", class_="track_history_item")
    song = song.text.strip() if song else "Unknown"

    return song

def reset():
    lcd.clear()
    lcd.text("Press button for current fm4 song", 1)


def fm4_callback(channel):
    lcd.clear()
    lcd.text("Loading...", 1)
    song = get_current_song()
    GPIO.remove_event_detect(11)
    lcd.clear()
    lcd.text(song, 1)
    sleep(5)
    setup()
    reset()

def setup():
    GPIO.add_event_detect(11,GPIO.RISING,callback=fm4_callback, bouncetime=500)



try:
    lcd = LCD()
    reset()
    GPIO.add_event_detect(11,GPIO.RISING,callback=fm4_callback, bouncetime=1000)
    print("Initializing done")
    while True:
       sleep(1)

except Exception:
    GPIO.cleanup()
    lcd.clear()
    lcd.text("Shutdown fm4 program", 1)
    sleep(1)
    lcd.clear()
    print("Program terminated")
    sys.exit(0)