'''
Weather Underground helper module
(c) 2018 - laymonage
'''

import os
from urllib.parse import quote
import requests


def weather(keyword):
    '''
    Send current weather condition of a location, obtained from
    Weather Underground.
    keyword (str): location to look up in wunderground.com
    '''
    # Weather Underground API key, obtained from wunderground.com/weather/api
    wunder_key = os.getenv('WUNDERGROUND_API_KEY', None)

    url = ('http://api.wunderground.com/api/{}/conditions/q/{}.json'
           .format(wunder_key, quote(keyword)))
    data = requests.get(url).json()
    try:
        locID = data['response']['results'][0]['l']
    except KeyError:
        pass
    else:
        url = url[:url.find('/q/')] + locID + '.json'
        data = requests.get(url).json()

    try:
        data = data['current_observation']
        result = ("Weather in {}:\n"
                  "{}\n"
                  "Temperature: {}°C ({}°F)\n"
                  "Feels like: {}°C ({}°F)"
                  .format(data['display_location']['full'],
                          data['weather'],
                          data['temp_c'], data['temp_f'],
                          data['feelslike_c'], data['feelslike_f']))
    except KeyError:
        result = "Location is not found or not specific enough."
    return result
