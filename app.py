


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
from datetime import datetime
import io
from scipy import misc
from PIL import Image






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
        api_key = request.args.get("key")
        link = request.args.get("link")
        if api_key == '89477':
            nameList = ['burrito', 'pizza', 'enchilada', 'salmon', 'fish', 'bacon', 'hotdog', 'beef', 'chicken', 'steak']
            name = np.random.choice(nameList, 1)



            # try:
            r = requests.get(link)
            data = io.BytesIO(r.content)
            im = Image.open(data)
            imgdata = misc.fromimage(im)
            # imgresized = misc.imresize(imgdata, size = (300,300))
            imgresized = imgdata
            imgresized = imgresized.astype('float32')
            imgresized.reshape(imgresized.shape + (1,))
            imgresized /= 255
            imgresized = np.reshape(imgresized, (1,  300, 300, 3))
            print((imgresized))

            # except Exception as e:
            #     return render_template('api_error.html', error = 'There was trouble with the image' )
            model = pickle.load( open( "model.pkl", "rb" ) )
            prdiction = model.predict(imgresized)





            # connect to mongo DB
            uri = str(os.environ.get("MONGODB_URI"))
            client = pymongo.MongoClient(uri)
            db = client.get_default_database()
            micro = db['micro']

            #make Query with prediction
            cursor = micro.find_one( {"$and":[ {"key":random.randint(0,98)}, {"cat":{"$regex": str(name)}}] })
            cat = cursor['cat']
            key = cursor['key']
            name = cursor['label']
            cals = cursor['calories']
            tn = cursor['totalNutrients']
            #return the data
            response = {'key': key, 'cat': cat, 'key' : key, 'name':name, 'calories' : cals, 'totalNutrients': tn}
            x = json.dumps(response, sort_keys=True, indent=4)


            #get data from api pings and add image to bucket
            req = db['api-req']
            req.insert_one({'api_key': api_key, 'date' : datetime.now() })
            return render_template('api.html', data = '', link = imgresized )
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
