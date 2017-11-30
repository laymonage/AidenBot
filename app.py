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
from urllib.parse import urlparse, quote

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

import wikipedia
import urbandictionary as ud
import praw
import prawcore
import requests


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

oxdict_appid = os.getenv('OXFORD_DICT_APPID', None)
oxdict_key = os.getenv('OXFORD_DICT_APPKEY', None)

reddit_client = os.getenv('REDDIT_CLIENT_ID', None)
reddit_secret = os.getenv('REDDIT_CLIENT_SECRET', None)
reddit_object = praw.Reddit(client_id=reddit_client,
                            client_secret=reddit_secret,
                            user_agent='AidenBot-line')

wolfram_appid = os.getenv('WOLFRAMALPHA_APPID', None)

wunder_key = os.getenv('WUNDERGROUND_API_KEY', None)

AidenBot = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

slap_items = ["frying pan", "baseball bat", "cricket bat", "guitar", "crowbar",
              "wooden stick", "nightstick", "golf club", "katana", "hand",
              "laptop", "book", "drawing book", "mouse", "keyboard"]

note_items = {}

akun = {}

help_msg = ("These commands will instruct me to:\n\n\n"
            "/ask <question> : Kulit Kerang Ajaib simulator\n\n"
            "/bye : leave this chat room\n\n"
            "/bencoin: send bencoin app's help message\n\n"
            "/cat : send a random cat image from thecatapi.com\n\n"
            "/define <word> : send definition(s) of <word>\n\n"
            "/echo <message> : send <message>\n\n"
            "/help : send this help message\n\n"
            "/isup <website> : check <website>'s status\n\n"
            "/isupd <website> : like /isup, but more detailed\n\n"
            "/mcs <question> : like /ask, but in English\n\n"
            "/lenny : send ( ͡° ͜ʖ ͡°)\n\n"
            "/notes : send your notes\n\n"
            "/noteadd <something> : save <something> in your notes\n\n"
            "/noterem <number> : remove note <number> from your notes\n\n"
            "/profile : send your display name and your status message\n\n"
            "/reddit <subreddit> : send hot 5 posts' titles in <subreddit>\n\n"
            "/shout <message> : SEND <MESSAGE>\n\n"
            "/shrug : send ¯\\_(ツ)_/¯\n\n"
            "/slap <someone> : slap <someone> with a random object\n\n"
            "/stalkig <username> : send a random image taken from "
            "<username>'s instagram profile.\n\n"
            "/urban <something> : send the top definition of <something> "
            "in UrbanDictionary\n\n"
            "/weather <location> : send current weather in <location>, "
            "obtained from weather.com\n\n"
            "/wiki <article> : send the summary of a wiki <article>\n\n"
            "/wikilang <language> : change /wiki language\n\n"
            "/wolfram <something> : ask WolframAlpha about <something>\n\n"
            "/wolframs <something> : short answer version of /wolfram")


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


class AkunBenCoin(object):
    '''
    Tipe objek berupa akun BenCoin.
    '''
    intro = ("=======================================\n"
             "Selamat datang di administrasi BenCoin LINE!\n"
             "Berikut adalah perintah-perintah yang tersedia:\n"
             "=======================================\n"
             "1. DAFTAR <nama> <jenis akun>\n"
             "2. TAMBAH <mata uang> <rate awal>\n"
             "3. UBAH <mata uang> <rate baru>\n"
             "4. SETOR <nama> <jumlah uang> <mata uang>\n"
             "5. TARIK <nama> <jumlah BenCoin> <mata uang>\n"
             "6. TRANSFER <nama pengirim> <nama penerima> <jumlah BenCoin>\n"
             "7. INFO <nama>\n"
             "\n"
             "-----------------------------------------\n"
             "Jenis akun yang tersedia:\n"
             "Pelajar: Limit tabungan :    150\n"
             "         Limit transaksi:    100\n"
             "         Biaya transaksi:      0\n"
             "\n"
             "Reguler: Limit tabungan :    500\n"
             "         Limit transaksi:    100\n"
             "         Biaya transaksi:      5\n"
             "\n"
             "Bisnis : Limit tabungan :   2000\n"
             "         Limit transaksi:    100\n"
             "         Biaya transaksi:     15\n"
             "\n"
             "Elite  : Limit tabungan : 100000\n"
             "         Limit transaksi:  10000\n"
             "         Biaya transaksi:     50\n"
             "-----------------------------------------")

    spek = {'Pelajar': {'lim_tbg': 150, 'lim_trx': 25, 'fee_trx': 0},
            'Reguler': {'lim_tbg': 500, 'lim_trx': 100, 'fee_trx': 5},
            'Bisnis': {'lim_tbg': 2000, 'lim_trx': 500, 'fee_trx': 15},
            'Elite': {'lim_tbg': 100000, 'lim_trx': 10000, 'fee_trx': 50}}
    valas = {}

    def __init__(self, Nama, Jenis):
        self.nama = Nama
        self.jenis = Jenis
        self.saldo = 0
        self.lim_tbg = AkunBenCoin.spek[Jenis]['lim_tbg']
        self.lim_trx = AkunBenCoin.spek[Jenis]['lim_trx']
        self.fee_trx = AkunBenCoin.spek[Jenis]['fee_trx']
        self.riwayat = ''

    def __str__(self):
        '''
        Mengembalikan info akun dengan format:
        Nama: <nama>
        Jenis akun: <jenis>
        Jumlah BenCoin: <saldo>
        Transaksi:
        <riwayat transaksi>
        '''
        info = ("Nama: {}\n"
                "Jenis akun: {}\n"
                "Jumlah BenCoin: {}\n"
                "Transaksi:"
                .format(self.nama, self.jenis, self.saldo))
        if self.riwayat == '':
            info += "\nBelum ada transaksi."
        else:
            info += self.riwayat
        return info

    def __repr__(self):
        return str(self)

    def setor(self, nominal, mata_uang):
        '''
        Menambahkan saldo akun sebesar (nominal/kurs).
        Apabila saldo > batas tabungan, maka hanya
        tambahkan hingga saldo mencapai batas tabungan.
        '''
        if nominal <= 0:
            return "Nilai setor harus > 0."

        if mata_uang not in AkunBenCoin.valas:
            return ("Mata uang {} belum terdaftar dalam sistem."
                    .format(mata_uang))

        if self.saldo + (nominal/AkunBenCoin.valas[mata_uang]) > self.lim_tbg:
            ben_setor = self.lim_tbg - self.saldo
        else:
            ben_setor = nominal/AkunBenCoin.valas[mata_uang]

        if ben_setor == 0:
            return ("Saldo akun {} sudah mencapai limit tabungan."
                    .format(self.nama))

        # Nominal yang berhasil disetor:
        # kas_setor = ben_setor * AkunBenCoin.valas[mata_uang]
        self.saldo += ben_setor
        self.riwayat += ("\nSETOR {} {} -> {} BenCoin"
                         .format(mata_uang, nominal, ben_setor))

        return ("Akun {} telah bertambah {} BenCoin."
                .format(self.nama, ben_setor))

    def tarik(self, nominal, mata_uang):
        '''
        Mengurangi saldo akun dengan jumlah * kurs
        dengan biaya transaksi yang sudah ditentukan.
        Apabila sisa saldo < 0, maka hanya tarik
        sehingga saldo bernilai 0 setelah dikurangi
        dengan biaya transaksi.
        '''
        if nominal <= 0:
            return "Nilai tarik harus > 0."

        if mata_uang not in AkunBenCoin.valas:
            return("Mata uang {} belum terdaftar dalam sistem."
                   .format(mata_uang))

        ben_tarik = nominal
        if ben_tarik > self.lim_trx:
            ben_tarik = self.lim_trx

        if self.saldo - ben_tarik <= self.fee_trx:
            ben_tarik = self.saldo - self.fee_trx

        if ben_tarik <= 0:
            return "Saldo tidak mencukupi untuk melakukan penarikan."

        kas_tarik = ben_tarik * AkunBenCoin.valas[mata_uang]
        self.riwayat += ("\nTARIK {} {} -> {:.2f} BenCoin"
                         .format(mata_uang, kas_tarik, ben_tarik))
        ben_tarik += self.fee_trx
        self.saldo -= ben_tarik

        return ("Penarikan {} {} dari akun {} berhasil."
                .format(mata_uang, kas_tarik, self.nama))

    def transfer(self, akun_penerima, nominal):
        '''
        Memindahkan saldo sebesar nominal dari saldo self
        ke saldo penerima dengan biaya transaksi yang
        sudah ditentukan.
        Apabila sisa saldo self < 0, maka hanya pindahkan
        sehingga saldo bernilai 0 setelah dikurangi
        dengan biaya transaksi.
        Apabila saldo penerima melebihi limit_tabungan,
        maka hanya pindahkan sehingga saldo penerima
        mencapai limit tabungan.
        '''
        if nominal <= 0:
            return "Nilai transfer harus > 0."

        if self.saldo == 0:
            return ("Saldo akun {} tidak mencukupi untuk melakukan transfer."
                    .format(self.nama))

        if akun_penerima == self:
            return ("{} tidak bisa melakukan transfer ke akunnya sendiri."
                    .format(self.nama))

        ben_transf = nominal
        if ben_transf > self.lim_trx:
            ben_transf = self.lim_trx

        if self.saldo - ben_transf <= self.fee_trx:
            ben_transf = self.saldo - self.fee_trx

        if ben_transf <= 0:
            return "Saldo tidak mencukupi untuk melakukan transfer."

        if ben_transf + akun_penerima.saldo > akun_penerima.lim_tbg:
            ben_transf = akun_penerima.lim_tbg - akun_penerima.saldo

        if ben_transf == 0:
            return ("Akun {} sudah mencapai limit tabungan."
                    .format(akun_penerima.nama))

        akun_penerima.saldo += ben_transf
        self.riwayat += ("\nTRANSFER {} -> {} BenCoin"
                         .format(akun_penerima.nama, ben_transf))
        self.saldo -= ben_transf + self.fee_trx

        return ("{} berhasil mentransfer {} BenCoin kepada {}."
                .format(self.nama, ben_transf, akun_penerima.nama))


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    '''
    Text message handler
    '''
    text = event.message.text

    # BenCoin begin
    def daftar(Nama, Jenis):
        '''
        Mendaftarkan akun baru di BenCoin dengan nama nasabah
        dan jenis tabungan yang telah ditentukan.
        '''
        if Nama in akun:
            return "Akun atas nama {} sudah ada dalam sistem!".format(Nama)
        if Jenis in AkunBenCoin.spek:
            akun[Nama] = AkunBenCoin(Nama, Jenis)
            return ("Akun atas nama {} telah terdaftar dengan paket {}."
                    .format(Nama, Jenis))
        return "Jenis tabungan salah."

    def perbarui_kurs(mata_uang, kurs, mode):
        '''
        Memperbarui daftar kurs valuta asing dengan menambah
        atau mengubah nilai tukar suatu mata uang dengan kurs
        yang ditentukan.
        '''
        if kurs <= 0:
            return "Rate mata uang harus > 0."

        if mata_uang not in AkunBenCoin.valas and mode == 'ubah':
            return "Mata uang {} belum terdaftar!".format(mata_uang)
        AkunBenCoin.valas[mata_uang] = kurs
        if mode == 'ubah':
            return ("Rate mata uang {} berubah menjadi {} per BenCoin."
                    .format(mata_uang, kurs))
        return ("Mata uang {} telah ditambahkan dengan rate {} per BenCoin."
                .format(mata_uang, kurs))
    # BenCoin end

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

    def cat():
        '''
        Send a random cat pic from thecatapi.com
        '''
        url = 'http://thecatapi.com/api/images/get'
        req = requests.get(url)
        url = req.url.replace('http://', 'https://')
        AidenBot.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )
        )

    def define(word):
        '''
        Send word definition from oxforddictionaries.com
        '''
        word = quote(word)
        url = ('https://od-api.oxforddictionaries.com:443/api/v1/entries/en/{}'
               .format(word))
        req = requests.get(url, headers={'app_id': oxdict_appid,
                                         'app_key': oxdict_key})
        if "No entry available" in req.text:
            quickreply('No entry available for "{}".'.format(word))
            return
        req = req.json()
        result = ''
        i = 0
        for each_result in req['results']:
            for each_lexEntry in each_result['lexicalEntries']:
                for each_entry in each_lexEntry['entries']:
                    for each_sense in each_entry['senses']:
                        if 'crossReferenceMarkers' in each_sense:
                            search = 'crossReferenceMarkers'
                        else:
                            search = 'definitions'
                        for each_def in each_sense[search]:
                            i += 1
                            result += '\n{}. {}'.format(i, each_def)

        if i == 1:
            result = 'Definition of {}:\n'.format(word) + result[4:]
        else:
            result = 'Definitions of {}:'.format(word) + result
        quickreply(result)

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

    def isup(site, mode='simple'):
        '''
        Send site status received from https://isitup.org
        '''
        if not site.startswith('http'):
            url = 'http://{}'.format(site)
        else:
            url = site
        domain = urlparse(url).netloc
        api_url = 'https://isitup.org/{}.txt'.format(domain)

        try:
            data = requests.get(api_url).text
            data = data.split(', ')
            status_code = int(data[2])
        except requests.exceptions.ConnectionError:
            status_code = 4

        if status_code == 1:
            result = "{} is up.".format(site)
        elif status_code == 2:
            result = "{} seems to be down.".format(site)
        elif status_code == 3:
            result = "{} is not a valid domain.".format(site)
        elif status_code == 4:
            result = "Sorry, the isitup.org service seems to be down."
        else:
            result = "Sorry, I encountered an error in the API."

        if mode == 'detailed' and status_code == 1:
            result += ("\nIP: {}"
                       "\nResponse code: {}"
                       "\nResponse time: {} ms"
                       .format(data[3], data[4], float(data[5])*1000))

        quickreply(result)

    def note_add(user_id, item):
        '''
        Save notes for a particular user.
        '''
        if user_id not in note_items.keys():
            note_items[user_id] = []

        if item in note_items[user_id]:
            quickreply("Note already exists.")

        elif len('num. \n'.join(note_items[user_id] + [item])) > 2000:
            quickreply(("Your notepad is full. "
                        "Please remove some of your notes."))
        else:
            note_items[user_id].append(item)
            quickreply("Saved.")

    def note_get(user_id):
        '''
        Send notes of a particular user.
        '''
        if user_id not in note_items.keys():
            quickreply("You haven't saved any notes.")
        elif not note_items[user_id]:
            quickreply("Your notepad is empty.")
        else:
            notes = "Your notes:\n"
            for num, items in enumerate(note_items[user_id]):
                notes = "{}. {}\n".format(num+1, items)
            quickreply(notes[:-1])

    def note_rem(user_id, num):
        '''
        Remove an item from a user's notes.
        '''
        if user_id not in note_items.keys():
            quickreply("You haven't saved any notes.")
        elif not note_items[user_id]:
            quickreply("Your notepad is empty.")
        else:
            try:
                del note_items[user_id][num-1]
                quickreply(("Item [{}] has been removed from your notes."
                            .format(num)))
            except IndexError:
                quickreply("Item [{}] is not in your notes.".format(num))

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
        s_name = subject.display_name
        me = AidenBot.get_profile(my_id)
        itsme = subject == me
        has_my_name = not itsme and me.display_name.title() in s_name.title()

        if has_my_name:
            if me.display_name.lower() == s_name.lower():
                slap_msg = ("IMPERSONATOR! >:(\n"
                            "I slapped you back and forth with a {} "
                            "for impersonating my creator."
                            .format(random.choice(slap_items)))
            else:
                slap_msg = ("NOT FUNNY! >:("
                            "I slapped you back and forth with a {} "
                            "for making fun of my creator."
                            .format(random.choice(slap_items)))

        if "Aiden" in target.title():
            if itsme:
                slap_msg = ("{} gently slapped me.\n"
                            "Sorry, {} :("
                            .format(s_name, s_name))

            elif has_my_name:
                slap_msg = slap_msg[:-1] + " AND trying to slap me."

            else:
                slap_msg = ("I slapped {} with a {} for trying to slap me."
                            .format(s_name, random.choice(slap_items)))

        elif ''.join(c for c in target.lower() if c.isalpha()) == "me":
            if itsme:
                slap_msg = ("Sorry, {}, but I can't bring myself to "
                            "slap you :("
                            .format(s_name))

            elif has_my_name:
                slap_msg = slap_msg[:-1] + " AND asking me to slap you."

            else:
                slap_msg = ("I slapped {} with a {} at their request."
                            .format(s_name, random.choice(slap_items)))

        elif "myself" in target.lower():
            if itsme:
                slap_msg = ("Sorry, {}, but I can't let you slap yourself :("
                            .format(s_name))

            elif has_my_name:
                slap_msg = slap_msg[:-1] + " AND wanted to slap yourself."

            else:
                slap_msg = ("{} slapped themself with a {}."
                            .format(s_name, random.choice(slap_items)))

        elif me.display_name.title() in target.title():
            slap_msg = ("You shouldn't include my creator's name in your "
                        "slapping target.")

        else:
            slap_msg = ("{} slapped {} with a {}."
                        .format(s_name, target, random.choice(slap_items)))

        quickreply(slap_msg)

    def stalkig(username):
        '''
        Send a random image taken from username's instagram profile.
        '''
        url = 'https://www.instagram.com/{}/?__a=1'.format(username)
        req = requests.get(url)
        if req.status_code == 404:
            quickreply("@{} not found!".format(username))
        else:
            req = req.json()
            if req['user']['is_private']:
                quickreply("@{} is a private account.".format(username))
            else:
                nodes = req['user']['media']['nodes']
                image = random.choice(nodes)['display_src']
                AidenBot.reply_message(
                    event.reply_token,
                    ImageSendMessage(
                        original_content_url=image,
                        preview_image_url=image
                    )
                )

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

    def weather(keyword):
        '''
        Send current weather condition of a location, obtained from
        Weather Underground.
        '''
        url = ('http://api.wunderground.com/api/{}/conditions/q/{}.json'
               .format(wunder_key, quote(keyword)))
        data = requests.get(url).json()
        if 'results' in data['response'].keys():
            locID = data['response']['results'][0]['l']
            url = url[:url.find('/q/')] + locID + '.json'
            data = requests.get(url).json()

        try:
            data = data['current_observation']
            result = ("Weather in {}:\n"
                      "{}\n"
                      "Temperature: {}°C ({}°F)\n"
                      "Feels like: {}°C ({}°F)"
                      .format(data['display_location']['full'],
                              data['weather'],
                              data['temp_c'], data['temp_f'],
                              data['feelslike_c'], data['feelslike_f']))
        except KeyError:
            result = "Location is not found or not specific enough."
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

    def wolfram(query, mode='simple'):
        '''
        Get answer from WolframAlpha.
        '''
        url = ('https://api.wolframalpha.com/v1/{}?i={}&appid={}'
               .format(mode, quote(query), wolfram_appid))
        if mode == 'simple':
            AidenBot.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=url,
                    preview_image_url=url
                )
            )
        if mode == 'result':
            quickreply(requests.get(url).text)

    if text[0] == '/':
        command = text[1:]

        if command.lower().strip().startswith('ask '):
            question = command[len('ask '):]
            ask(question, 'id')

        if command.lower().strip().startswith('bencoin'):
            quickreply(AkunBenCoin.intro)

        if command.lower().strip().startswith('bye'):
            bye()

        if command.lower().strip().startswith('cat'):
            cat()

        if command.lower().strip().startswith('define '):
            word = command[len('define '):]
            define(word)

        if command.lower().startswith('echo '):
            echo_msg = command[len('echo '):]
            quickreply(echo_msg)

        if command.lower().strip().startswith('help'):
            quickreply(help_msg)

        if command.lower().startswith('isup '):
            site = command[len('isup '):]
            isup(site)

        if command.lower().startswith('isupd '):
            site = command[len('isupd '):]
            isup(site, 'detailed')

        if command.lower().strip().startswith('mcs '):
            question = command[len('mcs '):]
            ask(question)

        if command.lower().strip().startswith('lenny'):
            quickreply('( ͡° ͜ʖ ͡°)')

        if command.lower().strip().startswith('notes'):
            note_get(event.source.user_id)

        if command.lower().startswith('noteadd '):
            item = command[len('noteadd '):]
            note_add(event.source.user_id, item)

        if command.lower().strip().startswith('noterem '):
            item = int(command[len('noterem ')])
            note_rem(event.source.user_id, item)

        if command.lower().strip().startswith('profile'):
            getprofile()

        if command.lower().startswith('reddit '):
            keyword = command[len('reddit '):].strip()
            reddit(keyword)

        if command.lower().startswith('shout '):
            shout_msg = command[len('shout '):].upper()
            quickreply(shout_msg)

        if command.lower().strip().startswith('shrug'):
            quickreply('¯\\_(ツ)_/¯')

        if command.lower().startswith('slap '):
            target = command[len('slap '):].strip()
            subject = AidenBot.get_profile(event.source.user_id)
            slap(subject, target)

        if command.lower().startswith('stalkig '):
            username = command[len('stalkig '):].strip()
            stalkig(username)

        if command.lower().startswith('urban '):
            keyword = command[len('urban '):].strip()
            urban(keyword)

        if command.lower().startswith('weather '):
            keyword = command[len('weather '):].strip()
            weather(keyword)

        if command.lower().startswith('wiki '):
            keyword = command[len('wiki '):].strip()
            wiki(keyword)

        if command.lower().startswith('wikilang '):
            keyword = command[len('wikilang '):].strip().lower()
            wikilang(keyword)

        if command.lower().startswith('wolfram '):
            query = command[len('wolfram '):].strip()
            wolfram(query)

        if command.lower().startswith('wolframs '):
            query = command[len('wolframs '):].strip()
            wolfram(query, 'result')

    # BenCoin begin
    try:
        perintah = text.split()
        operasi = perintah[0]

        if operasi == 'DAFTAR':
            nama, jenis = perintah[1].title(), perintah[2].title()
            msg = daftar(nama, jenis)
            quickreply(msg)

        elif operasi == 'TAMBAH':
            MATA_UANG, nilai_tukar = perintah[1].upper(), int(perintah[2])
            msg = perbarui_kurs(MATA_UANG, nilai_tukar, 'tambah')
            quickreply(msg)

        elif operasi == 'UBAH':
            MATA_UANG, nilai_tukar = perintah[1].upper(), int(perintah[2])
            msg = perbarui_kurs(MATA_UANG, int(nilai_tukar), 'ubah')
            quickreply(msg)

        elif operasi == 'SETOR':
            nama = perintah[1].title()
            jumlah, MATA_UANG = int(perintah[2]), perintah[3].upper()
            msg = akun[nama].setor(jumlah, MATA_UANG)
            quickreply(msg)

        elif operasi == 'INFO':
            nama = perintah[1].title()
            msg = str(akun[nama])
            quickreply(msg)

        elif operasi == 'TRANSFER':
            nama, penerima = perintah[1].title(), perintah[2].title()
            jumlah = int(perintah[3])
            msg = akun[nama].transfer(akun[penerima], jumlah)
            quickreply(msg)

        elif operasi == 'TARIK':
            nama = perintah[1].title()
            jumlah, MATA_UANG = int(perintah[2]), perintah[3].upper()
            msg = akun[nama].tarik(jumlah, MATA_UANG)
            quickreply(msg)

    except IndexError:
        quickreply("Format perintah yang Anda masukkan salah.")
    except KeyError as e:
        quickreply(("Akun atas nama {} belum terdaftar dalam sistem."
                    .format(e.args[0])))
    except ValueError:
        quickreply("Format nilai yang Anda masukkan salah.")
    # BenCoin end


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
                        quote((os.path.join('static', 'tmp', dist_name))))
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
