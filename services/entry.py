from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from invokes import invoke_http
from os import environ

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://is213@host.docker.internal:3306/raffle_db"
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://root:esd_a_plus_2021@raffle-db.c3e0re9oziwf.us-east-1.rds.amazonaws.com:3306/raffle_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

record_URL = environ.get('record_URL')  or 'http://raffleoak.tech:5000/record' 
# deduct_URL = "http://localhost:5000/deduct_product/"
location_URL = environ.get('location_URL')  or 'http://raffleoak.tech:5007/location' 

@app.route("/place_raffle", methods=["POST"])
def place_raffle():
    if request.is_json:
        try:
            # Dictionary
            entry = request.get_json() 

            raffle_entry = {
                "phone_number": entry['phone_number'],
                "company_id": entry["company_id"],
                "product_id": entry['product_id']
            }


            location_entry = {
                "phone_number": entry['phone_number'],
                "company_id": entry["company_id"],
                "product_id": entry['product_id'],
                "lat": entry['lat'],
                "lng": entry['lng']
            }

            print("\n Received an raffle entry in JSON:", raffle_entry)

            print("\n Received an location entry in JSON:", location_entry)


            result = processRaffle(raffle_entry, location_entry)

            return jsonify(result)
        
        except Exception as e:
            pass 
        
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processRaffle(raffle_entry, location_entry):
    # 1. Invoke record microservice
    print("\n ===== Invoking Record Microservice =====")
    raffle_result = invoke_http(record_URL, method="POST", json=raffle_entry)
    location_result = invoke_http(location_URL, method="POST", json=location_entry)

    print("Raffle Entry Result:", raffle_result)
    print("Location Entry Result:", location_result)

    raffle_code = raffle_result["code"]
    location_code = location_result["code"]


    if raffle_code not in range(200, 300):
        # We will have to invoke an error microservice here
        # But for now we will ignore this first.
        return {
            "code": 500,
            "data": {"raffle_result": raffle_result},
            "message": "Raffle creation failed due to server error."
        }
    
    if location_code not in range(200, 300):
    # We will have to invoke an error microservice here
    # But for now we will ignore this first.
        return {
            "code": 500,
            "data": {"location_result": location_result},
            "message": "Location creation failed due to server error."
        }
    

    return {
        "code": raffle_result['code'],
        "raffle_result": raffle_result['data'],
        "message": "success"
    }

if __name__ == '__main__':
    print("Flask Program " + os.path.basename(__file__) + ": managing Entry Complex Microservice")
    app.run(host='0.0.0.0', port=5002, debug=True)

