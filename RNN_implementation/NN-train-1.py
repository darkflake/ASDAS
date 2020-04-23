import functools
import numpy as np
import tensorflow as tf
import pandas as pd
#from sklearn.model_selection import train_test_split

# Just disables the warning, doesn't enable AVX/FMA
import os
from tensorflow.keras import optimizers
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

LABEL_COLUMN = 'Label'
LABELS = [0, 1, 2, 3, 4]

'''dataframe = pd.read_csv(f'FinalData_band.csv')

train_df, test_df = train_test_split(dataframe, test_size=0.35)
train_df.to_csv('train.csv', index=False)
test_df.to_csv('test.csv', index=False)'''


def get_dataset(file_path, **kwargs):
    dataset = tf.data.experimental.make_csv_dataset(
        file_path,
        batch_size=5,  # Artificially small to make examples easier to show.
        label_name=LABEL_COLUMN,
        na_value="?",
        num_epochs=1,
        ignore_errors=True,
        **kwargs)
    return dataset


raw_train_data = get_dataset(f'train.csv')
raw_test_data = get_dataset(f'test.csv')


def show_batch(dataset):
    for batch, label in dataset.take(1):
        for key, value in batch.items():
            print("{:20s}: {}".format(key, value.numpy()))


show_batch(raw_train_data)


class PackNumericFeatures(object):
    def __init__(self, names):
        self.names = names

    def __call__(self, features, labels):
        numeric_features = [features.pop(name) for name in self.names]
        numeric_features = [tf.cast(feat, tf.float32) for feat in numeric_features] #casting to float32 datatype
        numeric_features = tf.stack(numeric_features, axis=-1)
        features['numeric'] = numeric_features

        return features, labels


NUMERIC_FEATURES = ['B11', 'B2', 'B3', 'B4', 'B8']

packed_train_data = raw_train_data.map(
    PackNumericFeatures(NUMERIC_FEATURES))

packed_test_data = raw_test_data.map(
    PackNumericFeatures(NUMERIC_FEATURES))

show_batch(packed_train_data)

example_batch, labels_batch = next(iter(packed_train_data))

desc = pd.read_csv(f'train.csv')[NUMERIC_FEATURES].describe()
print(desc)

MEAN = np.array(desc.T['mean'])
STD = np.array(desc.T['std'])


def normalize_numeric_data(data, mean, std):
    # Center the data
    return (data - mean) / std


# See what you just created.
normalizer = functools.partial(normalize_numeric_data, mean=MEAN, std=STD)

numeric_column = tf.feature_column.numeric_column('numeric', normalizer_fn=normalizer, shape=[len(NUMERIC_FEATURES)])
numeric_columns = [numeric_column]
print(numeric_column)

print(example_batch['numeric'])

numeric_layer = tf.keras.layers.DenseFeatures(numeric_columns)
print(numeric_layer(example_batch).numpy())

preprocessing_layer = tf.keras.layers.DenseFeatures(numeric_columns)
print(preprocessing_layer(example_batch).numpy()[0])

model = tf.keras.Sequential([
  preprocessing_layer,
  tf.keras.layers.Dense(4, activation='softmax'),
  tf.keras.layers.Dense(2, activation='softmax'),
  tf.keras.layers.Dense(1),
])

Adam = optimizers.Adam(learning_rate=1.00, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False,
    name='Adam')


model.compile(
    loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    optimizer=Adam,
    metrics=['accuracy'])

train_data = packed_train_data
test_data = packed_test_data

model.fit(train_data, epochs=20)
train_loss, train_accuracy = model.evaluate(train_data)
test_loss, test_accuracy = model.evaluate(test_data)

print('\n\nTest Loss {}, Test Accuracy {}'.format(test_loss, test_accuracy))

predictions = model.predict(test_data)
print(predictions)
'''# Show some results
for prediction, survived in zip(predictions[:5], list(test_data)[0][1][:5]):
  prediction = tf.sigmoid(prediction).numpy()
  print("Predicted survival: {:.2%}".format(prediction[0]),
        " | Actual outcome: ",
        ("SURVIVED" if bool(survived) else "DIED"))'''
