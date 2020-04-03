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

batch_size = 30

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
print(labels)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(5, activation=tf.nn.sigmoid_cross_entropy_with_logits, input_shape=(5,)),  # input shape required
    tf.keras.layers.Dense(4, activation=tf.nn.sigmoid_cross_entropy_with_logits),
    tf.keras.layers.Dense(3, activation=tf.nn.sigmoid_cross_entropy_with_logits),
    tf.keras.layers.Dense(5)
])

predictions = model(features)
print(predictions[:5])

tf.nn.softmax(predictions[:5])

print("Prediction: {}".format(tf.argmax(predictions, axis=1)))
print("    Labels: {}".format(labels))

loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)


def loss(model, x, y, training):
    y_ = model(x, training=training)

    return loss_object(y_true=y, y_pred=y_)


l = loss(model, features, labels, training=False)
print("Loss test: {}".format(l))


def grad(model, inputs, targets):
    with tf.GradientTape() as tape:
        loss_value = loss(model, inputs, targets, training=True)
    return loss_value, tape.gradient(loss_value, model.trainable_variables)


optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

loss_value, grads = grad(model, features, labels)

print("Step: {}, Initial Loss: {}".format(optimizer.iterations.numpy(),
                                          loss_value.numpy()))

optimizer.apply_gradients(zip(grads, model.trainable_variables))

print("Step: {},         Loss: {}".format(optimizer.iterations.numpy(),
                                          loss(model, features, labels, training=True).numpy()))

## Note: Rerunning this cell uses the same model variables

# Keep results for plotting
train_loss_results = []
train_accuracy_results = []

num_epochs = 201

for epoch in range(num_epochs):
    epoch_loss_avg = tf.keras.metrics.Mean()
    epoch_accuracy = tf.keras.metrics.SparseCategoricalAccuracy()

    # Training loop - using batches of 32
    for x, y in train_dataset:
        # Optimize the model
        loss_value, grads = grad(model, x, y)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        # Track progress
        epoch_loss_avg(loss_value)  # Add current batch loss
        # Compare predicted label to actual label
        # training=True is needed only if there are layers with different
        # behavior during training versus inference (e.g. Dropout).
        epoch_accuracy(y, model(x, training=True))

    # End epoch
    train_loss_results.append(epoch_loss_avg.result())
    train_accuracy_results.append(epoch_accuracy.result())

    if epoch % 50 == 0:
        print("Epoch {:03d}: Loss: {:.3f}, Accuracy: {:.3%}".format(epoch,
                                                                    epoch_loss_avg.result(),
                                                                    epoch_accuracy.result()))
