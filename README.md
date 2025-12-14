# RFID/API/Slack Door Access Control System

A Raspberry Pi-based access control system that manages door entry through RFID cards/fobs, with remote access capabilities via HTTP API and Slack integration.

## Overview

This system reads RFID cards using a PN532 reader, validates them against a list of authorized users, and controls door access through a MOSFET-driven solenoid lock. Visual feedback is provided through a bi-color LED, and all access attempts are logged.

## Hardware Requirements

- Raspberry Pi (tested on Models 3B & 4B)
- RFID Reader (PN532)
- Bi-color LED (red/green)
- MOSFET power switch module
- 12V door solenoid lock

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

## Configuration File

The system requires a JSON configuration file at `/opt/rfid-door-lock/config/rfid-door-lock.json` with the following structure:

```json
{
    "config": {
        "log_level": "INFO",
        "log_file": "/opt/rfid-door-lock/config/door-access.log",
        "reader": "PN532",
        "open_door": true,
        "door_pass": "<Password>",
        "http_server_host": "0.0.0.0",
        "http_server_port": 8000,
        "token": "my-secret-token",
        "slack_bot_token": "xoxb-your-bot-token",
        "slack_app_token": "xapp-your-app-token"
    },
    "users": [
        {
            "uid": "1234567890",
            "created": "2020-08-09 21:01:52",
            "lastEntered": "",
            "keyType": "KeyCard",
            "active": true,
            "firstName": "User1",
            "lastName": "Person1",
            "notes": ""
        }
    ]
}
```

| Setting | Description |
|---------|-------------|
| `log_level` | Log file log level INFO or DEBUG |
| `log_file` | Path to the access log file |
| `reader` | PN532 (Old setting) |
| `open_door` | Enable/disable door unlocking (useful for testing) |
| `open_door` |  Old bio lock door system password (Old setting) |
| `http_server_host` | IP address for the HTTP API |
| `http_server_port` | Port for the HTTP API |
| `token` | Bearer token for HTTP API authentication |
| `slack_bot_token` | Slack bot OAuth token (starts with `xoxb-`) |
| `slack_app_token` | Slack app-level token for Socket Mode (starts with `xapp-`) |


## Features

### Access Control
- Validates RFID cards against a database of authorized users
- Supports both active and deactivated card states
- Tracks last entry time for each user
- Logs all access attempts (authorized and unauthorized)
- Listens on HTTP port 8000 for /open and correct bearer token
- Listens on specific slack channel for "Open"

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

1. Use Raspberry Pi Imager 2 and create a clean image.
   Tested with "Raspberry Pi OS Lite (64bit) - Debian Trixie no desktop"

2. Clone the required RFID reader libraries:
```bash
sudo apt update && sudo apt upgrade -y
sudo raspi-config nonint do_i2c 0
sudo apt install python3-rpi.gpio git python3-pip -y
sudo pip3 install slack-bolt --break-system-packages
```

3. Download this git repo to `/opt/rfid-door-lock`
```bash
sudo git clone https://github.com/aspittles/rfid.git /opt/rfid-door-lock
```

4. Add the menu system to show on logon and restart bash
```bash
cp /opt/rfid-door-lock/menu/.bash_aliases ~
echo 'sh /opt/rfid-door-lock/menu/menu.sh' >> ~/.bashrc
exec bash
```

5. Door Lock Menu, Use option 0 to show this menu
```Text
    Door Lock Menu
    1. Status
    2. Restart
    3. Start
    4. Stop

    5. Deploy Service
    6. Remove Service

    7. Add New User
    8. Show last 20 Log Entries
    9. Open Door

    0. This Menu
```

6. Update `/opt/rfid-door-lock/rfid-door-lock.json` with the Bearer `token`
   
8. Update `/opt/rfid-door-lock/rfid-door-lock.json` with the Slack `xoxb-your-bot-token` & `xapp-your-app-token`
   See **Slack App Setup** section below

9. Deploy the Service using option 5

10. Restart the Service after deploy using option 2 and watch for Flashing lights

### Slack App Setup

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**

2. **Enable Socket Mode** (Settings → Socket Mode → Enable)
   - Generate an app-level token with `connections:write` scope
   - Copy the token (starts with `xapp-`)

3. **Add Bot Permissions** (OAuth & Permissions → Bot Token Scopes):
   - `channels:history` - Read messages in public channels
   - `groups:history` - Read messages in private channels
   - `chat:write` - Send messages

4. **Subscribe to Events** (Event Subscriptions → Enable → Subscribe to bot events):
   - `message.channels`
   - `message.groups`

5. **Install App** to workspace and copy the Bot Token (starts with `xoxb-`)

6. **Invite the bot** to your private channel: `/invite @YourBotName`

## Usage

The system will:
1. Flash the Red/Green LED 15 times to indicate startup
2. Log the system restart and CPU temperature
3. Start the HTTP Listener in it's own thread
4. Start the Slack Listener in it's own thread
5. Enter the main loop, continuously waiting for RFID cards
6. Validate each card and control door access accordingly

## Operation

### RFID Authorized Access
1. Card is scanned
2. Green LED illuminates
3. Door solenoid activates (if configured)
4. Access is logged with user details
5. User's "lastEntered" timestamp is updated in config file
6. System waits 5 before locking door and resetting

### RFID Unauthorized Access
1. Card is scanned
2. Red LED illuminates
3. Access attempt is logged
4. System waits 5 seconds before resetting

### Enrolling Users
Use Option 7 to Add a new user
1. Follow the prompts to enter user details.
2. Present the RFID card to the reader.
3. Press Enter without typing a name to finish and restart the door access system.

### HTTP API
Open the door remotely with an authenticated POST request:

```bash
curl -X POST http://your-pi-ip:8000/open \
  -H "Authorization: Bearer your-secret-token"
```

**Responses:**
- `200 OK` — Door opened successfully
- `401 Unauthorized` — Invalid or missing token
- `404 Not Found` — Invalid endpoint

## Logging

All events are logged with timestamps including:
- System restarts
- Successful access attempts (with user details)
- Blocked access attempts (deactivated cards)
- Unknown card attempts
- System temperature readings

## File Structure

```
/opt/rfid-door-lock/
├── rfid-read-validate.py       # Main application
├── modules.py                  # Shared hardware functions
├── add-user.py                 # User enrollment utility
├── py532lib-master/            # PN532 I2C library
├── menu/                       # Bash Menu files
├── documentation/              # Hardware documentation files
└── config/                     # Config files
    ├── rfid-door-lock.json     # Configuration and user database
    ├── rfid-doorlock.service   # systemd service file
    └── door-access.log         # Access log
```

## Troubleshooting

**PN532 not detected:**
- Verify I2C is enabled: `sudo i2cdetect -y 1` (should show device at address 0x24)
- Check wiring connections
- Ensure the PN532 is set to I2C mode (check DIP switches)

**LED not working:**
- Verify GPIO pin numbers match your wiring
- Check LED polarity

**Door not unlocking:**
- Test the MOSFET module with `gpio_init()` and `mosfet_on()` in Python
- Verify 12V power supply is connected
- Check solenoid wiring

**Slack bot not responding:**
- Verify both tokens are correct in the config
- Ensure the bot is invited to the channel
- Check that Socket Mode is enabled in the Slack app settings

## Notes

- The system includes legacy code for a bio lock door system (commented out)
- CPU temperature is monitored to ensure system health
- The JSON database is updated in real-time with access timestamps
