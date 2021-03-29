import network
import layers
import activations
import losses
import optimizers
import numpy as np
import nnfs
from nnfs.datasets import spiral_data
from sklearn import datasets

nnfs.init()


if __name__ == "__main__":
    EPOCHS = 10001
    LEARNING_RATE = 0.001

    X, y = spiral_data(samples=100, classes=2)

    y = y.reshape(-1, 1)
    iris = datasets.load_iris()
    #X = iris.data[:, :2]
    #y = iris.target

    dense1 = layers.Dense(2, 64, weight_regularizer_l2=0.0005, bias_regularizer_l2=0.0005)
    relu1 = activations.ReLU()
    dense2 = layers.Dense(64, 1)
    sigmoid1 = activations.Sigmoid()

    loss_function = losses.BinaryCrossentropy()
    optimizer = optimizers.Adam(learning_rate=LEARNING_RATE, decay=0.0000005)

    for epoch in range(EPOCHS):
        x = dense1.forward(X)
        x = relu1.forward(x)
        x = dense2.forward(x)
        output = sigmoid1.forward(x)

        data_loss = loss_function.calculate(output, y)
        regularization_loss = loss_function.regularization_loss(dense1) + loss_function.regularization_loss(dense2)
        loss = data_loss + regularization_loss
        predictions = (output > 0.5) * 1
        accuracy = np.mean(predictions == y)

        if epoch % 100 == 0:
            print(f'epoch: {epoch}/{EPOCHS} || accuracy: {accuracy:.3f} || loss: {loss:.3f}')

        grad = loss_function.backward(output, y)
        grad = sigmoid1.backward(grad)
        grad = dense2.backward(grad)
        grad = relu1.backward(grad)
        grad = dense1.backward(grad)

        optimizer.update_params(dense1)
        optimizer.update_params(dense2)
        optimizer.update_learning_rate()

    X_test, y_test = spiral_data(samples=100, classes=2)

    y_test = y_test.reshape(-1, 1)

    x = dense1.forward(X_test)
    x = relu1.forward(x)
    x = dense2.forward(x)
    output = sigmoid1.forward(x)

    val_loss = loss_function.calculate(output, y_test)
    predictions = (output > 0.5) * 1

    val_acc = np.mean(predictions == y_test)

    print(f'val_acc: {val_acc} || val_loss: {val_loss}')
