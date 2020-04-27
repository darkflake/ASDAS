import datetime
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import SGD, Adam
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split


def data_preprocessing():
    dataframe = pd.read_csv(f'FinalData_band.csv')
    x_train, x_test = train_test_split(dataframe, test_size=0.33, shuffle=True)
    #x_train = pd.read_csv(f'train.csv')
    train_label = x_train.pop('Label')
    train_label = train_label.to_numpy()
    y_train = keras.utils.to_categorical(train_label, num_classes=5)
    x_train = x_train.div(1000).round(7)
    x_train = x_train.to_numpy()

    #x_test = pd.read_csv(f'test.csv')
    test_label = x_test.pop('Label')
    test_label = test_label.to_numpy()
    y_test = keras.utils.to_categorical(test_label, num_classes=5)
    x_test = x_test.div(1000).round(7)
    x_test = x_test.to_numpy()

    return x_train, y_train, x_test, y_test


def network():
    x_train, y_train, x_test, y_test = data_preprocessing()
    model = Sequential()
    model.add(Dense(4, activation='relu', input_dim=5))
    # model.add(Dropout(0.2))
    model.add(Dense(3, activation='relu'))
    # model.add(Dropout(0.2))
    model.add(Dense(4, activation='relu'))
    # model.add(Dropout(0.2))
    model.add(Dense(5, activation='softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.1, nesterov=True)
    #sgd = SGD(lr=0.001)

    model.compile(loss='categorical_crossentropy',
                  optimizer=sgd,
                  metrics=['accuracy'])

    log_dir = "logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

    model.fit(x_train, y_train,
              epochs=500,
              batch_size=25,
              callbacks=[tensorboard_callback],
              )

    score = model.evaluate(x_test, y_test, batch_size=25)
    print(model.metrics_names)
    print(score)

    # print(model.predict(x_test, batch_size=None, verbose=0, steps=None))
    # print(y_train)


network()