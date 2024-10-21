from gpiozero import Button
from time import sleep

button = Button(2)

while True:
    if button.is_held:
        print("Pressed")
    else:
        print("Released")
