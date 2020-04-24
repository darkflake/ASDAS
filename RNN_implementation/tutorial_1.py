import pandas as pd
import numpy as np
import math


def data_preprocessing():
    x_train = pd.read_csv(f'train.csv')
    train_label = x_train.pop('Label')
    train_label = train_label.to_numpy()
    y_train = train_label
    x_train = x_train.to_numpy()

    '''x_test = pd.read_csv(f'test.csv')
    test_label = x_test.pop('Label')
    test_label = test_label.to_numpy()
    #y_test = keras.utils.to_categorical(test_label, num_classes=5)
    x_test = x_test.to_numpy()'''

    return x_train, y_train


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def sigmoid_prime(x):
    return sigmoid(x)*(1-sigmoid(x))


X, Y = data_preprocessing()
print(X,Y)
epochs = 50000
input_size, hidden_size, output_size = 5, 3, 3032
LR = .1  # learning rate

w_hidden = np.random.uniform(size=(input_size, hidden_size))
print(w_hidden)
w_output = np.random.uniform(size=(hidden_size, output_size))

for epoch in range(epochs):

    # Forward
    temp = np.dot(X, w_hidden)
    sgmd = np.vectorize(sigmoid)
    act_hidden = sgmd(temp)
    output = np.dot(act_hidden, w_output)

    # Calculate error
    error = Y - output

    if epoch % 5000 == 0:
        print(f'error sum {sum(error)}')

    # Backward
    dZ = error * LR
    w_output += act_hidden.T.dot(dZ)
    sgmd_prm = np.vectorize(sigmoid_prime)
    dH = dZ.dot(w_output.T) * sgmd_prm(act_hidden)
    w_hidden += X.T.dot(dH)
