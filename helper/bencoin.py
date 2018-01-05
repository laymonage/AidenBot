'''
BenCoin Manager
Programming Assignment 3 (modified)
Foundations of Programming
Fasilkom UI 2017
'''

import os
from .dropson import dbx_dl, dbx_ul, toJSON, getJSON

accounts_path = os.getenv('BENCOIN_ACCOUNTS_PATH', None)
acclinks_path = os.getenv('ACCOUNT_LINKS_PATH', None)
exchrate_path = os.getenv('EXCHANGE_RATE_PATH', None)


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
             "4. SETOR <jumlah uang> <mata uang>\n"
             "5. TARIK <jumlah BenCoin> <mata uang>\n"
             "6. TRANSFER <nama penerima> <jumlah BenCoin>\n"
             "7. INFO\n"
             "8. BANTUAN\n"
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

    help_msg = ("Perintah:\n"
                "DAFTAR <nama> <jenis akun>\n"
                "Mendaftarkan ID LINE Anda ke dalam sistem BenCoin atas nama "
                "<nama> dengan paket <jenis akun>.\n"
                "Anda dapat menggunakan perintah ini untuk mengubah nama "
                "akun BenCoin Anda, namun pastikan <jenis akun> sama dengan "
                "jenis akun Anda saat ini. Apabila berbeda, maka akun Anda "
                "didaftarkan ulang dan semua data rekening Anda dihapus.\n"
                "\n"
                "TAMBAH <mata uang> <rate awal>\n"
                "Menambahkan <mata uang> baru ke dalam sistem BenCoin dengan "
                "<rate awal> sebagai nilai awal 1 BenCoin dalam <mata uang>.\n"
                "\n"
                "UBAH <mata uang> <rate baru>\n"
                "Mengubah rate <mata uang> menjadi <rate baru>\n"
                "\n"
                "SETOR <jumlah uang> <mata uang>\n"
                "Menyetor uang sebanyak <jumlah uang> dalam <mata uang> "
                "ke akun BenCoin Anda.\n"
                "\n"
                "TARIK <jumlah BenCoin> <mata uang>\n"
                "Menarik BenCoin dari akun Anda sebanyak <jumlah BenCoin> "
                "dalam <mata uang>\n"
                "\n"
                "TRANSFER <nama penerima> <jumlah BenCoin>\n"
                "Mentransfer BenCoin sebesar <jumlah BenCoin> ke akun atas "
                "nama <nama penerima>.\n"
                "\n"
                "INFO\n"
                "Menampilkan info mengenai akun BenCoin Anda.\n"
                "\n"
                "BANTUAN\n"
                "Menampilkan pesan bantuan ini.")

    spek = {'Pelajar': {'lim_tbg': 150, 'lim_trx': 25, 'fee_trx': 0},
            'Reguler': {'lim_tbg': 500, 'lim_trx': 100, 'fee_trx': 5},
            'Bisnis': {'lim_tbg': 2000, 'lim_trx': 500, 'fee_trx': 15},
            'Elite': {'lim_tbg': 100000, 'lim_trx': 10000, 'fee_trx': 50}}
    valas = getJSON(dbx_dl(exchrate_path))

    def __init__(self, Nama, Jenis, saldo=0, riwayat=''):
        self.nama = Nama
        self.jenis = Jenis
        self.saldo = saldo
        self.lim_tbg = AkunBenCoin.spek[Jenis]['lim_tbg']
        self.lim_trx = AkunBenCoin.spek[Jenis]['lim_trx']
        self.fee_trx = AkunBenCoin.spek[Jenis]['fee_trx']
        self.riwayat = riwayat

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
        nominal (int), mata_uang (str)
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
        nominal (int), mata_uang (str)
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
        akun_penerima (AkunBenCoin), nominal (int)
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

    def toJSON(self):
        '''
        Mengubah instance AkunBenCoin ke dalam bentuk dict yang
        kompatibel dengan format JSON.
        '''
        return {'Nama': self.nama, 'Jenis': self.jenis,
                'Saldo': self.saldo, 'Riwayat': self.riwayat}


def daftar(ID, Nama, Jenis):
    '''
    Mendaftarkan akun baru di BenCoin dengan nama nasabah
    dan jenis tabungan yang telah ditentukan.
    ID (str): identitas unik untuk setiap akun (gunakan LINE userID)
    Nama (str): nama untuk akun yang akan didaftarkan
    Jenis (str): jenis akun yang didaftarkan
    '''
    Nama = Nama.title()
    Jenis = Jenis.title()
    if ID in tautan:
        if Jenis == akun[tautan[ID]].jenis:
            if Nama in tautan.values():
                return ("Akun atas nama {} sudah ada dalam sistem."
                        "Mohon gunakan nama lain untuk akun Anda."
                        .format(Nama))
            akun[Nama].nama = Nama
            tautan[ID] = Nama
            return ("Nama akun BenCoin Anda telah diubah menjadi {}"
                    .format(Nama))
    if Jenis in AkunBenCoin.spek:
        if ID in tautan:
            msg = ("Akun BenCoin Anda telah didaftarkan ulang atas nama {} "
                   "dengan paket {}.".format(Nama, Jenis))
        else:
            msg = ("Akun BenCoin Anda telah terdaftar atas nama {} "
                   "dengan paket {}.".format(Nama, Jenis))
        akun[Nama] = AkunBenCoin(Nama, Jenis)
        tautan[ID] = Nama
        return msg
    return "Jenis tabungan salah."


def perbarui_kurs(mata_uang, kurs, mode):
    '''
    Memperbarui daftar kurs valuta asing dengan menambah
    atau mengubah nilai tukar suatu mata uang dengan kurs
    yang ditentukan.
    mata_uang (str): mata uang yang akan dioperasikan
    kurs (int): nilai baru untuk mata uang tersebut
    mode (str): 'ubah': memperbarui mata uang yang sudah ada
                'tambah': menambah mata uang baru
    '''
    if kurs <= 0:
        return "Rate mata uang harus > 0."

    if mata_uang not in AkunBenCoin.valas and mode == 'ubah':
        return "Mata uang {} belum terdaftar!".format(mata_uang)
    AkunBenCoin.valas[mata_uang] = kurs
    if mode == 'ubah':
        msg = ("Rate mata uang {} berubah menjadi {} per BenCoin."
               .format(mata_uang, kurs))
    else:
        msg = ("Mata uang {} telah ditambahkan dengan rate {} per BenCoin."
               .format(mata_uang, kurs))
    # Mengunggah data kurs ke Dropbox
    dbx_ul(toJSON(AkunBenCoin.valas), exchrate_path, overwrite=True)
    return msg


def penangan_operasi(ID, perintah):
    '''
    Menangani operasi berdasarkan perintah yang diberikan.
    '''
    try:
        perintah = perintah.split()
        operasi = perintah[0].upper()

        if operasi == 'DAFTAR':
            nasabah, jenis = perintah[1].title(), perintah[2].title()
            msg = daftar(ID, nasabah, jenis)

        elif operasi == 'TAMBAH':
            MATA_UANG, nilai_tukar = perintah[1].upper(), int(perintah[2])
            msg = perbarui_kurs(MATA_UANG, nilai_tukar, 'tambah')

        elif operasi == 'UBAH':
            MATA_UANG, nilai_tukar = perintah[1].upper(), int(perintah[2])
            msg = perbarui_kurs(MATA_UANG, int(nilai_tukar), 'ubah')

        elif operasi == 'SETOR':
            jumlah, MATA_UANG = int(perintah[1]), perintah[2].upper()
            msg = akun[tautan[ID]].setor(jumlah, MATA_UANG)

        elif operasi == 'INFO':
            msg = str(akun[tautan[ID]])

        elif operasi == 'TRANSFER':
            penerima = perintah[1].title()
            jumlah = int(perintah[2])
            msg = akun[tautan[ID]].transfer(akun[penerima], jumlah)

        elif operasi == 'TARIK':
            jumlah, MATA_UANG = int(perintah[1]), perintah[2].upper()
            msg = akun[tautan[ID]].tarik(jumlah, MATA_UANG)

        elif operasi == 'BANTUAN':
            msg = AkunBenCoin.help_msg

        else:
            msg = "Perintah tidak tersedia."

        return msg

    except IndexError:
        return "Format perintah yang Anda masukkan salah."
    except KeyError as e:
        return ("Akun atas nama {} belum terdaftar dalam sistem."
                .format(e.args[0]))
    except ValueError:
        return "Format nilai yang Anda masukkan salah."
    else:
        # Mengunggah data ke Dropbox apabila operasi sukses.
        dbx_ul(toJSON({nasabah: akun[nasabah].toJSON() for nasabah in akun}),
               accounts_path, overwrite=True)


# Memuat JSON dari Dropbox.
akun = getJSON(dbx_dl(accounts_path))
tautan = getJSON(dbx_dl(acclinks_path))

# Mengkonversi data JSON ke dalam bentuk objek AkunBenCoin.
for nama in akun:
    akun[nama] = AkunBenCoin(Nama=akun[nama]['Nama'],
                             Jenis=akun[nama]['Jenis'],
                             saldo=akun[nama]['Saldo'],
                             riwayat=akun[nama]['Riwayat'])
