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

class Transaction(db.Model):
        __tablename__ = 'transactions'

        phone_number = db.Column(db.String(10), nullable=False)
        raffle_id = db.Column(db.String(9), primary_key=True)
        amount = db.Column(db.Float, nullable=False)
        product_id = db.Column(db.String(9), nullable=False)
        company_id = db.Column(db.String(9), nullable=False)
        product_desc = db.Column(db.String(255), nullable=False)
        product_name = db.Column(db.String(255), nullable=False)
        paid = db.Column(db.String(10), nullable=False)

        def json(self):
            transaction = {
                'phone_number': self.phone_number,
                'raffle_id': self.raffle_id,
                'amount': self.amount,
                'product_id': self.product_id,
                'company_id': self.company_id,
                'product_name': self.product_name,
                'product_desc': self.product_desc,
                "paid": self.paid
            }
            return transaction


#====== Transaction =======#
@app.route("/transactions")
def get_all_transactions():
    transactions = Transaction.query.all()
    if len(transactions):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [transaction.json() for transaction in transactions]
                }
            }
        )
    return jsonify(
    {
        "code": 404,
        "message": "There are no transactions."
    }
), 404

# ==== Add Transactions (Called from Choose Complex Microservice) ===== #
@app.route("/add_transactions", methods=["POST"])
def add_transactions_into_db():

    phone_number = request.json.get("phone_number", None)
    raffle_id = request.json.get("raffle_id", None)
    amount = request.json.get("amount", None)
    product_id = request.json.get("product_id", None)
    company_id = request.json.get("company_id", None)
    product_name = request.json.get("product_name", None) 
    product_desc = request.json.get("product_desc", None) 
    paid = request.json.get("paid", None) 

    transaction = Transaction(phone_number=phone_number, raffle_id=raffle_id, amount=amount, product_id=product_id, company_id=company_id, product_name=product_name, product_desc=product_desc, paid=paid)


    try:
        db.session.add(transaction)
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
            'phone_number': phone_number,
            'raffle_id': raffle_id,
            'amount': amount,
            'product_id': product_id,
            'company_id': company_id,
            'product_name': product_name,
            'product_desc': product_desc,
            "paid": paid
        }
    ), 201



if __name__ == '__main__':
    print("Flask Program " + os.path.basename(__file__) + ": managing Transactions Microservice")
    app.run(host='0.0.0.0', port=5006, debug=True)