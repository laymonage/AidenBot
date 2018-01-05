'''
UrbanDictionary helper module
(c) 2018 - laymonage
'''

from urbandictionary_top import udtop


def urban(keyword, ex=False):
    '''
    Return the top definition of keyword in Urban Dictionary.
    keyword (str): keyword to look up in the dictionary
    ex (bool): return with example(s) (if any)
    '''
    try:
        result = udtop(keyword)
    except udtop.TermNotFound as e:
        result = str(e)
    else:
        if not ex:
            result = result.definition
        else:
            result = str(result)
    return result
