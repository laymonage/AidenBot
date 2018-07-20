'''
Wikipedia helper module
(c) 2018 - laymonage
'''

import os
import wikipedia
from .dropson import dbx_dl, dbx_ul, to_json, get_json

WIKI_SETTINGS_PATH = os.getenv('WIKI_SETTINGS_PATH', None)
WIKI_SETTINGS = get_json(dbx_dl(WIKI_SETTINGS_PATH))


def wiki_get(keyword, set_id, trim=True):
    '''
    Return a summary of a wikipedia article with keyword as the title,
    or return a list of titles in the disambiguation page.
    keyword (str): keyword to look up in Wikipedia
    set_id (str): a unique ID to associate the user with the language settings
    trim (bool): if true, trim result to 2000 characters max
    '''
    try:
        wikipedia.set_lang(WIKI_SETTINGS[set_id])
    except KeyError:
        wikipedia.set_lang('en')

    try:
        result = wikipedia.summary(keyword)

    except wikipedia.exceptions.DisambiguationError:
        articles = wikipedia.search(keyword)
        result = "{} disambiguation:".format(keyword)
        for item in articles:
            result += "\n{}".format(item)
    except wikipedia.exceptions.PageError:
        result = "{} not found!".format(keyword)

    else:
        if trim:
            result = result[:2000]
            if not result.endswith('.'):
                result = result[:result.rfind('.')+1]
    return result


def wiki_lang(lang, set_id):
    '''
    Change wikipedia language used by a user (identified by set_id).
    lang (str): language to be used
    set_id (str): a unique ID to associate the user with the settings
    '''
    langs_dict = wikipedia.languages()
    if lang in langs_dict:
        WIKI_SETTINGS[set_id] = lang
        dbx_ul(to_json(WIKI_SETTINGS), WIKI_SETTINGS_PATH, overwrite=True)
        return ("Language has been changed to {} successfully."
                .format(langs_dict[lang]))

    return ("{} not available!\n"
            "See meta.wikimedia.org/wiki/List_of_Wikipedias for "
            "a list of available languages, and use the prefix "
            "in the Wiki column to set the language."
            .format(lang))
