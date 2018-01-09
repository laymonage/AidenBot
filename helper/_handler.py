'''
Command handler module for AidenBot
'''

from functools import partial as pt
from . import (
    AkunBenCoin, cat_wrap, echo, shout, mock, is_palindrome, rng,
    rpick, translate, isup, kbbi_def, ask, define, reddit_hot,
    slap, stalkig_wrap, ticket_add, ticket_rem, ticket_get,
    surprise_wrap, urban, wiki_get, wiki_lang, wolfram,
    wolfram_wrap, weather
)

help_msg = ("Available commands:\n"
            "ask, bye, bencoin, cat, define, echo, help, isup, isupd, "
            "kbbi, kbbix, lenny, mcs, mock, palindrome, ppalindrome, "
            "pick, profile, reddit, rng, rngf, shout, shrug, slap, "
            "stalkig, surprise, ticket, tl, urban, urbanx, weather, wiki, "
            "wikilang, wolfram, wolframs\n"
            "Use /help <command> for more information.")

cmd_help = {'ask': "Usage: /ask <question>\n"
                   "Simulator Kulit Kerang Ajaib.\n"
                   "Example: /ask Apa aku boleh makan?",

            'bye': "Usage: /bye\n"
                   "Instruct me to leave this chat room.",

            'bencoin': "Usage: /bencoin\n"
                       "[Fasilkom UI 2017 joke]\n"
                       "Send bencoin help message.\n"
                       "(note: the commands actually work!)",

            'cat': "Usage: /cat\n"
                   "Get a random cat image, obtained from thecatapi.com.",

            'define': "Usage: /define <something>\n"
                      "Define <something>, obtained from "
                      "oxforddictionaries.com\n"
                      "Example: /define onomatopoeia",

            'echo': "Usage: /echo <something>\n"
                    "Repeat <something>.\n"
                    "Example: /echo Hello, world!",

            'help': "Usage: /help\n"
                    "Send a list of available commands.",

            'isup': "Usage: /isup <website>\n"
                    "Check <website>'s status, "
                    "obtained from isitup.org.\n"
                    "Example: /isup google.com",

            'isupd': "Usage: /isupd <website>\n"
                     "Check <website>'s status, along with its IP, "
                     "response code, and response time, "
                     "obtained from isitup.org.\n"
                     "Example: /isupd google.com",

            'kbbi': "Usage: /kbbi <something>\n"
                    "Define <something>, obtained from kbbi.kemdikbud.go.id.\n"
                    "Example: /kbbi eufemisme",

            'kbbix': "Usage: /kbbix <something>\n"
                     "Define <something> and give usage examples (if any), "
                     "obtained from kbbi.kemdikbud.go.id.\n"
                     "Example: /kbbix cinta",

            'lenny': "Usage: /lenny\n"
                     "Send ( ͡° ͜ʖ ͡°)",

            'mcs': "Usage: /mcs <question>\n"
                   "Magic Conch Shell simulator.\n"
                   "Example: /mcs Can I eat something?",

            'mock': "uSaGE: /mock <something>\n"
                    "sEnD <sOMetHiNg> iN A mOcKinG MaNnER.\n"
                    "ExaMpLE: /mock Don't tell me what I can't do!",

            'palindrome': "Usage: /palindrome <something>\n"
                          "Check if <something> is a palindrome.\n"
                          "(only alphanumeric characters are checked, "
                          "case-insensitive)\n"
                          "Example: /palindrome Dammit, I'm mad!",

            'ppalindrome': "Usage: /ppalindrome <something>\n"
                           "Check if <something> is a perfect palindrome\n"
                           "Example: /ppalindrome kasur nababan rusak",

            'pick': "Usage: /pick <something1>;<something2>;<somethingN>\n"
                    "Pick a random item from a semicolon-separated list.\n"
                    "Example: /pick Dota;LoL;Mobile Legends",

            'profile': "Usage: /profile\n"
                       "Send your display name and your status message "
                       "(if any).",

            'reddit': "Usage: /reddit <subreddit> <limit>\n"
                      "Get hot <limit> posts' titles in <subreddit>.\n"
                      "<limit> is optional, default is 5, maximum is 25.\n"
                      "Example: /reddit showerthoughts 7",

            'rng': "Usage: /rng <floor> <ceiling>\n"
                   "Random (integer) number generator in range "
                   "<floor>..<ceiling> (inclusive).\n"
                   "<floor> is optional, default is 1.\n"
                   "Example: /rng 4815 162342",

            'rngf': "Usage: /rngf <floor> <ceiling>\n"
                    "Random (float, 2 digit precision) number generator "
                    "in range <floor>..<ceiling> (inclusive).\n"
                    "<floor> is optional, default is 1.\n"
                    "Example: /rngf 2.19 4.2",

            'shout': "Usage: /shout <something>\n"
                     "REPEAT <SOMETHING> IN UPPERCASE.\n"
                     "Example: /shout how do you like them apples?",

            'shrug': "Usage: /shrug\n"
                     "Send ¯\\_(ツ)_/¯",

            'slap': "Usage: /slap <someone>\n"
                    "Slap <someone> with a random object.\n"
                    "Example: /slap Pak Dengklek",

            'stalkig': "Usage: /stalkig <username>\n"
                       "Get a random picture taken from <username>'s "
                       "instagram account, along with the post's link.\n"
                       "Example: /stalkig tychomusic",

            'surprise': "Usage: /surprise\n"
                        "?",

            'ticket': "Usage: /ticket <something>\n"
                      "Send <something> to my developer. "
                      "Don't worry, it's anonymous!\n"
                      "Example: /ticket this bot sucks",

            'tl': "Usage: /tl <src_lang> <dest_lang> <text>\n"
                  "Translate <text> from <src_lang> to <dest_lang>.\n"
                  "You can use auto as <src_lang> for auto-detection.\n"
                  "Look up ISO 639-1 for valid language codes.\n"
                  "Example: /tl auto id Sorry for my English",

            'urban': "Usage: /urban <something>\n"
                     "Define <something>, obtained from urbandictionary.com.\n"
                     "Example: /urban Mac DeMarco",

            'urbanx': "Usage: /urbanx <something>\n"
                      "Define <something>, and give usage examples (if any), "
                      "obtained from urbandictionary.com.\n"
                      "Example: /urbanx Young the Giant",

            'weather': "Usage: /weather <location>\n"
                       "Obtain current weather data in <location>, obtained "
                       "from wunderground.com.\n"
                       "Example: /weather Jakarta",

            'wiki': "Usage: /wiki <title>\n"
                    "Summarize a Wikipedia article titled <title>, or get "
                    "a list of titles in the disambiguation page.\n"
                    "Example: /wiki Vampire Weekend",

            'wikilang': "Usage: /wikilang <language>\n"
                        "Change /wiki language to <language>\n"
                        "Language settings will be reset to default (en) "
                        "every once in a while.\n"
                        "Example: /wikilang id",

            'wolfram': "Usage: /wolfram <something>\n"
                       "Ask wolframalpha.com about <something>.\n"
                       "Returns an image of the result summary.\n"
                       "Example: /wolfram Who are Cage the Elephant?",

            'wolframs': "Usage: /wolframs <something>\n"
                        "Ask wolframalpha.com about <something>.\n"
                        "Returns a short text answer (if available).\n"
                        "Example: /wolfram Tell me a computer science joke"}


def get_help(command=None):
    '''
    Return a command's help message.
    '''
    if not command:
        return help_msg
    try:
        return cmd_help[command]
    except KeyError:
        return command + " is unavailable."


def command_handler(text, user, me, set_id):
    '''
    Command handler for AidenBot.
    '''
    itsme = user.user_id == me.user_id
    command = text.split(maxsplit=1)
    cmd = text.lower().split(maxsplit=1)
    result = None

    no_arg_commands = {'bencoin': AkunBenCoin.intro,
                       'lenny': '( ͡° ͜ʖ ͡°)',
                       'shrug': '¯\\_(ツ)_/¯',
                       'tix': ticket_get}

    single_arg_commands = {'ask': pt(ask, id_=True),
                           'define': define,
                           'echo': echo,
                           'isup': isup,
                           'isupd': pt(isup, detailed=True),
                           'kbbi': kbbi_def,
                           'kbbix': pt(kbbi_def, ex=True),
                           'mcs': ask,
                           'mock': mock,
                           'palindrome': is_palindrome,
                           'ppalindrome': pt(is_palindrome, perfect=True),
                           'pick': rpick,
                           'rtix': ticket_rem,
                           'shout': shout,
                           'slap': pt(slap, user, me=me),
                           'ticket': ticket_add,
                           'tl': translate,
                           'urban': urban,
                           'urbanx': pt(urban, ex=True),
                           'weather': weather,
                           'wiki': pt(wiki_get, set_id=set_id),
                           'wikilang': pt(wiki_lang, set_id=set_id),
                           'wolframs': wolfram}

    double_arg_commands = {'reddit': pt(reddit_hot, splitted=True),
                           'rng': rng,
                           'rngf': pt(rng, frac=True)}

    distinct_commands = {'cat': cat_wrap,
                        'stalkig': pt(stalkig_wrap, *command[1:]),
                        'surprise': surprise_wrap,
                        'wolfram': pt(wolfram_wrap, *command[1:])}

    try:
      if cmd[0] == 'help':
          result = ('text', get_help(*cmd[1:]))

      elif cmd[0] in no_arg_commands and (cmd[0] != 'tix' or itsme):
          result = ('text', no_arg_commands[cmd[0]])

      elif cmd[0] in single_arg_commands and (cmd[0] != 'rtix' or itsme):
          result = ('text', single_arg_commands[cmd[0]](command[1]))

      elif cmd[0] in double_arg_commands:
          command = command[1].split()
          result = ('text', double_arg_commands[cmd[0]](command[0], command[-1]))

      elif cmd[0] in distinct_commands:
          result = distinct_commands[cmd[0]]()
    except (IndexError, TypeError):
      result = ('text', "Invalid format.\n"
                        "Please see /help {} for more info."
                        .format(cmd[0]))

    return result
