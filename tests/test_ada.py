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
    print("test_ada.py <rotate|normal> <training-set> <hypothesisOut> <testing-set>")

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
    tree = Adaboost()
    tree.define_positive_class(lambda x: x.classification == 'en')
    tree.define_classes(processing.classes)
    tree.define_attributes(processing.attr_definitions)
    tree.load_examples(examples)
    tree.generate(tree.examples)
    with open(argv[3], "w") as f:
        f.write("ada" + "\n")
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
    tree = Adaboost()
    tree.define_positive_class(lambda x: x.classification == 'en')
    tree.define_classes(processing.classes)
    tree.define_attributes(processing.attr_definitions)
    examples = process_file(argv[4], training=False)
    examples = tree.create_examples(examples)
    return tree.classify(examples, hypothesis)


def main():
    from collections import deque
    if len(sys.argv) != 5:
        usage()
        sys.exit(1)
    a = deque(processing.attr_definitions)
    b = deque(processing.attr_names)
    c = deque(processing.processing_funcs)
    if sys.argv[1] == "rotate":
        for i in range(11):
            print(f"=========== Rotation {i} ===========")
            a.rotate()
            b.rotate()
            c.rotate()
            # bad practice nono but just for testing
            processing.attr_definitions = list(a)
            processing.attr_names = list(b)
            processing.processing_funcs = list(c)

            handle_train(sys.argv)
            results = handle_predict(sys.argv)
            dutch = 0
            english = 0
            for i in range(50):
                if i < 25 and results[i] != 'nl':
                    dutch += 1
                    continue
                if i >= 25 and results[i] != 'en':
                    english += 1
            #print(results)
            print(f"Dutch Error: %{dutch/25*100}")
            print(f"English Error: %{english/25*100}")
    else:
        handle_train(sys.argv)
        results = handle_predict(sys.argv)
        dutch = 0
        english = 0
        for i in range(50):
            if i < 25 and results[i] != 'nl':
                dutch += 1
                continue
            if i >= 25 and results[i] != 'en':
                english += 1
        #print(results)
        print(f"Dutch Error: %{dutch/25*100}")
        print(f"English Error: %{english/25*100}")


if __name__ == '__main__':
    main()
