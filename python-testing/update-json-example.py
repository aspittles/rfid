import json, datetime

with open('rfid-door-lock.json') as f:
  data = json.load(f)

uid = 1062044203790
now = datetime.datetime.now()

data["users"][str(uid)]["lastEntered"] = now.strftime("%Y-%m-%d %H:%M:%S")

with open('rfid-door-lock.json', 'w') as f:
  json.dump(data,  f)

#import datetime
#now = datetime.datetime.now()
#now.strftime("%Y-%m-%d %H:%M:%S")

#import datetime

