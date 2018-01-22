'''
AidenBot
v0.96: public
'''

import errno
import os
import sys
import tempfile
from urllib.parse import quote

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
    SourceUser, SourceGroup, SourceRoom, FileMessage,
    UnfollowEvent, LeaveEvent
)

from helper._handler import command_handler
from helper.bencoin import penangan_operasi


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

AidenBot = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

my_id = os.getenv('MY_USER_ID', None)
me = AidenBot.get_profile(my_id)


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
    app.logger.info(("Request body: ", body))

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
    if isinstance(event.source, SourceGroup):
        subject = AidenBot.get_group_member_profile(event.source.group_id,
                                                    event.source.user_id)
        set_id = event.source.group_id
    elif isinstance(event.source, SourceRoom):
        subject = AidenBot.get_room_member_profile(event.source.room_id,
                                                   event.source.user_id)
        set_id = event.source.room_id
    else:
        subject = AidenBot.get_profile(event.source.user_id)
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
        AidenBot.reply_message(
            event.reply_token, content
        )

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

    if text[0] == '/':
        command = text[1:]
        result = command_handler(command, subject, me, set_id)
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

    elif text.split()[0] in ('DAFTAR', 'TAMBAH', 'UBAH', 'SETOR',
                             'INFO', 'TRANSFER', 'TARIK', 'BANTUAN'):
        quickreply(penangan_operasi(event.source.user_id, text.strip()))


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
        event.reply_token, [
            TextSendMessage(text="Mirror:"),
            TextSendMessage(text=request.host_url +
                            quote((os.path.join('static', 'tmp', dist_name))))
            ]
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
    # Create temporary directory for download content
    make_static_tmp_dir()

    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
