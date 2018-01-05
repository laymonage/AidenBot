'''
Reddit helper module
(c) 2018 - laymonage
'''

import requests


def reddit_hot(subname, limit=10):
    '''
    Return hot <limit> posts' titles in /r/subname.
    - subname (str): name of subreddit (case-insensitive)
    - limit (str or int): number of threads to be returned (max: 25)
    '''
    try:
        limit = int(limit)
        if limit > 25:
            limit = 25
    except ValueError:
        limit = 10
    r = requests.get(('https://www.reddit.com/r/{}.json?limit={}'
                      .format(subname, limit)),
                     headers={'user-agent': 'AidenBot'}).json()
    try:
        clean = r['data']['children'][-limit:]
    except KeyError:  # Happens when request limit is reached
        return r.text
    i = 0
    if clean:
        result = "Hot {} posts in reddit.com/r/{}:".format(len(clean), subname)
    else:
        result = "reddit.com/r/{} is unavailable.".format(subname)
    for thread in clean:
        i += 1
        result += "\n{}. {}".format(i, thread['data']['title'])
    return result
