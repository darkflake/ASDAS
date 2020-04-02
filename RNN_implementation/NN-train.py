import tensorflow as tf
import os
import matplotlib.pyplot as plt
import pandas as pd

# for cpu instruction compatibility
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

column_names = ['B11', 'B2', 'B3', 'B4', 'B8', 'Label']
feature_names = column_names[:-1]
target_class = column_names[-1]
print(f'Features : {feature_names}')
print(f'Target : {target_class}')

class_name = ['Agriculture', 'BarrenLand', 'Forests', 'Infrastructure', 'Water']

batch_size = 50

train_dataset = tf.data.experimental.make_csv_dataset(
    f'FinalData_band.csv',
    batch_size,
    column_names=column_names,
    label_name=target_class,
    num_epochs=1
)

features, labels = next(iter(train_dataset))
print(features)

print(labels)


def pack_features_vector(features, labels):
    """Pack the features into a single array."""
    features = tf.stack(list(features.values()), axis=1)
    return features, labels


train_dataset = train_dataset.map(pack_features_vector)
features, labels = next(iter(train_dataset))
print(features[:5])

model = tf.keras.Sequential([
  tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=(5,)),  # input shape required
  tf.keras.layers.Dense(10, activation=tf.nn.relu),
  tf.keras.layers.Dense(5)
])

predictions = model(features)
print(predictions[:5])

tf.nn.softmax(predictions[:5])

print("Prediction: {}".format(tf.argmax(predictions, axis=1)))
print("    Labels: {}".format(labels))