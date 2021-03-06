from scipy.misc import imread, imsave, imresize
from boto.s3.key import Key
from bs4 import BeautifulSoup
from scipy.ndimage import rotate
import pandas as pd
import requests, json
import os
import sys
import urllib.request, json
import pickle
import pymongo
import boto
import boto.s3
import boto.s3.connection
import io
import random





def main():
    '''Function to pull AWS images and convert them into numpy arrays for models
    OUTPUT: pickel file of all images'''
    AWS_ACCESS_KEY_ID = str(os.environ.get("AWS_ACCESS_KEY"))
    AWS_SECRET_ACCESS_KEY = str(os.environ.get("AWS_SECRET"))
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    mybucket = conn.get_bucket('dis-capstone-seefood')


    keylist = []
    for i, key in enumerate(mybucket.list()):
        keylist.append(key)
    full_data = []
    cats = []
    random.shuffle(keylist)

    for y,key in enumerate(keylist):
        if y == 60:
            break
        cat = key.name.split('/')[0]
        print(cat)
        contents = key.get_contents_to_filename('img/temp.jpg')
        imgdata = imread('img/temp.jpg')
        if imgdata.shape == (300, 300, 3):
            full_data.append(imgdata)
            cats.append(cat)

            rot36 = rotate(imgdata, 36, reshape=False)
            full_data.append(rot36)
            cats.append(cat)

            rot72 = rotate(imgdata, 72, reshape=False)
            full_data.append(rot72)
            cats.append(cat)

            rot108 = rotate(imgdata, 108, reshape=False)
            full_data.append(rot108)
            cats.append(cat)

            rot144 = rotate(imgdata, 144, reshape=False)
            full_data.append(rot144)
            cats.append(cat)

            rot180 = rotate(imgdata, 180, reshape=False)
            full_data.append(rot180)
            cats.append(cat)

            rot216 = rotate(imgdata, 216, reshape=False)
            full_data.append(rot216)
            cats.append(cat)

            rot252 = rotate(imgdata, 252, reshape=False)
            full_data.append(rot252)
            cats.append(cat)

            rot288 = rotate(imgdata, 288, reshape=False)
            full_data.append(rot288)
            cats.append(cat)

            rot324 = rotate(imgdata, 324, reshape=False)
            full_data.append(rot324)
            cats.append(cat)

    with open('../data/all_data.pkl', 'wb') as f:
        pickle.dump(full_data, f)
    with open('../data/cat.pkl', 'wb') as f:
        pickle.dump(cats, f)

def smash_one(name):
    '''Function to pull AWS images of a given category and convert them into numpy arrays for models
    INPUT: name of category (string)
    OUTPUT: pickel file of images'''
    AWS_ACCESS_KEY_ID = str(os.environ.get("AWS_ACCESS_KEY"))
    AWS_SECRET_ACCESS_KEY = str(os.environ.get("AWS_SECRET"))
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    mybucket = conn.get_bucket('dis-capstone-seefood')


    keylist = []
    for i, key in enumerate(mybucket.list(name + "/", "/")):
        keylist.append(key)
    keylist.pop(0)
    full_data = []
    cats = []

    for y,key in enumerate(keylist):
        if y == 30:
            break
        cat = key.name.split('/')[1]
        cat = cat.split(".")[0]

        print(cat)
        contents = key.get_contents_to_filename('img/temp.jpg')
        imgdata = imread('img/temp.jpg')
        if imgdata.shape == (300, 300, 3):
            full_data.append(imgdata)
            cats.append(cat)

            rot45 = rotate(imgdata, 45, reshape=False)
            full_data.append(rot45)
            cats.append(cat)

            rot90 = rotate(imgdata, 90, reshape=False)
            full_data.append(rot90)
            cats.append(cat)

            rot135 = rotate(imgdata, 135, reshape=False)
            full_data.append(rot135)
            cats.append(cat)

            rot180 = rotate(imgdata, 180, reshape=False)
            full_data.append(rot180)
            cats.append(cat)

            rot225 = rotate(imgdata, 225, reshape=False)
            full_data.append(rot225)
            cats.append(cat)

            rot270 = rotate(imgdata, 270, reshape=False)
            full_data.append(rot270)
            cats.append(cat)
            # imsave('../static/images/im8.jpg', rot45)
        with open('../data/'+name+'.pkl', 'wb') as f:
            pickle.dump(full_data, f)
        with open('../data/'+name+'_cat.pkl', 'wb') as f:
            pickle.dump(cats, f)


if __name__ == '__main__':
    # main()
    names = ['bacon','fish']
    for i in names:
        smash_one(i)
