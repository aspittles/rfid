import sys, json, datetime
from time import sleep

a_dictionary = {"users": {"1234567899012": {"created": "2020-07-01 19:00:00","lastEntered": "","keyType": "KeyFob","active": True,"firstName": "Krish","lastName": "Lee"}}}
#a_dictionary = {"users": {"1234567899012": "Test"}}

with open('rfid-door-lock.json', 'r+') as f:
  data = json.load(f)
print("Data")
print(data)

new_data = data.update(a_dictionary)
print("Dict")
print(a_dictionary)
print("Data")
print(data)
print("New")
print(new_data)

# Driver code
dict1 = {'a': 10, 'b': 8}
dict2 = {'d': 6, 'c': 4}
dict3  = {**dict1, **dict2}
# This return None
print("Test")
print(dict3)


#  f.seek(0)
#  json.dump(data, f)

#{
#  "users": {
#    "36199966818": {
#      "created": "2020-07-01 19:00:00",
#      "lastEntered": "",
#      "keyType": "Android",
#      "active": false,
#      "firstName": "Jone",
#      "lastName": "Mac"
#    }
#  }
#}
