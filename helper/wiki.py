'''
Wikipedia helper module
(c) 2018 - laymonage
'''

import wikipedia

WIKI_SETTINGS = {}


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
    if lang in langs_dict.keys():
        WIKI_SETTINGS[set_id] = lang
        return ("Language has been changed to {} successfully."
                .format(langs_dict[lang]))

    return ("{} not available!\n"
            "See meta.wikimedia.org/wiki/List_of_Wikipedias for "
            "a list of available languages, and use the prefix "
            "in the Wiki column to set the language."
            .format(lang))
