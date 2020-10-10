import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
  'login': '',
  'username': 'door',
  'password': '<Password>',
  'button': 'Open Door'
}

response = requests.post('http://192.168.0.210/dyn', headers=headers, data=data)

