'''
Roasting helper module.
(c) 2019 - laymonage
Idea from shivaroast.
'''

import os
import random
from .dropson import dbx_dl, get_json


def roast(target):
    '''
    Roast the target with a spicy line.
    '''
    roasts_file_path = os.getenv('ROASTS_FILE_PATH', None)
    if not roasts_file_path:
        return "Roast file isn't configured yet."
    roasts = get_json(dbx_dl(roasts_file_path))
    return random.choice(roasts['lines']).replace('$linename', target)
