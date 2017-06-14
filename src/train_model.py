from neural import NNmaker
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from keras import backend as K
from pymongo import MongoClient
from random import randint
from scipy.misc import imread, imsave, imresize



import random
import numpy as np
import pandas as pd
import names
import os
import pymongo
import pickle


def get_data():
    '''load data from pickled images'''
    X = pd.read_pickle("../data/tacos.pkl")
    y = pd.read_pickle("../data/tacos_cat.pkl")
    print(y)
    yc = preprocessing.LabelEncoder().fit_transform(y)
    # print(yc)
    clss = len(np.unique(yc))
    X_train, X_test, y_train, y_test = train_test_split(X, yc, test_size=0.25, random_state=42)
    X_train = np.asarray(X_train)
    X_test = np.asarray(X_test)
    X_train = X_train.astype('float32') #before conversion were uint8
    X_test = X_test.astype('float32')
    X_train /= 255 # normalizing (scaling from 0 to 1)
    X_test /= 255
    y_train = np.asarray(y_train)
    y_test = np.asarray(y_test)

    Y_train = np_utils.to_categorical(y_train, clss) # cool
    Y_test = np_utils.to_categorical(y_test, clss)

    return X_train, X_test, Y_train, Y_test, clss


def main():
    rng_seed = 20 # set random number generator seed
    X_train,X_test, y_train, y_test, classes = get_data()
    print(classes)
    maker = NNmaker()
    model = maker.handmade(X_train,X_test, classes)
    model.fit(X_train, y_train, batch_size=100, epochs=7,
      verbose=1, validation_data=(X_test, y_test), initial_epoch=0)
    model.fit(X_train, y_train, batch_size=1000, epochs=1,
          verbose=1, validation_data=(X_test, y_test), initial_epoch=5)

    # model.predict()
    score = model.evaluate(X_test, y_test, verbose=0)
    with open('tacos_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print(score)


def dance():
    X = pd.read_pickle("../data/tacos.pkl")
    y = pd.read_pickle("../data/tacos_cat.pkl")
    yc = preprocessing.LabelEncoder().fit_transform(y)

    imgdata = imread('img/24.jpg')
    img = np.array([imgdata])
    print(img)
    model = pickle.load( open( "tacos_model.pkl", "rb" ) )
    preds = model.predict(img)
    print(preds)
    # for i in X:
    #     img = np.array([i])
    #     preds = model.predict(img)
    #     print(preds)





if __name__ == '__main__':

    dance()
    # main()
