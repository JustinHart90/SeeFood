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



import random
import numpy as np
import pandas as pd
import names
import os
import pymongo
import pickle

def main():
    maker = NNmaker()
    model, DNA = maker.makeRanNN(100,10)

def get_data():
    '''load data from pickled images'''
    X = pd.read_pickle("../data/all_data.pkl")


    y = pd.read_pickle("../data/cat.pkl")

    yc = preprocessing.LabelEncoder().fit_transform(y)
    # print(yc)

    X_train, X_test, y_train, y_test = train_test_split(X, yc, test_size=0.25, random_state=42)

    X_train = np.asarray(X_train)
    X_test = np.asarray(X_test)
    X_train = X_train.astype('float32') #before conversion were uint8
    X_test = X_test.astype('float32')
    X_train /= 255 # normalizing (scaling from 0 to 1)
    X_test /= 255
    clss = len(np.unique(y_train))
    y_train = np.asarray(y_train)
    y_test = np.asarray(y_test)

    Y_train = np_utils.to_categorical(y_train, clss) # cool
    Y_test = np_utils.to_categorical(y_test, clss)

    return X_train, X_test, Y_train, Y_test, clss


def mixGenDNA(DNA_pool, X_train, y_train, X_test, y_test, classes, gen):
    #[name, test_acc, DNA]
    DNA_Pool = DNA_pool.copy()
    NewGenDNA = {}
    while len(DNA_Pool) > 1:
        mates = np.random.choice(list(DNA_Pool.keys()),2, replace=False)
        acc1 = DNA_Pool[mates[0]][1]
        acc2 = DNA_Pool[mates[1]][1]

        DNA1 = DNA_Pool[mates[0]][3]
        DNA2 = DNA_Pool[mates[1]][3]

        del DNA_Pool[mates[0]]
        del DNA_Pool[mates[1]]

        genes = list(DNA1.keys())
        mom = np.random.choice(genes,int(len(genes)/2), replace = False)
        momDNA = d = {g:DNA1[g] for g in mom}
        for key, value in momDNA.items():
            DNA2[key] = value

        name = names.get_first_name()
        maker = NNmaker()
        model = maker.reporduce_CNN(X_train, X_test, classes, DNA2)
        score = training_Time(model,DNA2, X_train, y_train, X_test, y_test, name, gen, mates[0], mates[1] )
        NewGenDNA[name]= [name, score[0],score[1], DNA2, name, gen]
        DNA_pool.update(NewGenDNA)
    return DNA_pool, len(NewGenDNA)
    # print('{} and {} had a baby'.format(mates[0],mates[1]))
    # print(DNA1)



def evolve():
    rng_seed = 20 # set random number generator seed
    X_train,X_test, y_train, y_test, classes = get_data()

    np.random.seed(rng_seed)
    DNAPop = {}
    num_gen = 5
    num_pop = 5
    for pop in range(num_pop):
        maker = NNmaker()
        name = names.get_first_name()
        model,DNA = maker.makerandom_CNN(X_train,X_test, classes)
        score = training_Time(model, DNA, X_train, y_train, X_test, y_test, name, 1, 'none', 'none')

        DNAPop[name]= [name, score[1],score[0], DNA, 1]

    for gen in range(num_gen):
        print('Generation: ' + str((gen + 1)))
        # for pop in range(num_pop):

        DNAPop, childs = mixGenDNA(DNAPop, X_train, y_train, X_test, y_test,classes, (gen+2))
        DNAPop = killOff(DNAPop,childs)

        # print(NewGenDNA)
def killOff(DNAPop, childs):
    pop = []
    for key in DNAPop.keys():
        pop.append([DNAPop[key][1], key])
    sorts = sorted(pop)
    for i in range(childs):
        for x, person in enumerate(sorts):
            if randint(0,3) != 3:
                print('kill')
                del DNAPop[person[1]]
                sorts.pop(x)
                break
        else:
            continue
        # add death to Mongo
    return DNAPop


def training_Time(model,DNA, X_train, y_train, X_test, y_test, name, gen, parent1, parent2):
    #[name, score[0],score[1], DNA2, name, gen]

    model.fit(X_train, y_train, batch_size=DNA['BS'], epochs=DNA['epochs'],
      verbose=1, validation_data=(X_test, y_test), initial_epoch=0)
    score = model.evaluate(X_test, y_test, verbose=0)
    print('score 1: ' + str(score[0]))
    print('score 2: ' + str(score[1]))
    uploadModels(DNA, model, name, score[0],score[1], gen, parent1, parent2)
    # with open('model.pkl', 'wb') as f:
    #     pickle.dump(model, f)
    return score

def uploadModels(DNA, model, name, score1, score2, gen, parent1, parent2):

        uri = str(os.environ.get("MONGODB_URI_MODELS"))
        client = pymongo.MongoClient(uri)
        db = client.get_default_database()
        m = db['models']
        m.insert_one({'name': name, 'DNA':DNA, 'score': score1, 'loss':score2, 'gen': gen, 'parent1': parent1, 'parent2': parent2 })



if __name__ == '__main__':
    # get_data()
    evolve()
    # popdna ={'Robert': ['Robert', 0.1087, {'NumN': 315, 'NumL': 3, 'LM': [4, 0, 5], 'LA': ['tanh', 'relu', 'tanh'], 'LI': 'random_uniform', 'LR': 0.0038882690316379698}], 'Brian': ['Brian', 0.1115, {'NumN': 485, 'NumL': 4, 'LM': [2, 2, 5, 0], 'LA': ['tanh', 'softplus', 'softsign', 'softsign'], 'LI': 'random_uniform', 'LR': 0.004628537323412493}], 'Celine': ['Celine', 0.14979999999999999, {'NumN': 32, 'NumL': 0, 'LM': [], 'LA': [], 'LI': 'random_uniform', 'LR': 0.0833583941408591}]}
    #mixGenDNA(popdna)
