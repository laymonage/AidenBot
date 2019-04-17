"""
KBBI helper module.

(c) 2018 - laymonage
"""

from kbbi import KBBI


def kbbi_def(keyword, ex=False):
    """
    Return scraped page of keyword in KBBI.

    keyword (str): keyword to look up in KBBI
    ex (bool): return with examples (if any)
    """
    try:
        entry = KBBI(keyword)
    except KBBI.TidakDitemukan as error:
        result = str(error)
    else:
        result = entry.__str__(contoh=ex)
    return result
