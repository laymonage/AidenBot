"""
Weather helper module.

(c) 2018-2019 - laymonage
"""

import os
from urllib.parse import quote
import requests


def weather(keyword, metric=True):
    """
    Send current weather condition of a location.

    Retrieved from OpenWeather API.
    keyword (str): location to look up in openweathermap.org
    """
    api_key = os.getenv('OPENWEATHER_API_KEY', None)
    units, symbol = ('metric', 'C') if metric else ('imperial', 'F')

    url = ('https://api.openweathermap.org/data/2.5/weather?units={}&appid={}&{{}}'
           .format(units, api_key))
    if ';' in keyword:
        arg1, arg2 = keyword.split(';', maxsplit=2)
        try:
            float(arg2)
        except ValueError:
            query = 'zip={},{}'.format(arg1, arg2)
        else:
            query = 'lat={}&lon={}'.format(arg1, arg2)
    else:
        try:
            keyword = int(keyword)
        except ValueError:
            query = 'q={}'.format(keyword)
        else:
            query = 'id={}'.format(keyword)
    data = requests.get(url.format(query)).json()
    try:
        return (
            "Weather in {}, {}:\n"
            "{}\n"
            "Temperature: {}°{}\n"
            "({}°{} min, {}°{} max)"
            .format(
                data['name'], data['sys']['country'],
                data['weather'][0]['main'],
                data['main']['temp'], symbol,
                data['main']['temp_min'], symbol,
                data['main']['temp_max'], symbol
            )
        )
    except KeyError:
        return data['message']
