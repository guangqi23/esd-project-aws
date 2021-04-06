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

class Survey(db.Model):
    __tablename__ = '443_Company_Survey'
    phone_number = db.Column(db.String(9), nullable=False, primary_key=True)
    product_id = db.Column(db.String(9), nullable=False, primary_key=True)
    satisfaction = db.Column(db.String(255), nullable=False)
    wish_item = db.Column(db.String(255), nullable=False)
    

    def json(self): 
        survey_result = {
            'phone_number':self.phone_number,
            'product_id': self.product_id,
            'satisfaction': self.satisfaction,
            'wish_item': self.wish_item
        }
        return survey_result

@app.route("/survey_results")
def get_all_surveys():
    survey_results = Survey.query.all()

    if len(survey_results):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "survey_results": [survey_result.json() for survey_result in survey_results]
                }
            }
        )
    return jsonify(
    {
        "code": 404,
        "message": "There are no survey entries."
    }
), 404 


@app.route("/post_survey", methods=["POST"])
def post_survey():
    phone_number = request.json.get("phone_number", None)
    product_id = request.json.get("product_id", None)
    satisfaction = request.json.get("satisfaction", None)
    wish_item = request.json.get("wish_item", None)

    survey = Survey(phone_number=phone_number, product_id=product_id, satisfaction=satisfaction, wish_item=wish_item)

    try: 
        db.session.add(survey)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": "An error occured while creating the order. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "phone_number": phone_number,
            "product_id": product_id,
            "satisfaction": satisfaction,
            "wish_item": wish_item,
            "messsage": "success"
        }
    ), 201


if __name__ == '__main__':
    print("Flask Program " + os.path.basename(__file__) + ": managing Survey microservice")
    app.run(host='0.0.0.0', port=5008, debug=True)

