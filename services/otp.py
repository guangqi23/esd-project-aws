import requests
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from urllib.request import urlopen

app = Flask(__name__)
CORS(app)

# D7 get otp url
# get_otp_url = "https://d7-verify.p.rapidapi.com/send"

# wipple url
url = "https://wipple-sms-verify-otp.p.rapidapi.com/send"
phone_number = ""

@app.route("/get_otp", methods=["POST"])
def get_otp():
    phone_number = str(request.json.get("phone_number"))

    # wipple get otp code
    payload = {
    "app_name": "Raffle Service",
    "code_length": 6,
    "code_type": "number",
    "expiration_second": 900,
    "phone_number": phone_number
    }

    payload = json.dumps(payload)

    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': "7406ce2570msh2cdf4c78aab3a28p12fc39jsn3be65634f33e",
        'x-rapidapi-host': "wipple-sms-verify-otp.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    # D7 get otp code
    # payload = {
    #     "expiry": 900,
    #     "message": "Your otp code is {code}",
    #     "mobile": phone_number,
    #     "sender_id": "SMSInfo"
    # }

    # payload = json.dumps(payload)

    # headers = {
    #     'content-type': "application/json",
    #     'authorization': "Token a3ffd7733c08d13296e2af0c7b4a18ab724a6887",
    #     'x-rapidapi-key': "7406ce2570msh2cdf4c78aab3a28p12fc39jsn3be65634f33e",
    #     'x-rapidapi-host': "d7-verify.p.rapidapi.com"
    #     }

    # response = requests.request("POST", get_otp_url, data=payload, headers=headers)

    # print(response.json())

    # # Dictionary
    # response = response.json() 

    
    # otp_id = response['otp_id']

    return jsonify(
        {
            'code': 201,
            "message": "OTP has been sent."
        }
    )

@app.route("/verify_otp", methods=["POST"])
def verify_otp():

    # wipple verify otp code
    url = "https://wipple-sms-verify-otp.p.rapidapi.com/verify"
    
    phone_number = request.json.get("phone_number")
    otp_code = request.json.get("otp_code")

    querystring = {
        "phone_number": phone_number,
        "verification_code": otp_code,
        "app_name":"Raffle Service"
    }

    headers = {
        'x-rapidapi-key': "7406ce2570msh2cdf4c78aab3a28p12fc39jsn3be65634f33e",
        'x-rapidapi-host': "wipple-sms-verify-otp.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    print(response)

    if response['message'] == 'verification was successful':
        return jsonify(
            {
                "code": 201,
                "message": "success"
            }
        ), 201
    
    return jsonify(
        {
            "code": 201,
            "message": "failed"
        }
    )


    # print(response.text)
    # D7 verify otp code
    # verify_otp_url = "https://d7-verify.p.rapidapi.com/verify"

    # otp_id = request.json.get("otp_id")
    # otp_code = request.json.get("otp_code")

    # payload = {
    #     "otp_code": otp_code,
    #     "otp_id": otp_id
    # }

    # payload = json.dumps(payload)
    

    # headers = {
    #     'content-type': "application/json",
    #     'authorization': "Token a3ffd7733c08d13296e2af0c7b4a18ab724a6887",
    #     'x-rapidapi-key': "7406ce2570msh2cdf4c78aab3a28p12fc39jsn3be65634f33e",
    #     'x-rapidapi-host': "d7-verify.p.rapidapi.com"
    #     }

    # response = requests.request("POST", verify_otp_url, data=payload, headers=headers)

    # response = response.json() 
    # print(response)
    
    # if response['status'] == 'success':
    #     return jsonify(
    #         {
    #             "code": 201,
    #             "message": "success"
    #         }
    #     ), 201
    
    # return jsonify(
    #     {
    #         "code": 201,
    #         "message": "failed"
    #     }
    # )
if __name__ == '__main__':
    print("Flask Program " + os.path.basename(__file__) + ": managing OTP API calls")
    app.run(host='0.0.0.0', port=5010, debug=True)