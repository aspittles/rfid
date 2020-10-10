import json

with open('/home/pi/pi-rfid-py-post/rfid-door-lock.json') as f:
  data = json.load(f)
  for p in data['users']:
    print ('Id: ' + str(p['userId']))
    print ('Name: ' + p['firstName'] + " " + p['lastName'])
