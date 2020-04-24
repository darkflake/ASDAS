# first neural network with keras tutorial
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import pandas as pd

...
# load the dataset
dataset = loadtxt(f'FinalData_band.csv', delimiter=',', skiprows=1)
# split into input (X) and output (y) variables
'''X = dataset[:, 0:5]
print(X)
y = dataset[:, 5]
B11 = loadtxt(f'FinalData_band.csv', delimiter=',', skiprows=1, usecols=0)
B2 = loadtxt(f'FinalData_band.csv', delimiter=',', skiprows=1, usecols=1)
B3 = loadtxt(f'FinalData_band.csv', delimiter=',', skiprows=1, usecols=2)
B4 = loadtxt(f'FinalData_band.csv', delimiter=',', skiprows=1, usecols=3)
B8 = loadtxt(f'FinalData_band.csv', delimiter=',', skiprows=1, usecols=4)

B11_std = np.std(B11)
B2_std = np.std(B2)
B3_std = np.std(B3)
B4_std = np.std(B4)
B8_std = np.std(B8)

B11_mean = np.mean(B11)
B2_mean = np.mean(B2)
B3_mean = np.mean(B3)
B4_mean = np.mean(B4)
B8_mean = np.mean(B8)
print(B11_std, B2_std, B3_std, B4_std, B8_std)
print(B11_mean, B2_mean, B3_mean, B4_mean, B8_mean)


def normalization(x, mean=None, std=None):
    x = (x - mean) / std
    return x


B11_reformatted = np.apply_along_axis(normalization, 0, B11, mean=B11_mean, std=B11_std)
B2_reformatted = np.apply_along_axis(normalization, 0, B2, mean=B2_mean, std=B2_std)
B3_reformatted = np.apply_along_axis(normalization, 0, B3, mean=B3_mean, std=B3_std)
B4_reformatted = np.apply_along_axis(normalization, 0, B4, mean=B4_mean, std=B4_std)
B8_reformatted = np.apply_along_axis(normalization, 0, B8, mean=B8_mean, std=B8_std)
print(B11_reformatted, B2_reformatted, B3_reformatted, B4_reformatted, B8_reformatted)

dataframe = pd.DataFrame({B11_reformatted, B2_reformatted, B3_reformatted, B4_reformatted, B8_reformatted})
dataframe_reformatted = dataframe.to_numpy()
print(dataframe_reformatted)

data = np.asarray([B11_reformatted, B2_reformatted, B3_reformatted, B4_reformatted, B8_reformatted])
print(data.shape)
data_transpose = np.transpose(data)
print(data_transpose)
X = data_transpose'''

df = pd.read_csv(f'FinalData_band.csv')
df = df.div(10000).round(7)
y = df.pop(f'Label')
X = df.to_numpy()
# define the keras model
model = Sequential()
model.add(Dense(12, input_dim=5, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
model.fit(X, y, epochs=150, batch_size=10)

# evaluate the keras model
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy * 100))

predictions = model.predict_classes(X)
# summarize the first 5 cases
for i in range(5):
    print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))
