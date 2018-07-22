'''
TheCatAPI helper module
(c) 2018 - laymonage
'''

import os
import requests
from .dropson import dbx_ul, dbx_tl

CAT_PATH = os.getenv('CAT_PATH', None)


def cat():
    '''
    Return a link to a random cat pic from thecatapi.com.
    '''
    url = 'http://thecatapi.com/api/images/get'
    req = requests.get(url)
    url = req.url.replace('http://', 'https://')
    path = CAT_PATH + url[url.find('/tumblr_'):]
    dbx_ul(req.content, path)
    return dbx_tl(path)
