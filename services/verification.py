import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from invokes import invoke_http
from os import environ

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://is213@host.docker.internal:3306/raffle_db"
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://root:esd_a_plus_2021@raffle-db.c3e0re9oziwf.us-east-1.rds.amazonaws.com:3306/raffle_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

record_URL = environ.get('record_URL') or 'http://100.25.39.15:5000/raffle_entry' 
entry_URL = environ.get('entry_URL')  or 'http://100.25.39.15:5002/place_raffle' 

@app.route("/verification", methods=['POST'])
def verify():
    # Get this from the POST request via d7-axios.html
    phone_number = request.json.get("phone_number", None)

    phone_number = str(phone_number)
    company_id = request.json.get("company_id", None)
    product_id = request.json.get("product_id", None)


    raffle_entries = invoke_http(record_URL)
    raffle_entries = raffle_entries['data']['raffle_entries']

    # Product ID, Company is not set up in front end yet (Suppose to use SESSION storage)
    for raffle_entry in raffle_entries:
        if phone_number == raffle_entry['phone_number'] and company_id == raffle_entry['company_id'] and product_id == raffle_entry['product_id']:
            return jsonify(
                {
                    "code": 201,
                    "status": "failed",
                    "message": "User already raffled for this. He/she is in the database."
                }
            ), 201 
    
    # If it is a new entry, we will carry on, we will invoke entry.py
    # raffle_entry = {
    #     # The raffle_id is hardcoded here, by right, should set_it autoincrement.
    #     # "raffle_id": 12,
    #     "phone_number": phone_number,
    #     "product_id": product_id,
    #     "company_id": company_id
    # }


    # print("\n ===== Invoking Entry Complex Microservice =====")
    # raffle_result = invoke_http(entry_URL, method="POST", json=raffle_entry)
    # print("Post-invocation of Entry Service's Result:", raffle_result)


    # code = raffle_result["code"]

    # if code not in range(200, 300):
    #     # We will have to invoke an error microservice here
    #     # But for now we will ignore this first.
    #     return {
    #         "code": 500,
    #         "data": {"raffle_result": raffle_result},
    #         "message": "Raffle creation failed due to server error."
    #     }
        
    return {
        # "code": raffle_result['code'],
        # "raffle_result": raffle_result,
        "status": "success"
    }

if __name__ == '__main__':
    print("Flask Program " + os.path.basename(__file__) + ": managing Verification Complex Microservice")
    app.run(host='0.0.0.0', port=5100, debug=True)








