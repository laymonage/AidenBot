'''
?
(c) 2018 - laymonage
'''

import os
import random
import requests
from .dropson import dbx_dl, getJSON


def surprise():
    '''
    ?
    '''
    surprise_links = os.getenv('SURPRISES_FILE_PATH', None)
    surprises = getJSON(dbx_dl(surprise_links))
    orig_url = random.choice(surprises)
    prev_url = 'http://thecatapi.com/api/images/get'
    prev_url = requests.get(prev_url)
    prev_url = prev_url.url.replace('http://', 'https://')
    return (orig_url, prev_url)
