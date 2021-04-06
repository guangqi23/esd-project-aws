import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
import bcrypt
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://is213@host.docker.internal:3306/raffle_db"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/raffle_db'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://root:esd_a_plus_2021@raffle-db.c3e0re9oziwf.us-east-1.rds.amazonaws.com:3306/raffle_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Client(db.Model):
    __tablename__ = 'clients'

    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

    def json(self):
        client_info = {
            "username": self.username,
            "password": self.password,
            "phone_number": self.phone_number
        }

        return client_info


# ===== Authetication Process for Clients ==== #
@app.route("/authenticate", methods=["GET", "POST"])
def authenticate_user():

    # https://zetcode.com/python/bcrypt/
    username = request.json.get("username", None)
    password = request.json.get("password")
    hashed = bytes(password, 'utf-8')
    
    # Should settle the password hashing process here
    clients = Client.query.all() 
    clients = [client.json() for client in clients]

    for client in clients:
        if username in client.values():
            client = list(client.values())

            db_password = bytes(client[1], 'utf-8')

            if bcrypt.checkpw(hashed, db_password):
                return jsonify(
                    {
                        "code": 201,
                        "message": "Login successful!",
                        "status": "success",
                        "company_id": "443"
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 201,
                        "message": "Login failed! Password is incorrect.",
                        "status": "failed"
                    }
                )

    return jsonify(
            {
                "code": 201,
                "message": "User authentication failed. User don't exist!",
                "status": "failed"
            }
        )

# ===== Create new users ===== #
@app.route("/register", methods=["POST"])
def register_user():

    clients = Client.query.all() 
    clients = [client.json() for client in clients]

    salt = bcrypt.gensalt()

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    phone_number = request.json.get("phone_number", None)

    for client in clients:
        if client['username'] == username:
            return jsonify(
                {
                    "code": 500,
                    "status": "failed",
                    "data": "User already exists. Please check with your company"
                }
            )

    byte_pw = bytes(password, 'utf-8')

    # Creates the Hash password
    hashed_pw = bcrypt.hashpw(byte_pw, salt)

    # Becomes a string to commit into the DB
    password = hashed_pw.decode('UTF-8')

    client = Client(username=username, phone_number=phone_number, password=password)

    try:
        db.session.add(client)
        db.session.commit()
    except Exception as e:
        return jsonify (
            {
                "code": 500,
                "data": "An error occured while creating the order. " + str(e),
                "status": "failed"
            }
        ), 500
    return jsonify( 
        {
            "code": 201,
            "data": client.json(),
            "status": "success",
            "company_id": "443"
        }
    ), 201

# # ===== Update Phone Number ===== #
# @app.route("/user/<string:username>", methods=["PUT"])
# def update_phone_number(username):

#     customer = Customers.query.filter_by(username=username).first() 


#     if customer:
#         customers = Customers.query.all() 
#         customers = [customer.json() for customer in customers]

#         raffle_entries = Raffle_Entry.query.all()

#         raffle_entries = [raffle_entry.json() for raffle_entry in raffle_entries]

#         data = request.get_json() 

#     # If number already exist, we don't allow user to change. (Probably need to ask Kennee how to link his OTP here)
#         if data['phone_number']:
#             for user in customers:
#                 if data['phone_number'] == user['phone_number']:
#                     return jsonify(
#                         {
#                             "code": 200,
#                             "message": "This phone number has already been registered."
#                         }
#                     )
#             for raffle_entry in raffle_entries:
#                 current_phone_number = raffle_entry.current_phone_number
                
#                 if current_phone_number == customer.phone_number:
#                     raffle_entry.phone_number = data['phone_number']
            
#             customer.phone_number = data['phone_number']

#         db.session.commit()

#         return jsonify(
#             {
#                 "code": 200,
#                 "data": customer.json()
#             }
#         ) 

#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "username": username
#             }, 
#             "message": "User not found."
#         }
#     ), 404

if __name__ == '__main__':
    print("Flask Program " + os.path.basename(__file__) + ": managing Authetication Microservice")
    app.run(host='0.0.0.0', port=5004, debug=True)

