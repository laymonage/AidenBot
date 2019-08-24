"""
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
"""


def cat_wrap():
    """Wrap cat command."""
    from .caturl import cat
    return ('image', cat())


def curx_wrap(query):
    """Wrap curx command."""
    from .currency import convert
    query = query.split()
    return ('text', convert(query[1], query[2], query[0]))


def define_wrap(query):
    """Wrap define command."""
    from .dictionary import define
    return ('text', define(*query.split(';', maxsplit=2)))


def meme_wrap(keyword=''):
    """Wrap meme command."""
    from .memes import meme
    keywords = keyword.split(';')[:5]
    if not keywords[0]:
        return ('image', meme())
    result = meme(*keywords)
    if 'not found' in result:
        return result
    return ('image', meme(*keywords))


def stalkig_wrap(username):
    """Wrap stalkig command."""
    from .stalker import stalkig
    result = stalkig(username)
    if result[0]:
        return ('multi', (('image', result[0]),
                          ('text', result[1])))
    return ('text', result[1])


def surprise_wrap(safe=False):
    """Wrap surprise command."""
    from .trap import surprise
    if safe:
        return ('custimg', (surprise(safe=True),))
    return ('custimg', (surprise(),))


def wolfram_wrap(query):
    """Wrap wolfram (simple mode) command."""
    from .wolframalpha import wolfram
    return ('image', wolfram(query, simple=True))
