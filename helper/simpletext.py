'''
Echo helper module
(c) 2018 - laymonage
'''

import random


def echo(text):
    '''
    Return echo function.
    '''
    return text


def shout(text):
    '''
    Return text in uppercase.
    '''
    return text.upper()


def mock(text):
    '''
    rEtURn tExT iN raNdoMcASe.
    '''
    result = ''
    for char in text:
        mocked_char = random.choice([char.upper(), char.lower()])
        if mocked_char.isupper() and result[-1:-3:-1].isupper():
            mocked_char = mocked_char.lower()
        elif mocked_char.islower() and result[-1:-3:-1].islower():
            mocked_char = mocked_char.upper()
        result += mocked_char
    return result


def space(text):
    '''
    R e t u r n   t e x t.
    '''
    return ' '.join(text)


def aesthetic(text):
    '''
    Return text in fullwidth unicode.
    '''
    halfwidth_to_fullwidth = str.maketrans(
        ('0123456789 abcdefghijklmnopqrstuvwxyz'
         'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
         '!"#$%&()*+,-./:;<=>?@[]^_`{|}~'),
        ('０１２３４５６７８９　ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
         'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
         '！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［］＾＿‘｛｜｝～'))
    return text.translate(halfwidth_to_fullwidth)


def bawl1(text):
    '''
    Return
    t e x t .
    e
    x
    t
    .
    or boxed if text is a palindrome.
    '''
    if text[0].lower() != text[-1].lower() or len(text) <= 2:
        return ' '.join(text) + '\n' + '\n'.join(text[1:])
    return (' '.join(text) + '\n' +
            '\n'.join(char + ' '*((len(text) - 2)*2 + 1) + char
                      for char in text[1:-1]) + '\n' +
            ' '.join(text))


def bawl2(text):
    '''
    Return
    t e x t .
    e e
    x   x
    t     t
    .       .
    '''
    return ' '.join(text) + ''.join('\n' + char + ' '*(2*idx + 1) + char
                                    for idx, char in enumerate(text[1:]))


def combine(text):
    '''
    Combine multiple functions.
    '''
    funcs = {'shout': shout,
             'mock': mock,
             'spc': space,
             'aes': aesthetic,
             'bawl1': bawl1,
             'bawl2': bawl2}
    used = {'shout': False,
            'mock': False,
            'spc': False,
            'aes': False,
            'bawl1': False,
            'bawl2': False}

    operation = text.split(maxsplit=1)
    num = int(operation[0])
    todo = operation[1].split(maxsplit=num)
    text = todo[num]
    for each_op in range(num):
        try:
            if not used[todo[each_op]]:
                text = funcs[todo[each_op]](text)
                if todo[each_op] in ('bawl1', 'bawl2'):
                    used['bawl1'], used['bawl2'] = True, True
                else:
                    used[todo[each_op]] = True
        except KeyError:
            return todo[each_op] + " is not available for combining."
    return text


def is_palindrome(text, perfect=False):
    '''
    Return a palindrome checking result of text
    (case-insensitive alphanumeric string).
    if perfect is True, then text must be a perfect palindrome.
    '''
    if perfect:
        if text == text[::-1]:
            return text + " is a perfect palindrome!"
        return text + " is not a perfect palindrome."
    test = ''.join(c.lower() for c in text if c.isalnum())
    if test == test[::-1]:
        return text + " is a palindrome!"
    return text + " is not a palindrome."


def rng(ceil, floor=1, frac=False):
    '''
    Return a random number from floor to ceil (inclusive).
    '''
    if frac:
        floor, ceil = float(floor), float(ceil)
    else:
        floor, ceil = int(floor), int(ceil)

    if floor == ceil:
        floor = 1
    elif floor > ceil:
        floor, ceil = ceil, floor

    if frac:
        result = ("From {} to {}, I pick {:.2f}."
                  .format(floor, ceil, random.uniform(floor, ceil)))
    else:
        result = ("From {} to {}, I pick {}."
                  .format(floor, ceil, random.randint(floor, ceil)))
    return result


def rpick(text):
    '''
    Pick a random item from a semicolon-separated list in a string.
    '''
    return "I pick {}.".format(random.choice(text.split(';')))


def emote(name, action):
    '''
    Emote an action.
    '''
    return "{} {}".format(name, action)
