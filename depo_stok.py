# ===================== DEPO & STOK SİSTEMİ =====================

# ================= GLOBAL ID =================
urun_id_counter = 1
siparis_id_counter = 1


# ================= ÜRÜN =================
class Urun:
    def __init__(self, ad, stok, fiyat):
        global urun_id_counter

        self.urun_id = urun_id_counter
        urun_id_counter += 1

        self.ad = ad
        self.stok = stok
        self.fiyat = fiyat

    def stok_arttir(self, miktar):
        self.stok += miktar

    def stok_azalt(self, miktar):
        if miktar > self.stok:
            return False
        self.stok -= miktar
        return True

    def __str__(self):
        return f"[{self.urun_id}] {self.ad} | Stok: {self.stok} | Fiyat: {self.fiyat}"


# ================= SİPARİŞ =================
class Siparis:
    def __init__(self, urun, adet):
        global siparis_id_counter

        self.siparis_id = siparis_id_counter
        siparis_id_counter += 1

        self.urun = urun
        self.adet = adet

    def siparis_olustur(self):
        if self.urun.stok_azalt(self.adet):
            return f"Sipariş oluşturuldu -> {self.urun.ad} x {self.adet}"
        else:
            return "Yetersiz stok"


    def __str__(self):
        return f"[{self.siparis_id}] {self.urun.ad} | Adet: {self.adet}"


# ================= SİSTEM =================
class Sistem:
    def __init__(self):
        self.urunler = []
        self.siparisler = []

    def urun_ekle(self, urun):
        self.urunler.append(urun)

    def urun_bul(self, uid):
        return next((u for u in self.urunler if u.urun_id == uid), None)

    def siparis_ekle(self, siparis):
        self.siparisler.append(siparis)


# ================= MENU =================
def menu():
    sistem = Sistem()

    while True:
        print("\n===== DEPO VE STOK SİSTEMİ =====")
        print("1- Ürün Ekle")
        print("2- Ürün Listele")
        print("3- Stok Arttır")
        print("4- Stok Azalt")
        print("5- Sipariş Oluştur")
        print("6- Siparişleri Gör")
        print("0- Çıkış")

        secim = input("Seçim: ")

        # ÜRÜN EKLE
        if secim == "1":
            ad = input("Ürün adı: ")
            stok = int(input("Stok: "))
            fiyat = float(input("Fiyat: "))
            sistem.urun_ekle(Urun(ad, stok, fiyat))
            print("Ürün eklendi")

        # ÜRÜN LİSTELE
        elif secim == "2":
            for u in sistem.urunler:
                print(u)

        # STOK ARTTIR
        elif secim == "3":
            for u in sistem.urunler:
                print(u)

            uid = int(input("Ürün ID: "))
            u = sistem.urun_bul(uid)

            if u:
                miktar = int(input("Miktar: "))
                u.stok_arttir(miktar)
                print("Stok arttırıldı")

        # STOK AZALT
        elif secim == "4":
            for u in sistem.urunler:
                print(u)

            uid = int(input("Ürün ID: "))
            u = sistem.urun_bul(uid)

            if u:
                miktar = int(input("Miktar: "))
                if u.stok_azalt(miktar):
                    print("Stok azaltıldı")
                else:
                    print("Yetersiz stok")

        # SİPARİŞ OLUŞTUR
        elif secim == "5":
            for u in sistem.urunler:
                print(u)

            uid = int(input("Ürün ID: "))
            u = sistem.urun_bul(uid)

            if u:
                adet = int(input("Adet: "))
                siparis = Siparis(u, adet)

                sonuc = siparis.siparis_olustur()

                if "oluşturuldu" in sonuc:
                    sistem.siparis_ekle(siparis)

                print(sonuc)

        # SİPARİŞ LİSTELE
        elif secim == "6":
            for s in sistem.siparisler:
                print(s)

        # ÇIKIŞ
        elif secim == "0":
            break

        else:
            print("Hatalı seçim")


menu()