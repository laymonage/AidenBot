"""
Google Translate helper module.

(c) 2018 - laymonage
"""

from googletrans import Translator


def translate(text):
    """Translate a string from src language to dest."""
    text = text.split(maxsplit=2)
    gtrans = Translator()
    try:
        result = gtrans.translate(text[2], src=text[0], dest=text[1])
    except IndexError:
        return "Wrong format."
    if text[0] == 'auto':
        result.origin = '({}) {}'.format(gtrans.detect(text[2]).lang,
                                         result.origin)
    return result.origin + ' -> ' + result.text
