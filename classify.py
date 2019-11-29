#! /usr/bin/python3
"""
Author: Ryan Cervantes (rxc3202)
Date: 11 November 2019
Filename: classification.py
"""
import sys
import re
import processing
from ast import literal_eval
from processing import *
from DecisionTree import DecisionTree

def usage():
    print("classify.py <train> <examples> <hypothesisOut> <learning-type>")
    print("classify.py <predict> <hypothesis> <file>")

def process_file(filename, training=True):
    raw_text = []
    with open(filename, 'r') as f:
        raw_text = [re.sub("[,.]",'', line).strip("\n ") for line in f]
    labeled_examples = []
    for example in raw_text:
        example = example.split("|")
        if training:
            labeled_examples.append(tuple([f(example[1]) for f in processing_funcs] + [example[0]]))
        else:
            labeled_examples.append(tuple([f(example[0]) for f in processing_funcs] + [None]))
    return labeled_examples


def handle_train(argv):
    examples = process_file(argv[2], training=True)
    tree = DecisionTree()
    tree.define_positive_class(lambda x: x.classification == 'en')
    tree.define_classes(processing.classes)
    tree.define_attributes(processing.attr_definitions)
    tree.load_examples(examples)
    tree.generate_tree(tree.examples)
    with open(argv[3], "w") as f:
        f.write(str(tree.tree))
    f.close()
    tree.print_tree()


def handle_predict(argv):
    hypothesis = None
    with open(argv[2], "r") as f:
        # DONT DO THIS ITS INSECURE. IM INSANE
        hypothesis = f.readline()
    f.close()
    hypothesis = literal_eval(hypothesis)
    tree = DecisionTree(hypothesis)
    tree.define_positive_class(lambda x: x.classification == 'en')
    tree.define_classes(processing.classes)
    tree.define_attributes(processing.attr_definitions)
    examples = process_file(argv[3], training=False)
    examples = tree.create_examples(examples)
    for classification in tree.classify(examples):
        print(classification)

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
