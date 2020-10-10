from time import sleep
import RPi.GPIO as GPIO
import sys
import json
import logging

sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522
logging.basicConfig(filename='rfid-read-validate.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s')

reader = SimpleMFRC522()

try:
  print("Hold a tag near the reader")
  uid, text = reader.read()
  print("Key ID: %s" % (uid))
  with open('/home/pi/pi-rfid-py-post/rfid-door-lock-v2.json') as f:
    data = json.load(f)
  try:
    print((data["users"][str(uid)]["firstName"]) + " " + (data["users"][str(uid)]["lastName"]) + " - Status: " + str(data["users"][str(uid)]["active"]))
    logging.info("Access by:" + (data["users"][str(uid)]["firstName"]) + " " + (data["users"][str(uid)]["lastName"]))
  except KeyError:
    print("ID doesn't exist")
    logging.warning("Access attempt by: " + str(uid))
finally:
#  sleep(2)
  GPIO.cleanup()
