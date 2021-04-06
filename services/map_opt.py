#imports databases
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import os
import sys

import urllib.request
#invoke
import json
from invokes import invoke_http

#maps and pandas
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

#gmplot
# import gmplot package
import gmplot

# GoogleMapPlotter return Map object
# Pass the center latitude and
# center longitude
gmplot.apikey = "AIzaSyBfQEhUN7BVQ2i4Km-KrpdLdbSI9EX26n4"

#SQLAlchemy
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://is213@host.docker.internal:3306/raffle_db"
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://root:esd_a_plus_2021@raffle-db.c3e0re9oziwf.us-east-1.rds.amazonaws.com:3306/raffle_db"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/raffle_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)  

# location_URL = environ.get("location_URL") or "http://localhost:5007/location"


@app.route("/show_map")
def show_map():
    return render_template("file4.html")

@app.route("/map_opt", methods=["GET","POST"])
def create_map_plot():
# Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            optimisation_item = request.get_json()
            print(optimisation_item)
            print("\nReceived an order in JSON:", optimisation_item)
            print(type(optimisation_item))

            # 1. Send optimisation item info {"product_id":2 , "company_id":443}
            #json received from locations
            result_from_process_optimisation = processOptimisation(optimisation_item)
            print("------------result from opt----------")
            print(result_from_process_optimisation)

            # results = result_from_process_optimisation['data']['location_entries']
            results = result_from_process_optimisation
            order_dict = {}
            location_dict = {}
            for i in range(len(results)):
                temp_dict = {}
                temp_dict['lat'] = results[i].get('lat')
                temp_dict['lng'] = results[i].get('lng')
                order_dict['order_'+str(i+1)] = temp_dict

            df= pd.DataFrame.from_dict(order_dict).transpose()
            print(df)
            lat_list = df['lat'].values.tolist()
            lng_list = df['lng'].values.tolist()

            print(lat_list)
            print(lng_list)

            #Using Google Map
            # latitude_list = [ 17.4567417, 17.5587901, 17.6245545]
            # longitude_list = [ 78.2913637, 78.007699, 77.9266135 ]
            gmap = gmplot.GoogleMapPlotter(1.3521,103.8198, 12 )

            #Scatter plot on map
            # gmap.scatter( lat_list, lng_list, '# FF0000', size = 20, marker = False)
            gmap.scatter(lat_list, (lng_list), '#E95C6F', size = 1000, marker = True)
            gmap.apikey = "AIzaSyBfQEhUN7BVQ2i4Km-KrpdLdbSI9EX26n4"
            gmap.draw( "./templates/file4.html" )
            print("gmap print")
            # html = urllib.request.urlopen("./file4.html")

            # return "file4.html"
            return jsonify(
                {
                    "file": "file4.html",
                    "status": "success"
                }
            )
            # return "./file4.html"
            
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            # print(ex_str)

            return jsonify({
                "code": 500,
                "message": "map-opt.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processOptimisation(order):

    #Invoke location microservice
    # print('\n-----Invoking location microservice-----')
    print("ORDER--------------",order)
    pid = str(order['product_id'])
    cid = str(order['company_id'])

    location_URL = "http://location:5007/location"
    location_URL = location_URL + "/" + pid +"/" + cid
    print(location_URL)
    order_result = invoke_http(location_URL, method='GET')

    return order_result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)