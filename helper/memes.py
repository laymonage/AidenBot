'''
Memes helper module.
(c) 2018 - laymonage
'''

import os
import random
from .dropson import dbx_ls, dbx_tl

memes_path = os.getenv('MEMES_PATH')
memes = dbx_ls(memes_path, sort=True, noext=True)


def getmemes(keyword=''):
    '''
    Return a list of meme pictures in a Dropbox folder.
    '''
    if not keyword:
        return '{} memes available:\n'.format(len(memes)) + ', '.join(memes)
    found = [each for each in memes if keyword.lower() in each.lower()]
    if not found:
        return 'No memes containing "{}".'.format(keyword)
    return '{} memes containing "{}":\n{}'.format(len(found), keyword,
                                                  ', '.join(found))


def meme(*keywords):
    '''
    Return a link to a meme picture, retrieved from Dropbox.
    '''
    if not keywords:
        return dbx_tl(memes_path + random.choice(dbx_ls(memes_path)))
    try:
        result = []
        for word in keywords:
            if not word:
                continue
            current = word
            result.append(dbx_tl(memes_path + word + '.jpg'))
    except KeyError:
        result = '"{}" is not found.'.format(current)
    return result


def updmemes():
    '''
    Update memes.
    '''
    del memes[:]
    memes.extend(dbx_ls(memes_path, sort=True, noext=True))
    return "Meme list has been updated."
