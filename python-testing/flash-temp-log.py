import subprocess, logging, RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(29, GPIO.OUT, initial=GPIO.LOW) # Set pin 29 (GPIO 5) to be an output pin and set initial value to low (off)
GPIO.setup(31, GPIO.OUT, initial=GPIO.LOW) # Set pin 31 (GPIO 6) to be an output pin and set initial value to low (off)
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW) # Set pin 22 (GPIO 25) to be an output pin and set initial value to low (off)


# Enable & configure logging
logging.basicConfig(filename="/home/pi/rfid/temprature.log",level=logging.INFO,format='%(asctime)s %(levelname)s:%(message)s')

def get_temp():
    """
    Get the core temperature.
    Run a shell script to get the core temp and parse the output.
    Raises:
        RuntimeError: if response cannot be parsed.
    Returns:
        float: The core temperature in degrees Celsius.
    """
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        raise RuntimeError('Could not parse temperature output.')

try:
  while True: # Run forever

    #GPIO.output(29, GPIO.LOW) # Red
    #GPIO.output(31, GPIO.HIGH) # Red
    GPIO.output(22, GPIO.HIGH) # MOSFET on
    #sleep(1) # Sleep for 1 second
    GPIO.output(29, GPIO.HIGH) # Green
    GPIO.output(31, GPIO.LOW) # Green
    sleep(5) # Sleep for 1 second
    GPIO.output(29, GPIO.LOW) # Turn off
    GPIO.output(31, GPIO.LOW) # Turn off
    GPIO.output(22, GPIO.LOW) # MOSFET off
    sleep(5) # Sleep for 1 second
    temp = get_temp()
    print(temp)

except KeyboardInterrupt:
  GPIO.cleanup()

#logging.info("*******************************************")
#logging.info("System Restarted")
#logging.info("Raspberry Pi Temp: " + str(temp))


