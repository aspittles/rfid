import json

with open('/home/pi/pi-rfid-py-post/rfid-door-lock.json') as f:
  data = json.load(f)
  for p in data['users']:
      if p['keyId'] == '1062287203790':
        print ('Id: ' + str(p['userId']))
        print ('Name: ' + p['firstName'] + " " + p['lastName'])
        break
