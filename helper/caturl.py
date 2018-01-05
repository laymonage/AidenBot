'''
TheCatAPI helper module
(c) 2018 - laymonage
'''

import requests


def cat():
    '''
    Return a link to a random cat pic from thecatapi.com.
    '''
    url = 'http://thecatapi.com/api/images/get'
    req = requests.get(url)
    url = req.url.replace('http://', 'https://')
    return url
