sudo cp rfid-doorlock.service /lib/systemd/system/rfid-doorlock.service
sudo systemctl daemon-reload
sudo systemctl enable rfid-doorlock.service
sudo systemctl start rfid-doorlock.service
sudo systemctl status rfid-doorlock.service
