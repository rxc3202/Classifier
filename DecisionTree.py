#! /usr/bin/python3
"""
File: DecisionTree.py
Author: Ryan Cervantes
"""
import math
from collections import namedtuple


class DecisionTree:

    POS_CLASS = ('A')

    ###           ###
    # CLASS METHODS #
    ###           ###

    @classmethod
    def fully_classified(cls, examples, classes):
        val = cls.plurality_value(examples, classes)
        return val == 1 or val == 0

    @classmethod
    def plurality_value(cls, examples, classes):
        # TODO: make this more extensible by not having to use indices for classes
        classifier = lambda x: x.classification == classes[0]
        total = sum(map(lambda x: 1 if classifier(x) else 0, examples))
        return total/len(examples)

    @classmethod
    def plurality(cls, examples, classes):
        return classes[0] if cls.plurality_value(examples, classes) > .5 else classes[1]
        
    
    @classmethod
    def H(cls, *probs):
        """
        Calculates Entropy H(V) given v0 - vk weights of decisions
        """
        try:
            return -1*sum(map(lambda vk : math.log2(vk)*vk, probs))
        except ValueError:
            return 0


    @classmethod
    def B(cls, q):
        """
        Calculates Entropy H(V) of a boolean variable given a weight
        """
        return cls.H(q, 1-q)


    @classmethod
    def Remainder(cls, examples, A, V, p, n):
        """
        Will calculate the total entropy remaining for a given set
        given an attribute A and V
        """
        remainder = 0
        for d in V: # over all distinct values of A
            Ek = list(filter(lambda dp: dp[A] == d, examples))
            pk, nk = cls.pos_neg(Ek, lambda dp: dp.classification in cls.POS_CLASS)
            partial = (pk + nk)/(p + n) * cls.B(pk/(pk + nk))
            remainder += partial
        return remainder


    @classmethod
    def Gain(cls, examples, A, V):
        """
        Calculates the information gain of the given attribute A
        that has V distinct values.
        """
        p, n = cls.pos_neg(examples, lambda x: x.classification in cls.POS_CLASS)
        return cls.B(p/(p+n)) - cls.Remainder(examples, A, V, p, n)
    
    @classmethod
    def pos_neg(cls, examples, classifier):
        pos = sum([1 if classifier(dp) else 0 for dp in examples])
        return (pos, len(examples) - pos)
    
    ###              ###
    # INSTANCE METHODS #
    ###              ###
    
    def __init__(self):
        self.examples = []
        self.classes = [] 
        self.attrs = []
        self._attr_spec = {}

    def define_attributes(self, *specs):
        attr_specifications = {}
        for spec in specs:
            attr_specifications[spec[0]] = spec[1:]
        self._attr_spec = attr_specifications

    def load_examples(self, attrs, tuples):
        """
        """
        Example = namedtuple('Example', attrs + ['classification'])
        self.examples.extend(list(map(Example._make, tuples)))
        self.classes.extend(set(map(lambda x: x[-1], tuples)))
        self.tree = None
        self.attrs.extend(attrs)
        self._used = set()

    def generate_tree(self, depth, examples, parent_examples=[], used_attrs=[]):
        def _generate(depth, examples, parent_examples, used_attrs):
            DT = DecisionTree
            used= list(used_attrs)
            # if examples is empty then return the majority of the parent
            if not examples:
                return DT.plurality(parent_examples, self.classes)
            # if they're all the same class return that class
            elif DT.fully_classified(examples, self.classes):
                return examples[0].classification
            # if there are no attributes left return majority of everyone
            elif not set(self.attrs) - set(used):
                return DT.plurality(examples, self.classes)
            # We can still generate the Tree
            else:
                # A <- argmax-a E attributes( IMPORTANCE(a, examples) )
                gain = []
                for i in range(0, len(self.attrs)):
                    if self.attrs[i] in used:
                        gain.append(-1)
                    else:
                        gain.append(DT.Gain(examples, i, ('True', 'False')))
                A = gain.index(max(gain))

                sub = []
                for vk in ('True', 'False'): 
                    # exs <- {e : e E examples and e.A = vk}
                    branch = list(filter(lambda dp: dp[A] == vk, examples))
                    # subtree <- DECISION-TREE-LEARNING(exs, attributes - A, examples)
                    if depth == 0:
                        sub.append(DT.plurality(examples, self.classes))
                    else:
                        used.append(self.attrs[A])
                        sub.append(_generate(depth-1, branch, examples, used))
                return (A, sub[0], sub[1])
        self.tree = _generate(depth, examples, parent_examples, used_attrs)


    def print_tree(self):
        def traverse(node, lvl=0):
            print('    ' * (lvl - 1), "|---" * (lvl > 0) + str(node[0]+1))
            for child in node[1:]:
                if child in self.classes:
                    print('    ' * lvl, "|---" + child)
                else:
                    traverse(child, lvl+1)
        traverse(self.tree)

            

if __name__ == '__main__':
    import sys
    training_set = []
    with open(sys.argv[1], "r") as data:
        training_set = [tuple(dp.strip(" \n").split(" ")) for dp in [l for l in data]]

    Tree = DecisionTree()
    Tree.load_examples(['attr1', 'attr2', 'attr3', 'attr4', 'attr5', 'attr6', 'attr7', 'attr8'], training_set)
    Tree.define_attributes(
            ('attr1', 'True', 'False'),
            ('attr2', 'True', 'False'),
            ('attr3', 'True', 'False'),
            ('attr4', 'True', 'False'),
            ('attr5', 'True', 'False'),
            ('attr6', 'True', 'False'),
            ('attr7', 'True', 'False'),
            ('attr8', 'True', 'False')
            )
    Tree.generate_tree(3, Tree.examples)
    print(Tree._attr_spec)
    Tree.print_tree()
