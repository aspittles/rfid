#!/usr/bin/env python3

import json
import os
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Load config
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
with open(config_path) as f:
    config = json.load(f)

app = App(token=config["SLACK_BOT_TOKEN"])

@app.message(re.compile(r"^open$", re.IGNORECASE))
def handle_open(message, say, client):
    user_info = client.users_info(user=message["user"])
    name = user_info["user"]["real_name"]
    print(name)
    say("Station Door Opened")

@app.message(re.compile(r".*"))
def handle_unknown(message, say):
    say("I don't understand, please say 'open' to open the station door")

@app.event("message")
def handle_message_events(body, logger):
    pass

if __name__ == "__main__":
    handler = SocketModeHandler(app, config["SLACK_APP_TOKEN"])
    handler.connect()
    print("Listening for messages... Press Enter to exit.")
    input()
    handler.close()
