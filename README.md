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
sudo git clone https://github.com/aspittles/rfid.git -b slack-open /opt/rfid-door-lock
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

6. Update /opt/rfid-door-lock/rfid-door-lock.json with 'xoxb-your-bot-token' & 'xapp-your-app-token'
   See 'Slack App Setup' below

7. Deploy the Service using option 5

8. Restart the Service after deploy using option 2 and watch for Flashing lights

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

## Slack App Setup

## Slack App Setup

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**

2. **Enable Socket Mode** (Settings → Socket Mode → Enable)
   - Generate an app-level token with `connections:write` scope
   - Copy the token (starts with `xapp-`)

3. **Add Bot Permissions** (OAuth & Permissions → Bot Token Scopes):
   - `channels:history`
   - `groups:history` (for private channels)

4. **Subscribe to Events** (Event Subscriptions → Enable → Subscribe to bot events):
   - `channels:history` - Read messages in public channels
   - `groups:history` - Read messages in private channels
   - `chat:write` - Send messages

5. **Install App** to workspace and copy the Bot Token (starts with `xoxb-`)

6. **Invite the bot** to your private channel: `/invite @YourBotName`






### 1. Create the Slack App
1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App** → **From scratch**
3. Name it "Door Opener" and select your workspace

### 2. Configure Bot Permissions
1. Go to **OAuth & Permissions** in the sidebar
2. Under **Scopes → Bot Token Scopes**, add:
   - `channels:history` - Read messages in public channels
   - `groups:history` - Read messages in private channels
   - `chat:write` - Send messages

### 3. Install the App
1. Go to **Install App** in the sidebar
2. Click **Install to Workspace**
3. Authorize the app
4. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### 4. Get Your Signing Secret
1. Go to **Basic Information** in the sidebar
2. Under **App Credentials**, copy the **Signing Secret**

### 5. Get Channel ID
1. In Slack, right-click on your private channel
2. Click **View channel details**
3. At the bottom, copy the **Channel ID** (starts with `C`)

### 6. Invite the Bot
1. In your private channel, type `/invite @Door Opener`


## Notes

- The system includes legacy code for a bio lock door system (commented out)
- CPU temperature is monitored to ensure system health
- The JSON database is updated in real-time with access timestamps
