"""
WolframAlpha helper module.

(c) 2018 - laymonage
"""

import os
from urllib.parse import quote
import requests


def wolfram(query, simple=False):
    """
    Get answer from WolframAlpha.

    query (str): string to be queried
    simple (bool): if true, return result as image link
    """
    # WolframAlpha AppID, obtained from developer.wolframalpha.com
    wolfram_appid = os.getenv('WOLFRAMALPHA_APPID', None)

    url = 'https://api.wolframalpha.com/v1/{}?i={}&appid={}'
    if not simple:
        mode = 'result'
        return requests.get(url.format(mode, quote(query), wolfram_appid)).text
    mode = 'simple'
    return url.format(mode, quote(query), wolfram_appid)
