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
        if y == 200:
            break
        cat = key.name.split('/')[0]
        print(cat)
        contents = key.get_contents_to_filename('img/temp.jpg')
        imgdata = imread('img/temp.jpg')
        if imgdata.shape == (300, 300, 3):
            full_data.append(imgdata)
            cats.append(cat)

            rot90 = rotate(img, 90, reshape=False)
            full_data.append(rot90)
            cats.append(cat)

            rot180 = rotate(img, 180, reshape=False)
            full_data.append(rot180)
            cats.append(cat)

            rot270 = rotate(img, 270, reshape=False)
            full_data.append(rot270)
            cats.append(cat)

    with open('../data/all_data.pkl', 'wb') as f:
        pickle.dump(full_data, f)
    with open('../data/cat.pkl', 'wb') as f:
        pickle.dump(cats, f)

if __name__ == '__main__':
    main()
