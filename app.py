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

count = 1
od = OrderedDict()
od[0] = 'What is your age?'
od[1] = 'What is your gender? 1 : Male 0 : Transgender -1 : Female'
od[2] = 'Do you have a family history of mental illness? 1 : yes 0 : no'
od[3] = 'If you have a mental health condition, do you feel that it interferes with your work? 0 : never 1 : rarely 2 : sometimes 3 : often'
od[4] = 'How many employees does your company or organization have? 1 : 1-5 2 : 6-25 3 : 26-100 4 : 100-500 5 : 500-1000 6: More than 1000'
od[5] = 'Do you work remotely (outside of an office) at least 50% of the time? 1 : yes 0 : no'
od[6] = 'Is your employer primarily a tech company/organization? 1 : yes 0 : no'
od[7] = 'Does your employer provide mental health benefits? 1 : yes 0 : don\'t know -1 : no'
od[8] = 'Do you know the options for mental health care your employer provides? 1 : yes 0 : not sure -1 : no'
od[9] = 'Has your employer ever discussed mental health as part of an employee wellness program? 1 : yes 0 : don\'t know -1 : no'
od[10] = 'Does your employer provide resources to learn more about mental health issues and how to seek help? 1 : yes 0 : don\'t know -1 : no'
od[11] = 'Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources? 1 : yes 0 : don\'t know -1 : no'
od[12] = 'How easy is it for you to take medical leave for a mental health condition? 0 : very easy 1 : somewhat easy 2 : don\'t know 3 : somewhat difficult 4 : very difficult'
od[13] = 'Do you think that discussing a mental health issue with your employer would have negative consequences? 1 : yes 0 : maybe -1 : no'
od[14] = 'Do you think that discussing a physical health issue with your employer would have negative consequences? 1 : yes 0 : maybe -1 : no'
od[15] = 'Would you be willing to discuss a mental health issue with your coworkers? 1 : yes 0 : some of them -1 : no'
od[16] = 'Would you be willing to discuss a mental health issue with your direct supervisor(s)? 1 : yes 0 : some of them -1 : no'
od[17] = 'Would you bring up a mental health issue with a potential employer in an interview?1 : yes 0 : maybe -1 : no'
od[18] = 'Would you bring up a physical health issue with a potential employer in an interview? 1 : yes 0 : maybe -1 : no'
od[19] = 'Do you feel that your employer takes mental health as seriously as physical health? 1 : yes 0 : don\'t know -1 : no'
od[20] = 'Have you heard of or observed negative consequences for coworkers with mental health conditions in your workplace? 1 : yes 0 : no'
od[21] = 'Thanks! Calculating...'
allval = OrderedDict()
x = 0


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
          # outcome = predict(tup)
          # response = "The outcome is {}".format(str(outcome))
       
    return response
    #else:


def log(message):
    print(message)
    sys.stdout.flush()    


if __name__ == "__main__":
    #app.run(debug = True, port = 7667)
    app.run(debug = True)
