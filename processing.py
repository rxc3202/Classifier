#! /usr/bin/python3
"""
Filename: processing.py
"""


def has_double_oo(text):
    text = text.split(' ')
    for word in text:
        if "oo" in word:
            return True
    return False


def has_double_aa(text):
    text = text.split(' ')
    for word in text:
        if "aa" in word:
            return True
    return False


def has_double_ee(text):
    text = text.split(' ')
    for word in text:
        if "oo" in word:
            return True
    return False


def has_double_uu(text):
    text = text.split(' ')
    for word in text:
        if "uu" in word:
            return True
    return False


def has_word_zijn(text):
    text = text.split(' ')
    for word in text:
        if word == "zijn":
            return True
    return False


def van_count_gt_2(text):
    return text.count("van") >= 2


def has_word_a(text):
    text = text.split(' ')
    for word in text:
        if word == "a":
            return True
    return False


def count_en_ending(text):
    text = text.split(' ')
    for word in text:
        if word[-2:] == "en":
            return True
    return False


def has_word_gt15(text):
    text = text.split(' ')
    for word in text:
        if len(word) > 15:
            return True
    return False

processing_funcs = [
    has_double_oo,
    has_double_aa,
    has_double_ee,
    has_double_uu
]


def process_file(filename):
    examples = []
    with open(filename, 'r') as f:
        examples = [re.sub("[,.]",'', line).strip("\n ") for line in f]
    return [tuple([func(l.split("|")[1]) for func in processing_funcs] + [l.split("|")[0]]) for l in examples]


if __name__ == '__main__':
    import sys
    import re
    from collections import namedtuple
    from DecisionTree import DecisionTree
    examples = []
    examples.extend(process_file("etc/language-data.txt"))
    Tree = DecisionTree()
    Tree.define_positive_class(lambda dp: dp.classification == 'en')
    Tree.define_classes(['en', 'nl'])
    Tree.load_examples(["oo", "aa","ee","uu"], examples)
    Tree.define_attributes(
        ("oo", True, False),
        ("aa", True, False),
        ("ee", True, False),
        ("uu", True, False))
    Tree.generate_tree(Tree.examples)
    Tree.print_tree()
    test_example = namedtuple(
            'Example', 
            ["oo", "aa", "ee", "uu"]
        )._make((False, False, True, False))
    print(Tree.classify([test_example]))
