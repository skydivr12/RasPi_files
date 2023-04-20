import os
import time
import schedule
from MCP3008 import MCP3008

# Define variables
adc = MCP3008()
min_light_value = 200
max_light_value = 900
min_backlight_value = 15
max_backlight_value = 100
schedule_time = 1  # in seconds
sleep_time = 0.1  # in seconds

# Define function to read light sensor value and set backlight value
def set_backlight():
    # Read light sensor value
    light_value = adc.read(channel=0)

    # Map light sensor value to backlight value
    if light_value < min_light_value:
        backlight_value = min_backlight_value
    elif light_value > max_light_value:
        backlight_value = max_backlight_value
    else:
        backlight_value = (light_value - min_light_value) * (max_backlight_value - min_backlight_value) / (max_light_value - min_light_value) + min_backlight_value

    # Set backlight value
    os.system("vcgencmd set_backlight {}".format(int(backlight_value)))

# Schedule function to run periodically
schedule.every(schedule_time).seconds.do(set_backlight)

# Main loop
while True:
    schedule.run_pending()
    time.sleep(sleep_time)
