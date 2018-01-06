'''
Stalking helper module
(c) 2018 - laymonage
'''

import random
import requests


def stalkig(username):
    '''
    Return a tuple that consists of image link and post link,
    taken randomly from username's instagram profile.
    username (str): username to stalk
    '''
    url = 'https://www.instagram.com/{}/?__a=1'.format(username)
    req = requests.get(url)
    if req.status_code == 404:
        return (False, "@{} not found!".format(username))

    req = req.json()
    if req['user']['is_private']:
        return (False, "@{} is a private account.".format(username))

    nodes = req['user']['media']['nodes']
    anode = random.choice(nodes)
    image = anode['display_src']
    ncode = anode['code']
    nlink = 'instagram.com/p/{}'.format(ncode)
    return (image, nlink)
