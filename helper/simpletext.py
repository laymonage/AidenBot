'''
Echo helper module
(c) 2018 - laymonage
'''

import random


def echo(text):
    '''
    Return echo function.
    '''
    return text


def shout(text):
    '''
    Return text in uppercase.
    '''
    return text.upper()


def mock(text):
    '''
    rEtURn tExT iN raNdoMcASe.
    '''
    result = ''
    for c in text:
        d = random.choice([c.upper(), c.lower()])
        if d.isupper() and result[-1:-3:-1].isupper():
            d = d.lower()
        elif d.islower() and result[-1:-3:-1].islower():
            d = d.upper()
        result += d
    return result


def is_palindrome(text, perfect=False):
    '''
    Return a palindrome checking result of text
    (case-insensitive alphanumeric string).
    if perfect is True, then text must be a perfect palindrome.
    '''
    if perfect:
        if text == text[::-1]:
            return text + " is a perfect palindrome!"
        return text + " is not a perfect palindrome."
    test = ''.join(c.lower() for c in text if c.isalnum())
    if test == test[::-1]:
        return text + " is a palindrome!"
    return text + " is not a palindrome."


def rng(ceil, floor=1):
    '''
    Return a random integer from floor to ceil (inclusive).
    '''
    try:
        floor, ceil = int(floor), int(ceil)
        result = ("From {} to {}, I pick {}."
                  .format(floor, ceil, str(random.randint(floor, ceil))))
    except ValueError:
        result = "Wrong format."
    return result


def rpick(text):
    '''
    Pick a random item from a semicolon-separated list in a string.
    '''
    return "I pick {}.".format(random.choice(text.split(';')))
