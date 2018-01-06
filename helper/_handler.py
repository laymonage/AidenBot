'''
Command handler module for AidenBot
'''

from . import (
    AkunBenCoin, cat, echo, shout, mock, is_palindrome, isup,
    kbbi_def, ask, define, reddit_hot, slap, stalkig,
    ticket_add, ticket_rem, ticket_get, surprise, urban,
    wiki_get, wiki_lang, wolfram, weather
)

help_msg = ("These commands will instruct me to:\n\n\n"
            "/ask <question> : Kulit Kerang Ajaib simulator\n\n"
            "/bye : leave this chat room\n\n"
            "/bencoin: [Fasilkom UI 2017 joke] send bencoin help message\n\n"
            "/cat : send a random cat image from thecatapi.com\n\n"
            "/define <word> : send definition(s) of <word>\n\n"
            "/echo <message> : send <message>\n\n"
            "/help : send this help message\n\n"
            "/isup <website> : check <website>'s status\n\n"
            "/isupd <website> : like /isup, but more detailed\n\n"
            "/kbbi <something> : send an entry of <something> in KBBI\n\n"
            "/kbbix <something> : like /kbbi, but with examples (if any)\n\n"
            "/lenny : send ( ͡° ͜ʖ ͡°)\n\n"
            "/mcs <question> : like /ask, but in English\n\n"
            "/profile : send your display name and your status message\n\n"
            "/reddit <subreddit> : send hot 5 posts' titles in <subreddit>\n\n"
            "/shout <message> : SEND <MESSAGE>\n\n"
            "/shrug : send ¯\\_(ツ)_/¯\n\n"
            "/slap <someone> : slap <someone> with a random object\n\n"
            "/stalkig <username> : send a random image taken from "
            "<username>'s instagram profile.\n\n"
            "/surprise : ?\n\n"
            "/ticket <something> : send <something> as a suggestion or bug "
            "report to the developer\n\n"
            "/urban <something> : send the top definition of <something> "
            "in UrbanDictionary\n\n"
            "/urbanx <something> : like /urban, but with examples (if any)\n\n"
            "/weather <location> : send current weather in <location>, "
            "obtained from weather.com\n\n"
            "/wiki <article> : send the summary of a Wikipedia <article>\n\n"
            "/wikilang <language> : change /wiki language\n\n"
            "/wolfram <something> : ask WolframAlpha about <something>\n\n"
            "/wolframs <something> : short answer version of /wolfram")

no_arg_commands = {'bencoin': AkunBenCoin.intro,
                   'help': help_msg,
                   'lenny': '( ͡° ͜ʖ ͡°)',
                   'shrug': '¯\\_(ツ)_/¯'}

single_arg_commands = {'define': define,
                       'echo': echo,
                       'isup': isup,
                       'kbbi': kbbi_def,
                       'mcs': ask,
                       'mock': mock,
                       'palindrome': is_palindrome,
                       'shout': shout,
                       'ticket': ticket_add,
                       'urban': urban,
                       'weather': weather,
                       'wolframs': wolfram}

double_arg_commands = {'ask': ask,
                       'isupd': isup,
                       'kbbix': kbbi_def,
                       'urbanx': urban}


def command_handler(text, user, me, set_id):
    '''
    Command handler for AidenBot.
    '''
    command = text.split(maxsplit=1)
    cmd = text.lower().split(maxsplit=1)
    result = None

    if cmd[0] in no_arg_commands:
        result = ('text', no_arg_commands[cmd[0]])

    elif cmd[0] == 'tix' and user.user_id == me.user_id:
        result = ('text', ticket_get())

    elif cmd[0] in single_arg_commands:
        result = ('text', single_arg_commands[cmd[0]](command[1]))

    elif cmd[0] == 'rtix' and user.user_id == me.user_id:
        result = ('text', ticket_rem(command[1]))

    elif cmd[0] == 'stalkig':
        result = stalkig(command[1])
        result = ('multi', (('image', result[0]),
                            ('text', result[1])))

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

    return result
