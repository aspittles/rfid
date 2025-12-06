import RPi.GPIO as GPIO
import sys, logging, json, datetime, requests, subprocess
from time import sleep
from modules import *

# Read the config file and store in memory
with open('/home/aspittles/rfid/config/rfid-door-lock.json') as f:
  data = json.load(f)

# Enable & configure logging
logging.basicConfig(filename=(data["config"]["log_file"]),level=logging.INFO,format='%(asctime)s %(levelname)s:%(message)s')

# Setup GPIO Pins for use with Bi-Colour LED & Mosfet Power Switch Module
gpio_init()

temp = get_temp()
led_green()
logging.info("ALLOW: Remote Door Open")
logging.info("Raspberry Pi Temp: " + str(temp))
print("**** Door Open ****")
print("This window will auto close in 5 Seconds")
mosfet_on() # Send 12V power to door Solenoid to open door
sleep(5);
led_off()
mosfet_off()
