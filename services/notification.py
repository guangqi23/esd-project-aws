import requests
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from urllib.request import urlopen
# import time

import amqp_setup

app = Flask(__name__)
CORS(app)

#============= AMQP ==============#

# monitorBindingKey should be == to routing_key when creating the queue
monitorBindingKey='*.info'

def receiveChosenNoti():
    amqp_setup.check_setup()

    queue_name = 'chosen_noti'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

# IDK what this function does
def callback(channel, method, properties, body): # required signature for the callback; no return

    # send_api_url = "https://d7sms.p.rapidapi.com/secure/send"
    url = "https://post-paid-sms.p.rapidapi.com/SMS"
    print("\nReceived a chosen_noti by " + __file__)

    # Assuming the body is a json file after loading
    bodies = json.loads(body) 
    selected_numbers = []
    # Invoke the function below
    for body in bodies:

        product_name = body['product_name']
        phone_number = int(body['phone_number'])

        selected_numbers.append(phone_number)

        content = f"Testing for a school project {product_name}" 

        # D7
        # payload = {
        #     "content": content,
        #     "from": "Raffle Svc",
        #     "to": phone_number
        # }
        # headers = {
        #     'content-type': "application/json",
        #     'authorization': "Basic cW5jYTM5NDc6Q0x6aVZRVFg=",
        #     'x-rapidapi-key': "7406ce2570msh2cdf4c78aab3a28p12fc39jsn3be65634f33e",
        #     'x-rapidapi-host': "d7sms.p.rapidapi.com"
        # }
        # response = requests.request("POST", send_api_url, data=payload, headers=headers)

        payload = {
            "From": "Raffle Svc",
            "To": str(phone_number),
            "Message": content,
            "StatusCallbackURL": "string(URL)"
        }

        payload = json.dumps(payload)

        headers = {
            'content-type': "application/json",
            'x-rapidapi-key': "7406ce2570msh2cdf4c78aab3a28p12fc39jsn3be65634f33e",
            'x-rapidapi-host': "post-paid-sms.p.rapidapi.com"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        ### Response ###
        print(response.json())
        # Dictionary
        response = response.json() 

    print("SMS has been sent to the chosen rafflers")
    print("The selected numbers are: ", selected_numbers)

if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveChosenNoti()