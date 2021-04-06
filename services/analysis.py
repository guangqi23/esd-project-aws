import requests
import pandas as pd
import numpy as np
from flask import request, jsonify
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

# ===== General Functions ===== #
def convert_df(data, table_name):
    result_list = data['data'][table_name]
    return pd.DataFrame(result_list)

# ===== Raffle Entry Functions ====
def get_raffle_entries_by_product_id(df, product_id):
    return df[df['product_id'] == product_id]


def get_transactions_by_product_id(df, product_id):
    return df[df['product_id'] == product_id]

def get_current_raffle_count(df):
    return df['product_id'].count()

app = dash.Dash()

raffle_entries_url = "http://record:5000/raffle_entry" 

data = requests.get(raffle_entries_url)
data = data.json()
raffle_entries = convert_df(data, "raffle_entries")
raffle_entries = raffle_entries.astype({'raffle_id': 'object'})
current_raffle_count = get_current_raffle_count(raffle_entries)
current_raffle_count = f"Current Raffle Count: {str(current_raffle_count)}"


raffle_company_url = "http://record:5000/raffle_company"


data = requests.get(raffle_company_url)
data = data.json()
raffle_company = convert_df(data, "raffle_companies")
merged_df = pd.merge(raffle_entries, raffle_company, how="inner", on=["product_id"])
merged_df = merged_df[["company_id_x", "product_id", "amount", "product_name", "raffle_id_x", "no_of_products"]]
merged_df.rename(columns={
    'company_id_x': 'company_id',
    'raffle_id_x': 'raffle_id'
}, inplace=True)
# For now this is grouping by product_name
raffle_by_product = merged_df.groupby("product_name")['product_id'].count()
raffle_by_product_df = pd.DataFrame(raffle_by_product)
raffle_by_product_df.reset_index(inplace=True)

# Creating the Pie charts
fig2 = px.pie(raffle_by_product_df, values='product_id', names="product_name", title="Distribution of Products")
fig2 = dcc.Graph( 
    id="plot_area_2",
    figure=fig2 
)

# === Customer Satisfaction === #
survey_url = "http://survey:5008/survey_results"
data = requests.get(survey_url)
data = data.json()
survey = convert_df(data, "survey_results")

satisfaction_df = survey.groupby("satisfaction")['phone_number'].count()
satisfaction_df = pd.DataFrame(satisfaction_df)
satisfaction_df.reset_index(inplace=True)
satisfaction_df.rename(columns={
    "phone_number": "count"
}, inplace=True)



fig1 = px.bar(satisfaction_df, x="satisfaction", y="count", title="Satisfaction of Raffle")
fig1 = dcc.Graph(
    id="plot_area_1",
    figure=fig1
)

transaction_url = "http://transaction:5006/transactions"
data = requests.get(transaction_url)
data = data.json() 
if data['code'] == 404:
    survey_df = "No data accumulated. Please choose rafflers first."
    fig3 = html.H3(current_raffle_count, style={
            "color":"green",
            "height": "100%",
            "font-size": "300%",
            "text-align": "center",
            "border-style":"solid",
            "width": "50%"
    })
else:
    survey_df = convert_df(data, "transactions")
    survey_df = pd.DataFrame(survey_df.groupby("product_name")['amount'].sum())
    survey_df.reset_index(inplace=True)


    survey_df.rename(columns={
        'amount': 'expected_revenue'
    }, inplace=True)

    fig3 = px.bar(survey_df, x="product_name", y="expected_revenue", title="Expected Revenue per Product")
    fig3 = dcc.Graph(
        id="plot_area_3",
        figure=fig3
    )

survey_df = pd.DataFrame(survey.groupby('wish_item')['phone_number'].count())
survey_df.reset_index(inplace=True)

survey_df.rename(columns={
    'phone_number': 'count'
}, inplace=True)
survey_df

fig4 = px.pie(survey_df, values='count', names="wish_item", title="Customer's Wish List")
fig4 = dcc.Graph( 
    id="plot_area_4",
    figure=fig4
)


# === DISPLAYING THE CHARTS === #

app.layout = html.Div(children=[
            html.Div("Raffle's Dashboard", style={
                        "color": "black",
                        "text-align": "center",
                        "border-style": "solid",
                        "display": "inline-block",
                        "width": "100%",
                        "height": "100%"
            }),
    
    
#             html.Div(children=[
#                 html.H1("Current Raffle Count"),
#                 html.H3(current_raffle_count, style={
#                     "color":"green",
#                     "height": "100%",
#                     "font-size": "300%",
#                     "text-align": "center",
#                     "border-style":"solid",
#                     "text-align": "center",
#                     "border-style": "solid",
#                 })
#             ], style={
#                 "float":"left",
#                 "width": "50%"
#             }),
    
            html.Div(current_raffle_count, style={
                    "color":"green",
                    "height": "100%",
                    "font-size": "300%",
                    "text-align": "center",
                    "border-style":"solid",
                    "text-align": "center",
                    "border-style": "solid",
            }),

            html.Div(fig2, style={
                "float":"left",
                "width": "50%"
            }),
            html.Div(fig1, style={
                "float":"left",
                "width": "50%"
            }),
            html.Div(fig3, style={
                "float":"left",
                "width": "50%"
            }),
            html.Div(fig4, style={
                "float": "left",
                "width": "50%"
            })
    
    ]   
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8051, host="0.0.0.0")