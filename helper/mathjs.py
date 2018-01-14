'''
Mathjs.org helper module
(c) 2018 - laymonage
'''

from urllib.parse import quote
import requests


def calc(expr):
    '''
    Return evaluation result of expr, retrieved from mathjs.org.
    '''
    return requests.get('http://api.mathjs.org/v1/?expr=' +
                        quote(expr, safe='')).text
