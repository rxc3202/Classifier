#! /usr/bin/python3
"""
Author: Ryan Cervantes (rxc3202)
Date: 11 November 2019
Filename: test_dt.py
"""
import sys
# used for testing
sys.path.append("..")
import re
from ast import literal_eval
import test_processing as processing
from decisiontree import DecisionTree
from adaboost import Adaboost

def usage():
    print("test_dt.py <ssize|depth> <training-set> <hypothesisOut> <testing-set>")

def process_file(filename, training=True):
    raw_text = []
    with open(filename, 'r') as f:
        raw_text = [re.sub("[^(a-zA-Z\d\-\s\|)]",'', line).strip("\n ").lower() for line in f]
    labeled_examples = []
    for example in raw_text:
        example = example.split("|")
        if training:
            labeled_examples.append(tuple([f(example[1]) for f in processing.processing_funcs] + [example[0]]))
        else:
            labeled_examples.append(tuple([f(example[0]) for f in processing.processing_funcs] + [None]))
    return labeled_examples


def handle_train(argv, size=None, depth=None):
    examples = process_file(argv[2], training=True)
    tree = None
    tree = DecisionTree()
    tree.define_positive_class(lambda x: x.classification == 'en')
    tree.define_classes(processing.classes)
    tree.define_attributes(processing.attr_definitions)
    if size:
        tree.load_examples(examples[:size])
    else:
        tree.load_examples(examples)
    if depth != None:
        tree.generate(tree.examples, depth)
    else:
        tree.generate(tree.examples)
    with open(argv[3], "w") as f:
        f.write("dt" + "\n")
        f.write(str(tree.tree))
    f.close()
    tree.print()


def handle_predict(argv):
    hypothesis = None
    model = None
    with open(argv[3], "r") as f:
        # DONT DO THIS ITS INSECURE. IM INSANE
        model = f.readline().strip('\n')
        hypothesis = f.readline()
    f.close()
    hypothesis = literal_eval(hypothesis)
    tree = None
    tree = DecisionTree()
    tree.define_positive_class(lambda x: x.classification == 'en')
    tree.define_classes(processing.classes)
    tree.define_attributes(processing.attr_definitions)
    examples = process_file(argv[4], training=False)
    examples = tree.create_examples(examples)
    return tree.classify(examples, hypothesis)


def main():
    def predict():
        results = handle_predict(sys.argv)
        dutch = 0
        english = 0
        for i in range(50):
            if i < 25 and results[i] != 'nl':
                dutch += 1
                continue
            if i >= 25 and results[i] != 'en':
                english += 1
        print(results)
        print(f"Dutch Error: %{dutch/25*100}")
        print(f"English Error: %{english/25*100}")

    if len(sys.argv) != 5:
        usage()
        sys.exit(1)
    if sys.argv[1] == "ssize":
        for size in range(10, 101, 10):
            print(f"===================== Sample Size: {size} =====================")
            handle_train(sys.argv, size)
            predict()
    else:
        for i in range(10):
            print(f"===================== Depth: {i+1} =====================")
            handle_train(sys.argv, depth=i)
            predict()


if __name__ == '__main__':
    main()
