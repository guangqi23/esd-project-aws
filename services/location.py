import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://is213@host.docker.internal:3306/raffle_db"
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://root:esd_a_plus_2021@raffle-db.c3e0re9oziwf.us-east-1.rds.amazonaws.com:3306/raffle_db"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/raffle_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Location(db.Model):
    __tablename__ = 'location'
    phone_number = db.Column(db.String(9), nullable=False)
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.String(9), nullable=False)
    product_id = db.Column(db.String(9), nullable=False)
    lat = db.Column(db.String(9), nullable=False)
    lng = db.Column(db.String(9), nullable=False)

    def json(self): 
        location = {
            'phone_number':self.phone_number,
            'location_id': self.location_id,
            'company_id': self.company_id,
            'product_id': self.product_id,
            'lat': self.lat,
            'lng': self.lng
        }
        return location

#====== Location =======#
#get all locations
@app.route("/location")
def get_all_locations():
    location_entries = Location.query.all()

    if len(location_entries):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "location_entries": [location_entry.json() for location_entry in location_entries]
                }
            }
        )
    return jsonify(
    {
        "code": 404,
        "message": "There are no location entries."
    }
), 404 

#get specific location based on product_id and company_id
@app.route("/location/<string:product_id>/<string:company_id>")
def get_all_locations2(product_id, company_id):
    location_entries2 = Location.query.all()
    location_entries2 = [location_entry2.json() for location_entry2 in location_entries2]
    result = []
    for location_entry2 in location_entries2:
        if location_entry2['product_id'] == product_id and location_entry2['company_id'] == company_id:
            result.append(location_entry2)
            print("hello")
    return jsonify(result)
    

# Creating a new location record into the database 

# This is assuming, the user has been verified to POST a new raffle
@app.route("/location", methods=["POST"])
def create_location():
    phone_number = request.json.get("phone_number",None)
    #location_id not required because it has autoincrement 
    # location_id = request.json.get("location_id", None)
    product_id = request.json.get("product_id", None)
    company_id = request.json.get("company_id", None)
    lat = request.json.get("lat", None)
    lng = request.json.get("lng", None)

    # Check if location_id is already present in the database
    location_entries = Location.query.all()
    location_entries = [location_entry.json() for location_entry in location_entries]
    for location_entry in location_entries:
        if phone_number in location_entry.values():
            return jsonify(
                {
                    "code": 201,
                    "data": "User already exist in the database."
                }
            ), 201

    # If it's a new user, we will carry on
    location_entry = Location(phone_number=phone_number, product_id=product_id, company_id=company_id, lat=lat, lng=lng)

    try: 
        db.session.add(location_entry)
        db.session.commit()
    except Exception as e:
        return jsonify (
            {
                "code": 500,
                "data": "An error occured while creating the order. " + str(e)
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": {
                "phone_number": phone_number,
                "product_id": product_id,
                "company_id": company_id,
                "lat":lat,
                "lng":lng
            }
        }
    ), 201


if __name__ == '__main__':
    print("Flask Program " + os.path.basename(__file__) + ": managing location microservice")
    app.run(host='0.0.0.0', port=5007, debug=True)

