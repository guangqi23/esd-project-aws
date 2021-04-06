#imports databases
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import os
import sys
#Import http client and set routific vrp url and necessary packages
from os import environ

import json
from invokes import invoke_http
import urllib3
URL   = "https://api.routific.com/v1/vrp"
#SQLAlchemy
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://is213@host.docker.internal:3306/raffle_db"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/raffle_db'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://root:esd_a_plus_2021@raffle-db.c3e0re9oziwf.us-east-1.rds.amazonaws.com:3306/raffle_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)  

location_URL = environ.get("location_url") or 'http://100.25.39.15:5000/location' 

#optimise route function
@app.route("/optimisation")
def optimise_route():
# Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            optimisation_item = request.get_json()
            
            print("\nReceived an order in JSON:", optimisation_item)
            print(type(optimisation_item))
            # do the actual work, which is optimising the route
            # 1. Send optimisation item info {"product_id":2 , "company_id":443}
            #json received from records
            result_from_process_optimisation = processOptimisation(optimisation_item)
            # print("--------RECORD---------")
            # print("from record",result_from_process_optimisation)
            results = result_from_process_optimisation['data']['location_entries']

            order_dict = {}
            for i in range(len(results)):
                temp_dict = {}
                temp_dict['name'] = "name"
                temp_dict['lat'] = results[i].get('lat')
                temp_dict['lng'] = results[i].get('lng')
                location_dict = {'location':temp_dict}
                order_dict['order_'+str(i+1)] = location_dict
            # print(order_dict)

            #tailoring dictionary to API specifications

            #fleet will be hardcoded because we assume the same place that is sent out
            fleet_json = """
            {
                "vehicle_1": {
                    "start_location": {
                        "id":"depot",
                        "name":"SMU",
                        "lat":1.29686,
                        "lng":103.852202
                    }
                }
            }
            """
            fleet = json.loads(fleet_json)
            
            #prepare data payload
            data ={
                "visits": order_dict,
                "fleet":fleet
            }
            return data

            print('\n-----ERROR-----')

            

            # Step 5: Put together request
            # This is your demo token
            token = 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MDU3OTE0ODhlYjE4MDAwMTdiM2IyZDQiLCJpYXQiOjE2MTczNTkyMDJ9.E5Evuoozroqnlwew-a-Du6R3xWvIPhRGJfYtOsO9WFM'
            http = urllib3.PoolManager()
            req = http.request('GET', URL, fields=json.dumps(data))
            req.add_header('Content-Type', 'application/json')
            req.add_header('Authorization', "bearer " + token)

            # Step 6: Get route
            res = urllib3.urlopen(req).read()
            print (res)


            # req = http.request('GET', URL, json.dumps(data))
            # req.add_header('Content-Type', 'application/json')
            # req.add_header('Authorization', "bearer " + token)
            
            
            # req = http.request(
            #     'GET',
            #     URL,
            #     json.dumps(data),
            #     headers={
            #         'Content-Type' : 'application/json',
            #         'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI1MzEzZDZiYTNiMDBkMzA4MDA2ZTliOGEiLCJpYXQiOjEzOTM4MDkwODJ9.PR5qTHsqPogeIIe0NyH2oheaGR-SJXDsxPTcUQNq90E'
            #     })
        #    res = urllib3.urlopen(req).read()
        #     print(res)


            

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "optimise_route.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processOptimisation(order):
    # 2.  Send optimisation item info {"product_id":2 , "company_id":443} to records
    #Invoke records microservice

    # print('\n-----Invoking records microservice-----')
    print('\n-----INPUT-----')

    order_result = invoke_http(location_URL, method='GET', json=order)


    # Check the order result; if a failure, send it to the error microservice.
    code = order_result["code"]

    message = json.dumps(order_result)
    # print(type(order_result))

    
    return order_result



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)