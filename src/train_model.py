from neural import NNmaker
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential, Model
from keras.layers.core import Dense
from keras.layers import Input, Flatten
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from keras import backend as K
from pymongo import MongoClient
from random import randint
from scipy.misc import imread, imsave, imresize
import os
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras import optimizers
from keras.preprocessing import image
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from keras.models import load_model



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
    # print('train: ')
    print(len(X_train))
    # print('test: ')
    print(len(X_test))
    Y_train = np_utils.to_categorical(y_train, clss) # cool
    # print(Y_train)
    Y_test = np_utils.to_categorical(y_test, clss)
    # print(Y_test)
    # return X_train, X_test, Y_train, Y_test, clss


def main():
    os.environ["THEANO_FLAGS"] = 'allow_gc=False, optimizer_including="local_ultra_fast_sigmoid", nvcc.fastmath=True, use_fast_math=True, optimizer=fast_compile, borrow=True'
    rng_seed = 20 # set random number generator seed
    X_train,X_test, y_train, y_test, classes = get_data()
    print(classes)
    maker = NNmaker()
    model = maker.handmade(X_train,X_test, classes)
    model.fit(X_train, y_train, batch_size=1000, epochs=20,
      verbose=1, validation_data=(X_test, y_test), initial_epoch=0)
    model.fit(X_train, y_train, batch_size=1000, epochs=1,
          verbose=1, validation_data=(X_test, y_test), initial_epoch=5)

    # model.predict()
    score = model.evaluate(X_test, y_test, verbose=0)
    with open('tacos_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print(score)


def dance():
    # os.environ["THEANO_FLAGS"] = ''
    X = pd.read_pickle("../data/all_data.pkl")
    y = pd.read_pickle("../data/cat.pkl")
    yc = preprocessing.LabelEncoder().fit_transform(y)
    print(y)
    # print(len(X))
    key2 = ['bacon', 'beef', 'burrito' ,'chicken', 'enchilada', 'fish' ,'hotdog', 'salmon'
 'steak', 'tacos']
    imgdata = imread('img/0.jpg')
    img = np.array([imgdata])

    model = load_model('../models/main_model.h5')
    preds = model.predict(img)
    print(preds)
    pre = np.argmax(preds)
    print(pre)
    print(key2[pre])
    for y, i in enumerate(X):
        img = np.array([i])
        img = img.astype('float32')
        img /= 255
        preds = model.predict(img)
        pre = np.argmax(preds)
        print(preds)
        print(key2[pre])

def _image_generator(X_train, Y_train):
    seed = 1337
    train_datagen = image.ImageDataGenerator(
            rotation_range=30,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=True)
    train_datagen.fit(X_train, seed=seed)
    return train_datagen

def vgg16(name):

    batch_size = 20
    epochs = 20

    X_train,X_test, y_train, y_test, classes = get_data()
    model_vgg16_conv = VGG16(weights='imagenet', include_top=False)
    #model_vgg16_conv.summary()

    #Create your own input format (here 3x200x200)
    input_ = Input(shape=(300,300,3), name = 'image_input')

    #Use the generated model
    output_vgg16_conv = model_vgg16_conv(input_)

    #Add the fully-connected layers
    x = Flatten(name='flatten')(output_vgg16_conv)
    x = Dense(512, activation='relu', name='fc1')(x)
    #x = Dense(1024, activation='relu', name='fc2')(x)
    x = Dense(classes, activation='softmax', name='predictions')(x)

    #Create your own model
    my_model = Model(inputs=input_, outputs=x)

    # Specify SGD optimizer parameters
    sgd = optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)

    # Compile model
    my_model.compile(loss='categorical_crossentropy',
                  optimizer=sgd,
                  metrics=['accuracy'])

    #In the summary, weights and layers from VGG part will be hidden, but they will be fit during the training
    generator = _image_generator(X_train, y_train)

    # checkpoint
    filepath="weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5"
    # checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=0, save_best_only=True, mode='max')

    # Change learning rate when learning plateaus
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1,
              patience=4, min_lr=0.00001)

    # Stop model once it stops improving to prevent overfitting
    early_stop = EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='auto')

    # put all callback functions in a list
    callbacks_list = [early_stop, reduce_lr]

    history = my_model.fit_generator(
    generator.flow(X_train, y_train, batch_size=batch_size),
    steps_per_epoch=(X_train.shape[0] // batch_size),
    epochs=epochs,
    validation_data=(X_test, y_test),
    callbacks=callbacks_list
    )
    score = my_model.evaluate(X_test, y_test, verbose=1)
    probs = my_model.predict(X_test, batch_size=batch_size)
    print(score)
    print(my_model.summary())


def vgg19(name):

    batch_size = 7
    epochs = 50

    X_train,X_test, y_train, y_test, classes = get_data()
    model_vgg19_conv = VGG19(weights='imagenet', include_top=False)
    #model_vgg16_conv.summary()

    #Create your own input format (here 3x200x200)
    input_ = Input(shape=(300,300,3), name = 'image_input')

    #Use the generated model
    output_vgg19_conv = model_vgg19_conv(input_)

    #Add the fully-connected layers
    x = Flatten(name='flatten')(output_vgg19_conv)
    x = Dense(512, activation='relu', name='fc1')(x)
    x = Dense(512, activation='relu', name='fc2')(x)
    x = Dense(classes, activation='softmax', name='predictions')(x)

    #Create your own model
    my_model = Model(inputs=input_, outputs=x)

    # Specify SGD optimizer parameters
    sgd = optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)

    # Compile model
    my_model.compile(loss='categorical_crossentropy',
                  optimizer=sgd,
                  metrics=['accuracy'])

    #In the summary, weights and layers from VGG part will be hidden, but they will be fit during the training
    generator = _image_generator(X_train, y_train)

    # checkpoint
    filepath="weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5"
    # checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=0, save_best_only=True, mode='max')

    # Change learning rate when learning plateaus
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1,
              patience=4, min_lr=0.00001)

    # Stop model once it stops improving to prevent overfitting
    early_stop = EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='auto')

    # put all callback functions in a list
    callbacks_list = [early_stop, reduce_lr]

    history = my_model.fit_generator(
    generator.flow(X_train, y_train, batch_size=batch_size),
    steps_per_epoch=(X_train.shape[0] // batch_size),
    epochs=epochs,
    validation_data=(X_test, y_test),
    callbacks=callbacks_list
    )
    score = my_model.evaluate(X_test, y_test, verbose=1)
    probs = my_model.predict(X_test, batch_size=batch_size)
    print(score)
    print(my_model.summary())

def get_keys():
    '''load data from pickled images'''
    names = ['bacon','fish']
    for i in names:
        print(i)
        y = pd.read_pickle("../data/"+i+"_cat.pkl")
        # print(y)

        # y = pd.read_pickle("../data/cat.pkl")
        le = preprocessing.LabelEncoder()
        yc = le.fit_transform(y)
        clss = np.unique(yc)
        key = le.inverse_transform(clss)

        print(key)






if __name__ == '__main__':
    get_keys()
    # getdata()
    # vgg19('main')
    #dance()
    # main()
