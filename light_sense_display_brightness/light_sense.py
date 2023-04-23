import os
import time
from spidev import SpiDev
 
class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000 # 1MHz
 
    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz
    
    def read(self, channel = 0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def close(self):
        self.spi.close()
 
# Define variables
adc = MCP3008()
min_light_value = 100
max_light_value = 900
min_backlight_value = 15
max_backlight_value = 100
delay_time = 3

while True:
    # Read light sensor value
    light_value = adc.read(channel=0)
    print(light_value)
    # Map light sensor value to backlight value
    if light_value < min_light_value:
        backlight_value = min_backlight_value
    elif light_value > max_light_value:
        backlight_value = max_backlight_value
    else:
        backlight_value = (light_value - min_light_value) * (max_backlight_value - min_backlight_value) / (max_light_value - min_light_value) + min_backlight_value

    # Set backlight value
    os.system("vcgencmd set_backlight {}".format(int(backlight_value)))

    # Delay
    time.sleep(delay_time)
