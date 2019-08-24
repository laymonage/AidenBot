"""
(Unofficial) Google Dictionary helper module.

(c) 2019 - laymonage
"""

import os
from urllib.parse import quote
import requests


def define(keyword, lang='en'):
    """
    Return word definition from Google Dictionary.

    keyword (str): keyword to look up in the dictionary
    """
    word = quote(keyword)
    url = (
        'https://mydictionaryapi.appspot.com/?define={}&lang={}'
        .format(word, lang)
    )
    req = requests.get(url)
    if "No definitions found" in req.text:
        return (
            'No entry available for "{}" in "{}" language.'
            .format(keyword, lang)
        )

    data = req.json()
    result = ''
    i = 0

    if isinstance(data, dict):
        data = [data]
    for word in data:
        try:
            result += '{} {}'.format(word['word'], word['phonetic'])
        except KeyError:
            result +=  word['word']
        if not word['meaning']:
            continue
        result += '\n\n'
        for pos, defs in word['meaning'].items():
            result += pos + '\n'
            current = ''
            for d in defs:
                if d:
                    i += 1
                    current += '{}. {}\n'.format(i, d['definition'])
            if i == 1:
                current = current[3:]
            i = 0
            result += current + '\n'
        result += '\n'
    result = result.strip()
    return result


def _define(query):
    """Pass lang argument to define using semicolon-separated string."""
    return define(*query.split(';', maxsplit=2))
