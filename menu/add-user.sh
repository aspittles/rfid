sudo systemctl stop rfid-doorlock.service

python3 ~/rfid/add-user.py

sudo systemctl start rfid-doorlock.service
