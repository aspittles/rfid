import RPi.GPIO as GPIO
import sys, logging, json, datetime, requests, subprocess
from time import sleep
sys.path.append('/home/pi/rfid/MFRC522-python')
from mfrc522 import SimpleMFRC522
sys.path.append('/home/pi/rfid/py532lib-master')
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *

# Function to Read the RFID card Using RC522 Reader
def rfid_read_RC522():
  #print("Hold a tag near the RC522 reader")
  uid, text = reader.read()
  return uid

# Function to Read the RFID card Using PN532 Reader
def rfid_read_PN532():
  #print("Hold a tag near the PN532 reader")
  pn532 = Pn532_i2c()
  pn532.SAMconfigure()
  card_data = pn532.read_mifare().get_data()
  uid = uid_to_num(card_data[7:7+card_data[6]],card_data[6])
#  uid = uid_to_num(card_data[7:11])
  return uid

# Function to convert UID bytearray to a decimal UID
def uid_to_num(uid,size):
  n = 0
  for i in range(0, size):
    n = n * 256 + uid[i]
  return n

# Function to Open the Door lock via URL post to door system
def open_door(doorpass):
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  data = {
    'login': '',
    'username': 'door',
    'password': doorpass,
    'button': 'Open Door'
  }
  response = requests.post('http://192.168.0.210/dyn', headers=headers, data=data)

# Function to Init GPIO for LED
def gpio_init():
  # Setup GPIO Pins for use with Bi-Colour LED
  # And MOSFET Power Switch Module
  # Use physical pin numbering
  GPIO.setmode(GPIO.BOARD)
  GPIO.setwarnings(False)

  # Set pin 29 & 31 to be an output pin and set initial value to low (off)
  GPIO.setup(29, GPIO.OUT, initial=GPIO.LOW) # Short Leg (Cathod)
  GPIO.setup(31, GPIO.OUT, initial=GPIO.LOW) # Long Leg (Anode)
  GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW) # Mosfet Trigger

# Function to Turn on LED green
def led_green():
  GPIO.output(29, GPIO.HIGH) # Turn on
  GPIO.output(31, GPIO.LOW) # Turn off

# Function to Turn on LED red
def led_red():
  GPIO.output(29, GPIO.LOW) # Turn off
  GPIO.output(31, GPIO.HIGH) # Turn on

# Function to Turn off LED
def led_off():
  GPIO.output(29, GPIO.LOW) # Turn off
  GPIO.output(31, GPIO.LOW) # Turn off

# Function to Turn on Mosfet Power Switch
def mosfet_on():
  GPIO.output(22, GPIO.HIGH) # Turn on

# Function to Turn off Mosfet Power Switch
def mosfet_off():
  GPIO.output(22, GPIO.LOW) # Turn off

# Function to get Raspberry Pi CPU Temp
def get_temp():
    """Get the core temperature.
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
