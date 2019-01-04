'''
Reddit helper module
(c) 2018 - laymonage
'''

import requests


def reddit_hot(subname, limit=5, splitted=False):
    '''
    Return hot <limit> posts' titles in /r/subname.
    - subname (str): name of subreddit (case-insensitive)
    - limit (str or int): number of threads to be returned (max: 25)
    - splitted (bool): if True, split result every 2000 chars and make a list
    '''
    try:
        limit = int(limit)
    except ValueError:
        limit = 5
    if limit > 25:
        limit = 25
    sub = requests.get(('https://www.reddit.com/r/{}.json?limit={}'
                        .format(subname, limit)),
                       headers={'user-agent': 'AidenBot'}).json()
    try:
        threads = [thread['data']['title']
                   for thread in sub['data']['children'][-limit:]]
    except KeyError:  # Happens when request limit is reached or 404
        print(sub)
        return "reddit.com/r/{} is currently unavailable.".format(subname)
    result = "Hot {} posts in reddit.com/r/{}\n".format(len(threads), subname)
    if not splitted:
        result += '\n'.join(['{}. {}'.format(i+1, title)
                             for i, title in enumerate(threads)])
    else:
        result_split = []
        for i, each in enumerate(threads):
            temp = '{}. {}\n'.format(i+1, each)
            if len(result + temp[:-1]) > 2000 and i+1 < len(threads):
                result_split.append(result[:-1])
                result = temp
            else:
                result += temp
                if i+1 == len(threads):
                    result_split.append(result[:-1])
        result = result_split
    return result
