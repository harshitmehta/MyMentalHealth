# -*- coding: utf-8 -*-
"""
@author: HARSHIT
"""

import os, sys
from flask import Flask, request
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAHKjO47FbUBAFuUAr3jhifpZAVfKM0srqjHRhPKRAhtMhvahCfdBe2Aav68jQFLrQJM9GmzLmPCvhPk2M0kwPNWr4eqrwG5DhbZCcruF7vbGhJtkfMTZA7w5hN5fU6ypqmMFEKijNclYjfiWk6uY4G8iv5mk2FJIfKsEKkiJfNq13MNp7T1eZBlfgOfvZBvaJHZBFKYCUZBQZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    # Webhook Verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"],200
    return "Hello World from mentalhealthbot",200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)
    messaging_text = None
    if data['object']=='page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                
                # Sender and Recipient IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                #If message is a text or not
                if messaging_event.get('message'):
                    if 'text' in messaging_event['message'] and 'is_echo' not in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'
                
                #Echo bot
                response = messaging_text
                bot.send_text_message(sender_id, response)
                
    return "ok", 200

def log(message):
    print(message)
    sys.stdout.flush()    


if __name__ == "__main__":
    #app.run(debug = True, port = 7667)
    app.run(debug = True)
