from decisiontree import DecisionTree
from math import e, log2

class Adaboost(DecisionTree):

    def __init__(self, tree=None):
        super().__init__(tree)

    def generate(self, examples):
        """
        Generate a forest with weights given a list of processed
        examples. 
        :param examples: a list of named tuples formatted by DecisionTree.create_examples
        """
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
                if super().classify(xj, h[k]) != xj_class:
                    error += w[j]

                # adjust sample weights
                if super().classify(xj, h[k]) == xj_class:
                    w[j] = w[j] * pow(e, z[k])
                else:
                    w[j] = w[j] * pow(e, -z[k])

            w = normalize(w)
            z[k] = .5 * log2(((1-error)/error) + .0001)
        self.tree = list(zip(z, h))
        return self.tree

    def classify(self, examples, hypothesis=None):
        """
        Classify a list of examples or a single example using the internal
        Adaboost model or an external hypothesis which is a list of tuples 
        where the first attribute is a weight and the second is a decision stump

        :param examples: a list of examples created from DecisionTree.create_examples
        :param hypothesis: an external hypothesis to test
        """
        def traverse(example):
            totals = {key:0 for key in self.classes}
            classified = []
            for weight, h in hypothesis:
                # run the example through all the hypothesis
                classified.append((h[0], super(Adaboost, self).classify(example, h)))

            # figure out which of the classes the majority of stumps said
            for c in classified:
                # for each hypothesis result, get that hypothesis weight
                # and add it to the total
                totals[c[1]] += hypothesis[c[0]][0]
            return max(self.classes, key=lambda x: totals[x])

        # choose which hypothese to use, if one was passed in
        # prioritize that one over the one stored in self.tree
        if not hypothesis:
            hypothesis = self.tree

        if isinstance(examples, list):
            return [traverse(e) for e in examples]
        else:
            return traverse(examples)
        
    def print(self):
        for tree in self.tree:
            print(f"{self.attrs[tree[1][0]]}:(~{tree[0]:.2f})")
            for child in tree[1][1:]:
                print(f"    |---{child}")
