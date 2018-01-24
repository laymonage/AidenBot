'''
Stalking helper module
(c) 2018 - laymonage
'''

import os
import random
import requests
from twitter import Twitter, OAuth
from twitter.api import TwitterHTTPError


def stalkig(username):
    '''
    Return a tuple that consists of image link and post link,
    taken randomly from username's Instagram profile.
    username (str): username to stalk
    '''
    url = 'https://www.instagram.com/{}/?__a=1'.format(username)
    req = requests.get(url)
    if req.status_code == 404:
        return (False, "@{} is unavailable.".format(username))

    req = req.json()
    if req['user']['is_private']:
        return (False, "@{} is a private account.".format(username))

    nodes = req['user']['media']['nodes']
    anode = random.choice(nodes)
    image = anode['display_src']
    ncode = anode['code']
    nlink = 'instagram.com/p/{}'.format(ncode)
    return (image, nlink)


def stalktwt(username):
    '''
    Return a random tweet taken from username's Twitter profile.
    username (str): username to stalk
    '''
    access_token = os.getenv('TWITTER_ACCESS_TOKEN', None)
    access_secret = os.getenv('TWITTER_ACCESS_SECRET', None)
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY', None)
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET', None)
    t = Twitter(auth=OAuth(access_token, access_secret,
                           consumer_key, consumer_secret))
    try:
        timeline = t.statuses.user_timeline(screen_name=username, count=200)
        if timeline[0]['user']['protected']:
            return "@{} is a protected account.".format(username)
    except IndexError:
        return "@{} hasn't Tweeted.".format(username)
    except TwitterHTTPError as e:
        if 'Not authorized' in str(e):
            return "@{} is a protected account.".format(username)
        return "@{} is unavailable.".format(username)
    tweet = random.choice(timeline)
    username = tweet['user']['screen_name']
    return ("@{}: {}".format(username, tweet['text']),
            "twitter.com/{}/status/{}".format(username, tweet['id']))
