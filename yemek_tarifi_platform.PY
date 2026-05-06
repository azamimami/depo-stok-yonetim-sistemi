# ===================== YEMEK TARİF PLATFORMU =====================
from datetime import datetime

# ================= SAFE INPUT =================
def safe_int_input(text):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Hatalı giriş. Sadece sayı giriniz.")

# ================= GLOBAL IDS =================
tarif_id_counter = 1
kullanici_id_counter = 1


# ================= MALZEME =================
class Malzeme:
    def __init__(self, malzeme_adi, miktar):
        self.malzeme_adi = malzeme_adi
        self.miktar = miktar

    def __str__(self):
        return f"{self.malzeme_adi} - {self.miktar}"


# ================= TARİF =================
class Tarif:
    def __init__(self, tarif_adi, kategori, dakika, saat):
        global tarif_id_counter

        self.tarif_id = tarif_id_counter
        tarif_id_counter += 1

        self.tarif_adi = tarif_adi
        self.kategori = kategori

        self.hazirlama_suresi = (saat * 60) + dakika

        self.malzemeler = []
        self.degerlendirmeler = []

    def malzeme_ekle(self, malzeme):
        self.malzemeler.append(malzeme)

    def malzeme_guncelle(self, index, yeni_ad, yeni_miktar):
        if 0 <= index < len(self.malzemeler):
            self.malzemeler[index].malzeme_adi = yeni_ad
            self.malzemeler[index].miktar = yeni_miktar
            return True
        return False

    def tarif_guncelle(self, ad=None, kategori=None, dakika=None, saat=None):
        if ad:
            self.tarif_adi = ad
        if kategori:
            self.kategori = kategori
        if dakika is not None and saat is not None:
            self.hazirlama_suresi = (saat * 60) + dakika

    def ortalama_puan(self):
        if not self.degerlendirmeler:
            return 0
        return sum(p for _, p in self.degerlendirmeler) / len(self.degerlendirmeler)

    def __str__(self):
        malzeme_listesi = "\n   ".join(str(m) for m in self.malzemeler)
        return (
            f"[{self.tarif_id}] {self.tarif_adi} | {self.kategori} | {self.hazirlama_suresi} dk | Puan: {self.ortalama_puan():.1f}"
            f"\n   Malzemeler:\n   {malzeme_listesi if malzeme_listesi else 'Yok'}"
        )


# ================= KULLANICI =================
class Kullanici:
    def __init__(self, ad, soyad):
        global kullanici_id_counter

        self.kullanici_id = kullanici_id_counter
        kullanici_id_counter += 1

        self.ad = ad
        self.soyad = soyad

    def __str__(self):
        return f"[{self.kullanici_id}] {self.ad} {self.soyad}"


# ================= SİSTEM =================
class Sistem:
    def __init__(self):
        self.tarifler = []
        self.kullanicilar = []

    def tarif_ekle(self, t):
        self.tarifler.append(t)

    def kullanici_ekle(self, k):
        self.kullanicilar.append(k)

    def tarif_bul(self, tid):
        return next((t for t in self.tarifler if t.tarif_id == tid), None)

    def kullanici_bul(self, kid):
        return next((k for k in self.kullanicilar if k.kullanici_id == kid), None)

    def tarif_sil(self, tid):
        t = self.tarif_bul(tid)
        if t:
            self.tarifler.remove(t)
            return True
        return False

    def kullanici_sil(self, kid):
        k = self.kullanici_bul(kid)
        if k:
            self.kullanicilar.remove(k)
            return True
        return False


# ================= MENU =================

def menu():
    sistem = Sistem()

    while True:
        print("\n===== YEMEK TARİF SİSTEMİ =====")
        print("1- Tarif Ekle")
        print("2- Malzeme Ekle")
        print("3- Tarif Listele")
        print("4- Tarif Güncelle")
        print("5- Kullanıcı Ekle")
        print("6- Kullanıcı Sil")
        print("7- Kullanıcı Listele")
        print("8- Tarif Sil")
        print("9- Malzeme Güncelle")
        print("10- Değerlendir (Puan)")
        print("11- Değerlendirmeleri Gör")
        print("12- Çıkış")

        secim = input("Seçim: ")

        # TARİF EKLE
        if secim == "1":
            ad = input("Tarif adı: ")
            kategori = input("Kategori: ")
            dakika = safe_int_input("Dakika: ")
            saat = safe_int_input("Saat: ")
            sistem.tarif_ekle(Tarif(ad, kategori, dakika, saat))
            print("Eklendi")

        # MALZEME EKLE
        elif secim == "2":
            if not sistem.tarifler:
                print("Liste boş")
                continue

            for t in sistem.tarifler:
                print(t)

            tid = safe_int_input("Tarif ID: ")
            t = sistem.tarif_bul(tid)

            if t:
                ad = input("Malzeme adı: ")
                miktar = input("Miktar: ")
                t.malzeme_ekle(Malzeme(ad, miktar))
            else:
                print("Geçersiz ID")

        # TARİF LİSTE
        elif secim == "3":
            if not sistem.tarifler:
                print("Liste boş")
            else:
                for t in sistem.tarifler:
                    print(t)

        # TARİF GÜNCELLE
        elif secim == "4":
            if not sistem.tarifler:
                print("Liste boş")
                continue

            for t in sistem.tarifler:
                print(t)

            tid = safe_int_input("Tarif ID: ")
            t = sistem.tarif_bul(tid)

            if t:
                ad = input("Yeni ad: ")
                kat = input("Yeni kategori: ")
                dk = input("Dakika: ")
                st = input("Saat: ")

                dakika = int(dk) if dk.isdigit() else None
                saat = int(st) if st.isdigit() else None

                t.tarif_guncelle(ad, kat, dakika, saat)
            else:
                print("Geçersiz ID")

        # KULLANICI EKLE
        elif secim == "5":
            ad = input("Ad: ")
            soyad = input("Soyad: ")
            sistem.kullanici_ekle(Kullanici(ad, soyad))

        # KULLANICI SİL
        elif secim == "6":
            if not sistem.kullanicilar:
                print("Liste boş")
            else:
                for k in sistem.kullanicilar:
                    print(k)
                kid = safe_int_input("Kullanıcı ID: ")
                print("Silindi" if sistem.kullanici_sil(kid) else "Bulunamadı")

        # KULLANICI LİSTE
        elif secim == "7":
            if not sistem.kullanicilar:
                print("Liste boş")
            else:
                for k in sistem.kullanicilar:
                    print(k)

        # TARİF SİL
        elif secim == "8":
            if not sistem.tarifler:
                print("Liste boş")
            else:
                for t in sistem.tarifler:
                    print(t)
                tid = safe_int_input("Tarif ID: ")
                print("Silindi" if sistem.tarif_sil(tid) else "Bulunamadı")

        # MALZEME GÜNCELLE
        elif secim == "9":
            if not sistem.tarifler:
                print("Liste boş")
                continue

            for t in sistem.tarifler:
                print(t)

            tid = safe_int_input("Tarif ID: ")
            t = sistem.tarif_bul(tid)

            if t:
                if not t.malzemeler:
                    print("Malzeme yok")
                    continue

                for i, m in enumerate(t.malzemeler):
                    print(i, m)

                mid = safe_int_input("Malzeme index: ")

                ad = input("Yeni ad: ")
                miktar = input("Yeni miktar: ")

                if t.malzeme_guncelle(mid, ad, miktar):
                    print("Güncellendi")
                else:
                    print("Geçersiz seçim")

        # DEĞERLENDİR
        elif secim == "10":
            if not sistem.tarifler:
                print("Liste boş")
                continue

            for t in sistem.tarifler:
                print(t)

            tid = safe_int_input("Tarif ID: ")
            t = sistem.tarif_bul(tid)

            if t:
                if not sistem.kullanicilar:
                    print("Kullanıcı yok")
                    continue

                for k in sistem.kullanicilar:
                    print(k)

                kid = safe_int_input("Kullanıcı ID: ")
                k = sistem.kullanici_bul(kid)

                if k:
                    puan = safe_int_input("Puan: ")
                    t.degerlendirmeler.append((k.ad, puan))

        # GÖR
        elif secim == "11":
            if not sistem.tarifler:
                print("Liste boş")
            else:
                for t in sistem.tarifler:
                    print(f"\n{t.tarif_adi}")
                    for k, p in t.degerlendirmeler:
                        print(k, p)

        # EXIT
        elif secim == "0":
            break

        else:
            print("Hatalı")


menu()