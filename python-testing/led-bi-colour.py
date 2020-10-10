import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
#GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(29, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(31, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
# try:
#   while True: # Run forever
#     GPIO.output(29, GPIO.HIGH) # Turn on (Green)
#     GPIO.output(31, GPIO.LOW) # Turn off (Green)
#     sleep(1) # Sleep for 1 second
#     GPIO.output(29, GPIO.LOW) # Turn off (Red)
#     GPIO.output(31, GPIO.HIGH) # Turn off (Red)
#     sleep(1) # Sleep for 1 second
try:
  while True: # Run forever
    GPIO.output(29, GPIO.LOW) # Turn on (Red)
    GPIO.output(31, GPIO.HIGH) # Turn off (Red)
    sleep(.2) # Sleep for 1 second
    GPIO.output(29, GPIO.LOW) # Turn off
    GPIO.output(31, GPIO.LOW) # Turn off
    sleep(5) # Sleep for 5 second



except KeyboardInterrupt:
  GPIO.cleanup()
