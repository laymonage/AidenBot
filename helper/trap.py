'''
?
(c) 2018 - laymonage
'''

import os
import random
from .caturl import cat
from .dropson import dbx_dl, get_json


def surprise(safe=False):
    '''
    ?
    '''
    prev_url = cat()

    if safe:
        orig_url = cat()
    else:
        surprise_links = os.getenv('SURPRISES_FILE_PATH', None)
        surprises = get_json(dbx_dl(surprise_links))
        orig_url = random.choice(surprises)

    return (orig_url, prev_url)
