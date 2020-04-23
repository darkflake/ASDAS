import datetime

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import numpy as np
import pandas as pd
import tensorflow as tf


def data_preprocessing():
    x_train = pd.read_csv(f'train.csv')
    train_label = x_train.pop('Label')
    train_label = train_label.to_numpy()
    y_train = keras.utils.to_categorical(train_label, num_classes=5)
    x_train = x_train.to_numpy()

    x_test = pd.read_csv(f'test.csv')
    test_label = x_test.pop('Label')
    test_label = test_label.to_numpy()
    y_test = keras.utils.to_categorical(test_label, num_classes=5)
    x_test = x_test.to_numpy()

    return x_train, y_train, x_test, y_test


def network():
    x_train, y_train, x_test, y_test = data_preprocessing()
    model = Sequential()
    model.add(Dense(10, activation='relu', input_dim=5))
    model.add(Dropout(0.2))
    model.add(Dense(20, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(5, activation='softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.1, nesterov=True)

    model.compile(loss='categorical_crossentropy',
                  optimizer=sgd,
                  metrics=['accuracy'])

    model.fit(x_train,y_train,
              epochs=3000,
              batch_size=25,
              )

    score = model.evaluate(x_test, y_test, batch_size=25)
    print(model.metrics_names)
    print(score)

    print(model.predict(x_train[50:51], batch_size=None, verbose=0, steps=None))
    print(y_train[50:51])

network()
