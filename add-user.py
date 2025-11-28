import RPi.GPIO as GPIO
import sys, json, datetime
from time import sleep
sys.path.append('/home/pi/rfid/MFRC522-python')
from mfrc522 import SimpleMFRC522
from modules import *

# function to add to JSON
def write_json(data, filename='rfid-door-lock.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

# Sleep for 3 seconds to ensure RFID service has stopped
print("Stopping RFID Service")
sleep(3)
print("RFID Service Stopped")
print("")

# Read the config file and store in memory
with open('rfid-door-lock.json') as f:
  data = json.load(f)

gpio_init()

# Main Loop
while True:
  firstname = ""
  lastname = ""
  keytype = ""
  notes = ""
  print("Press Enter to Finish")
  firstname = input('Enter First Name:')
  if (firstname == ""):
    break
  lastname = input('Enter Last Name:')
  keytype = input('Enter Key Type (KeyFob/KeyCard/CreditCard/OpalCard/Other):')
  notes = input('Enter Notes:')

  uid = rfid_read_PN532()

  led_green()

  with open('rfid-door-lock.json') as json_file:
    data = json.load(json_file)

  users = data["users"]

  # python object to be appended
  now = datetime.datetime.now()
  new_user = {'uid': str(uid),
              'created': now.strftime("%Y-%m-%d %H:%M:%S"),
              'lastEntered': "",
              'keyType': keytype,
              'active': True,
              'firstName': firstname,
              'lastName': lastname,
              'notes': notes
             }

  print(new_user)

  # appending data to emp_details
  users.append(new_user)
  write_json(data)

  sleep(2)
  led_off()

GPIO.cleanup()
sleep(3)


# {
#     "users": [
#         {
#             "uid": "1234567890",
#             "created": "2020-07-01 19:00:00",
#             "lastEntered": "",
#             "keyType": "KeyCard",
#             "active": true,
#             "firstName": "Fred",
#             "lastName": "Blogs",
#             "notes": ""
#         }
#     ]
# }
