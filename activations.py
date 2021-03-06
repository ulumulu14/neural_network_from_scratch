import numpy as np
import layers


class ReLU(layers.Layer):

    def __init__(self, name=None):
        super(ReLU, self).__init__(trainable=False, name=name)
        self._inputs = None
        self._d_inputs = None

    @property
    def inputs(self):
        if self._inputs is None:
            raise ValueError('inputs is None')

        return self._inputs

    @property
    def d_inputs(self):
        if self._d_inputs is None:
            raise ValueError('d_inputs is None')

        return self._d_inputs

    @inputs.setter
    def inputs(self, inputs):
        self._inputs = inputs

    @d_inputs.setter
    def d_inputs(self, d_inputs):
        self._d_inputs = d_inputs

    def forward(self, inputs, training=True):
        self.inputs = inputs

        return np.maximum(0, self.inputs)

    def backward(self, gradient):
        # gradient argument is gradient of next layer

        self.d_inputs = gradient.copy()

        # Gradient w.r.t inputs
        self.d_inputs[self.inputs <= 0] = 0

        return self.d_inputs

    def get_details(self):
        return f'Name: {self.name} || Type: ReLU || Output Size: {len(self.inputs)}\n'


class Softmax(layers.Layer):

    def __init__(self, name=None):
        super(Softmax, self).__init__(trainable=False, name=name)
        self._inputs = None
        self._d_inputs = None
        self._output = None

    @property
    def inputs(self):
        if self._inputs is None:
            raise ValueError('inputs is None')

        return self._inputs

    @property
    def d_inputs(self):
        if self._d_inputs is None:
            raise ValueError('d_inputs is None')

        return self._d_inputs

    @property
    def output(self):
        if self._output is None:
            raise ValueError('output is None')

        return self._output

    @inputs.setter
    def inputs(self, inputs):
        self._inputs = inputs

    @d_inputs.setter
    def d_inputs(self, d_inputs):
        self._d_inputs = d_inputs

    @output.setter
    def output(self, output):
        self._output = output

    def forward(self, inputs, training=True):
        self.inputs = inputs
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        self.output = exp_values / np.sum(exp_values, axis=1, keepdims=True)

        return self.output

    def backward(self, gradient):
        # gradient argument is gradient of next layer

        self.d_inputs = np.empty_like(gradient)

        for i, (single_output, partial_deriv) in enumerate(zip(self.output, gradient)):
            single_output = single_output.reshape(-1, 1)
            jacobian = np.diagflat(single_output) - np.dot(single_output, single_output.T)

            # Calculate sample-wise gradient w.r.t inputs
            self.d_inputs[i] = np.dot(jacobian, partial_deriv)

        return self.d_inputs

    def predictions(self, outputs):
        return np.argmax(outputs, axis=1)

    def get_details(self):
        return f'Name: {self.name} || Type: Softmax || Output Size: {len(self.inputs)}\n'


class Sigmoid(layers.Layer):

    def __init__(self, name=None):
        super().__init__(trainable=False, name=name)
        self._inputs = None
        self._d_inputs = None
        self._output = None

    @property
    def inputs(self):
        if self._inputs is None:
            raise ValueError('inputs is None')

        return self._inputs

    @property
    def d_inputs(self):
        if self._d_inputs is None:
            raise ValueError('d_inputs is None')

        return self._d_inputs

    @property
    def output(self):
        if self._output is None:
            raise ValueError('output is None')

        return self._output

    @inputs.setter
    def inputs(self, inputs):
        self._inputs = inputs

    @d_inputs.setter
    def d_inputs(self, d_inputs):
        self._d_inputs = d_inputs

    @output.setter
    def output(self, output):
        self._output = output

    def forward(self, inputs, training=True):
        self.inputs = inputs
        self.output = 1 / (1 + np.exp(-self._inputs))
        return self.output

    def backward(self, gradient):
        # gradient argument is gradient of next layer

        self.d_inputs = gradient * (1-self.output) * self.output

        return self.d_inputs

    def predictions(self, outputs):
        return (outputs > 0.5) * 1

    def get_details(self):
        return f'Name: {self.name} || Type: Sigmoid || Output Size: {len(self.inputs)}\n'


class Linear(layers.Layer):

    def __init__(self, name=None):
        super().__init__(trainable=False, name=name)
        self._inputs = None
        self._d_inputs = None
        self._output = None

    @property
    def inputs(self):
        if self._inputs is None:
            raise ValueError('inputs is None')

        return self._inputs

    @property
    def d_inputs(self):
        if self._d_inputs is None:
            raise ValueError('d_inputs is None')

        return self._d_inputs

    @property
    def output(self):
        if self._output is None:
            raise ValueError('output is None')

        return self._output

    @inputs.setter
    def inputs(self, inputs):
        self._inputs = inputs

    @d_inputs.setter
    def d_inputs(self, d_inputs):
        self._d_inputs = d_inputs

    @output.setter
    def output(self, output):
        self._output = output

    def forward(self, inputs, training=True):
        self.inputs = inputs
        self.output = inputs
        return self.output

    def backward(self, gradient):
        # gradient argument is gradient of next layer

        self.d_inputs = gradient.copy()

        return self.d_inputs

    def predictions(self, outputs):
        return outputs

    def get_details(self):
        return f'Name: {self.name} || Type: Linear || Output Size: {len(self.inputs)}\n'