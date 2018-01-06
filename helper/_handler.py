'''
Command handler module for AidenBot
'''

from . import (
    AkunBenCoin, cat, echo, shout, mock, is_palindrome, rng,
    rpick, isup, kbbi_def, ask, define, reddit_hot, slap,
    stalkig, ticket_add, ticket_rem, ticket_get, surprise,
    urban, wiki_get, wiki_lang, wolfram, weather
)

help_msg = ("Available commands:\n"
            "ask, bye, bencoin, cat, define, echo, help, isup, isupd, "
            "kbbi, kbbix, lenny, mcs, mock, palindrome, ppalindrome, "
            "pick, profile, reddit, rng, shout, shrug, slap, stalkig, "
            "surprise, ticket, urban, urbanx, weather, wiki, wikilang, "
            "wolfram, wolframs\n"
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
                   "<floor>..<ceiling> (inclusive, ceiling > floor).\n"
                   "<floor> is optional, default is 1.\n"
                   "Example: /rng 4815 162342",

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


def get_help(command):
    '''
    Return a command's help message.
    '''
    if not command:
        return help_msg
    try:
        return cmd_help[command]
    except KeyError:
        return command + " is unavailable."


no_arg_commands = {'bencoin': AkunBenCoin.intro,
                   'lenny': '( ͡° ͜ʖ ͡°)',
                   'shrug': '¯\\_(ツ)_/¯'}

single_arg_commands = {'define': define,
                       'echo': echo,
                       'isup': isup,
                       'kbbi': kbbi_def,
                       'mcs': ask,
                       'mock': mock,
                       'palindrome': is_palindrome,
                       'pick': rpick,
                       'shout': shout,
                       'ticket': ticket_add,
                       'urban': urban,
                       'weather': weather,
                       'wolframs': wolfram}

double_arg_commands = {'ask': ask,
                       'isupd': isup,
                       'kbbix': kbbi_def,
                       'ppalindrome': is_palindrome,
                       'urbanx': urban}


def command_handler(text, user, me, set_id):
    '''
    Command handler for AidenBot.
    '''
    command = text.split(maxsplit=1)
    cmd = text.lower().split(maxsplit=1)
    result = None

    if cmd[0] == 'help':
        cmd = [cmd[0], ''] if len(cmd) == 1 else cmd
        result = ('text', get_help(cmd[1]))

    elif cmd[0] in no_arg_commands:
        result = ('text', no_arg_commands[cmd[0]])

    elif cmd[0] == 'tix' and user.user_id == me.user_id:
        result = ('text', ticket_get())

    elif cmd[0] in single_arg_commands:
        result = ('text', single_arg_commands[cmd[0]](command[1]))

    elif cmd[0] == 'rtix' and user.user_id == me.user_id:
        result = ('text', ticket_rem(command[1]))

    elif cmd[0] == 'stalkig':
        result = stalkig(command[1])
        if result[0]:
            result = ('multi', (('image', result[0]),
                                ('text', result[1])))
        else:
            result = ('text', result[1])

    elif cmd[0] in double_arg_commands:
        result = ('text', double_arg_commands[cmd[0]](command[1], True))

    elif cmd[0] == 'wolfram':
        result = ('image', wolfram(command[1], True))

    elif cmd[0] == 'wiki':
        result = ('text', wiki_get(command[1], set_id))

    elif cmd[0] == 'wikilang':
        result = ('text', wiki_lang(command[1], set_id))

    elif cmd[0] == 'slap':
        result = ('text', slap(user, command[1], me))

    elif cmd[0] == 'surprise':
        result = ('custimg', surprise())

    elif cmd[0] == 'cat':
        result = cat()
        result = ('image', result)

    elif cmd[0] == 'reddit':
        command = command[1].split()
        result = ('text', reddit_hot(command[0], command[-1], split=True))

    elif cmd[0] == 'rng':
        command = command[1].split()
        try:
            result = ('text', rng(command[-1], command[0]))
        except IndexError:
            result = ('text', rng(cmd[0]))

    return result
