# ===================== FITNESS TAKİP SİSTEMİ =====================
from datetime import datetime

# ================= SAFE INPUT =================
def safe_int_input(text):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Hatalı giriş. Sadece sayı giriniz.")


# ================= GLOBAL ID COUNTERS =================
sporcu_id_counter = 1
antrenman_id_counter = 1


# ================= SPORCU =================
class Sporcu:
    def __init__(self, ad, kilo, boy):
        global sporcu_id_counter

        self.sporcu_id = sporcu_id_counter
        sporcu_id_counter += 1

        self.ad = ad
        self.kilo = kilo
        self.boy = boy
        self.ilerleme = []

    def ilerleme_kaydet(self, kilo=None):
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M")

        if kilo is not None:
            self.kilo = kilo

        self.ilerleme.append((tarih, self.kilo))

    def __str__(self):
        return f"[{self.sporcu_id}] {self.ad} | Kilo: {self.kilo} | Boy: {self.boy}"


# ================= ANTRENMAN =================
class Antrenman:
    def __init__(self, tur, saat, dakika):
        global antrenman_id_counter

        self.antrenman_id = antrenman_id_counter
        antrenman_id_counter += 1

        self.tur = tur
        self.saat = saat
        self.dakika = dakika

        self.sure = (saat * 60) + dakika  # toplam dakika

    def __str__(self):
        return f"[{self.antrenman_id}] {self.tur} | {self.saat} saat {self.dakika} dk"


# ================= TAKİP =================
class Takip:
    def __init__(self, sporcu, antrenman, kalori):
        self.sporcu = sporcu
        self.antrenman = antrenman
        self.kalori = kalori
        self.tarih = datetime.now().strftime("%Y-%m-%d %H:%M")

    def __str__(self):
        return f"{self.tarih} | {self.sporcu.ad} | {self.antrenman.tur} | {self.kalori} kcal"


# ================= SİSTEM =================
class Sistem:
    def __init__(self):
        self.sporcular = []
        self.antrenmanlar = []
        self.takipler = []

    # SPORCU
    def sporcu_ekle(self, s):
        self.sporcular.append(s)

    def sporcu_bul(self, sid):
        return next((s for s in self.sporcular if s.sporcu_id == sid), None)

    def sporcu_sil(self, sid):
        s = self.sporcu_bul(sid)
        if s:
            self.sporcular.remove(s)
            return True
        return False

    # ANTRENMAN
    def antrenman_ekle(self, a):
        self.antrenmanlar.append(a)

    def antrenman_bul(self, aid):
        return next((a for a in self.antrenmanlar if a.antrenman_id == aid), None)

    # TAKİP
    def takip_ekle(self, t):
        self.takipler.append(t)


# ================= MENU =================
def menu():
    sistem = Sistem()

    while True:
        print("\n===== FITNESS TAKİP SİSTEMİ =====")
        print("1- Sporcu Ekle")
        print("2- Sporcu Listele")
        print("3- Sporcu Sil")
        print("4- Antrenman Ekle")
        print("5- Antrenman Listele")
        print("6- Takip Oluştur")
        print("7- İlerleme Kaydet")
        print("8- Takipleri Gör")
        print("0- Çıkış")

        secim = input("Seçim: ")

        # SPORCU EKLE
        if secim == "1":
            ad = input("Ad: ")
            kilo = safe_int_input("Kilo: ")
            boy = safe_int_input("Boy: ")
            sistem.sporcu_ekle(Sporcu(ad, kilo, boy))
            print("Sporcu eklendi")

        # SPORCU LİSTE
        elif secim == "2":
            if not sistem.sporcular:
                print("Liste boş")
            for s in sistem.sporcular:
                print(s)

        # SPORCU SİL
        elif secim == "3":
            for s in sistem.sporcular:
                print(s)
            sid = safe_int_input("Sporcu ID: ")
            print("Silindi" if sistem.sporcu_sil(sid) else "Bulunamadı")

        # ANTRENMAN EKLE (SAAT + DAKİKA)
        elif secim == "4":
            tur = input("Antrenman türü: ")
            saat = safe_int_input("Saat: ")
            dakika = safe_int_input("Dakika: ")

            sistem.antrenman_ekle(Antrenman(tur, saat, dakika))
            print("Antrenman eklendi")

        # ANTRENMAN LİSTE
        elif secim == "5":
            if not sistem.antrenmanlar:
                print("Liste boş")
            for a in sistem.antrenmanlar:
                print(a)

        # TAKİP OLUŞTUR
        elif secim == "6":
            if not sistem.sporcular or not sistem.antrenmanlar:
                print("Eksik veri")
                continue

            for s in sistem.sporcular:
                print(s)
            sid = safe_int_input("Sporcu ID: ")
            s = sistem.sporcu_bul(sid)

            for a in sistem.antrenmanlar:
                print(a)
            aid = safe_int_input("Antrenman ID: ")
            a = sistem.antrenman_bul(aid)

            if s and a:
                kalori = safe_int_input("Kalori: ")
                sistem.takip_ekle(Takip(s, a, kalori))
                print("Takip eklendi")
            else:
                print("Geçersiz seçim")

        # İLERLEME
        elif secim == "7":
            for s in sistem.sporcular:
                print(s)

            sid = safe_int_input("Sporcu ID: ")
            s = sistem.sporcu_bul(sid)

            if s:
                kilo = safe_int_input("Yeni kilo: ")
                s.ilerleme_kaydet(kilo)
                print("İlerleme kaydedildi")

        # TAKİP LİSTE
        elif secim == "8":
            if not sistem.takipler:
                print("Liste boş")
            for t in sistem.takipler:
                print(t)

        # EXIT
        elif secim == "0":
            break

        else:
            print("Hatalı seçim")


menu()