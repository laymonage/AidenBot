'''
KBBI helper module
(c) 2018 - laymonage
'''

from kbbi import KBBI


def kbbi_def(keyword, ex=False):
    '''
    Return an entry of keyword in KBBI.
    keyword (str): keyword to look up in KBBI
    ex (bool): return with examples (if any)
    '''
    try:
        entry = KBBI(keyword)
    except KBBI.TidakDitemukan as e:
        result = str(e)
    else:
        result = "Definisi {}:\n".format(keyword)
        if ex:
            result += '\n'.join(entry.arti_contoh)
        else:
            result += str(entry)
    return result
