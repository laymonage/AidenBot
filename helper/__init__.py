'''
Initialization
'''
# pylint: disable=unused-import
# flake8: noqa

from .bencoin import AkunBenCoin
from .caturl import cat
from .dropson import dbx_dl, dbx_ul, to_json, get_json
from .gtrans import translate
from .isitup import isup
from .kbbih import kbbi_def
from .mathjs import calc
from .mcs import ask
from .memes import getmemes, meme, updmemes
from .oxdict import define
from .reddit import reddit_hot
from .simpletext import (
    combine, echo, shout, mock, space, aesthetic,
    bawl1, bawl2, is_palindrome, rng, rpick, emote
)
from .slapper import slap
from .stalker import stalkig, stalktwt
from .ticket import about, ticket_add, ticket_rem, ticket_get
from .trap import surprise
from .urban import urban
from .wiki import wiki_get, wiki_lang
from .wolframalpha import wolfram
from .wunderground import weather
from ._wrapper import (
    cat_wrap, meme_wrap, stalkig_wrap, surprise_wrap, wolfram_wrap
)
