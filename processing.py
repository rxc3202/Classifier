#! /usr/bin/python3
"""
Filename: processing.py
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

def has_gt2z(text):
    text = text.split(' ')
    count = 0
    for word in text:
        if "z" in word:
            count+= 1
    return count > 2


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

processing_funcs = [
    has_aa,
    has_uu,
    has_the,
    has_jn,
    has_de,
    has_gt2z,
    has_van,
    has_a,
    ends_en
]

classes = ['en', 'nl']
attr_names = ["aa", "uu", "the", "jn", "de", "gt2z", "van", "a", "en_ending"]
attr_definitions = [
        ("aa", True, False),
        ("uu", True, False),
        ("the", True, False),
        ("jn", True, False),
        ("de", True, False),
        ("gt2z", True, False),
        ("van", True, False),
        ("a", True, False),
        ("en_ending", True, False)
]
