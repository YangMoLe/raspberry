from gpiozero import LED
from time import sleep

led = LED(17)


while True:
    led.on() # [led.on() for led in leds]
    sleep(1)
    led.off() #[led.off() for led in leds]
    sleep(1)