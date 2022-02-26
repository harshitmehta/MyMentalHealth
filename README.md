# MyMentalHealth
Mental Health Bot for Facebook Messenger - A survey bot for Machine Learning predictions

Data used for machine learning model -  Open Sourcing Mental Illness [https://osmihelp.org/]

# Description: 
A survey chatbot to collect user information using Facebook messenger and return predictions back to user.

# Technologies:
•	Python – Flask, Pandas, Numpy, Sklearn, Requests, joblib, etc\
•	Git\
•	Gunicorn\
•	Heroku\
•	Ngrok\
•	Wit.ai\
•	Facebook Page and Messenger\


# Steps:
## 1.	Create a Facebook page and link it to an app
  a.	Create a new Facebook page\
  b.	Use Facebook developer’s portal to create a new app\
  c.	Link app with Facebook page\
  d.	Generate Page Access Token\

## 2.	Setting up the project
  a.	Create python virtual environment\
  b.	Install Flask, Requests and pymessenger, pandas, numpy in your virtual environment\
  c.	Create a python file containing the app – app.py\

## 3.	Setting up webhook
  a.	In the app.py file create a webhook – refer to Facebook documentation\
      Use the verification token you created in your Facebook app \
      (This is different from Page Access Token) \
```
      @app.route('/', methods=['GET'])
      def verify()
      if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
          if not request.args.get("hub.verify_token") == <your-token-here>:
              return "Verification token mismatch", 403
          return request.args["hub.challenge"],200
      return "Hello World",200
```
  b.	Download and install ngrok – to tunnel from localhost to web url\
  c.	Run flask app on Port 80\
  d.	 Setup Facebook app webhook callback url to ngrok url\

## 4.	Receiving Messages
  a.	Create a method in app.py to receive http post requests\
```
      @app.route('/', methods=['POST'])
      def webhook():
          data = request.get_json()
          log(data)
      return “ok”, 200
```
  b.	Send message using Messenger chat on your Facebook page\
  c.	View received message in json format – in the Flask app logs\

## 5.	Sending Messages
  a.	Parse json data to decode the received message and extract the message text of interest\
```
      if data['object']=='page':
          for entry in data['entry']:
              for messaging_event in entry['messaging']:
                  if 'message' in messaging_event:
                      sender_id = messaging_event['sender’][‘id’]
                      if messaging_event.get('message'):
                          if 'text' in messaging_event['message'] and 'is_echo' not in messaging_event['message']:
                              messaging_text = messaging_event['message']['text']
                          else:
                              messaging_text = 'no text'
```
  b.	Create another method for returning a response back to Facebook\
```
      def fb_message(sender_id, text):
          data = {
          'recipient': {'id': sender_id},
          'message': {'text': text}
          }
          # Setup the query string with your PAGE TOKEN
          qs = 'access_token=' + <Facebook_PAGE_ACCESS_TOKEN>
          # Send POST request to messenger
          resp = requests.post('https://graph.facebook.com/me/messages?' + qs,
                         json=data)
          return resp.content  
```
  c.	Call the Facebook message function to send your response using Sender ID and Text \
  d.	Verify the sent messages in Facebook page Messenger chat\

## 6.	Heroku Setup
  a.	Download and install Heroku-CLI, Git-CLI and gunicorn in your virtual environment\
  b.	Create a requirements .txt file for the app\
      You can use a pip command like:  \
```
      pip freeze > requirements.txt
```
  c.	Create a Procfile for gunicorn\
      This file instructs gunicorn where your app is\
```
      web: gunicorn app:app
```
  d.	Initialize a git repository in your app directory\
```
      git init
      git status
```
  e.	Use .gitignore to exclude system or virtual environment specific files\
  f.	Add the app files to git repo\
```
      git add .
      git commit -m “comment” 
```
  g.	Create a Heroku app and note app name and URL\
```
      heroku create
```
## 7.	Heroku Deployment
  a.	Push local git repository to Heroku app\
```
      heroku git:remote -a <your_heroku_app_name>
      git push heroku master
```
  b.	Logon to Heroku from your browser to view the deployed app\
  c.	Open app from Heroku to view the app in your browser\
  d.	Use the new app URL provided by Heroku to update the callback URL in Facebook app\
  e.	Test the app again – using heroku logs to verify \

## 8.	Wit.ai Integration
  a.	Install Wit.ai python client in your project environment – update requirements.txt\
  b.	Create an account on Wit.ai\
  c.	Create an app on Wit.ai\
  d.	Create a new python file to interact with Wit\
      Refer to Wit.ai documentation\
```
      from wit import Wit
      access_token = "<YOUR_WIT_ACCESS_TOKEN>"
      client = Wit(access_token = access_token)
      message_text = "good evening"
      resp = client.message(message_text)
      print(resp)
```
## 9.	Wit.ai Training – NLP
  a.	Train Wit.ai app with utterances to identify entities, traits, and intents in texts\
  b.	Pass the Facebook chat text you receive to Wit.ai using the wit python file created above\
```
      message_text = <your-text-message-here>
      resp = client.message(message_text)
```
  c.	Parse Wit.ai json response to extract entity, traits, and intents from the text\
  d.	Analyze text to prepare appropriate responses\
```
      if 'greetings' in resp['entities']:
          entity = ‘greetings’

      if entity == 'greetings':
          response = "Hi, Welcome to my app!"
```
  e.	Send back your response using the send message function\
  f.	Write logic to handle expected inputs and responses based on Wit.ai training\

## 10.	Train Machine Learning Model and save model weights
  a.	Create a new python file to train your machine learning model of choice\
      Use a model that relates to your app idea and collect inputs from user to predict use the model\
  b.	Install joblib in your project repository to save pre-trained models for quick predictions\
  c.	Generate a joblib file in your train function to store model weights\
```
      model.fit(x,y)
      # save model weights in a joblib file
      joblib.dump(model, "./pre_trained_model.joblib")
```
  d.	Use a predict a function to read pre-trained model and make predictions\
```
      loaded_model = joblib.load("./pre_trained_model.joblib")
      prediction = loaded_model.predict(user_data)
      return prediction
```
## 11.	Manage sender session
  a.	Manage sender session using sender ID and csv files containing collected survey data\
```
      if sender_id_file exists:
          #read file and append new information
```
  b.	Use file length to determine user input information and context of conversation\
  c.	Continue to send and receive responses based on your prediction requirements\
  d.	Utilize Wit.ai to analyze responses and send follow-up questions\
  e.	End user conversation when all responses are received\
  f.	Set specific key words or phrases in Wit.ai to start and end sessions\

## 12.	Predict based on user input
  a.	Use collected survey responses to predict based on pre-trained model\
  b.	Send predicted responses back to user\
