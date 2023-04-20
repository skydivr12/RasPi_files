import RPi.GPIO as GPIO
import time

# Define pin numbers
PIN1 = 17
PIN2 = 18

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Wait for pins to settle
time.sleep(0.1)

# Wait for state change on first pin
print("Waiting for state change on first pin (GPIO {})...".format(PIN1))
state1 = GPIO.input(PIN1)
while GPIO.input(PIN1) == state1:
    time.sleep(0.001)
start_time = time.time()

# Wait for state change on second pin
print("Waiting for state change on second pin (GPIO {})...".format(PIN2))
state2 = GPIO.input(PIN2)
while GPIO.input(PIN2) == state2:
    time.sleep(0.001)
end_time = time.time()

# Calculate time difference
time_diff = end_time - start_time

# Print time difference
print("Time difference: {} seconds".format(time_diff))

# Clean up GPIO pins
GPIO.cleanup()
