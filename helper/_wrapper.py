'''
Helper wrapper module

Wrap results from more complex helper modules
into tuples suitable for use with quickreply
function defined in app.py.

Example:
('text', ("Hello", "This is a wrapper module."))
('image', (imagelink1, imagelink2))
('custimg', ((imgorig1, imgprev1), (imgorig2, imgprev2)))
('multi', (('text', "Hello"),
           ('image', imagelink)))
'''

from . import (
    AkunBenCoin, cat, stalkig, surprise, wolfram
)


def cat_wrap():
    '''
    Wrap cat command.
    '''
    return ('image', cat())


def stalkig_wrap(username):
    '''
    Wrap stalkig command.
    If result[0] == False then result is not found.
    '''
    result = stalkig(username)
    if result[0]:
        return ('multi', (('image', result[0]),
                          ('text', result[1])))
    return ('text', result[1])


def surprise_wrap():
    '''
    ?
    '''
    return ('custimg', (surprise(),))


def wolfram_wrap(query):
    '''
    Wrap wolfram (simple mode) command.
    '''
    return ('image', wolfram(query, simple=True))
