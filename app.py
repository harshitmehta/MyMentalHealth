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

od[0] = "Let's do this!\n  What is your age?"
od[1] = 'What is your gender?\n 1 : Male 0 : Transgender -1 : Female'
od[2] = 'Do you have a family history of mental illness?\n 1 : yes 0 : no'
od[3] = 'If you have a mental health condition, do you feel that it interferes with your work?\n 0 : never 1 : rarely 2 : sometimes 3 : often'
od[4] = 'How many employees does your company or organization have?\n 1 : 1-5 2 : 6-25 3 : 26-100 4 : 100-500 5 : 500-1000 6: More than 1000'
od[5] = 'Do you work remotely (outside of an office) at least 50% of the time?\n 1 : yes 0 : no'
od[6] = 'Is your employer primarily a tech company/organization?\n 1 : yes 0 : no'
od[7] = 'Does your employer provide mental health benefits?\n 1 : yes 0 : don\'t know -1 : no'
od[8] = 'Do you know the options for mental health care your employer provides?\n 1 : yes 0 : not sure -1 : no'
od[9] = 'Has your employer ever discussed mental health as part of an employee wellness program?\n 1 : yes 0 : don\'t know -1 : no'
od[10] = 'Does your employer provide resources to learn more about mental health issues and how to seek help?\n 1 : yes 0 : don\'t know -1 : no'
od[11] = 'Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources?\n 1 : yes 0 : don\'t know -1 : no'
od[12] = 'How easy is it for you to take medical leave for a mental health condition?\n 0 : very easy 1 : somewhat easy 2 : don\'t know 3 : somewhat difficult 4 : very difficult'
od[13] = 'Do you think that discussing a mental health issue with your employer would have negative consequences?\n 1 : yes 0 : maybe -1 : no'
od[14] = 'Do you think that discussing a physical health issue with your employer would have negative consequences?\n 1 : yes 0 : maybe -1 : no'
od[15] = 'Would you be willing to discuss a mental health issue with your coworkers?\n 1 : yes 0 : some of them -1 : no'
od[16] = 'Would you be willing to discuss a mental health issue with your direct supervisor(s)?\n 1 : yes 0 : some of them -1 : no'
od[17] = 'Would you bring up a mental health issue with a potential employer in an interview?\n1 : yes 0 : maybe -1 : no'
od[18] = 'Would you bring up a physical health issue with a potential employer in an interview?\n1 : yes 0 : maybe -1 : no'
od[19] = 'Do you feel that your employer takes mental health as seriously as physical health?\n1 : yes 0 : don\'t know -1 : no'
od[20] = 'Have you heard of or observed negative consequences for coworkers with mental health conditions in your workplace?\n1 : yes 0 : no'
od[21] = 'Thanks! Calculating... Send 9 to see your result'

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
    # print("################## IN WEBHOOK ###################")
    messaging_text = None
    
    # data = request.json
    log(data)
    # if data['object'] == 'page':
    #     for entry in data['entry']:
    #         # get all the messages
    #         messages = entry['messaging']
    #         if messages[0]:
    #             # Get the first message
    #             message = messages[0]
    #             print("Message**************")
    #             print(message)
    #             # Yay! We got a new message!
    #             # We retrieve the Facebook user ID of the sender
    #             fb_id = message['sender']['id']
    #             # We retrieve the message content
    #             text = message['message']['text']
    #             print("Collected Info **************")
    #             print("Sender ID: " + "\'" + fb_id + "\'")
    #             print("Text: " + text)
    #             fb_id = ("\'" + fb_id + "\'")
    #             text = ("\'" + text + "\'")
    #             # Let's forward the message to Wit /message
    #             # and customize our response to the message in handle_message
    #             response = client.message(msg=text, context={'session_id':fb_id})
    #             handle_message(response=response, fb_id=fb_id)
     
    
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
                            print("################## A new POST message received ###################")
                            messaging_text = messaging_event['message']['text']
                            print("JSON Request Data :")
                            print(data)
                            print("Sender ID :")
                            print(sender_id)
                            print("Message Text :")
                            print(messaging_text)
                            print("#"*30)
                            print("----Going beyond Webhook----")
                            response = chatbot(sender_id, messaging_text)
                            fb_message(sender_id, response)
                        else:
                            messaging_text = 'no text'
                            fb_message(sender_id, messaging_text)
                
                    # #Echo bot
                    # response = messaging_text
                    # response = client.message(messaging_text)
                    # response = chatbot(messaging_text)
                    # bot.send_text_message(sender_id, response)
                    # print("JSON Request Data :")
                    # print(data)
                    # print("Sender ID :")
                    # print(sender_id)
                    # print("Message Text :")
                    # print(messaging_text)
                    # print("#"*30)
                    # print("(msg=" + messaging_text +","+ "context={'session_id':" + sender_id + "})")
                    # response = client.message(msg=messaging_text, context={'session_id':sender_id})
                    # print("Beyond response")
                    # response = chatbot(messaging_text)
                    # fb_message(sender_id, response)
                    # bot.send_text_message(sender_id, response)
                    # handle_message(response=response, fb_id=sender_id)
                
    else:
        # Returned another event
        return 'Received Different Event'
    # return None
    return "ok", 200

def chatbot(sender_id,txt):
    global allval, od, x
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
    
    # allval[x] = value
    # Append to CSV here
    # x = x + 1
    tup = ()
 
    if intent == 'greetings':
        response = "Hi, Welcome to My Mental Health app! We will do a small survey to predict how work related stress could be affecting your mental health. Shall we begin?"

    elif intent == 'confirmation':
        if entity == 'yes_no' and value == 'yes':
            if path.exists(file_name):
                os.remove(filename)
                print("----EXISTING SURVEY FILE DELETED----")
            
            df = pd.DataFrame({1: sender_id},index=[0])
            df.to_csv(file_name, sep=",", index=False)
            print("----NEW SURVEY FILE CREATED----")
            #global my_ques_series
            PRINT("---------BEGIN SURVEY---------")
            print(0, "-----------FIRST QUESTION IN SURVEY LIST-------")
            response = od[0]
        elif entity == 'yes_no' and value == 'no':
            response = "Okay maybe next time."
        elif entity == 'exit' and value == 'exit':
            print("Exit with keyword")
            response = "See you later!!"
        else:
            pass
           
    
    elif entity == 'wit$number' and counter < 24:
        # global count
        print(counter, "-------IN QUESTION LIST NOW-----------")
        response = od[counter]
        # print(count, " in Question list")
        # response = od[count]
        # count = count + 1
        # print(allval)
    elif counter == 21:
        print("----SURVEY ENDED-----")
        # allval.pop(0)
        # allval.pop(1)
        # for key, value in allval.items():
        #     tup = tup + (value,)
        if path.exists(file_name):
            fdf = pd.read_csv(file_name, sep=",")
            tup = list(fdf.itertuples(index=False, name=None))[0]
            print(tup)
            response = "Check the Tuple!!"
            # outcome = model_predict(tup)
            # response = "The outcome is {}".format(str(outcome))
        else:
            response = "Survery File Not Found!!"
    else:
        response = "Exit due to error"
      
    
    
    # elif intent == 'info' and start_flag == 1:
    #     if entity == 'wit$number' and value.isnumeric():
    #         if value < 10 and value > 80:
    #             response = "You are either too young or too old!!"
            
#             global count
#             print(count, " in Question list")
#             response = od[count]
#             count = count + 1
#             print(allval)
    
#     elif len(allval) == 24:
#           print("reached the end!")
#           allval.pop(0)
#           allval.pop(1)
#           for key, value in allval.items():
#             tup = tup + (value,)
#           outcome = predict(tup)
#           response = "The outcome is {}".format(str(outcome))
    
    
    # elif entity == 'number' and len(allval) < 24:
    #       #value > -1 and value < 100:
    #       global count
    #       print(count, " in Question list")
    #       response = od[count]
    #       count = count + 1
    #       print(allval)
    # elif len(allval) == 24:
    #       print("reached the end!")
    #       allval.pop(0)
    #       allval.pop(1)
    #       for key, value in allval.items():
    #         tup = tup + (value,)
          # outcome = predict(tup)
          # response = "The outcome is {}".format(str(outcome))
     
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
    print("-----MESSAGE POSTED FROM BOT------")
    return resp.content    
    
    

def handle_message(response, fb_id):
    """
    Customizes our response to the message and sends it
    """
    # Checks if user's message is a greeting
    # Otherwise we will just repeat what they sent us
    # greetings = first_trait_value(response['traits'], 'wit$greetings')
    # if greetings:
    #     text = "hello!"
    # else:
    #     text = "We've received your message: " + response['_text']
    # # send message
    # fb_message(fb_id, text)
    # print("################## IN HANDLE_MESSAGE ###################")
    # intent, entity, value = wit_response(response)
    # if intent == 'greetings':
    #     text = "Hi, Welcome to My Mental Health app! We will do a small survey to predict how work related stress could be affecting your mental health. Shall we begin?"
    # else:
    #     text = "We've received your message: " + response['_text']
    # send message
    # text = "We've received your message: " + response['text']
    # fb_message(fb_id, text)
            
    
    
def log(message):
    # print(message)
    sys.stdout.flush()    


if __name__ == "__main__":
    #app.run(debug = True, port = 7667)
    app.run(debug = True)
