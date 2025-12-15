import RPi.GPIO as GPIO
import sys, logging, json, datetime, requests, subprocess, os
from time import sleep

# Base application directory
APP_DIR = "/opt/rfid-door-lock"

sys.path.append(APP_DIR)
from modules import *

# Read the config file and store in memory
with open(os.path.join(APP_DIR, 'config/rfid-door-lock.json')) as f:
  data = json.load(f)

# Enable & configure logging
logging.basicConfig(filename=(data["config"]["log_file"]), level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Setup GPIO Pins for use with Bi-Colour LED & Mosfet Power Switch Module
gpio_init()

temp = get_temp()
led_green() # Show the Green Light to indicate Door is open
logging.info("ALLOW: Remote Door Open")
logging.info("Raspberry Pi Temp: " + str(temp))
print("Door Open")
mosfet_on() # Send 12V power to door Solenoid to open door
sleep(5) # Keep door open for 5 sec
led_off()
mosfet_off() # Stop 12V power to door Solenoid to close door
