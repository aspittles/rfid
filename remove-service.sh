sudo systemctl status rfid-doorlock.service
sudo systemctl stop rfid-doorlock.service
sudo systemctl disable rfid-doorlock.service
sudo rm /lib/systemd/system/rfid-doorlock.service
sudo systemctl daemon-reload
