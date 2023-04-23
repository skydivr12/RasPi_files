#!/usr/bin/env python3
import subprocess
from gpiozero import Button

# Define the GPIO pin for the button
BUTTON_PIN = 3

# Setup the button pin as input with a pull-up resistor
button = Button(BUTTON_PIN, pull_up=True)

# Define a function to shutdown the Raspberry Pi
def shutdown():
    subprocess.run(['sudo', 'shutdown', '-h', 'now'], check=True)

# Wait for the button to be pressed
button.wait_for_press()

# Call the shutdown function when the button is pressed
shutdown()