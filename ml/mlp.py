# -*- coding: utf-8 -*-
"""
Created on Mon Aug 01 20:31:00 2016

@author: Administrator
"""

import numpy as np

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
import preprocessing
import pandas as pd

df1 = pd.read_csv('E:/dota2/datasets/train.csv')
df2 = pd.read_csv('E:/dota2/datasets/test1.csv')
df1 = preprocessing.preprocessing(df1)
df2 = preprocessing.preprocessing(df2)
X_train = df1.iloc[:,0:222].values
Y_train = df1["label"].values
X_test = df2.iloc[:,0:222].values
Y_test = df2["label"].values

batch_size = 128
nb_classes = 2
nb_epoch = 20


X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

print(X_train.shape[0], 'train samples')


# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(Y_train, nb_classes)
Y_test = np_utils.to_categorical(Y_test, nb_classes)

model = Sequential()
model.add(Dense(512, input_shape=(222,)))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(2))
model.add(Activation('softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

history = model.fit(X_train, Y_train,
                    batch_size=batch_size, nb_epoch=nb_epoch,
                    validation_data=(X_test, Y_test))
