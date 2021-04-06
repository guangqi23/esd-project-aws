import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://is213@host.docker.internal:3306/raffle_db"
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/raffle_db'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://root:esd_a_plus_2021@raffle-db.c3e0re9oziwf.us-east-1.rds.amazonaws.com:3306/raffle_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Company(db.Model):
    __tablename__ = 'company'

    company_id = db.Column(db.String(9), primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)

    # If not it will just be Company1, Company2... in object form
    def json(self):
        company_info = {
            'company_id': self.company_id,
            'company_name': self.company_name
        }

        return company_info

class Raffle_Company(db.Model):
    __tablename__ = 'raffle_company'

    raffle_id = db.Column(db.String(9), primary_key=True)
    product_id = db.Column(db.String(9), nullable=False)
    company_id = db.Column(db.String(9), primary_key=True)
    product_desc = db.Column(db.String(255), nullable=False)
    no_of_products = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)

    def json(self):
        raffle_company_info = {
            'raffle_id': self.raffle_id,
            'product_id': self.product_id,
            'company_id': self.company_id,
            'product_desc': self.product_desc,
            'no_of_products': self.no_of_products,
            'amount': self.amount,
            'product_name': self.product_name
        }
        return raffle_company_info

class Raffle_Entry(db.Model):
    __tablename__ = 'raffle_entry'

    raffle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_number = db.Column(db.String(10), primary_key=True)   
    company_id = db.Column(db.String(9), nullable=False)
    product_id = db.Column(db.String(9), nullable=False)

    def json(self):
        raffle_entry = {
            'phone_number': self.phone_number,
            'raffle_id': self.raffle_id,
            'company_id': self.company_id,
            'product_id': self.product_id
        }
        return raffle_entry



#====== Company =======#
@app.route("/company")
def get_all_companies():
    companies = Company.query.all()
    if len(companies):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "companies": [company.json() for company in companies]
                }
            }
        )
    return jsonify(
    {
        "code": 404,
        "message": "There are no companies."
    }
), 404

#====== Raffle Company =======#
@app.route("/raffle_company")
def get_all_raffle_companies():
    raffle_companies = Raffle_Company.query.all()
    if len(raffle_companies):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "raffle_companies": [raffle_company.json() for raffle_company in raffle_companies]
                }
            }
        )
    return jsonify(
    {
        "code": 404,
        "message": "There are no raffle companies."
    }
), 404

@app.route("/deduct_product/<string:product_id>")
def deduct_product(product_id):

    raffle_company = Raffle_Company.query.filter_by(product_id=product_id).first()
    raffle_company.no_of_products -= 1

    db.session.commit()

    return jsonify(
        {
            "code": 200,
            "data": "Item count successfully deducted!"
        }
    )


#====== Raffle Entry =======#
@app.route("/raffle_entry")
def get_all_raffle_entries():
    raffle_entries = Raffle_Entry.query.all()
    if len(raffle_entries):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "raffle_entries": [raffle_entry.json() for raffle_entry in raffle_entries]
                }
            }
        )
    return jsonify(
    {
        "code": 404,
        "message": "There are no raffle entries."
    }
), 404

@app.route("/raffle_entry/<string:product_id>/<string:company_id>")
def get_raffles_by_product_company(product_id, company_id):
    selected_raffle = []
    raffle_entries = Raffle_Entry.query.all()
    raffle_entries = [raffle_entry.json() for raffle_entry in raffle_entries]

    for raffle_entry in raffle_entries:
        if str(raffle_entry['product_id']) == product_id and raffle_entry['company_id'] == company_id:
            selected_raffle.append(raffle_entry)
    
    #================AMQP===================#
    # Added this | to return code "200"/"404"
    # If there is at least 1 raffler
    if len(selected_raffle):
        return jsonify(
            {
                "code": 200,
                "data": selected_raffle
            }
        )
    # if there are no rafflers for the selected raffle
    return jsonify(
    {
        "code": 404,
        "message": "There are no rafflers in the selected_raffler entries."
    }
), 404

    #=============Excluded this==============#
    # return jsonify(selected_raffle)



# Creating a new raffle record into the database 
# This is assuming, the user has been verified to POST a new raffle
@app.route("/record", methods=["POST"])
def create_raffle():

    # raffle_id = request.json.get("raffle_id", None)
    phone_number = request.json.get("phone_number", None)
    product_id = request.json.get("product_id", None)
    company_id = request.json.get("company_id", None)

    # Check if phone_number already exists in the db
    raffle_entries = Raffle_Entry.query.all()
    raffle_entries = [raffle_entry.json() for raffle_entry in raffle_entries]


    # By right, the high-level workflow... Verification microservices checks this.
    # for raffle_entry in raffle_entries:
    #     if phone_number in raffle_entry.values():
    #         return jsonify( 
    #             {
    #                 "code": 201,
    #                 "data": "User already exists in the database."
    #             }
    #         ), 201

    # If it's a new user, we will carry on
    raffle_entry = Raffle_Entry(phone_number=phone_number, product_id=product_id, company_id=company_id)

    try: 
        db.session.add(raffle_entry)
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
            # "data": "raffle_entry.json()"
            "data": {
                "product_id": product_id,
                "phone_number": phone_number,
                "company_id": company_id
            }
        }
    ), 201


if __name__ == '__main__':
    print("Flask Program " + os.path.basename(__file__) + ": managing Record Microservice")
    app.run(host='0.0.0.0', port=5000, debug=True)

