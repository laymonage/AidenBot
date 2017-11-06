'''
AidenBot
Early test 3: indev
'''

from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
import random
from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom, FileMessage,
    UnfollowEvent, LeaveEvent
)

import wikipedia
import urbandictionary as ud
import praw
import prawcore


app = Flask(__name__)

# Get channel_secret and channel_access_token from environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

my_id = os.getenv('MY_USER_ID', None)

reddit_client = os.getenv('REDDIT_CLIENT_ID', None)
reddit_secret = os.getenv('REDDIT_CLIENT_SECRET', None)
reddit_object = praw.Reddit(client_id=reddit_client,
                            client_secret=reddit_secret,
                            user_agent='AidenBot-line')

AidenBot = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

slap_items = ["frying pan", "baseball bat", "cricket bat", "guitar", "crowbar",
              "wooden stick", "nightstick", "golf club", "katana", "hand",
              "laptop", "book", "drawing book", "mouse", "keyboard"]

help_msg = ("These commands will instruct me to:\n\n\n"
            "/ask <question> : Kulit Kerang Ajaib simulator\n\n"
            "/bye : leave this chat room\n\n"
            "/echo <message> : send <message>\n\n"
            "/help : send this help message\n\n"
            "/mcs <question> : like /ask, but in English\n\n"
            "/profile : send your display name and your status message\n\n"
            "/reddit <subreddit> : send hot 5 posts' titles in <subreddit>\n\n"
            "/shout <message> : SEND <MESSAGE>\n\n"
            "/slap <someone> : slap <someone> with a random object\n\n"
            "/urban <something> : send the top definition of <something> "
            "in UrbanDictionary\n\n"
            "/wiki <article> : send the summary of a wiki <article>\n\n"
            "/wikilang <language> : change /wiki language")


def make_static_tmp_dir():
    '''
    Create temporary directory for download content
    '''
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


@app.route("/callback", methods=['POST'])
def callback():
    '''
    Webhook callback function
    '''
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    '''
    Text message handler
    '''
    text = event.message.text

    def quickreply(msg):
        '''
        Reply a message with msg as reply content.
        '''
        AidenBot.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )

    def ask(question, lang=None):
        '''
        Send something a magic conch shell would say.
        '''
        kka = ["Ya.", "Tidak."]
        mcs = ["Yes.", "No."]

        if "Akan" in question.title():
            kka.append("Mungkin suatu hari.")
        elif "Will " in question.title():
            mcs.append("Maybe someday.")

        if ("Belum" in question.title() or
                "Sudah" in question.title() or
                "Belom" in question.title() or
                "Udah" in question.title() or
                "Udeh" in question.title()):
            kka.remove("Ya.")
            kka.remove("Tidak.")
            kka.append("Sudah.")
            kka.append("Belum.")

        if lang == 'id':
            say = random.choice(kka)
        else:
            say = random.choice(mcs)

        if "jawab" in question.lower() and "lain" in question.lower():
            say = "Coba tanya lagi."
        if (("say" in question.lower() or
             "answer" in question.lower() or
             "reply" in question.lower()) and
                ("anything else" in question.lower() or
                 "other than" in question.lower())):
            say = "Try asking again."

        quickreply(say)

    def bye():
        '''
        Leave a chat room.
        '''
        if isinstance(event.source, SourceGroup):
            quickreply("Leaving group...")
            AidenBot.leave_group(event.source.group_id)

        elif isinstance(event.source, SourceRoom):
            quickreply("Leaving room...")
            AidenBot.leave_room(event.source.room_id)

        else:
            quickreply("I can't leave a 1:1 chat.")

    def getprofile():
        '''
        Send display name and status message of a user.
        '''
        if isinstance(event.source, (SourceUser, SourceGroup, SourceRoom)):
            profile = AidenBot.get_profile(event.source.user_id)
            if profile.status_message:
                status = profile.status_message
            else:
                status = ""

            quickreply("Display name: " + profile.display_name +
                       "\nStatus message: " + status)

        else:
            quickreply("Bot can't use profile API without user ID")

    def reddit(subname):
        '''
        Send top 5 posts' titles in a subreddit.
        '''
        sub = reddit_object.subreddit(subname).hot(limit=5)
        try:
            i = 1
            result = "Top 5 posts in /r/{}:\n".format(keyword)
            for posts in sub:
                result += "{}. {}\n".format(i, posts.title)
                i += 1

        except prawcore.exceptions.Redirect:
            result = "{} subreddit not found.".format(keyword)

        quickreply(result.strip())

    def slap(subject, target):
        '''
        Send a message stating "Subject slapped target with a random object."
        '''
        subject_name = subject.display_name

        if "Aiden" in target.title():
            if subject.user_id == my_id:
                slap_msg = ("{} gently slapped me.\n"
                            "Sorry :("
                            .format(subject_name))
            else:
                slap_msg = ("I slapped {} with a {} for trying to slap me."
                            .format(subject, random.choice(slap_items)))

        elif (''.join(c for c in target.lower() if c.isalpha()) == "me"
              or "myself" in target.lower()):
            slap_msg = ("I slapped {} with a {} at their request."
                        .format(subject, random.choice(slap_items)))

        else:
            slap_msg = ("{} slapped {} with a {}."
                        .format(subject, target,
                                random.choice(slap_items)))

        quickreply(slap_msg)

    def urban(keyword):
        '''
        Send the top definition of keyword in Urban Dictionary.
        '''
        if keyword.lower() == 'sage':
            item = ud.define(keyword)[5]
        else:
            item = ud.define(keyword)[0]

        if item == []:
            result = "{} not found in UrbanDictionary.".format(keyword)

        else:
            result = "{}:\n{}".format(item.word, item.definition)

        quickreply(result)

    def wiki(keyword):
        '''
        Send a summary of a wikipedia article with keyword as the title,
        or send a list of titles in the disambiguation page.

        '''
        try:
            result = wikipedia.summary(keyword)[:2000]
            if not result.endswith('.'):
                result = result[:result.rfind('.')+1]

        except wikipedia.exceptions.DisambiguationError:
            articles = wikipedia.search(keyword)
            result = "{} disambiguation:\n".format(keyword)
            for item in articles:
                result += "{}\n".format(item)

        except wikipedia.exceptions.PageError:
            result = "{} not found!".format(keyword)

        quickreply(result)

    def wikilang(lang):
        '''
        Change wikipedia language.
        '''
        if lang in list(wikipedia.languages().keys()):
            wikipedia.set_lang(lang)
            quickreply(("Language has been changed to {} successfully."
                        .format(lang)))

        else:
            langlist = ("{} not available!\nList of available languages:\n"
                        .format(lang))
            for available in list(wikipedia.languages().keys()):
                langlist += "{}, ".format(available)
            langlist_1 = langlist[:2000]
            langlist_1 = langlist_1[:langlist_1.rfind(' ')]
            langlist_2 = langlist.replace(langlist_1, '').strip(', ')

            AidenBot.reply_message(
                event.reply_token, [
                    TextSendMessage(text=langlist_1),
                    TextSendMessage(text=langlist_2)
                ]
            )

    if text[0] == '/':
        command = text[1:]

        if command.lower().strip().startswith('ask '):
            question = command[len('ask '):]
            ask(question, 'id')

        if command.lower().strip().startswith('bye'):
            bye()

        if command.lower().startswith('echo '):
            echo_msg = command[len('echo '):]
            quickreply(echo_msg)

        if command.lower().strip().startswith('help'):
            quickreply(help_msg)

        if command.lower().strip().startswith('mcs '):
            question = command[len('mcs '):]
            ask(question)

        if command.lower().strip().startswith('profile'):
            getprofile()

        if command.lower().startswith('reddit '):
            keyword = command[len('reddit '):].strip()
            reddit(keyword)

        if command.lower().startswith('shout '):
            shout_msg = command[len('shout '):].upper()
            quickreply(shout_msg)

        if command.lower().startswith('slap '):
            target = command[len('slap '):].strip()
            subject = AidenBot.get_profile(event.source.user_id)
            slap(subject, target)

        if command.lower().startswith('urban '):
            keyword = command[len('urban '):].strip()
            urban(keyword)

        if command.lower().startswith('wiki '):
            keyword = command[len('wiki '):].strip()
            wiki(keyword)

        if command.lower().startswith('wikilang '):
            keyword = command[len('wikilang '):].strip().lower()
            wikilang(keyword)


@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    '''
    File message handler
    '''
    message_content = AidenBot.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-',
                                     delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '-' + event.message.file_name
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    AidenBot.reply_message(
        event.reply_token,
        TextSendMessage(text="Mirror: " + request.host_url +
                        (os.path.join('static', 'tmp', dist_name)
                         .replace(' ', '%20')))
    )


@handler.add(UnfollowEvent)
def handle_unfollow():
    '''
    Unfollow event handler
    '''
    app.logger.info("Got Unfollow event")


@handler.add(LeaveEvent)
def handle_leave():
    '''
    Leave event handler
    '''
    app.logger.info("Got leave event")


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # Create temporary directory for download content
    make_static_tmp_dir()
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', debug=options.debug, port=port)
