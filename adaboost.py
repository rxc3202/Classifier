from DecisionTree import DecisionTree
from math import e, log2

class Adaboost(DecisionTree):

    def __init__(self, tree=None):
        super().__init__(tree)

    def generate(self, examples):
        def weighted_majority(h, z):
            return [(z[i],h[i]) for i in range(len(h))]

        def normalize(w):
            return [float(i)/sum(w) for i in w]

        # sample weights
        w = [1/len(examples) for e in examples]
        # stump weights
        z = [1 for _ in range(len(self.attrs))]
        # stumps
        h = []

        # create a stump for each attribute
        for k in range(len(self.attrs)):
            attr = self.attrs[k]
            mask = set(self.attrs) - set([attr])
            x = super().generate(examples, 1, mask)
            h.append(x)
            error = 0
            for j in range(len(examples)):
                xj = examples[j]
                xj_class = examples[j].classification
                # add up the total error for this stump
                if self.classify(xj, h[k]) != xj_class:
                    error += w[j]

                # adjust sample weights
                if self.classify(xj, h[k]) == xj_class:
                    w[j] = w[j] * pow(e, z[k])
                else:
                    w[j] = w[j] * pow(e, -z[k])

            w = normalize(w)
            z[k] = log2(((1-error)/error) + .0001)
        self.tree = weighted_majority(h, z)

    def classify(self, examples, ensemble):
        pass
    

    def print(self):
        print(self.tree)
