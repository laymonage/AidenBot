'''
Oxford Dictionaries helper module
(c) 2018 - laymonage
'''

import os
from urllib.parse import quote
import requests


def define(keyword):
    '''
    Return word definition from oxforddictionaries.com
    keyword (str): keyword to look up in the dictionary
    '''
    # Oxford Dictionaries AppID and AppKey, obtained from
    # developer.oxforddictionaries.com
    oxdict_appid = os.getenv('OXFORD_DICT_APPID', None)
    oxdict_key = os.getenv('OXFORD_DICT_APPKEY', None)

    word = quote(keyword)
    url = ('https://od-api.oxforddictionaries.com:443/api/v1/entries/en/{}'
           .format(word))
    req = requests.get(url, headers={'app_id': oxdict_appid,
                                     'app_key': oxdict_key})
    if "No entry available" in req.text:
        return 'No entry available for "{}".'.format(word)

    req = req.json()
    result = ''
    i = 0
    for each_result in req['results']:
        for each_lexEntry in each_result['lexicalEntries']:
            for each_entry in each_lexEntry['entries']:
                for each_sense in each_entry['senses']:
                    if 'crossReferenceMarkers' in each_sense:
                        search = 'crossReferenceMarkers'
                    else:
                        search = 'definitions'
                    for each_def in each_sense[search]:
                        i += 1
                        result += '\n{}. {}'.format(i, each_def)

    if i == 1:
        result = 'Definition of {}:\n'.format(keyword) + result[4:]
    else:
        result = 'Definitions of {}:'.format(keyword) + result
    return result
