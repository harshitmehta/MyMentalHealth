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
    entity_val = None
    # trait = None
    
    # yes_no = "yes_no"
    # greetings = "wit$greetings"
    
    try:
        if 'greetings:greetings' in resp['entities']:
            entity = resp['entities']['greetings:greetings'][0]['name']
            entity_val = resp['entities']['greetings:greetings'][0]['value']
        elif 'yes_no:yes_no' in resp['entities']:
            entity = resp['entities']['yes_no:yes_no'][0]['name']
            entity_val = resp['entities']['yes_no:yes_no'][0]['value']
        elif 'exit:exit' in resp['entities']:
            entity = resp['entities']['exit:exit'][0]['name']
            entity_val = resp['entities']['exit:exit'][0]['value']
        elif 'wit$number:number' in resp['entities']:
            entity = resp['entities']['wit$number:number'][0]['name']
            entity_val = resp['entities']['wit$number:number'][0]['value']
        else:
            entity = "Not Entity detected"
            entity_val = "No Entity value found"
            
        if 'name' in resp['intents'][0]:
            intent = resp['intents'][0]['name']
        else:
            intent = "No Intent detected" 
        
        
        # intent, intent_val = resp['intents'][0]['name']
        # entity, entity_val = list(resp['entities'])[0]
        # value = resp['entities'][entity][0]['body']
        # trait, trait_val = resp['traits']
        print("-------Wit Returns--------")
        print(intent)
        print(entity)
        print(entity_val)
        # print(resp['entities']['timeofday:timeofday'][0]['body'])
        #entity = list(resp['entities'])
        #for i in entity:
            #value.append(resp['entities'][i][0]['value'])
            #print(value)
    except:
        pass
    return (intent, entity, entity_val)
    # return (intent, entity, value, trait)

# resp = client.message(message_text)
# print(wit_response("give me sports news"))

def convo():
   print("this is inside convo")