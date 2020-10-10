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
  with open('/home/pi/pi-rfid-py-post/rfid-door-lock.json') as f:
    data = json.load(f)
    for p in data['users']:
      if p['keyId'] == str(uid):
        print ('User Id: ' + str(p['userId']))
        print ('Name: ' + p['firstName'] + " " + p['lastName'])
        logging.info(p['firstName'] + " " + p['lastName'] + ' Swiped')
        break
finally:
  sleep(2)
  GPIO.cleanup()
