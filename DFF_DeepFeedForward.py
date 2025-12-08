import numpy as np

# use numpy module

class DFF_DeepFeedForward(object):
    def __init__(self, cellList, activationV="sigmoid", factor=1, gap=0):

        self.activationV = activationV
        self.factor = factor
        self.gap = gap

        self.cellSize = cellList
        self.inputSize = cellList[0]
        self.outputSize = cellList[len(cellList)-1]

        self.hiddenSize = []
        for i in range(1, len(cellList) - 1):
            self.hiddenSize.append(cellList[i])


        # synapses configuration
        self.W = []
        for i in range(len(self.cellSize)-1):
            self.W.append(np.random.randn(self.cellSize[i], self.cellSize[i+1]))


    def activation(self, x):
        if self.activationV=="sigmoid":
            res =  1/(1+np.exp(-x))
        elif self.activationV=="sigmoidL":
            res = x / (1+np.exp(-x))
        elif self.activationV=="identity":
            res = x
        elif self.activationV=="gaussian":
            res = np.exp(-x)**2
        elif self.activationV=="tanh":
            res = ((np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x)))
        return (res+self.gap) * self.factor

    def activationPrime(self, x):
        if self.activationV=="sigmoid":
            res = x*(1-x)
        elif self.activationV=="sigmoidL":
            res = (1+np.exp(-x) + x*np.exp(-x)) / ((1+np.exp(-x))**2)
        elif self.activationV=="identity":
            res = 1
        elif self.activationV=="gaussian":
            res = -2*x*np.exp(-x)**2
        elif self.activationV=="tanh":
            res = 1-(activationV(x)**2)
        return res*self.factor


    def forward(self, x):
        self.z = []

        self.z.append(self.activation(np.dot(x, self.W[0]))) # inputs start
        for i in range(1, len(self.W) - 1): # sans le input "1", et sans le output "-1"
            self.z.append(self.activation(np.dot(self.z[i-1], self.W[i]))) # inputs start

        o = self.activation(np.dot( self.z[-1],  self.W[-1] ))

        return o


    def backward(self, x, y, o):

        self.z_error_delta = [np.array([])] * len(self.z)

        self.o_error = y-o
        self.o_error_delta = self.o_error*self.activationPrime(o)

        self.z_error_delta[-1] = np.dot(self.o_error_delta,  self.W[-1].T ) * self.activationPrime( self.z[-1] )

        for i in range(len(self.hiddenSize) - 1):
            self.z_error_delta[-(i+2)] = np.dot(self.z_error_delta[-(i+1)],  self.W[-(i+2)].T ) * self.activationPrime( self.z[-(i+2)] )


        self.W[0] += np.dot(x.T, self.z_error_delta[0])
        for i in range(1, len(self.W)-1):
            self.W[i] += np.dot(self.z[i-1].T, self.z_error_delta[i])

        self.W[-1] += np.dot(self.z[-1].T, self.o_error_delta)

    def train(self, x, y):
        o = self.forward(x)
        self.backward(x, y, o)
