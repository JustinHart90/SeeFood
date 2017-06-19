


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

from keras.models import load_model
from scipy.misc import imread, imsave, imresize
from PIL import Image





ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'PNG', 'JPG'])
app = Flask(__name__)
app.config['MAX_CONTENT_PATH'] = 4000000
global main_model
global bacon_model
global burrito_model
global enchilada_model
global hotdog_model
global salmon_model
global tacos_model


def choose2nd(name, img):
    #['bacon', 'beef', 'burrito', 'chicken', 'enchilada', 'fish',
    #'hotdog', 'salmon', 'steak', 'tacos']
    if name == 'bacon':
        keys = ['1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '22',
 '23', '24', '25', '26', '27', '28', '29', '3', '30', '31', '32', '33', '34', '35', '36']
        global bacon_model
        preds = bacon_model.predict(img).flatten()
        pre = np.argmax(preds)
        return keys[pre]
    elif name == 'beef':
        keys = ['1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '22',
 '23', '24', '25', '26', '27', '28', '29', '3', '30', '31', '32', '33', '34', '35', '36']
        global beef_model
        preds = beef_model.predict(img).flatten()
        pre = np.argmax(preds)
        return keys[pre]
    elif name == 'burrito':
        keys = ['1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2' ,'20', '21', '22',
 '23', '24', '25', '26', '27', '28', '29', '3', '30', '31', '32', '33', '34', '35', '36']
        global burrito_model
        preds = burrito_model.predict(img).flatten()
        pre = np.argmax(preds)
        return keys[pre]
    elif name == 'chicken':
        keys = ['1', '10' ,'11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '22',
 '23', '24', '25', '26', '27', '28', '29', '3', '30', '31', '32', '33', '34', '35', '36']
        global chicken_model
        preds = chicken_model.predict(img).flatten()
        pre = np.argmax(preds)
        return keys[pre]
    elif name == 'enchilada':
        keys = ['1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '22',
 '23', '24', '25', '26', '27', '28', '29', '3', '30', '31', '32', '33', '34', '35', '36']
        global enchilada_model
        preds = enchilada_model.predict(img).flatten()
        pre = np.argmax(preds)
        return keys[pre]
    elif name == 'fish':
        ['1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2' ,'20' ,'21', '22',
 '23', '24', '25', '26', '27', '28', '29' ,'3', '30', '31', '32', '33', '34', '35', '36']
        global fish_model
        preds = fish_model.predict(img).flatten()
        pre = np.argmax(preds)
        return keys[pre]
    elif name == 'hotdog':
        keys = ['1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '22',
 '23', '24', '25', '26', '27', '28' ,'29', '3' ,'30', '31', '32', '33', '34', '35', '36']
        global hotdog_model
        preds = hotdog_model.predict(img).flatten()
        pre = np.argmax(preds)
        return keys[pre]
    elif name == 'salmon':
        keys = ['1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '22',
 '23', '24', '25', '26', '27', '28', '29', '3', '30', '31', '32', '33', '34', '35', '36']
        global salmon_model
        preds = salmon_model.predict(img).flatten()
        pre = np.argmax(preds)
        return keys[pre]
    elif name == 'steak':
        keys = ['1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '22',
 '23', '24', '25', '26', '27', '28', '29', '3', '30', '31', '32', '33', '34', '35', '36']
        global steak_model
        preds = steak_model.predict(img).flatten()
        pre = np.argmax(preds)
        return keys[pre]
    elif name == 'tacos':
        keys = ['0', '1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21',
 '22', '23', '24', '25', '26', '27', '28', '29', '3', '30', '31', '32', '33', '34', '35']
        global tacos_model
        preds = tacos_model.predict(img).flatten()
        pre = np.argmax(preds)
        return keys[pre]

def choose1st(im):
    keys = ['bacon', 'beef', 'burrito', 'chicken', 'enchilada', 'fish',
    'hotdog', 'salmon', 'steak', 'tacos']
    global main_model
    preds = main_model.predict(im).flatten()
    pre = np.argmax(preds)
    return keys[pre]

def processPhoto(im):
    half_the_width = im.size[0] / 2
    half_the_height = im.size[1] / 2
    img4 = im.crop(
    (
    half_the_width - 150,
    half_the_height - 150,
    half_the_width + 150,
    half_the_height + 150
    )
    )
    imgdata = misc.fromimage(img4)
    imgresized = misc.imresize(imgdata, (300,300,3))
    image = imgresized.reshape((1,) + imgresized.shape)
    imgresized = image.astype('float32')
    imgresized /= 255
    return imgresized

@app.before_first_request
def _run_on_start():
    print('hello')
    # global main_model
    # main_model = load_model('models/main_model.h5')
    # global bacon_model
    # bacon_model = load_model('models/bacon_model.h5')
    # global burrito_model
    # burrito_model = load_model('models/burrito_modelV2.h5')
    # global enchilada_model
    # enchilada_model = load_model('models/enchilada_model.h5')
    # global hotdog_model
    # hotdog_model = load_model('models/hotdog_modelV2.h5')
    # global salmon_model
    # salmon_model = load_model('models/salmon_model.h5')
    # global tacos_model
    # tacos_model = load_model('models/tacos_modelV2.h5')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# index page
@app.route('/')
def index():

    return render_template('index.html')



#page for prediction results
@app.route('/predict', methods = ["GET", "POST"])
def predict():


    return render_template('predict.html')


@app.route('/results', methods = ["GET", "POST"])
def results():
    if request.method == 'POST':
        if 'file' not in request.files:
            message = 'Invalid Request File Not Found'
            return redirect('predict.html', error=message)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            message = 'File Not Found'
            return redirect('predict.html', error=message)
        if file and allowed_file(file.filename):
            file.save('static/images/temp.jpg')
            im = Image.open('static/images/temp.jpg')
            im = processPhoto(im)
            name = choose1st(im)
            label = int(choose2nd(name, im))
            print(label)

            uri = str(os.environ.get("MONGODB_URI"))
            client = pymongo.MongoClient(uri)
            db = client.get_default_database()
            micro = db['micro']

            #make Query with prediction
            cursor = micro.find_one( {"$and":[ {"key":label}, {"cat":{"$regex": str(name)}}] })
            cat = cursor['cat']
            label = cursor['label']
            cals = cursor['calories']
            tn = cursor['totalNutrients']
            return render_template('results.html', cat = cat, label = label, cals= cals, th = tn)



    message = 'Picture must exist and be either png, jpg, or jpeg'
    return render_template('predict.html', error = message)


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
            # model = pickle.load( open( "model.pkl", "rb" ) )
            # prdiction = model.predict(imgresized)





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
            return render_template('api.html', data = x )
        else:
            return render_template('api_error.html' )
    else:
        return render_template('api_error.html' )






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8105, debug=True)
