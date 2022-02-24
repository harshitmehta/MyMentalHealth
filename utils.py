from wit import Wit

access_token = "ORT6OK2G7SPKVVMB35Z3N3WE6FGIB64K"

client = Wit(access_token = access_token)

# message_text = "good evening"
# resp = client.message(message_text)
# print(resp)

def wit_response(message_text):
    resp = client.message(message_text)
    print("Inside Wit")
    print(resp)
    print("*"*20)
    intent = None
    entity = None
    value = None
    trait = None
    
    try:
        intent = resp['intents'][0]['name']
        entity = list(resp['entities'])[0]
        value = resp['entities'][entity][0]['body']
        trait = resp['traits']
        print("-------Wit Returns--------")
        print(intent)
        print(entity)
        print(value)
        print(trait)
        # print(resp['entities']['timeofday:timeofday'][0]['body'])
        #entity = list(resp['entities'])
        #for i in entity:
            #value.append(resp['entities'][i][0]['value'])
            #print(value)
    except:
        pass
    return (intent, entity, value, trait)

# resp = client.message(message_text)
# print(wit_response("give me sports news"))

def convo():
   print("this is inside convo")