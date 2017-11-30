'''
BenCoin Manager
Programming Assignment 3
Foundations of Programming
Fasilkom UI 2017
'''


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
