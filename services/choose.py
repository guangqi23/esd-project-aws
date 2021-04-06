from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests
from invokes import invoke_http
import random
import json
import amqp_setup
import pika
import requests
from os import environ


app = Flask(__name__) 

CORS(app)

product_URL = environ.get('product_URL')  or 'http://52.45.19.10:5000/raffle_company' 
transaction_URL = environ.get('transaction_URL') or 'http://52.45.19.10:5006/add_transactions'



@app.route("/choose_rafflers", methods=['POST'])
def choose_rafflers():

    product_id = request.json.get("product_id", None)
    company_id = request.json.get("company_id", None)
    
    record_URL = "http://record:5000/raffle_entry" + "/" + product_id + "/" + company_id 

    print("Record URL is at:", record_URL)

    # Getting Raffle Entries
    raffle_entries = invoke_http(record_URL)

    print(f"These are the raffle entries for the {product_id}: ")
    print(raffle_entries)

    # retrieve code from raffle_entries?
    code = raffle_entries["code"]
    
    # If there are no rafflers for the selected raffle, send message to 'error' queue
    if code not in range(200, 300):
        message = "There are no rafflers for the Raffle that you selected"

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="chosen.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

    # If there are rafflers for the selected raffle, send message to 'chosen_noti' queue
    else:
        raffle_entries = raffle_entries['data']
        original_raffle_ids = [raffle_entry['raffle_id'] for raffle_entry in raffle_entries]
        selected_raffle_ids = []
        selected_raffles = []
        amount_of_entries = len(raffle_entries)

        # counter = 0
        # # The 3 refers to only selecting 3 from the raffle with that particular product_id.
        # while counter < 2:
        #     index = random.randint(1, amount_of_entries-1)
            
        #     if original_raffle_ids[index] not in selected_raffle_ids:
        #         selected_raffle_ids.append(original_raffle_ids[index])
        #         counter += 1

        num_to_select = 3
        # change num_to_select if num of rafflers is less than num_to_select
        if len(original_raffle_ids) < num_to_select:
            num_to_select = len(original_raffle_ids)

        selected_raffle_ids = random.sample(original_raffle_ids, num_to_select)
        print("Selected Rafflers: ", selected_raffles)
        print("These are the selected raffle_ids:", selected_raffle_ids)

        for raffle_entry in raffle_entries:
            if raffle_entry['raffle_id'] in selected_raffle_ids:
                selected_raffles.append(raffle_entry)
        
        # Getting Product Description
        product_info = invoke_http(product_URL)
        product_info = product_info['data']['raffle_companies']

        # Merging both Inputs based on 'product_id'
        merged = []
        for raffle in selected_raffles:
            item = {}
            for info in product_info:
                if raffle['product_id'] == info['product_id'] and raffle['company_id'] == info['company_id']:

                    item['company_id'] = info['company_id']
                    item['amount'] = info['amount']
                    item['product_desc'] = info['product_desc']
                    item['product_name'] = info['product_name']
                    item['product_id'] = raffle['product_id']
                    item['raffle_id'] = raffle['raffle_id']
                    item['phone_number'] = raffle['phone_number']
                    item['paid'] = 'unpaid'
                    
            transaction_result = invoke_http(transaction_URL, method="POST", json=item)
            print("Transaction invocation result: ", transaction_result)

            merged.append(item)
        
        #========AMPQ Messaging========#
        message = json.dumps(merged)

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="chosen.info", 
        body=message)

        print("\n Transaction information published to RabbitMQ Exchange")

        # return jsonify(merged)
        return jsonify(
            {
                "status":"success",
                "data": merged
            }
        )
    
if __name__ == '__main__':
    print("Flask Program " + os.path.basename(__file__) + ": managing Choose Complex Microservice")
    app.run(host='0.0.0.0', port=5011, debug=True)
