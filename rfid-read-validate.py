import RPi.GPIO as GPIO
import sys, logging, json, datetime, requests, subprocess
from time import sleep
sys.path.append('/home/pi/rfid/MFRC522-python')
from mfrc522 import SimpleMFRC522
sys.path.append('/home/pi/rfid/py532lib-master')
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from modules import *

# Function to Validate the Card UID against JSON list of allowed users
def validate_access( uid, data ):
  # Check if UID is defined
  found = False
  for i in range(0, len(data["users"])):
    record = data["users"][i]
    if (record["uid"] == str(uid)):
      name = record["firstName"] + " " + record["lastName"]
      authorised = record["active"]
      found = True
      record_num = i
  if found:
    if authorised:
      led_green()
      if (data["config"]["open_door"]):
        doorpass = data["config"]["door_pass"]
        open_door(doorpass)
      logging.info("ALLOW: Access by: " + str(uid) + " (" + name + ")")
      logging.debug((data["users"][record_num]))
      now = datetime.datetime.now()
      data["users"][record_num]["lastEntered"] = now.strftime("%Y-%m-%d %H:%M:%S")
      with open('/home/pi/rfid/rfid-door-lock.json', 'w') as f:
        json.dump(data, f, indent=4)
      temp = get_temp()
      logging.info("Raspberry Pi Temp: " + str(temp))
    else:
      logging.info("BLOCK: Deactivated card attempt by: " + str(uid) + " (" + name + ")")
      logging.debug((data["users"][record_num]))
      led_red()
  else:
    authorised = False
    logging.info("BLOCK: Access attempt by: " + str(uid))
    led_red()
  return authorised;

# Read the config file and store in memory
with open('/home/pi/rfid/rfid-door-lock.json') as f:
  data = json.load(f)

# Enable & configure logging
logging.basicConfig(filename=(data["config"]["log_file"]),level=logging.INFO,format='%(asctime)s %(levelname)s:%(message)s')

# Setup GPIO Pins for use with Bi-Colour LED
led_init()

# Create RFID reader object
reader = SimpleMFRC522()

#Signal that we are up and running
for led_flash in range(0, 15):
  led_green()
  sleep(0.05)
  led_red()
  sleep(0.05)
  led_off()
  sleep(0.05)

temp = get_temp()
logging.info("*******************************************")
logging.info("System Restarted")
logging.info("Raspberry Pi Temp: " + str(temp))

# Main Loop
try:
  while True:
    if (data["config"]["reader"] == "RC522"):
      uid = rfid_read_RC522()
    elif (data["config"]["reader"] == "PN532"):
      uid = rfid_read_PN532()
    else:
      uid = 0
    authorised = validate_access( uid, data );
    sleep(2);
    led_off()

except KeyboardInterrupt:
  GPIO.cleanup()
