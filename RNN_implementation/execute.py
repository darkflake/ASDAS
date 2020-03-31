import importlib

mnist_loader = importlib.import_module('mnist_loader')

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
test_data = list(test_data)
training_data = list(training_data)
validation_data = list(validation_data)
'''network = importlib.import_module('network')


print(len(training_data), len(test_data), len(validation_data))
net = network.Network([784,100,50,10])

net.SGD(training_data, 30, 10, 3.0, test_data=test_data)
'''

network2 = importlib.import_module('network2')

net = network2.Network([784, 30, 10])
cost = network2.CrossEntropyCost()

net.large_weight_initializer()

net.SGD(training_data[:1000], 400, 10, 0.5, niin  = 10, evaluation_data=test_data, monitor_evaluation_accuracy=True,
        monitor_training_accuracy=True, monitor_training_cost=True)
