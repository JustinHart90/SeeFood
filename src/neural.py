import random
import numpy as np
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import SGD
import theano

class NNmaker():

    def __init__(self):
        self.PopDNA = []
        # DNA Straind {NumN : number of neurons, NumL : number of layers, LI: layer inits,   }

    def reproduce_NN(self,DNA,inputs, classes):
        ''' defines multi-layer-perceptron neural network '''
        # available activation functions at:
        # https://keras.io/activations/
        # https://en.wikipedia.org/wiki/Activation_function
        # options: 'linear', 'sigmoid', 'tanh', 'relu', 'softplus', 'softsign'
        # there are other ways to initialize the weights besides 'uniform', too

        model = Sequential() # sequence of layers
        num_neurons_in_layer = 500 # number of neurons in a layer
        num_inputs = X_train.shape[1] # number of features (784)
        num_classes = y_train_ohe.shape[1]  # number of classes, 0-9
         # only 12 neurons in this layer!

        model.add(Dense(input_dim=(num_inputs * 2),
                         output_dim=num_neurons_in_layer,
                         init='random_uniform',
                         activation='relu'))
         # only 12 neurons - keep softmax at last layer
        sgd = SGD(lr=0.0044, decay=1e-7, momentum=.9) # using stochastic gradient descent (keep)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=["accuracy"] ) # (keep)
        return model

    def makeRanNN(self, inputs, classes):
        DNA = {}
        actList = ['linear', 'sigmoid', 'tanh', 'relu', 'softplus', 'softsign']
        model = Sequential() # sequence of layers
        NumN = random.randint(0,500) # number of neurons in a layer
        DNA['NumN'] = NumN
        num_inputs = inputs # number of features (784)
        num_classes = classes  # number of classes, 0-9
         # only 12 neurons in this layer!
        layers = random.randint(0,5)
        LM = []
        LA = []
        LK = 'random_uniform'
        DNA['NumL'] = layers
        act = random.choice(actList)
        model.add(Dense(input_dim=num_inputs,
                     units=NumN,
                     kernel_initializer= LK,
                     activation= act))
        for r in range(layers):
            lm = random.randint(0,5)
            act = random.choice(actList)
            LM.append(lm)
            LA.append(act)
            if r != 1:
                model.add(Dense(input_dim=(num_inputs * lm),
                             units=NumN,
                             kernel_initializer= LK,
                             activation= act))

        model.add(Dense(input_dim=NumN,
                         units=num_classes,
                         kernel_initializer='uniform',
                         activation='softmax'))
        DNA['LM'] = LM
        DNA['LA'] = LA
        DNA['LI'] = LK

        LR = random.uniform(0.1, 0.0001)
        DNA['LR'] = LR
        sgd = SGD(lr=LR, decay=1e-7, momentum=.9) # using stochastic gradient descent (keep)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=["accuracy"] )
        self.PopDNA.append(DNA)
        return model, DNA
