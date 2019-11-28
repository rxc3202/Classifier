#! /usr/bin/python3
"""
Author: Ryan Cervantes (rxc3202)
Date: 11 November 2019
Filename: classification.py
"""
import sys
import re
from ast import literal_eval
from processing import *
from processing import processing_funcs
from DecisionTree import DecisionTree

def usage():
    print("classify.py <train> <examples> <hypothesisOut> <learning-type>")
    print("classify.py <predict> <hypothesis> <file>")

def process_file(filename):
    examples = []
    with open(filename, 'r') as f:
        examples = [re.sub("[,.]",'', line).strip("\n ") for line in f]
    return [tuple( [f(l.split("|")[1]) for f in processing_funcs] + [l.split("|")[0]]) for l in examples] 


def handle_train(argv):
    examples = process_file(argv[2])
    tree = DecisionTree()
    tree.define_positive_class(lambda x: x.classification == 'en')
    tree.load_examples(["oo", "aa", "ee", "uu"], examples)
    tree.define_attributes(
        ("oo", True, False),
        ("aa", True, False),
        ("ee", True, False),
        ("uu", True, False))
    tree.generate_tree(tree.examples)
    with open(argv[3], "w") as f:
        f.write(str(tree.tree))
    f.close()


def handle_predict(argv):
    hypothesis = None
    with open(argv[2], "r") as f:
        # DONT DO THIS ITS INSECURE. IM INSANE
        hypothesis = f.readline()
    hypothesis = literal_eval(hypothesis)
    tree = DecisionTree(hypothesis)
    tree.define_classes(['en', 'nl'])
    tree.define_positive_class(lambda x: x.classification == 'en')
    tree.define_attributes(
        ("oo", True, False),
        ("aa", True, False),
        ("ee", True, False),
        ("uu", True, False))
    from collections import namedtuple
    test_example = namedtuple(
            'Example', 
            ["oo", "aa", "ee", "uu"]
        )._make((False, False, True, False))
    print(tree.classify([test_example]))

def main():
    if sys.argv[1] == "train":
        if len(sys.argv) != 5:
            usage()
            sys.exit(1)
        handle_train(sys.argv)
    elif sys.argv[1] == "predict":
        if len(sys.argv) != 4:
            usage()
            sys.exit(1)
        handle_predict(sys.argv)
    else:
        usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
