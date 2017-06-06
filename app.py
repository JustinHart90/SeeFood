import pandas as pd
import requests, json
import random
import numpy as np
import os
import sys
import pickle
from flask import Flask, render_template, request, redirect
from flask_restful import Resource, Api
from pymongo import MongoClient


app = Flask(__name__,  template_folder='templates')
app.config['DEBUG'] = True
global logged_In
logged_In = False
global username
username = ''


# Add log in page


# index page
@app.route('/')
def index():
    # global logged_In
    # if logged_In != True:
    #     return redirect("/login")
    return render_template('index.html', user = 'Jimmy Dean', TP = 3048, FP = 41, FN = 232, TN = 264, accuracy = 'NA', percision = 'NA', F1 =  65.9, time='0s')



#page for prediction results
@app.route('/predict', methods = ["GET", "POST"])
def predict():
    # global logged_In
    # if logged_In != True:
    #     return redirect("/login")
    # global username
    # user = username
    # if request.method == 'POST':
    #     f2 = request.files['file']
    #     df = pd.read_csv(f2)
    #     print(df.head())
    #     X = df['body']
    #     y = df['section_name']
    # with open('static/model.pkl', 'rb') as f:
    #     model = pickle.load(f)

    return render_template('predict.html', user = user, )




#API Dashboard
@app.route('/api_dash', methods = ["GET", "POST"])
def api_dash():
    # global logged_In
    # if logged_In != True:
        # return redirect("/login")
    # global username
    # user = username


    return render_template('api_dash.html', user = 'Jimmy Dean', )



#API request page
@app.route('/api', methods = ["GET", "POST"])
def api():
    if request.method == 'GET':
        key = request.args.get("key")
        print(key)
        if key == '89477':
            rando = [{'calories': 3777.3231101292263,'image_url': 'https://www.edamam.com/web-img/b6d/b6da6e61ae1e9e4c6d0dec0a06b2e0c5.jpg','key': 0,'label': "Uncle Ray's Crawfish Tacos",
 'totalNutrients': {'CA': {'label': 'Calcium',
   'quantity': 2645.8104272238634,
   'unit': 'mg'},
  'CHOCDF': {'label': 'Carbs', 'quantity': 82.93138786965841, 'unit': 'g'},
  'CHOLE': {'label': 'Cholesterol',
   'quantity': 1505.9827301979064,
   'unit': 'mg'},
  'ENERC_KCAL': {'label': 'Energy',
   'quantity': 3777.3231101292263,
   'unit': 'kcal'},
  'FAMS': {'label': 'Monounsaturated',
   'quantity': 130.17326769163503,
   'unit': 'g'},
  'FAPU': {'label': 'Polyunsaturated',
   'quantity': 22.17917192474904,
   'unit': 'g'},
  'FASAT': {'label': 'Saturated', 'quantity': 115.27750486814912, 'unit': 'g'},
  'FAT': {'label': 'Fat', 'quantity': 294.4100541766353, 'unit': 'g'},
  'FATRN': {'label': 'Trans', 'quantity': 3.604879048194885, 'unit': 'g'},
  'FE': {'label': 'Iron', 'quantity': 19.494643457930632, 'unit': 'mg'},
  'FIBTG': {'label': 'Fiber', 'quantity': 27.028811426874757, 'unit': 'g'},
  'FOLDFE': {'label': 'Folate (Equivalent)',
   'quantity': 449.028968314048,
   'unit': 'µg'},
  'K': {'label': 'Potassium', 'quantity': 4515.394603613797, 'unit': 'mg'},
  'MG': {'label': 'Magnesium', 'quantity': 550.9793977346346, 'unit': 'mg'},
  'NA': {'label': 'Sodium', 'quantity': 4425.2672222572855, 'unit': 'mg'},
  'NIA': {'label': 'Niacin (B3)',
   'quantity': 22.070284788691357,
   'unit': 'mg'},
  'P': {'label': 'Phosphorus', 'quantity': 4102.917357457969, 'unit': 'mg'},
  'PROCNT': {'label': 'Protein', 'quantity': 217.05912140846726, 'unit': 'g'},
  'RIBF': {'label': 'Riboflavin (B2)',
   'quantity': 2.1095807390074492,
   'unit': 'mg'},
  'SUGAR': {'label': 'Sugars', 'quantity': 32.48175626122265, 'unit': 'g'},
  'THIA': {'label': 'Thiamin (B1)',
   'quantity': 1.0617380517936088,
   'unit': 'mg'},
  'TOCPHA': {'label': 'Vitamin E',
   'quantity': 45.70922011611537,
   'unit': 'mg'},
  'VITA_RAE': {'label': 'Vitamin A',
   'quantity': 1563.6353102594699,
   'unit': 'µg'},
  'VITB12': {'label': 'Vitamin B12',
   'quantity': 21.153781525230407,
   'unit': 'µg'},
  'VITB6A': {'label': 'Vitamin B6',
   'quantity': 1.722504711193002,
   'unit': 'mg'},
  'VITC': {'label': 'Vitamin C', 'quantity': 55.95560162973405, 'unit': 'mg'},
  'VITD': {'label': 'Vitamin D', 'quantity': 3.1667771244049074, 'unit': 'µg'},
  'VITK1': {'label': 'Vitamin K', 'quantity': 91.54439890533888, 'unit': 'µg'},
  'ZN': {'label': 'Zinc', 'quantity': 23.953853427761885, 'unit': 'mg'}}}, {'calories': 3370.297051334064,
 'image_url': 'https://www.edamam.com/web-img/b78/b7800146742e14e278069bf840a2cfe3.jpg',
 'key': 12,
 'label': 'Tacos de Acelgas',
 'totalNutrients': {'CA': {'label': 'Calcium',
   'quantity': 2833.5211503561286,
   'unit': 'mg'},
  'CHOCDF': {'label': 'Carbs', 'quantity': 436.58582059110915, 'unit': 'g'},
  'CHOLE': {'label': 'Cholesterol',
   'quantity': 222.00000000000003,
   'unit': 'mg'},
  'ENERC_KCAL': {'label': 'Energy',
   'quantity': 3370.297051334064,
   'unit': 'kcal'},
  'FAMS': {'label': 'Monounsaturated',
   'quantity': 39.494761377656374,
   'unit': 'g'},
  'FAPU': {'label': 'Polyunsaturated',
   'quantity': 44.84051090072337,
   'unit': 'g'},
  'FASAT': {'label': 'Saturated', 'quantity': 50.051574719824465, 'unit': 'g'},
  'FAT': {'label': 'Fat', 'quantity': 146.9137193732057, 'unit': 'g'},
  'FE': {'label': 'Iron', 'quantity': 22.409514037778543, 'unit': 'mg'},
  'FIBTG': {'label': 'Fiber', 'quantity': 75.68753145530248, 'unit': 'g'},
  'FOLDFE': {'label': 'Folate (Equivalent)',
   'quantity': 345.09522811290975,
   'unit': 'µg'},
  'K': {'label': 'Potassium', 'quantity': 6907.594818689806, 'unit': 'mg'},
  'MG': {'label': 'Magnesium', 'quantity': 1178.9709475004843, 'unit': 'mg'},
  'NA': {'label': 'Sodium', 'quantity': 4493.743359049177, 'unit': 'mg'},
  'NIA': {'label': 'Niacin (B3)',
   'quantity': 21.889474765575486,
   'unit': 'mg'},
  'P': {'label': 'Phosphorus', 'quantity': 4611.170256444182, 'unit': 'mg'},
  'PROCNT': {'label': 'Protein', 'quantity': 110.48220356052072, 'unit': 'g'},
  'RIBF': {'label': 'Riboflavin (B2)',
   'quantity': 2.2887814630915164,
   'unit': 'mg'},
  'SUGAR': {'label': 'Sugars', 'quantity': 51.04288959702225, 'unit': 'g'},
  'THIA': {'label': 'Thiamin (B1)',
   'quantity': 1.529164882551756,
   'unit': 'mg'},
  'TOCPHA': {'label': 'Vitamin E',
   'quantity': 26.518203043560217,
   'unit': 'mg'},
  'VITA_RAE': {'label': 'Vitamin A',
   'quantity': 2470.2841558424448,
   'unit': 'µg'},
  'VITB12': {'label': 'Vitamin B12', 'quantity': 5.0172, 'unit': 'µg'},
  'VITB6A': {'label': 'Vitamin B6',
   'quantity': 3.5217142235816645,
   'unit': 'mg'},
  'VITC': {'label': 'Vitamin C', 'quantity': 330.23377564430234, 'unit': 'mg'},
  'VITD': {'label': 'Vitamin D', 'quantity': 1.11, 'unit': 'µg'},
  'VITK1': {'label': 'Vitamin K',
   'quantity': 3892.4490982873513,
   'unit': 'µg'},
  'ZN': {'label': 'Zinc', 'quantity': 22.90685475529249, 'unit': 'mg'}}}, {'calories': 4954.39379654953,
 'image_url': 'https://www.edamam.com/web-img/8dc/8dcf33536c55ac48a8d42686433ccd9c.jpg',
 'key': 20,
 'label': "Ralphie's Special Tacos",
 'totalNutrients': {'CA': {'label': 'Calcium',
   'quantity': 522.5483858904913,
   'unit': 'mg'},
  'CHOCDF': {'label': 'Carbs', 'quantity': 120.21481271623993, 'unit': 'g'},
  'CHOLE': {'label': 'Cholesterol',
   'quantity': 1275.728576660156,
   'unit': 'mg'},
  'ENERC_KCAL': {'label': 'Energy',
   'quantity': 4954.39379654953,
   'unit': 'kcal'},
  'FAMS': {'label': 'Monounsaturated',
   'quantity': 168.11521225826462,
   'unit': 'g'},
  'FAPU': {'label': 'Polyunsaturated',
   'quantity': 72.35177866033416,
   'unit': 'g'},
  'FASAT': {'label': 'Saturated', 'quantity': 79.9158406700537, 'unit': 'g'},
  'FAT': {'label': 'Fat', 'quantity': 346.7634941564056, 'unit': 'g'},
  'FATRN': {'label': 'Trans', 'quantity': 2.2942222924804687, 'unit': 'g'},
  'FE': {'label': 'Iron', 'quantity': 20.750370543233142, 'unit': 'mg'},
  'FIBTG': {'label': 'Fiber', 'quantity': 24.925306040969847, 'unit': 'g'},
  'FOLDFE': {'label': 'Folate (Equivalent)',
   'quantity': 252.7510122511291,
   'unit': 'µg'},
  'K': {'label': 'Potassium', 'quantity': 4579.743419963578, 'unit': 'mg'},
  'MG': {'label': 'Magnesium', 'quantity': 545.1833483111631, 'unit': 'mg'},
  'NA': {'label': 'Sodium', 'quantity': 5747.572526987259, 'unit': 'mg'},
  'NIA': {'label': 'Niacin (B3)',
   'quantity': 120.15913176282211,
   'unit': 'mg'},
  'P': {'label': 'Phosphorus', 'quantity': 3229.800182050476, 'unit': 'mg'},
  'PROCNT': {'label': 'Protein', 'quantity': 333.713129208165, 'unit': 'g'},
  'RIBF': {'label': 'Riboflavin (B2)',
   'quantity': 2.33732224717102,
   'unit': 'mg'},
  'SUGAR': {'label': 'Sugars', 'quantity': 15.581211993847656, 'unit': 'g'},
  'THIA': {'label': 'Thiamin (B1)',
   'quantity': 1.4529587749078368,
   'unit': 'mg'},
  'TOCPHA': {'label': 'Vitamin E',
   'quantity': 25.47489645075684,
   'unit': 'mg'},
  'VITA_RAE': {'label': 'Vitamin A',
   'quantity': 797.8242672819518,
   'unit': 'µg'},
  'VITB12': {'label': 'Vitamin B12',
   'quantity': 5.273011450195312,
   'unit': 'µg'},
  'VITB6A': {'label': 'Vitamin B6',
   'quantity': 6.896860237235563,
   'unit': 'mg'},
  'VITC': {'label': 'Vitamin C', 'quantity': 195.42774185180662, 'unit': 'mg'},
  'VITD': {'label': 'Vitamin D', 'quantity': 3.40194287109375, 'unit': 'µg'},
  'VITK1': {'label': 'Vitamin K', 'quantity': 259.3651151188507, 'unit': 'µg'},
  'ZN': {'label': 'Zinc', 'quantity': 25.654742932240886, 'unit': 'mg'}}}]
            entry = rando[random.randint(0,2)]
            index = entry['key']
            cals = entry['calories']
            tn = entry['totalNutrients']
            data = {'index' : index, 'calories' : cals, 'totalNutrients': tn }
            # x = {'key': str(key), 'response': data }
            # response = json.dumps(x, ensure_ascii=False)
            # #nice

            return render_template('api.html', data = data )
        else:
            return render_template('api_error.html' )
    else:
        return render_template('api_error.html' )










@app.route('/login', methods=['GET', 'POST'])
def login():
    client = MongoClient()
    # Access/Initiate Database
    db = client['DSI_Fraud']
    # Access/Initiate Table
    users = db['users']
    if request.method == 'GET':
        user = db['users'].find_one({"username": str(request.args.get("username"))})
        if user and  request.args.get("password") == user['password']:
            global logged_In
            logged_In = True
            global username
            username = str(request.args.get("username"))
            return redirect("/")


    return render_template('login.html', title= 'Login')

@app.route('/signout')
def singout():
    global logged_In
    logged_In = False
    return render_template('login.html', title= 'Login')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8105, debug=True)
