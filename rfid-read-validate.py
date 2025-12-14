import RPi.GPIO as GPIO
import sys, logging, json, datetime, requests, subprocess, os, threading
from time import sleep
from http.server import HTTPServer, BaseHTTPRequestHandler

# Base application directory
APP_DIR = "/opt/rfid-door-lock"

sys.path.append(os.path.join(APP_DIR, 'MFRC522-python'))
from mfrc522 import SimpleMFRC522
sys.path.append(os.path.join(APP_DIR, 'py532lib-master'))
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
sys.path.append(APP_DIR)
from modules import *

# Function to Validate the Card UID against JSON list of allowed users
def validate_access(uid, data):
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
        # doorpass = data["config"]["door_pass"]
        # open_door(doorpass) # Old Bio lock method to open door
        mosfet_on()  # Send 12V power to door Solenoid to open door
      logging.info("ALLOW: Access by: " + str(uid) + " (" + name + ")")
      logging.debug((data["users"][record_num]))
      now = datetime.datetime.now()
      data["users"][record_num]["lastEntered"] = now.strftime("%Y-%m-%d %H:%M:%S")
      with open(os.path.join(APP_DIR, 'config/rfid-door-lock.json'), 'w') as f:
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
  return authorised

# Read the config file and store in memory
with open(os.path.join(APP_DIR, 'config/rfid-door-lock.json')) as f:
  data = json.load(f)

# Enable & configure logging
logging.basicConfig(filename=(data["config"]["log_file"]), level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Setup GPIO Pins for use with Bi-Colour LED & Mosfet Power Switch Module
gpio_init()

# Setup HTTP Server for Open Door API call
SECRET_TOKEN = data["config"]["token"]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
#        if self.path == '/status':
#            self.send_response(200)
#            self.send_header('Content-Type', 'text/plain')
#            self.end_headers()
#            self.wfile.write(b'Hello from GET')
#        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')
    def do_POST(self):
        if self.path == '/open':
            token = self.headers.get('Authorization')

            if token != f'Bearer {SECRET_TOKEN}':
                self.send_response(401)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Unauthorized')
                return

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Door Open')
            led_green()
            mosfet_on()  # Send 12V power to door Solenoid to open door
            sleep(5)
            led_off()
            mosfet_off()
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

# Create RFID reader object
# reader = SimpleMFRC522()

# Signal that we are up and running
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

# Startup HTTP Server
server = HTTPServer((data["config"]["http_server_host"], data["config"]["http_server_port"]), Handler)
# data["config"]["http_server_ip"]
thread = threading.Thread(target=server.serve_forever)
thread.daemon = True
thread.start()

# Main Loop
try:
  while True:
    if (data["config"]["reader"] == "RC522"):
      uid = rfid_read_RC522()
    elif (data["config"]["reader"] == "PN532"):
      uid = rfid_read_PN532()
    else:
      uid = 0
    authorised = validate_access(uid, data)
    sleep(5)
    led_off()
    mosfet_off()

except KeyboardInterrupt:
  GPIO.cleanup()
  server.shutdown()
