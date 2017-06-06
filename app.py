


import requests, json
import random
import numpy as np
import os
import sys
import pickle
from flask import Flask, render_template, request, redirect
from flask_restful import Resource, Api
from pymongo import MongoClient
import pymongo


app = Flask(__name__)

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
            name = np.random.choice(nameList, 1)
            uri = str(os.environ.get("MONGODB_URI"))
            client = pymongo.MongoClient(uri)
            db = client.get_default_database()
            micro = db['micro']
            cursor = micro.find_one( {"$and":[ {"key":0}, {"cat":{"$regex": str(name)}}] })


            return render_template('api.html', data = cursor )
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
