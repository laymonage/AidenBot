'''
AidenBot
v0.97
'''

import errno
import os
import sys

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
    SourceGroup, SourceRoom, FileMessage, UnfollowEvent, LeaveEvent
)

from helper._handler import command_handler
from helper.file import mirror


APP = Flask(__name__)

# Get CHANNEL_SECRET and CHANNEL_ACCESS_TOKEN from environment variable
CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', None)
CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if CHANNEL_SECRET is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if CHANNEL_ACCESS_TOKEN is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

AIDEN = LineBotApi(CHANNEL_ACCESS_TOKEN)
HANDLER = WebhookHandler(CHANNEL_SECRET)

MAXIMUM_MIRROR_SIZE = 52428800
STATIC_TMP_PATH = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

MY_ID = os.getenv('MY_USER_ID', None)
MYSELF = AIDEN.get_profile(MY_ID)


def make_static_tmp_dir():
    '''
    Create temporary directory for download content
    '''
    try:
        os.makedirs(STATIC_TMP_PATH)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(STATIC_TMP_PATH):
            pass
        else:
            raise


@APP.route("/callback", methods=['POST'])
def callback():
    '''
    Webhook callback function
    '''
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    APP.logger.info(("Request body: ", body))

    # handle webhook body
    try:
        HANDLER.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@HANDLER.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    '''
    Text message HANDLER
    '''
    text = event.message.text
    if isinstance(event.source, SourceGroup):
        subject = AIDEN.get_group_member_profile(event.source.group_id,
                                                 event.source.user_id)
        set_id = event.source.group_id
    elif isinstance(event.source, SourceRoom):
        subject = AIDEN.get_room_member_profile(event.source.room_id,
                                                event.source.user_id)
        set_id = event.source.room_id
    else:
        subject = AIDEN.get_profile(event.source.user_id)
        set_id = event.source.user_id

    def quickreply(*msgs, mode=('text',)*5):
        '''
        Reply a message with msgs as reply content.
        '''
        msgs = msgs[:5]
        content = []
        for idx, msg in enumerate(msgs):
            if mode[idx] == 'text':
                if isinstance(msg, (tuple, list)):
                    content = [TextSendMessage(text=item) for item in msg]
                else:
                    content.append(TextSendMessage(text=msg))
            elif mode[idx] == 'image':
                if isinstance(msg, (tuple, list)):
                    content = [ImageSendMessage(original_content_url=item,
                                                preview_image_url=item)
                               for item in msg]
                else:
                    content.append(ImageSendMessage(
                        original_content_url=msg,
                        preview_image_url=msg))
            elif mode[idx] == 'custimg':
                if isinstance(msg, (tuple, list)):
                    content = [ImageSendMessage(original_content_url=item[0],
                                                preview_image_url=item[1])
                               for item in msg]
                else:
                    content.append(ImageSendMessage(
                        original_content_url=msg[0],
                        preview_image_url=msg[1]))
        AIDEN.reply_message(
            event.reply_token, content
        )

    def bye():
        '''
        Leave a chat room.
        '''
        if isinstance(event.source, SourceGroup):
            quickreply("K, Bye")
            AIDEN.leave_group(event.source.group_id)

        elif isinstance(event.source, SourceRoom):
            quickreply("K, Bye")
            AIDEN.leave_room(event.source.room_id)

        else:
            quickreply("I can't leave a 1:1 chat, idiot.")

    def getprofile():
        '''
        Send display name and status message of a user.
        '''
        result = ("Display name: " + subject.display_name + "\n"
                  "Profile picture: " + subject.picture_url)
        try:
            profile = AIDEN.get_profile(event.source.user_id)
            if profile.status_message:
                result += "\n" + "Status message: " + profile.status_message
        except LineBotApiError:
            pass
        quickreply(result)

    if text[0] == '/':
        command = text[1:]
        result = command_handler(command, subject, MYSELF, set_id)
        if command.lower().strip().startswith('bye'):
            bye()
        elif command.lower().strip().startswith('profile'):
            getprofile()
        elif result:
            if result[0] in ('text', 'image', 'custimg'):
                quickreply(*result[1:], mode=(result[0],)*len(result[1:]))
            elif result[0] == 'multi':
                mode, content = [], []
                for item in result[1]:
                    mode.append(item[0])
                    content.append(item[1])
                quickreply(*content, mode=mode)
            else:
                quickreply(result)


@HANDLER.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    '''
    File message HANDLER
    '''
    message_content = AIDEN.get_message_content(event.message.id)
    if isinstance(event.source, SourceGroup):
        set_id = event.source.group_id
    elif isinstance(event.source, SourceRoom):
        set_id = event.source.room_id
    else:
        set_id = event.source.user_id

    link = mirror(message_content, event.message.file_name,
                  request.host_url, set_id)

    if not link:
        return

    file_size = int(message_content.response.headers['Content-Length'])

    if file_size > MAXIMUM_MIRROR_SIZE:
        AIDEN.reply_message(
            event.reply_token,
            TextSendMessage(text="File size shouldn't exceed 50 MB.")
        )

    AIDEN.reply_message(
        event.reply_token, [
            TextSendMessage(text="Mirror:"),
            TextSendMessage(text=link)
            ]
    )


@HANDLER.add(UnfollowEvent)
def handle_unfollow():
    '''
    Unfollow event HANDLER
    '''
    APP.logger.info("Got Unfollow event")


@HANDLER.add(LeaveEvent)
def handle_leave():
    '''
    Leave event HANDLER
    '''
    APP.logger.info("Got leave event")


if __name__ == "__main__":
    # Create temporary directory for download content
    make_static_tmp_dir()

    PORT = int(os.getenv('PORT', 5000))
    APP.run(host='0.0.0.0', port=PORT)
