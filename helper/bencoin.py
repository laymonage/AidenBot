"""
BenCoin Manager.

Programming Assignment 3 (modified)
Foundations of Programming
Fasilkom UI 2017
"""

import os
from .dropson import dbx_dl, dbx_ul, to_json, get_json

ACCOUNTS_PATH = os.getenv('BENCOIN_ACCOUNTS_PATH', None)
ACCLINKS_PATH = os.getenv('ACCOUNT_LINKS_PATH', None)
EXCHRATE_PATH = os.getenv('EXCHANGE_RATE_PATH', None)


class AkunBenCoin:
    """Tipe objek berupa akun BenCoin."""

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
                "Jenis akun yang tersedia: Pelajar, Reguler, Bisnis, Elite\n"
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
    valas = get_json(dbx_dl(EXCHRATE_PATH))

    def __init__(self, Nama, Jenis, saldo=0, riwayat=''):
        """Membuat objek AkunBenCoin."""
        self.nama = Nama
        self.jenis = Jenis
        self.saldo = saldo
        self.lim_tbg = AkunBenCoin.spek[Jenis]['lim_tbg']
        self.lim_trx = AkunBenCoin.spek[Jenis]['lim_trx']
        self.fee_trx = AkunBenCoin.spek[Jenis]['fee_trx']
        self.riwayat = riwayat

    def __str__(self):
        """
        Mengembalikan info akun dengan format berikut.

        Nama: <nama>
        Jenis akun: <jenis>
        Jumlah BenCoin: <saldo>
        Transaksi:
        <riwayat transaksi>
        """
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
        """Mengembalikan representasi string dari AkunBenCoin."""
        return str(self)

    def setor(self, nominal, mata_uang):
        """
        Menambahkan saldo akun sebesar (nominal/kurs).

        Apabila saldo > batas tabungan, maka hanya
        tambahkan hingga saldo mencapai batas tabungan.

        nominal (int), mata_uang (str)
        """
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
            return "Saldo akun Anda sudah mencapai limit tabungan."

        # Nominal yang berhasil disetor:
        # kas_setor = ben_setor * AkunBenCoin.valas[mata_uang]
        self.saldo += ben_setor
        self.riwayat += ("\nSETOR {} {} -> {} BenCoin"
                         .format(mata_uang, nominal, ben_setor))

        return ("Akun Anda telah bertambah {} BenCoin."
                .format(ben_setor))

    def tarik(self, nominal, mata_uang):
        """
        Mengurangi saldo akun dengan jumlah * kurs.

        Apabila sisa saldo < 0, maka hanya tarik
        sehingga saldo bernilai 0 setelah dikurangi
        dengan biaya transaksi.

        nominal (int), mata_uang (str)
        """
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
            return "Saldo Anda tidak mencukupi untuk melakukan penarikan."

        kas_tarik = ben_tarik * AkunBenCoin.valas[mata_uang]
        self.riwayat += ("\nTARIK {} {} -> {:.2f} BenCoin"
                         .format(mata_uang, kas_tarik, ben_tarik))
        ben_tarik += self.fee_trx
        self.saldo -= ben_tarik

        return ("Penarikan {} {} dari akun Anda berhasil."
                .format(mata_uang, kas_tarik))

    def transfer(self, akun_penerima, nominal):
        """
        Memindahkan saldo sebesar nominal dari saldo self ke saldo penerima.

        Apabila sisa saldo self < 0, maka hanya pindahkan
        sehingga saldo bernilai 0 setelah dikurangi
        dengan biaya transaksi.
        Apabila saldo penerima melebihi limit_tabungan,
        maka hanya pindahkan sehingga saldo penerima
        mencapai limit tabungan.

        akun_penerima (AkunBenCoin), nominal (int)
        """
        if nominal <= 0:
            return "Nilai transfer harus > 0."

        if self.saldo == 0:
            return "Saldo akun Anda tidak mencukupi untuk melakukan transfer."

        if akun_penerima == self:
            return "Anda tidak dapat melakukan transfer ke akun Anda sendiri."

        ben_transf = nominal
        if ben_transf > self.lim_trx:
            ben_transf = self.lim_trx

        if self.saldo - ben_transf <= self.fee_trx:
            ben_transf = self.saldo - self.fee_trx

        if ben_transf <= 0:
            return "Saldo akun Anda tidak mencukupi untuk melakukan transfer."

        if ben_transf + akun_penerima.saldo > akun_penerima.lim_tbg:
            ben_transf = akun_penerima.lim_tbg - akun_penerima.saldo

        if ben_transf == 0:
            return ("Akun {} sudah mencapai limit tabungan."
                    .format(akun_penerima.nama))

        akun_penerima.saldo += ben_transf
        self.riwayat += ("\nTRANSFER {} -> {} BenCoin"
                         .format(akun_penerima.nama, ben_transf))
        self.saldo -= ben_transf + self.fee_trx

        return ("Anda berhasil mentransfer {} BenCoin kepada {}."
                .format(ben_transf, akun_penerima.nama))

    def to_json(self):
        """Mengubah instance AkunBenCoin ke dalam bentuk JSON dictionary."""
        return {'Nama': self.nama, 'Jenis': self.jenis,
                'Saldo': self.saldo, 'Riwayat': self.riwayat}


def daftar(user_id, nama, jenis):
    """
    Mendaftarkan akun baru di BenCoin.

    user_id (str): identitas unik untuk setiap akun (gunakan LINE userID)
    nama (str): nama untuk akun yang akan didaftarkan
    jenis (str): jenis akun yang didaftarkan
    """
    nama = nama.title()
    jenis = jenis.title()
    if user_id in TAUTAN:
        if jenis == AKUN[TAUTAN[user_id]].jenis:
            if nama in TAUTAN.values():
                return ("Akun atas nama {} sudah ada dalam sistem."
                        "Mohon gunakan nama lain untuk akun Anda."
                        .format(nama))
            AKUN[nama] = AKUN.pop(TAUTAN[user_id])
            AKUN[nama].nama = nama
            TAUTAN[user_id] = nama
            return ("Nama akun BenCoin Anda telah diubah menjadi {}."
                    .format(nama))
    if jenis in AkunBenCoin.spek:
        if user_id in TAUTAN:
            msg = ("Akun BenCoin Anda telah didaftarkan ulang atas nama {} "
                   "dengan paket {}.".format(nama, jenis))
            del AKUN[TAUTAN[user_id]]
        else:
            msg = ("Akun BenCoin Anda telah terdaftar atas nama {} "
                   "dengan paket {}.".format(nama, jenis))
        AKUN[nama] = AkunBenCoin(nama, jenis)
        TAUTAN[user_id] = nama
        return msg
    return "Jenis tabungan salah."


def perbarui_kurs(mata_uang, kurs, mode):
    """
    Memperbarui daftar kurs valuta asing.

    mata_uang (str): mata uang yang akan dioperasikan
    kurs (int): nilai baru untuk mata uang tersebut
    mode (str): 'ubah': memperbarui mata uang yang sudah ada
                'tambah': menambah mata uang baru
    """
    if kurs <= 0:
        return "Rate mata uang harus > 0."

    if mata_uang not in AkunBenCoin.valas and mode == 'ubah':
        return "Mata uang {} belum terdaftar.".format(mata_uang)
    AkunBenCoin.valas[mata_uang] = kurs
    if mode == 'ubah':
        msg = ("Rate mata uang {} berubah menjadi {} per BenCoin."
               .format(mata_uang, kurs))
    else:
        msg = ("Mata uang {} telah ditambahkan dengan rate {} per BenCoin."
               .format(mata_uang, kurs))
    # Mengunggah data kurs ke Dropbox
    dbx_ul(to_json(AkunBenCoin.valas), EXCHRATE_PATH, overwrite=True)
    return msg


def penangan_operasi(user_id, masukan):
    """Mengandal semua operasi dan menangani apabila terjadi kesalahan."""
    def pelaku_operasi():
        """Melakukan operasi berdasarkan masukan yang diberikan."""
        perintah = masukan.split()
        operasi = perintah[0].upper()

        if operasi == 'DAFTAR':
            nasabah, jenis = perintah[1].title(), perintah[2].title()
            msg = daftar(user_id, nasabah, jenis)

        elif operasi == 'TAMBAH':
            mata_uang, nilai_tukar = perintah[1].upper(), int(perintah[2])
            msg = perbarui_kurs(mata_uang, nilai_tukar, 'tambah')

        elif operasi == 'UBAH':
            mata_uang, nilai_tukar = perintah[1].upper(), int(perintah[2])
            msg = perbarui_kurs(mata_uang, int(nilai_tukar), 'ubah')

        elif operasi == 'SETOR':
            jumlah, mata_uang = int(perintah[1]), perintah[2].upper()
            msg = AKUN[TAUTAN[user_id]].setor(jumlah, mata_uang)

        elif operasi == 'INFO':
            msg = str(AKUN[TAUTAN[user_id]])

        elif operasi == 'TRANSFER':
            penerima = perintah[1].title()
            jumlah = int(perintah[2])
            msg = AKUN[TAUTAN[user_id]].transfer(AKUN[penerima], jumlah)

        elif operasi == 'TARIK':
            jumlah, mata_uang = int(perintah[1]), perintah[2].upper()
            msg = AKUN[TAUTAN[user_id]].tarik(jumlah, mata_uang)

        elif operasi == 'BANTUAN':
            msg = AkunBenCoin.help_msg

        else:
            msg = "Perintah tidak tersedia."

        return msg

    try:
        msg = pelaku_operasi()
    except IndexError:
        return "Format perintah yang Anda masukkan salah."
    except KeyError as error:
        if error.args[0] == user_id:
            return "Anda belum mendaftarkan akun dalam sistem BenCoin."
        return ("Akun atas nama {} belum terdaftar dalam sistem BenCoin."
                .format(error.args[0]))
    except ValueError:
        return "Format nilai yang Anda masukkan salah."
    else:
        # Mengunggah data ke Dropbox apabila operasi sukses.
        dbx_ul(to_json({nasabah: AKUN[nasabah].to_json() for nasabah in AKUN}),
               ACCOUNTS_PATH, overwrite=True)
        dbx_ul(to_json(TAUTAN), ACCLINKS_PATH, overwrite=True)
        return msg


# Memuat JSON dari Dropbox.
AKUN = get_json(dbx_dl(ACCOUNTS_PATH))
TAUTAN = get_json(dbx_dl(ACCLINKS_PATH))


# Mengkonversi data JSON ke dalam bentuk objek AkunBenCoin.
for tiap_nama in AKUN:
    AKUN[tiap_nama] = AkunBenCoin(Nama=AKUN[tiap_nama]['Nama'],
                                  Jenis=AKUN[tiap_nama]['Jenis'],
                                  saldo=AKUN[tiap_nama]['Saldo'],
                                  riwayat=AKUN[tiap_nama]['Riwayat'])
