import numpy as np
from .StreamingGradientTree import StreamingGradientTree


class StreamingGradientTreeNetwork:

    def __init__(self, featureInfo, options, numTrees, layers):

        self.mTrees = [StreamingGradientTree(featureInfo, options) for _ in range(numTrees)]

        self.layers = layers

    def getNumNodes(self):
        return sum([tree.getNumNodes() for tree in self.mTrees])

    def getNumNodeUpdates(self):
        return sum([tree.getNumNodeUpdates() for tree in self.mTrees])
    
    def getNumSplits(self):
        return sum([tree.getNumSplits() for tree in self.mTrees])
    
    def getMaxDepth(self):
        return np.amax([tree.getDepth() for tree in self.mTrees])

    def getNumTrees(self):
        return len(self.mTrees)

    def randomlyInitialize(self, rng, predBound):
        for tree in self.mTrees:
            tree.randomlyInitialize(rng, predBound)
    
    def update(self, features, gradHesses):
        activations = []
        activations.append([tree.predict(features) for tree in self.mTrees])

        for i in range(len(self.layers)):
            activations.append(self.layers[i].predict(activations[i]))

        for i in range(len(self.layers)-1, 0, -1):
            gradHesses = self.layers[i].update(activations[i], gradHesses)

        [tree.update(features, gradHesses[i]) for i, tree in enumerate(self.mTrees)]

    def predict(self, features):
        activations = []
        activations.append([tree.predict(features) for tree in self.mTrees])

        for i in range(len(self.layers)):
            activations.append(self.layers[i].predict(activations[i]))

        return activations

class IdentityLayer:
    def __init__(self):
        pass
    
    def update(self, features, gradHess):
        return gradHess.copy()
    
    def predict(self, features):
        return features.copy()
