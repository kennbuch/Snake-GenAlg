import numpy as np
import time

class NN():
    
    def __init__(self, layer_dims, model_size, auto=True, weights=None):
        self.model_size = model_size

        layers = []

        # initialize layers
        for i in range(1, len(layer_dims)):
            layers.append(np.random.randint(-127, 128, (layer_dims[i-1], layer_dims[i])))

        # insert weights into layers
        self.model = np.array(layers)

    def predict(self, x, get_index=False):
        z = x
        for layer in self.model:
            z = np.dot(z, layer)
            #z = 1 / (1 + np.exp(-z))

        if get_index:
            return np.argmax(z)

        return z

    def set_weights(self, weights):
        # insert the given whights in to the model
        start = 0
        for i, layer in enumerate(self.model):
            j = start + layer.shape[0] * layer.shape[1]
            self.model[i] = weights[start:j].reshape(layer.shape)
            start = j

    def get_weights(self):
        # retrieve the weights of the model
        weights = np.zeros(self.model_size, dtype=np.float32)

        start = 0
        for layer in self.model:
            j = start + layer.shape[0] * layer.shape[1]
            weights[start:j] = layer.flatten()
            start = j
        
        return weights