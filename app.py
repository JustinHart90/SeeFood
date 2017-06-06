import pandas as pd
import requests, json
import random
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
            nameList = ['burrito', 'pizza', 'enchilada', 'salmon', 'fish', 'bacon', 'hotdog', 'beef', 'chicken', 'steak']
            name = random.choice(nameList)
            df = pd.read_pickle('data/tacos.pickle')
            entry = random.sample(df, 1)
            index = entry[0]['key']
            cals = entry[0]['calories']
            tn = entry[0]['totalNutrients']
            data = {'index' : index, 'calories' : cals, 'totalNutrients': tn }
            x = {'key': str(key), 'response': data }
            response = json.dumps(x, ensure_ascii=False)
            # #nice

            return render_template('api.html', data = nameList )
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
