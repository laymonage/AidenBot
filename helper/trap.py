'''
?
(c) 2018 - laymonage
'''

import os
import random
import requests
from .dropson import dbx_dl, get_json


def surprise(safe=False):
    '''
    ?
    '''
    cat_api = 'http://thecatapi.com/api/images/get'
    prev_url = requests.get(cat_api)
    prev_url = prev_url.url.replace('http://', 'https://')

    if safe:
        orig_url = requests.get(cat_api)
        orig_url = orig_url.url.replace('http://', 'https://')
    else:
        surprise_links = os.getenv('SURPRISES_FILE_PATH', None)
        surprises = get_json(dbx_dl(surprise_links))
        orig_url = random.choice(surprises)

    return (orig_url, prev_url)
