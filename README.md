# RFID Door Access Control System

A Raspberry Pi-based RFID door access control system that validates cards against a JSON database and controls door entry via GPIO outputs.

## Overview

This system reads RFID cards using either RC522 or PN532 readers, validates them against a list of authorized users, and controls door access through a MOSFET-driven solenoid lock. Visual feedback is provided through a bi-color LED, and all access attempts are logged.

## Hardware Requirements

- Raspberry Pi (tested on models with GPIO)
- RFID Reader (either RC522 or PN532)
- Bi-color LED (red/green)
- MOSFET power switch module
- 12V door solenoid lock
- Appropriate resistors and wiring

## GPIO Pin Assignments

- **Pin 02**: PN532 RFID VCC
- **Pin 03**: PN532 RFID SDA
- **Pin 05**: PN532 RFID SCL
- **Pin 06**: PN532 RFID GND
- **Pin 20**: MOSFET GND (door solenoid control)
- **Pin 22**: MOSFET TRIG (door solenoid control)
- **Pin 29**: LED Cathode (short leg)
- **Pin 31**: LED Anode (long leg)  

<p align="center">
  <img src="./images/GPIO-Pinout.jpg" alt="GPIO-Pinout">
</p>

## Software Dependencies

```bash
# Required Python libraries
RPi.GPIO
requests

# RFID reader libraries
MFRC522-python (for RC522 reader)
py532lib (for PN532 reader)
```

## Configuration File

The system requires a JSON configuration file at `/home/pi/rfid/rfid-door-lock.json` with the following structure:

```json
{
  "config": {
    "reader": "RC522 or PN532",
    "open_door": true,
    "log_file": "/path/to/logfile.log"
  },
  "users": [
    {
      "uid": "card_uid_number",
      "firstName": "John",
      "lastName": "Doe",
      "active": true,
      "lastEntered": "2024-01-01 12:00:00"
    }
  ]
}
```

## Features

### Access Control
- Validates RFID cards against a database of authorized users
- Supports both active and deactivated card states
- Tracks last entry time for each user
- Logs all access attempts (authorized and unauthorized)

### Visual Feedback
- **Green LED**: Access granted
- **Red LED**: Access denied
- **Flashing sequence**: System startup indicator

### Door Control
- Activates MOSFET to supply 12V to door solenoid
- Configurable door opening via JSON config
- 5-second door unlock duration

### System Monitoring
- Logs Raspberry Pi CPU temperature
- Comprehensive access logging with timestamps
- User activity tracking

## Installation

1. Clone the required RFID reader libraries:
```bash
cd /home/pi/rfid
git clone https://github.com/pimylifeup/MFRC522-python.git
git clone https://github.com/HubertD/py532lib.git py532lib-master
```

2. Place `rfid-read-validate.py` and `modules.py` in `/home/pi/rfid/`

3. Create your configuration file at `/home/pi/rfid/rfid-door-lock.json`

4. Install Python dependencies:
```bash
pip3 install RPi.GPIO requests
```

Notes to be sorted
Raspberry Pi OS Lite (64bit) - Debian Trixie no desktop
```bash
sudo apt update && sudo apt upgrade -y
sudo raspi-config nonint do_i2c 0
sudo apt install python3-rpi.gpio git -y
sudo git clone https://github.com/aspittles/rfid.git -b slack-open /opt/rfid-door-lock
cp /opt/rfid-door-lock/menu/.bash_aliases ~
echo 'sh /opt/rfid-door-lock/menu/menu.sh' >> ~/.bashrc
exec bash 
echo "Deploy the Service using option 5"
echo "Restart the Service after deploy using option 2"
echo "Watch for Flashing lights"
```

## Usage

Run the main script:
```bash
python3 /home/pi/rfid/rfid-read-validate.py
```

The system will:
1. Flash the LED 30 times to indicate startup
2. Log the system restart and CPU temperature
3. Enter the main loop, continuously reading for RFID cards
4. Validate each card and control door access accordingly

## Operation

### Authorized Access
1. Card is scanned
2. Green LED illuminates
3. Door solenoid activates (if configured)
4. Access is logged with user details
5. User's "lastEntered" timestamp is updated
6. System waits 5 seconds before resetting

### Unauthorized Access
1. Card is scanned
2. Red LED illuminates
3. Access attempt is logged
4. System waits 5 seconds before resetting

## Logging

All events are logged with timestamps including:
- System restarts
- Successful access attempts (with user details)
- Blocked access attempts (deactivated cards)
- Unknown card attempts
- System temperature readings

## Safety & Shutdown

Press `Ctrl+C` to safely shutdown the system. This will properly clean up GPIO resources.

## Notes

- The system includes legacy code for a bio lock door system (commented out)
- CPU temperature is monitored to ensure system health
- The JSON database is updated in real-time with access timestamps
