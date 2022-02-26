# -*- coding: utf-8 -*-
"""
@author: HARSHIT
"""

import os, sys
import requests
from flask import Flask, request
from pymessenger import Bot
from utils import wit_response
import pandas as pd
import numpy as np
from core import model_predict
from collections import OrderedDict
from wit import Wit
from os import path
app = Flask(__name__)

# Wit.ai parameters
WIT_TOKEN = "ORT6OK2G7SPKVVMB35Z3N3WE6FGIB64K"
# WIT_CLIENT_TOKEN = "5XI7DIJOVZ6R44YP7JBR4P3LCH6NLE7S"
# Setup Wit Client
client = Wit(access_token=WIT_TOKEN)

PAGE_ACCESS_TOKEN = "EAAHKjO47FbUBAFuUAr3jhifpZAVfKM0srqjHRhPKRAhtMhvahCfdBe2Aav68jQFLrQJM9GmzLmPCvhPk2M0kwPNWr4eqrwG5DhbZCcruF7vbGhJtkfMTZA7w5hN5fU6ypqmMFEKijNclYjfiWk6uY4G8iv5mk2FJIfKsEKkiJfNq13MNp7T1eZBlfgOfvZBvaJHZBFKYCUZBQZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)

count = 1
od = OrderedDict()
#### New Information
od[0] = "Let's do this! \nWhat is your age?"
od[1] = 'What is your gender?\n1 : Male \n2 : Female \n3 : Other'
od[2] = 'Do you have a family history of mental illness?\n0 : no \n1 : yes '
od[3] = 'If you have a mental health condition, do you feel that it interferes with your work?\n0 : never \n1 : rarely \n2 : sometimes \n3 : often'
od[4] = 'How many employees does your company or organization have?\n1 : 1-5 employees \n2 : 6-25 \n3 : 26-100 \n4 : 100-500 \n5 : 500-1000 \n6: More than 1000'
od[5] = 'Do you work remotely (outside of an office) at least 50% of the time?\n0 : no \n1 : yes '
od[6] = 'Is your employer primarily a tech company/organization?\n0 : no \n1 : yes '
od[7] = 'Does your employer provide mental health benefits?\n0 : no \n1 : yes \n2 : don\'t know'
od[8] = 'Do you know the options for mental health care your employer provides?\n0 : no \n1 : yes \n2 : not sure'
od[9] = 'Has your employer ever discussed mental health as part of an employee wellness program?\n0 : no \n1 : yes \n2 : don\'t know'
od[10] = 'Does your employer provide resources to learn more about mental health issues and how to seek help?\n0 : no \n1 : yes \n2 : don\'t know'
od[11] = 'Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources?\n0 : no \n1 : yes \n2 : don\'t know'
od[12] = 'How easy is it for you to take medical leave for a mental health condition?\n0 : very easy \n1 : somewhat easy \n2 : don\'t know \n3 : somewhat difficult \n4 : very difficult'
od[13] = 'Do you think that discussing a mental health issue with your employer would have negative consequences?\n0 : no \n1 : yes \n2 : maybe '
od[14] = 'Do you think that discussing a physical health issue with your employer would have negative consequences?\n0 : no \n1 : yes \n2 : maybe '
od[15] = 'Would you be willing to discuss a mental health issue with your coworkers?\n0 : no \n1 : yes \n2 : some of them '
od[16] = 'Would you be willing to discuss a mental health issue with your direct supervisor(s)?\n0 : no \n1 : yes \n2 : some of them '
od[17] = 'Would you bring up a mental health issue with a potential employer in an interview?\n0 : no \n1 : yes \n2 : maybe '
od[18] = 'Would you bring up a physical health issue with a potential employer in an interview?\n0 : no \n1 : yes \n2 : maybe '
od[19] = 'Do you feel that your employer takes mental health as seriously as physical health?\n0 : no \n1 : yes \n2 : don\'t know '
od[20] = 'Have you heard of or observed negative consequences for coworkers with mental health conditions in your workplace?\n0 : no \n1 : yes '
od[21] = 'Thanks! Calculating... \nSend \'9\' to see your result'

# allval = OrderedDict()
# x = 0


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
    # print("################## IN WEBHOOK ###################")
    messaging_text = None
    
    # data = request.json
    log(data)   
    
    if data['object']=='page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if 'message' in messaging_event:
                    # Sender and Recipient IDs
                    sender_id = messaging_event['sender']['id']
                    recipient_id = messaging_event['recipient']['id']
                    #If message is a text or not
                    if messaging_event.get('message'):
                        if 'text' in messaging_event['message'] and 'is_echo' not in messaging_event['message']:
                            # print("################## A new POST message received ###################")
                            messaging_text = messaging_event['message']['text']
                            # print("JSON Request Data :")
                            # print(data)
                            # print("Sender ID :")
                            # print(sender_id)
                            # print("Message Text :")
                            # print(messaging_text)
                            # print("#"*30)
                            # print("----Going beyond Webhook----")
                            response = chatbot(sender_id, messaging_text)
                            fb_message(sender_id, response)
                        else:
                            messaging_text = 'no text'
                            fb_message(sender_id, messaging_text)
                
    else:
        # Returned another event
        return 'Received Different Event'
    # return None
    return "ok", 200

def chatbot(sender_id,txt):
    global od
    counter=0
    tup = ()
    file_name = sender_id + ".csv"
    # response = "Some response received from Wit"
    intent, entity, value = wit_response(txt)
    print("INTENT, ENTITY, VALUE FROM WIT RECEIVED INTO APP----------")
    print(intent, entity, value)
    if path.exists(file_name):
        print("----SURVEY FILE EXISTS----UPDATING SURVEY FILE-----")
        rdf = pd.read_csv(file_name, sep=",")
        counter = len(rdf.columns)
        rdf[counter+1] = [value]
        rdf.to_csv(file_name, sep=",", index=False)
        print("----SURVEY FILE UPDATED----SURVEY FILE UPDATED-----")
 
    if intent == 'greetings':
        response = "Hi, Welcome to My Mental Health app!\nWe will do a small survey to predict how work related stress could be affecting your mental health.\nShall we begin?"

    elif intent == 'confirmation':
        if entity == 'yes_no' and value == 'yes':
            if path.exists(file_name):
                os.remove(file_name)
                print("----EXISTING SURVEY FILE DELETED----")
            
            df = pd.DataFrame({1: sender_id},index=[0])
            df.to_csv(file_name, sep=",", index=False)
            print("----NEW SURVEY FILE CREATED----")
            #global my_ques_series
            print("---------BEGIN SURVEY---------")
            print(0, "-----------FIRST QUESTION IN SURVEY LIST-------")
            response = od[0]
        elif entity == 'yes_no' and value == 'no':
            response = "Okay maybe next time."
        elif entity == 'exit' and value == 'exit':
            print("Exit with keyword")
            response = "See you later!!"
        else:
            response = "Unrecognized response received, start with a 'Hey' again!"
           
    
    elif entity == 'wit$number' and counter < 22:
        print(counter, "-------IN QUESTION LIST NOW-----------")
        response = od[counter]
    elif counter == 22:
        print("----SURVEY ENDED-----")
        if path.exists(file_name):
            fdf = pd.read_csv(file_name, sep=",")
            #Trial with df
            # fdf = fdf.iloc[: , 1:22]
            tup = list(fdf.itertuples(index=False, name=None))[0]
            print("-----------Check the Tuple!!----------")
            print(tup)
            L1 = list(tup)
            L1.pop(0)
            L1.pop(21)
            T1 = tuple(L1)
            arr = np.array([T1])
            ff_df = pd.DataFrame(arr)
            # ff_df = ff_df.iloc[: , 1:22]
            # ##Trial below
            # tup = np.array([[44,1,0,1,6,0,1,0,-1,0,0,0,2,0,-1,-1,-1,-1,-1,0,0]])
            # print(tup.shape)
            # df = pd.DataFrame(tup)
            print(ff_df)
            # print(T1)
            # response = "Check the Tuple!!"
            outcome = model_predict(ff_df)
            if outcome[0] == 1:
                response = "Our analysis suggests your workplace could be affecting your mental health.\nKindly seek professional help or visit\nhttps://osmihelp.org/ for more information"
            else:
                response = "You have nothing to worry about!"
        else:
            response = "Survery File Not Found!!"
    else:
        response = "Exit due to error"
     
    return response


def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }
    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + PAGE_ACCESS_TOKEN
    # Send POST request to messenger
    resp = requests.post('https://graph.facebook.com/me/messages?' + qs,
                         json=data)
    # print("-----MESSAGE POSTED FROM BOT------")
    return resp.content    
            
    
    
def log(message):
    # print(message)
    sys.stdout.flush()    


if __name__ == "__main__":
    #app.run(debug = True, port = 7667)
    app.run(debug = True)
