'''
?
(c) 2018 - laymonage
'''

import os
import random
import requests


def surprise():
    '''
    ?
    '''
    imgur_client = os.getenv('IMGUR_CLIENT_ID', None)
    surprise_album = os.getenv('SURPRISE_ALBUM_HASH', None)
    surprises = [image['link']
                 for image in
                 requests.get('https://api.imgur.com/3/album/{}'
                              .format(surprise_album),
                              headers={'authorization':
                                       'Client-ID ' + imgur_client}).json()
                 ['data']['images']]
    orig_url = random.choice(surprises)
    prev_url = 'http://thecatapi.com/api/images/get'
    prev_url = requests.get(prev_url)
    prev_url = prev_url.url.replace('http://', 'https://')
    return (orig_url, prev_url)
