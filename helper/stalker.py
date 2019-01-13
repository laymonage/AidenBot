'''
Stalking helper module.
(c) 2018 - laymonage
'''

from html import unescape
import json
import os
import random
import requests
from bs4 import BeautifulSoup as bs
from twitter import Twitter, OAuth
from twitter.api import TwitterHTTPError


def stalkig(username):
    '''
    Return a tuple that consists of image link and post link,
    taken randomly from username's Instagram profile.
    username (str): username to stalk
    '''
    url = 'https://www.instagram.com/{}'.format(username)
    req = requests.get(url)
    if req.status_code == 404:
        return (False, "@{} is unavailable.".format(username))

    page = bs(req.content, "html.parser")
    scripts = page.find_all('script')
    shared_data = [s for s in scripts if "_sharedData = " in str(s)].pop()
    shared_data = str(shared_data)
    data_json = shared_data[shared_data.find("{"):shared_data.rfind(";")]
    data_json = json.loads(data_json)
    user = data_json['entry_data']['ProfilePage'][0]['graphql']['user']
    if user['is_private']:
        return (False, "@{} is a private account.".format(username))

    nodes = user['edge_owner_to_timeline_media']['edges']
    anode = random.choice(nodes)['node']
    image = anode['display_url']
    ncode = anode['shortcode']
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
    twitter = Twitter(auth=OAuth(access_token, access_secret,
                                 consumer_key, consumer_secret))
    try:
        timeline = twitter.statuses.user_timeline(screen_name=username,
                                                  count=200,
                                                  tweet_mode='extended')
        if timeline[0]['user']['protected']:
            return "@{} is a protected account.".format(username)
    except IndexError:
        return "@{} hasn't Tweeted.".format(username)
    except TwitterHTTPError as error:
        if 'Not authorized' in str(error):
            return "@{} is a protected account.".format(username)
        return "@{} is unavailable.".format(username)
    tweet = random.choice(timeline)
    username = tweet['user']['screen_name']
    return ("@{}: {}".format(username, unescape(tweet['full_text'])),
            "twitter.com/{}/status/{}".format(username, tweet['id']))
