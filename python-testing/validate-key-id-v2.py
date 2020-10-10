import json

with open('/home/pi/pi-rfid-py-post/rfid-door-lock-v2.json') as f:
  data = json.load(f)
try:
    print(data["users"]["699481201718"]["firstName"])
except KeyError:
    print("ID doesn't exist")
