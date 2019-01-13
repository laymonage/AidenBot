'''
Helper wrapper module.

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
    cat, convert, meme, stalkig, surprise, wolfram
)


def cat_wrap():
    '''
    Wrap cat command.
    '''
    return ('image', cat())


def curx_wrap(query):
    '''
    Wrap curx command.
    '''
    query = query.split()
    return ('text', convert(query[1], query[2], query[0]))


def meme_wrap(keyword=''):
    '''
    Wrap meme command.
    '''
    keywords = keyword.split(';')[:5]
    if not keywords[0]:
        return ('image', meme())
    result = meme(*keywords)
    if 'not found' in result:
        return result
    return ('image', meme(*keywords))


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


def surprise_wrap(safe=False):
    '''
    ?
    '''
    if safe:
        return ('custimg', (surprise(safe=True),))
    return ('custimg', (surprise(),))


def wolfram_wrap(query):
    '''
    Wrap wolfram (simple mode) command.
    '''
    return ('image', wolfram(query, simple=True))
