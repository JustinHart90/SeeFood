from neural import NNmaker
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import SGD
import theano
import random
import numpy as np
import names

def main():
    maker = NNmaker()
    model, DNA = maker.makeRanNN(100,10)

def load_and_condition_MNIST_data():
    ''' loads and shapes MNIST image data '''
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    print ("\nLoaded MNIST images")
    theano.config.floatX = 'float32'
    X_train = X_train.astype(theano.config.floatX) #before conversion were uint8
    X_test = X_test.astype(theano.config.floatX)
    X_train.resize(len(y_train), 784) # 28 pix x 28 pix = 784 pixels
    X_test.resize(len(y_test), 784)
    print ('\nFirst 5 labels of MNIST y_train: ', y_train[:5])
    y_train_ohe = np_utils.to_categorical(y_train)
    print ('\nFirst 5 labels of MNIST y_train (one-hot):\n', y_train_ohe[:5])
    print ('')
    return X_train, y_train, X_test, y_test, y_train_ohe

def print_output(model, y_train, y_test, X_train, X_test, rng_seed):
    '''prints model accuracy results'''
    y_train_pred = model.predict_classes(X_train, verbose=0)
    y_test_pred = model.predict_classes(X_test, verbose=0)
    print( '\nRandom number generator seed: ', rng_seed)
    print( '\nFirst 30 labels:      ', y_train[:30])
    print( 'First 30 predictions: ', y_train_pred[:30])
    train_acc = np.sum(y_train == y_train_pred, axis=0) / X_train.shape[0]
    print ('Training accuracy: {}'.format((train_acc * 100)))
    test_acc = np.sum(y_test == y_test_pred, axis=0) / X_test.shape[0]
    print ('Test accuracy: {}'.format((test_acc * 100)))
    if test_acc < 0.95:
        print ('\nMan, your test accuracy is bad! ')
        print ("Can't you get it up to 95%?")
    else:
        print ("\nYou've made some improvements, I see...")
    return test_acc

def mixGenDNA(DNA_pool, X_train, y_train, X_test, y_test, y_train_ohe):
    #[name, test_acc, DNA]
    NewGenDNA = {}
    while len(DNA_pool) > 1:
        mates = np.random.choice(list(DNA_pool.keys()),2)
        acc1 = DNA_pool[mates[0]][1]
        acc2 = DNA_pool[mates[1]][1]

        DNA1 = DNA_pool[mates[0]][2]
        DNA2 = DNA_pool[mates[1]][2]
        del DNA_pool[mates[0]]
        del DNA_pool[mates[1]]
        print(DNA2)
        genes = list(DNA1.keys())
        mom = np.random.choice(genes,int(len(genes)/2), replace = False)
        momDNA = d = {g:DNA1[g] for g in mom}
        for key, value in momDNA.items():
            DNA2[key] = value
        print(DNA2)
        name = names.get_first_name()
        NewGenDNA[name] = [name, DNA2]
        maker = NNmaker()
        model = maker.reproduce_NN(X_train.shape[1],y_train_ohe.shape[1])
        model.fit(X_train, y_train_ohe, epochs=1, batch_size=500000, verbose=1,
                  validation_split=0.0599)
        test_acc = print_output(model, y_train, y_test, X_train, X_test, rng_seed)
        NewGenDNA[name]= [name, test_acc, DNA]
    return NewGenDNA
    # print('{} and {} had a baby'.format(mates[0],mates[1]))
    # print(DNA1)



def evolve():
    rng_seed = 20 # set random number generator seed
    X_train, y_train, X_test, y_test, y_train_ohe = load_and_condition_MNIST_data()
    np.random.seed(rng_seed)
    DNAPop = {}
    num_gen = 1
    num_pop = 3
    for pop in range(num_pop):
        maker = NNmaker()
        model, DNA = maker.makeRanNN(X_train.shape[1],y_train_ohe.shape[1])
        model.fit(X_train, y_train_ohe, epochs=1, batch_size=500000, verbose=1,
                  validation_split=0.0599) # .0599 cross val to estimate test error
        test_acc = print_output(model, y_train, y_test, X_train, X_test, rng_seed)
        name = names.get_first_name()
        DNAPop[name]= [name, test_acc, DNA]
    for gen in range(num_gen):
        for pop in range(num_pop):
            print(DNAPop)
            NewGenDNA = mixGenDNA(DNAPop, X_train, y_train, X_test, y_test, y_train_ohe)
        # print(NewGenDNA)


if __name__ == '__main__':
    evolve()
    # main()
    popdna ={'Robert': ['Robert', 0.1087, {'NumN': 315, 'NumL': 3, 'LM': [4, 0, 5], 'LA': ['tanh', 'relu', 'tanh'], 'LI': 'random_uniform', 'LR': 0.0038882690316379698}], 'Brian': ['Brian', 0.1115, {'NumN': 485, 'NumL': 4, 'LM': [2, 2, 5, 0], 'LA': ['tanh', 'softplus', 'softsign', 'softsign'], 'LI': 'random_uniform', 'LR': 0.004628537323412493}], 'Celine': ['Celine', 0.14979999999999999, {'NumN': 32, 'NumL': 0, 'LM': [], 'LA': [], 'LI': 'random_uniform', 'LR': 0.0833583941408591}]}
    #mixGenDNA(popdna)
