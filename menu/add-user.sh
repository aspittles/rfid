sudo systemctl stop rfid-doorlock.service

python3 /opt/rfid-door-lock/add-user.py

sudo systemctl start rfid-doorlock.service
