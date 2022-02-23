# -*- coding: utf-8 -*-
"""
@author: HARSHIT
"""

import os, sys
from flask import Flask, request
from pymessenger import Bot
from utils import wit_response
from core import predict
import pandas as pd
from collections import OrderedDict

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
                
                # #Echo bot
                # response = messaging_text
                response = chatbot(messaging_text)
                bot.send_text_message(sender_id, response)
                
    return "ok", 200

def chatbot(txt):
    global allval, od, x
    response = None
    intent, entity, value = wit_response(txt)
    print("Intent, Entity and Value from Wit----------"
    print(intent, entity, value)
    allval[x] = value
    x = x + 1
    tup = ()
   
    #if len(allval) < 24:
    if intent == 'greetings':
          response = "Hi, Welcome to My Mental Health app! We will do a small survey to predict how work related stress could be affecting your mental health. Shall we begin?"
          #global count
          #print(count, allval[count])
    elif entity == 'yes_no':
          if value == 'yes':
            print(0, "First in Question list")
            response = od[0]
          else:
            response = "Okay maybe next time."
           
    elif entity == 'number' and len(allval) < 24:
          #value > -1 and value < 100:
          global count
          print(count, " in Question list")
          response = od[count]
          count = count + 1
          print(allval)
    elif len(allval) == 24:
          print("reached the end!")
          allval.pop(0)
          allval.pop(1)
          for key, value in allval.items():
            tup = tup + (value,)
          outcome = predict(tup)
          response = "The outcome is {}".format(str(outcome))
       
    return response
    #else:


def log(message):
    print(message)
    sys.stdout.flush()    


if __name__ == "__main__":
    #app.run(debug = True, port = 7667)
    app.run(debug = True)
