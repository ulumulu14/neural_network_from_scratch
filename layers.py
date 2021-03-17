import numpy as np
from abc import ABC
from abc import abstractmethod


class Layer(ABC):

    def __init__(self, name=None):
        self.name = name

    @abstractmethod
    def forward(self, inputs):
        raise NotImplementedError()

    @abstractmethod
    def backward(self, d_inputs):
        raise NotImplementedError()

    #@abstractmethod
    #def structure(self):
        #raise NotImplementedError()


class Dense(Layer):

    def __init__(self, n_neurons: int, name=None):
        super().__init__(name)
        self.n_neurons = n_neurons
        self.inputs = None
        self.weights = None
        self.biases = np.zeros((1, n_neurons))
        self.d_weights = None
        self.d_biases = None
        self.d_inputs = None

    def forward(self, inputs):
        self.inputs = np.array(inputs)
        self.weights = 0.1 * np.random.randn(len(inputs[0]), self.n_neurons)

        return np.dot(self.inputs, self.weights) + self.biases

    def backward(self, d_inputs):
        self.d_inputs = d_inputs
        pass

    def get_details(self):
        return f'Name: {self.name} || Type: Dense || Output Size: {self.n_neurons}\n'

'''''
class Dense(Layer):

    def __init__(self, n_neurons: int, activation_function: str):
        super().__init__(n_neurons)
        self.inputs = None
        self.weights = None
        self.biases = np.zeros((1, n_neurons))
        self.activation_function = activation_function
        self.learning_rate = None

    def forward(self):
        if self.activation_function == "relu":
            return self.relu(self.linear(self.inputs, self.weights, self.biases))
        elif self.activation_function == "sigmoid":
            return self.sigmoid(self.linear(self.inputs, self.weights, self.biases))
        elif self.activation_function == "softmax":
            return self.softmax(self.linear(self.inputs, self.weights, self.biases))
        elif self.activation_function == None:
            return self.linear(self.inputs, self.weights, self.biases)
        else:
            raise Exception("Gówno")

    def backward(self, nl_gradient):
        #zapisywać output warstwy bo tu jest liczony drugi raz?
        if self.activation_function == "relu":
            activation_grad = self.relu_deriv(self.linear(self.inputs, self.weights, self.biases))
        elif self.activation_function == "sigmoid":
            activation_grad = self.sigmoid_deriv(self.linear(self.inputs, self.weights, self.biases))
        elif self.activation_function == "softmax":
            activation_grad = self.softmax_deriv(self.linear(self.inputs, self.weights, self.biases))

        weights_grad = self.weight_deriv(inputs=self.inputs, activation_grad=activation_grad)
        biases_grad = self.bias_deriv(activation_grad=activation_grad)

        self.weights += -self.learning_rate * weights_grad
        self.biases += -self.learning_rate * biases_grad

        return #cos co ma byc przekazane do nastepnej warstwy

    def gradient(self, y_true, y_pred):
        err_deriv = self.err_deriv(y_true, y_pred)
        local_gradient = err_deriv * self.sigmoid_deriv(self.linear(self.inputs, self.weights, self.biases))
        return local_gradient * self.inputs

    def update_weights(self, sums):
        for n in self.n_neurons:
            for i, weight in enumerate(self.weights[n]):
                weight = weight - self.learning_rate * sums[n] * self.inputs[i]

    def update_bias(self, sums):
        for i in self.n_neurons:
            self.biases[i] = self.biases[i] - self.learning_rate * sums[i]

    def error(self, y, y_hat):
        return np.sum(np.square(y - y_hat))

    def err_deriv(self, y, y_hat):
        return 2 * (y - y_hat)

    def read_input(self, inputs):
        self.inputs = np.array(inputs)
        self.weights = 0.1 * np.random.randn(len(inputs[0]), self.n_neurons)

    def linear(self, inputs, weights, biases):
        #return np.dot(self.weights, self.inputs) + self.biases
        return np.dot(inputs, weights) + biases

    def relu(self, inputs):
        return np.maximum(0, inputs)

    def sigmoid(self, inputs):
        return 1 / (1 + np.exp(-inputs))

    def softmax(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        return  exp_values / np.sum(exp_values, axis=1, keepdims=True)

    def linear_deriv(self, x):
        pass

    def weight_deriv(self, inputs, activation_grad):
        return np.dot(inputs.T, activation_grad)

    def bias_deriv(self, activation_grad):
        return np.sum(activation_grad, axis=0, keepdims=True)

    def relu_deriv(self, x):
        return np.greater(x, 0).astype(int)

    def sigmoid_deriv(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def softmax_deriv(self, x):

        pass

    def structure(self):
        return f"Neurons: {self.n_neurons} \nActivation function: {self.activation_function}\n"

class Linear(Layer):
    pass


class Input(Layer):
    pass


class Output(Layer):

    def __init__(self, n_neurons: int, activation_function: str):
        super().__init__(n_neurons)
        self.inputs = None
        self.weights = None
        self.biases = np.zeros((1, n_neurons))
        self.activation_function = activation_function
        #self.learning_rate = None

    def forward(self):
        if self.activation_function == "relu":
            return self.relu(self.linear(self.inputs, self.weights, self.biases))
        elif self.activation_function == "sigmoid":
            return self.sigmoid(self.linear(self.inputs, self.weights, self.biases))
        elif self.activation_function == "softmax":
            return self.softmax(self.linear(self.inputs, self.weights, self.biases))
        elif self.activation_function == None:
            return self.linear(self.inputs, self.weights, self.biases)
        else:
            raise Exception("Gówno")

    # ten backward pass to backward pass w warstwie output
    def backward(self, y_true, y_pred, learning_rate):
        sums = []
        gradients = self.gradient(y_true, y_pred)
        self.update_weights(gradients, learning_rate)
        self.update_bias(gradients, learning_rate)

        for input in range(len(self.inputs)):
            sums.append(np.sum(gradients * self.weights[input]))

        return sums

    def gradient(self, y_true, y_pred):
        err_deriv = self.err_deriv(y_true, y_pred)
        local_gradient = err_deriv * self.sigmoid_derivative(self.linear(self.inputs, self.weights, self.biases))
        return local_gradient * self.inputs

    def update_weights(self, gradients, learning_rate):
        for n in self.n_neurons:
            for i, weight in enumerate(self.weights[n]):
                weight = weight - learning_rate * gradients[n] * self.inputs[i]

    def update_bias(self, gradients, learning_rate):
        for i in self.n_neurons:
            self.biases[i] = self.biases[i] - learning_rate * gradients[i]

    def error(self, y, y_hat):
        return np.sum(np.square(y - y_hat))

    def err_deriv(self, y, y_hat):
        return 2 * (y - y_hat)

    def read_input(self, inputs):
        self.inputs = np.array(inputs)
        self.weights = 0.1 * np.random.randn(len(inputs[0]), self.n_neurons)

    def linear(self, inputs, weights, biases):
        # return np.dot(self.weights, self.inputs) + self.biases
        return np.dot(inputs, weights) + biases

    def relu(self, inputs):
        return np.maximum(0, inputs)

    def sigmoid(self, inputs):
        return 1 / (1 + np.exp(-inputs))

    def softmax(self, inputs):
        return np.exp(inputs) / np.sum(np.exp(inputs))

    def relu_derivative(self, x):
        return np.greater(x, 0).astype(int)

    def sigmoid_derivative(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def softmax_derivative(self, x):
        pass

    def structure(self):
        return f"Neurons: {self.n_neurons} \nActivation function: {self.activation_function}\n"
'''''