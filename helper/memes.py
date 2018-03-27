'''
Memes helper module.
(c) 2018 - laymonage
'''

import os
import random
from .dropson import dbx_ls, dbx_tl

MEMES_PATH = os.getenv('MEMES_PATH')
MEMES = dbx_ls(MEMES_PATH, sort=True, noext=True)


def getmemes(keyword=''):
    '''
    Return a list of meme pictures in a Dropbox folder.
    '''
    if not keyword:
        return '{} memes available:\n'.format(len(MEMES)) + ', '.join(MEMES)
    found = [each for each in MEMES if keyword.lower() in each.lower()]
    if not found:
        return 'No memes containing "{}".'.format(keyword)
    return '{} memes containing "{}":\n{}'.format(len(found), keyword,
                                                  ', '.join(found))


def meme(*keywords):
    '''
    Return a link to a meme picture, retrieved from Dropbox.
    '''
    if not keywords:
        return dbx_tl(MEMES_PATH + random.choice(dbx_ls(MEMES_PATH)))
    try:
        result = []
        for word in keywords:
            if not word:
                continue
            current = word
            result.append(dbx_tl(MEMES_PATH + word + '.jpg'))
    except KeyError:
        result = '"{}" is not found.'.format(current)
    return result


def updmemes(allowed=True):
    '''
    Update memes.
    '''
    if not allowed:
        return None
    del MEMES[:]
    MEMES.extend(dbx_ls(MEMES_PATH, sort=True, noext=True))
    return "Meme list has been updated."
