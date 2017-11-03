'''
AidenBot
Early test 2: kitchensink
'''

from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
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

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')


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

    if text == '/profile':
        if isinstance(event.source, (SourceUser, SourceGroup, SourceRoom)):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Display name: ' + profile.display_name +
                                '\nStatus message: ' + profile.status_message)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't use profile API without user ID")
            )

    elif text == '/bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text='Leaving group...')
            )
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text='Leaving room...')
            )
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't leave from 1:1 chat")
            )

    elif text[0] == '/':
        command = text[1:]
        if command.lower().startswith('wiki '):
            keyword = command[len('wiki '):].strip()
            try:
                wiki_result = wikipedia.summary(keyword)[:2000]
                if not wiki_result.endswith('.'):
                    wiki_result = wiki_result[:wiki_result.rfind('.')+1]

            except wikipedia.exceptions.DisambiguationError:
                wiki_articles = wikipedia.search(keyword)
                wiki_result = "{} disambiguation:\n".format(keyword)
                for article in wiki_articles:
                    wiki_result += "{}\n".format(article)

            except wikipedia.exceptions.PageError:
                wiki_result = "{} not found!".format(keyword)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=wiki_result)
            )

        elif command.lower().startswith('wikilang '):
            lang = command[len('wikilang '):].strip().lower()
            if lang in list(wikipedia.languages().keys()):
                wikipedia.set_lang(lang)
            else:
                langlist = ("{} not available!\nList of available languages:\n"
                            .format(lang))
                for available in list(wikipedia.languages().keys()):
                    langlist += "{}, ".format(available)
                langlist_1 = langlist[:2000]
                langlist_1 = langlist_1[:langlist_1.rfind(' ')]
                langlist_2 = langlist.replace(langlist_1, '').strip(', ')
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text=langlist_1),
                        TextSendMessage(text=langlist_2)
                    ]
                )

        elif command.lower().startswith('echo '):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=command[len('echo '):])
            )


@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    '''
    File message handler
    '''
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-',
                                     delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '-' + event.message.file_name
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Mirror: " + request.host_url +
                        os.path.join('static', 'tmp', dist_name))
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
