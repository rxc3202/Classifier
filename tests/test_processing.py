#! /usr/bin/python3
"""
Filename: test_processing.py
"""


def has_aa(text):
    text = text.split(' ')
    for word in text:
        if "aa" in word:
            return True
    return False

def has_the(text):
    text = text.split(' ')
    for word in text:
        if word == "the":
            return True
    return False


def has_jn(text):
    text = text.split(' ')
    for word in text:
        if "jn" in word:
            return True
    return False


def has_de(text):
    text = text.split(' ')
    for word in text:
        if "de" == word:
            return True
    return False


def has_van(text):
    text = text.split(' ')
    for word in text:
        if "van" == word:
            return True
    return False


def has_a(text):
    text = text.split(' ')
    for word in text:
        if "a" == word:
            return True
    return False


def has_jk(text):
    text = text.split(' ')
    for word in text:
        if "jk" in word:
            return True
    return False


def ends_en(text):
    text = text.split(' ')
    for word in text:
        if word[-2:] == "en":
            return True
    return False


def has_uu(text):
    text = text.split(' ')
    for word in text:
        if "uu" in word:
            return True
    return False


def has_oo(text):
    text = text.split(' ')
    for word in text:
        if "oo" in word:
            return True
    return False


def has_of(text):
    text = text.split(' ')
    for word in text:
        if "of" == word:
            return True
    return False

def has_ee(text):
    text = text.split(' ')
    for word in text:
        if "ee" in word:
            return True
    return False

def has_oo(text):
    text = text.split(' ')
    for word in text:
        if "oo" in word:
            return True
    return False

#icht ending

processing_funcs = [
    has_aa,
    has_uu,
    has_the,
    #has_jn,
    #has_de,
    #has_van,
    has_a,
    ends_en,
    #has_oo,
    has_of,
    has_ee,

]

classes = ['en', 'nl']
attr_definitions = [
        ("aa", True, False),
        ("uu", True, False),
        ("the", True, False),
        #("jn", True, False),
        #("de", True, False),
        #("van", True, False),
        ("a", True, False),
        ("en_ending", True, False),
        #("oo", True, False),
        ("of", True, False),
        ("ee", True, False),
]
attr_names = [x[0] for x in attr_definitions]
