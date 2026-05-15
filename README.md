# 🏪 DEPO & STOK YÖNETİM SİSTEMİ

Profesyonel ve kullanıcı dostu bir Depo ve Stok Yönetim Sistemi. PyQt5 ve Matplotlib kullanılarak geliştirilmiş, SQLite veritabanı desteğine sahip, kapsamlı raporlama ve stok takibi özellikleriyle donatılmıştır.

**🔐 Giriş Bilgileri:**
- Admin: `admin` / `admin123`
- Personel: `depo` / `depo123`

<img width="450" height="473" alt="Screenshot 2026-05-15 at 19 04 22" src="https://github.com/user-attachments/assets/6d3558e6-6ac3-4556-8d35-89abd2e7a12e" />



# 📋 Özellikler

# 📊 Dashboard & Anlık Takip
- **📦 Toplam Ürün Sayısı** - Sistemde kayıtlı ürün sayısı
- **📊 Toplam Stok Adedi** - Tüm ürünlerin stok toplamı
- **💰 Toplam Stok Değeri** - Stoktaki tüm ürünlerin toplam değeri (TL)
- **🛒 Aktif Sipariş Sayısı** - Bekleyen ve hazırlanan siparişler
- Gerçek zamanlı güncelleme (3 saniyede bir)

<img width="1440" height="900" alt="main" src="https://github.com/user-attachments/assets/7cd1beeb-202f-447c-8a58-02b9b05ad526" />



# 📦 Ürün Yönetimi
- ➕ **Ürün Ekle** - Ürün kodu, ad, kategori, stok, fiyat ve detaylı bilgilerle yeni ürün kaydı
- 📈 **Stok Arttır** - Seçili ürüne stok ekleme ve hareket kaydı
- 📉 **Stok Azalt** - Seçili üründen stok düşme ve hareket kaydı
- 🗑️ **Ürün Sil** - Seçili ürünü sistemden kaldırma
- 🔍 **Kategori Filtreleme** - Kategori bazlı ürün listeleme
- ⚠️ **Düşük Stok Uyarısı** - Minimum stok seviyesinin altındaki ürünleri vurgulama
- 🔄 **Anlık Arama** - Ürün adı, kodu veya kategoriye göre anlık arama



# 🛒 Sipariş Yönetimi
- ➕ **Sipariş Oluştur** - Ürün seçimi ve adet ile sipariş oluşturma
- ✅ **Sipariş Onayla** - Sipariş onaylandığında stoktan otomatik düşüş
- 🚚 **Teslim Et** - Siparişin teslim edildiğini işaretleme
- ❌ **Sipariş İptal** - İptal durumunda stok iadesi
- 💰 **Otomatik Fiyat Hesaplama** - Adet ve birim fiyata göre toplam tutar
- 📋 **Durum Bazlı Filtreleme** - Beklemede, hazırlanıyor, teslim edildi, iptal edildi
- 👤 **Müşteri Bilgileri** - Müşteri adı ve telefon kaydı

<img width="1440" height="900" alt="Siparis" src="https://github.com/user-attachments/assets/a499d719-ce82-4920-bd45-17a62cd57b5d" />



# 📊 Stok Hareketleri
- 📝 **Hareket Geçmişi** - Tüm stok giriş/çıkış işlemlerinin kaydı
- 🔄 **Önceki/Sonraki Stok** - Her işlemde stok değişimi takibi
- 📅 **Tarih Bazlı Sıralama** - En son işlemler önce gelecek şekilde listeleme
- 📈 **İşlem Tipi Renklendirme** - Giriş (yeşil) / Çıkış (kırmızı) vurgusu

<img width="1440" height="900" alt="stok hareketleri" src="https://github.com/user-attachments/assets/c43d1a8f-b881-4767-9d92-43e624913f1e" />



# 📊 Grafikler & İstatistikler
- 🥧 **Kategori Dağılımı** - Kategorilere göre ürün sayıları bar grafiği
- 🥧 **Stok Durumu** - Normal stok vs düşük stok oranı pasta grafiği
- 📊 **Sistem İstatistikleri** - Ürün, stok, sipariş ve düşük stok karşılaştırması
- 🎨 **Profesyonel Görünüm** - Koyu tema ile modern grafik tasarımı

<img width="1440" height="900" alt="Rapor" src="https://github.com/user-attachments/assets/d3abfa83-c9de-42b4-9e6b-72cc03c97c81" />



# 📄 Raporlama Sistemi
- ⚠️ **Düşük Stok Raporu** - Minimum stok seviyesinin altındaki ürünler
- 🏆 **En Çok Satan Ürünler** - Toplam satış adedine göre sıralama
- 📅 **Aylık Satış Özeti** - Aylık sipariş, ürün ve ciro analizi
- 📋 **Kapsamlı Sistem Raporu** - Tüm sistem istatistiklerini içeren detaylı rapor

# 👤 Kullanıcı Yönetimi (Admin)
- 🔐 **Kullanıcı Ekle/Sil** - Personel ve admin rollü kullanıcı yönetimi
- 👥 **Rol Bazlı Yetkilendirme** - Admin ve personel farklı yetkiler
- 🚪 **Oturum Yönetimi** - Güvenli giriş/çıkış işlemleri

<img width="1440" height="900" alt="kullanici" src="https://github.com/user-attachments/assets/d363e7d9-766e-4e57-b3fc-f9825a9a32f0" />



# 🎨 Tema Desteği
- 🌙 **Koyu Tema** - Varsayılan koyu arka plan tema
- ☀️ **Açık Tema** - Beyaz arka plan alternatifi (kod içinde hazır)



# 🖥️ Teknolojiler

| Teknoloji | Kullanım Alanı |
|-----------|----------------|
| Python 3.9+ | Ana programlama dili |
| PyQt5 | GUI Framework (Modern arayüz) |
| SQLite3 | Veritabanı yönetimi |
| Matplotlib | Grafik ve görselleştirme |


