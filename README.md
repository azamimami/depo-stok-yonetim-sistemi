# Depo ve Stok Yönetim Sistemi
Python ile geliştirilmiş terminal tabanlı bir depo ve stok yönetim sistemidir. Sistem,
ürün stoklarının yönetilmesini ve sipariş süreçlerinin nesne yönelimli programlama (OOP) yapısı ile kontrol edilmesini sağlar.


# Sınıflar ve Yapı

# Ürün (Model)

Ürün bilgilerini ve stok durumunu temsil eder.

* urun_id
* ad
* stok
* fiyat

# Metodlar

* stok_arttir() → Ürün stok miktarını artırır
* stok_azalt() → Ürün stok miktarını azaltır (yetersiz stok kontrolü yapılabilir)

# Sipariş (Model)

Ürünler üzerinden oluşturulan sipariş işlemlerini yönetir.

* siparis_id
* urun
* adet

# Metodlar

* siparis_olustur() → Ürün stok kontrolü yaparak sipariş oluşturur ve stoktan düşer



