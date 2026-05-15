import sys
from datetime import datetime, timedelta
import sqlite3
from contextlib import contextmanager
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLabel,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox,
    QTabWidget, QFrame, QTextEdit, QHeaderView, QProgressBar, QGroupBox,
    QRadioButton, QCheckBox, QSlider, QDateEdit, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer, QDate, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIcon, QPalette
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False


# ============ MODERN STYLE SHEET (Koyu Arka Plan) ============

DARK_STYLE = """
    QMainWindow {
        background-color: #0d1b2a;
    }
    QTabWidget::pane {
        border: none;
        background-color: #1b263b;
        border-radius: 12px;
    }
    QTabBar::tab {
        background-color: #1b263b;
        color: #e0e1dd;
        padding: 12px 30px;
        margin-right: 5px;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        font-weight: bold;
        font-size: 13px;
    }
    QTabBar::tab:selected {
        background-color: #0077b6;
        color: white;
    }
    QTabBar::tab:hover:!selected {
        background-color: #2a3a5c;
    }
    QTableWidget {
        background-color: #1b263b;
        alternate-background-color: #2a3a5c;
        color: #e0e1dd;
        gridline-color: #415a77;
        border: none;
        border-radius: 10px;
    }
    QTableWidget::item {
        padding: 10px;
        color: #e0e1dd;
    }
    QTableWidget::item:selected {
        background-color: #0077b6;
        color: white;
    }
    QHeaderView::section {
        background-color: #0d1b2a;
        color: #0077b6;
        font-weight: bold;
        padding: 12px;
        border: none;
    }
    QPushButton {
        background-color: #0077b6;
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: #00b4d8;
    }
    QPushButton:pressed {
        background-color: #03045e;
    }
    QPushButton#danger {
        background-color: #e63946;
    }
    QPushButton#danger:hover {
        background-color: #ff6b6b;
    }
    QPushButton#success {
        background-color: #2ec4b6;
    }
    QPushButton#success:hover {
        background-color: #48cae4;
    }
    QPushButton#warning {
        background-color: #ff9f1c;
    }
    QPushButton#warning:hover {
        background-color: #ffbf69;
    }
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTextEdit {
        background-color: #2a3a5c;
        border: 1px solid #415a77;
        border-radius: 8px;
        padding: 10px;
        color: #e0e1dd;
        font-size: 12px;
    }
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
        border: 1px solid #0077b6;
    }
    QLabel {
        color: #e0e1dd;
    }
    QDialog {
        background-color: #1b263b;
    }
    QGroupBox {
        border: 1px solid #415a77;
        border-radius: 10px;
        margin-top: 12px;
        font-weight: bold;
        color: #0077b6;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 15px;
        padding: 0 8px;
        color: #0077b6;
    }
    QProgressBar {
        border: 1px solid #415a77;
        border-radius: 8px;
        text-align: center;
        color: white;
    }
    QProgressBar::chunk {
        background-color: #0077b6;
        border-radius: 8px;
    }
    QCheckBox {
        color: #e0e1dd;
    }
    QRadioButton {
        color: #e0e1dd;
    }
"""

# ============ AÇIK TEMA (Beyaz Arka Plan için) ============

LIGHT_STYLE = """
    QMainWindow {
        background-color: #f0f2f5;
    }
    QTabWidget::pane {
        border: none;
        background-color: #ffffff;
        border-radius: 12px;
    }
    QTabBar::tab {
        background-color: #e9ecef;
        color: #495057;
        padding: 12px 30px;
        margin-right: 5px;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        font-weight: bold;
        font-size: 13px;
    }
    QTabBar::tab:selected {
        background-color: #0077b6;
        color: white;
    }
    QTabBar::tab:hover:!selected {
        background-color: #dee2e6;
    }
    QTableWidget {
        background-color: #ffffff;
        alternate-background-color: #f8f9fa;
        color: #212529;
        gridline-color: #dee2e6;
        border: none;
        border-radius: 10px;
    }
    QTableWidget::item {
        padding: 10px;
        color: #212529;
    }
    QTableWidget::item:selected {
        background-color: #0077b6;
        color: white;
    }
    QHeaderView::section {
        background-color: #e9ecef;
        color: #0077b6;
        font-weight: bold;
        padding: 12px;
        border: none;
    }
    QPushButton {
        background-color: #0077b6;
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: #00b4d8;
    }
    QPushButton:pressed {
        background-color: #03045e;
    }
    QPushButton#danger {
        background-color: #e63946;
    }
    QPushButton#danger:hover {
        background-color: #ff6b6b;
    }
    QPushButton#success {
        background-color: #2ec4b6;
    }
    QPushButton#success:hover {
        background-color: #48cae4;
    }
    QPushButton#warning {
        background-color: #ff9f1c;
    }
    QPushButton#warning:hover {
        background-color: #ffbf69;
    }
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTextEdit {
        background-color: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 8px;
        padding: 10px;
        color: #212529;
        font-size: 12px;
    }
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
        border: 1px solid #0077b6;
    }
    QLabel {
        color: #212529;
    }
    QDialog {
        background-color: #ffffff;
    }
    QGroupBox {
        border: 1px solid #dee2e6;
        border-radius: 10px;
        margin-top: 12px;
        font-weight: bold;
        color: #0077b6;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 15px;
        padding: 0 8px;
        color: #0077b6;
    }
    QProgressBar {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        text-align: center;
        color: #212529;
    }
    QProgressBar::chunk {
        background-color: #0077b6;
        border-radius: 8px;
    }
    QCheckBox {
        color: #212529;
    }
    QRadioButton {
        color: #212529;
    }
"""


# ============ DATABASE MANAGER ============

class DatabaseManager:
    """Veritabanı işlemlerini yöneten sınıf"""

    def __init__(self, db_name="warehouse.db"):
        self.db_name = db_name
        self.create_tables()

    @contextmanager
    def get_connection(self):
        """Veritabanı bağlantısı sağlayan context manager"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def create_tables(self):
        """Tüm tabloları oluşturur"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Ürünler tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS urunler (
                    urun_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    urun_kodu TEXT UNIQUE NOT NULL,
                    ad TEXT NOT NULL,
                    kategori TEXT NOT NULL,
                    stok INTEGER DEFAULT 0,
                    minimum_stok INTEGER DEFAULT 10,
                    fiyat REAL NOT NULL,
                    alis_fiyati REAL,
                    birim TEXT DEFAULT 'adet',
                    raf_no TEXT,
                    aciklama TEXT,
                    durum TEXT DEFAULT 'Aktif',
                    eklenme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Siparişler tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS siparisler (
                    siparis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    siparis_no TEXT UNIQUE NOT NULL,
                    urun_id INTEGER NOT NULL,
                    urun_adi TEXT NOT NULL,
                    adet INTEGER NOT NULL,
                    birim_fiyat REAL NOT NULL,
                    toplam_tutar REAL NOT NULL,
                    siparis_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    teslim_tarihi TIMESTAMP,
                    durum TEXT DEFAULT 'Beklemede',
                    odeme_durumu TEXT DEFAULT 'Beklemede',
                    musteri_adi TEXT,
                    musteri_tel TEXT,
                    notlar TEXT,
                    FOREIGN KEY (urun_id) REFERENCES urunler (urun_id)
                )
            ''')

            # Stok hareketleri tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stok_hareketleri (
                    hareket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    urun_id INTEGER NOT NULL,
                    urun_adi TEXT NOT NULL,
                    hareket_tipi TEXT NOT NULL,
                    miktar INTEGER NOT NULL,
                    onceki_stok INTEGER,
                    sonraki_stok INTEGER,
                    islem_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    islem_yapan TEXT,
                    aciklama TEXT,
                    FOREIGN KEY (urun_id) REFERENCES urunler (urun_id)
                )
            ''')

            # Tedarikçiler tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tedarikciler (
                    tedarikci_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tedarikci_adi TEXT UNIQUE NOT NULL,
                    yetkili_adi TEXT,
                    telefon TEXT NOT NULL,
                    email TEXT,
                    adres TEXT,
                    durum TEXT DEFAULT 'Aktif'
                )
            ''')

            # Sistem kullanıcıları tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sistem_kullanicilari (
                    kullanici_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kullanici_adi TEXT UNIQUE NOT NULL,
                    sifre TEXT NOT NULL,
                    ad TEXT NOT NULL,
                    soyad TEXT NOT NULL,
                    rol TEXT DEFAULT 'personel',
                    durum TEXT DEFAULT 'Aktif',
                    olusturma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Kategoriler tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kategoriler (
                    kategori_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kategori_adi TEXT UNIQUE NOT NULL
                )
            ''')

            # Varsayılan kategoriler
            default_categories = ['Elektronik', 'Giyim', 'Gıda', 'Kozmetik', 'Ev Eşyası',
                                 'Ofis Malzemesi', 'Hırdavat', 'Spor', 'Oyuncak', 'Diğer']
            for kategori in default_categories:
                cursor.execute('INSERT OR IGNORE INTO kategoriler (kategori_adi) VALUES (?)', (kategori,))

            # Varsayılan ürünler
            cursor.execute('SELECT COUNT(*) FROM urunler')
            if cursor.fetchone()[0] == 0:
                default_products = [
                    ("PRD001", "Laptop", "Elektronik", 15, 5, 15000.00, 12000.00, "adet", "A-01"),
                    ("PRD002", "Mouse", "Elektronik", 50, 10, 250.00, 150.00, "adet", "A-02"),
                    ("PRD003", "Klavye", "Elektronik", 30, 8, 500.00, 350.00, "adet", "A-03"),
                    ("PRD004", "Monitör", "Elektronik", 10, 3, 3000.00, 2500.00, "adet", "A-04"),
                    ("PRD005", "Kulaklık", "Elektronik", 40, 10, 400.00, 250.00, "adet", "A-05"),
                    ("PRD006", "T-Shirt", "Giyim", 100, 20, 80.00, 45.00, "adet", "B-01"),
                    ("PRD007", "Kot Pantolon", "Giyim", 60, 10, 200.00, 120.00, "adet", "B-02"),
                    ("PRD008", "Çikolata", "Gıda", 200, 30, 15.00, 8.00, "adet", "C-01"),
                    ("PRD009", "Su", "Gıda", 500, 50, 5.00, 2.50, "adet", "C-02"),
                    ("PRD010", "Parfüm", "Kozmetik", 80, 10, 350.00, 200.00, "adet", "D-01"),
                ]
                for urun in default_products:
                    cursor.execute('''
                        INSERT INTO urunler (urun_kodu, ad, kategori, stok, minimum_stok, fiyat, alis_fiyati, birim, raf_no)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', urun)

            # Varsayılan kullanıcılar
            cursor.execute('SELECT COUNT(*) FROM sistem_kullanicilari WHERE kullanici_adi = "admin"')
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO sistem_kullanicilari (kullanici_adi, sifre, ad, soyad, rol)
                    VALUES ('admin', 'admin123', 'Admin', 'Kullanıcı', 'admin')
                ''')

            cursor.execute('SELECT COUNT(*) FROM sistem_kullanicilari WHERE kullanici_adi = "depo"')
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO sistem_kullanicilari (kullanici_adi, sifre, ad, soyad, rol)
                    VALUES ('depo', 'depo123', 'Depo', 'Görevlisi', 'personel')
                ''')

    # ============ ÜRÜN İŞLEMLERİ ============

    def urun_ekle(self, urun_kodu, ad, kategori, stok, minimum_stok, fiyat, alis_fiyati=None, birim="adet", raf_no="", aciklama=""):
        """Yeni ürün ekler"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO urunler (urun_kodu, ad, kategori, stok, minimum_stok, fiyat, alis_fiyati, birim, raf_no, aciklama)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (urun_kodu, ad, kategori, stok, minimum_stok, fiyat, alis_fiyati, birim, raf_no, aciklama))

            hareket_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO stok_hareketleri (urun_id, urun_adi, hareket_tipi, miktar, onceki_stok, sonraki_stok, aciklama)
                VALUES (?, ?, 'Giriş', ?, 0, ?, 'Yeni ürün eklendi')
            ''', (hareket_id, ad, stok, stok))

            return hareket_id

    def urunleri_getir(self, kategori=None, dusuk_stok=False):
        """Tüm ürünleri getirir"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM urunler WHERE durum = "Aktif"'
            params = []
            if kategori:
                query += ' AND kategori = ?'
                params.append(kategori)
            if dusuk_stok:
                query += ' AND stok <= minimum_stok'
            query += ' ORDER BY ad'
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def urun_getir(self, urun_id):
        """ID'ye göre ürün getirir"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM urunler WHERE urun_id = ?', (urun_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def stok_arttir(self, urun_id, miktar, aciklama=""):
        """Stok arttırır"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT ad, stok FROM urunler WHERE urun_id = ?', (urun_id,))
            urun = cursor.fetchone()
            if not urun:
                raise ValueError("Ürün bulunamadı!")
            onceki_stok = urun['stok']
            yeni_stok = onceki_stok + miktar
            cursor.execute('UPDATE urunler SET stok = ? WHERE urun_id = ?', (yeni_stok, urun_id))
            cursor.execute('''
                INSERT INTO stok_hareketleri (urun_id, urun_adi, hareket_tipi, miktar, onceki_stok, sonraki_stok, aciklama)
                VALUES (?, ?, 'Giriş', ?, ?, ?, ?)
            ''', (urun_id, urun['ad'], miktar, onceki_stok, yeni_stok, aciklama or "Stok arttırıldı"))
            return yeni_stok

    def stok_azalt(self, urun_id, miktar, aciklama=""):
        """Stok azaltır"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT ad, stok FROM urunler WHERE urun_id = ?', (urun_id,))
            urun = cursor.fetchone()
            if not urun:
                raise ValueError("Ürün bulunamadı!")
            if urun['stok'] < miktar:
                raise ValueError(f"Yetersiz stok! Mevcut stok: {urun['stok']}")
            onceki_stok = urun['stok']
            yeni_stok = onceki_stok - miktar
            cursor.execute('UPDATE urunler SET stok = ? WHERE urun_id = ?', (yeni_stok, urun_id))
            cursor.execute('''
                INSERT INTO stok_hareketleri (urun_id, urun_adi, hareket_tipi, miktar, onceki_stok, sonraki_stok, aciklama)
                VALUES (?, ?, 'Çıkış', ?, ?, ?, ?)
            ''', (urun_id, urun['ad'], miktar, onceki_stok, yeni_stok, aciklama or "Stok azaltıldı"))
            return yeni_stok

    def siparis_olustur(self, urun_id, adet, birim_fiyat, musteri_adi="", musteri_tel="", notlar=""):
        """Yeni sipariş oluşturur"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT ad FROM urunler WHERE urun_id = ?', (urun_id,))
            urun = cursor.fetchone()
            if not urun:
                raise ValueError("Ürün bulunamadı!")
            cursor.execute("SELECT COUNT(*) as count FROM siparisler")
            count = cursor.fetchone()['count'] + 1
            siparis_no = f"ORD{count:06d}"
            toplam_tutar = adet * birim_fiyat
            cursor.execute('''
                INSERT INTO siparisler (siparis_no, urun_id, urun_adi, adet, birim_fiyat, toplam_tutar,
                                        musteri_adi, musteri_tel, notlar)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (siparis_no, urun_id, urun['ad'], adet, birim_fiyat, toplam_tutar,
                  musteri_adi, musteri_tel, notlar))
            return siparis_no

    def siparis_onayla(self, siparis_id):
        """Siparişi onaylar ve stoktan düşer"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT urun_id, adet FROM siparisler WHERE siparis_id = ? AND durum = "Beklemede"', (siparis_id,))
            siparis = cursor.fetchone()
            if not siparis:
                raise ValueError("Sipariş bulunamadı veya zaten işleme alınmış!")
            self.stok_azalt(siparis['urun_id'], siparis['adet'], f"Sipariş #{siparis_id} onaylandı")
            cursor.execute('UPDATE siparisler SET durum = "Hazırlanıyor" WHERE siparis_id = ?', (siparis_id,))

    def siparis_teslim_et(self, siparis_id):
        """Siparişi teslim eder"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE siparisler SET durum = 'Teslim Edildi', teslim_tarihi = ?
                WHERE siparis_id = ?
            ''', (datetime.now(), siparis_id))

    def siparis_iptal(self, siparis_id):
        """Siparişi iptal eder"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT urun_id, adet, durum FROM siparisler WHERE siparis_id = ?', (siparis_id,))
            siparis = cursor.fetchone()
            if not siparis:
                raise ValueError("Sipariş bulunamadı!")
            if siparis['durum'] == "Hazırlanıyor":
                self.stok_arttir(siparis['urun_id'], siparis['adet'], f"Sipariş #{siparis_id} iptal edildi")
            cursor.execute('UPDATE siparisler SET durum = "İptal Edildi" WHERE siparis_id = ?', (siparis_id,))

    def siparisleri_getir(self, durum=None):
        """Siparişleri getirir"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT s.*, u.stok as mevcut_stok FROM siparisler s LEFT JOIN urunler u ON s.urun_id = u.urun_id'
            params = []
            if durum:
                query += ' WHERE s.durum = ?'
                params.append(durum)
            query += ' ORDER BY s.siparis_tarihi DESC'
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def stok_hareketlerini_getir(self, urun_id=None, limit=50):
        """Stok hareketlerini getirir"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if urun_id:
                cursor.execute('SELECT * FROM stok_hareketleri WHERE urun_id = ? ORDER BY islem_tarihi DESC LIMIT ?', (urun_id, limit))
            else:
                cursor.execute('SELECT * FROM stok_hareketleri ORDER BY islem_tarihi DESC LIMIT ?', (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def toplam_urun_sayisi(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM urunler WHERE durum = "Aktif"')
            return cursor.fetchone()['count']

    def toplam_stok_adeti(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT SUM(stok) as total FROM urunler WHERE durum = "Aktif"')
            return cursor.fetchone()['total'] or 0

    def toplam_urun_degeri(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT SUM(stok * fiyat) as total FROM urunler WHERE durum = "Aktif"')
            return cursor.fetchone()['total'] or 0

    def dusuk_stoklu_urunler(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM urunler WHERE durum = "Aktif" AND stok <= minimum_stok ORDER BY (stok * 1.0 / minimum_stok) ASC')
            return [dict(row) for row in cursor.fetchall()]

    def kategori_dagilimi(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT kategori, COUNT(*) as sayi, SUM(stok) as toplam_stok FROM urunler WHERE durum = "Aktif" GROUP BY kategori ORDER BY sayi DESC')
            return [dict(row) for row in cursor.fetchall()]

    def aylik_siparis_ozeti(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT strftime('%Y-%m', siparis_tarihi) as ay, COUNT(*) as siparis_sayisi,
                       SUM(adet) as toplam_urun, SUM(toplam_tutar) as toplam_ciro
                FROM siparisler WHERE durum = 'Teslim Edildi'
                GROUP BY strftime('%Y-%m', siparis_tarihi) ORDER BY ay DESC LIMIT 6
            ''')
            return [dict(row) for row in cursor.fetchall()]

    def en_cok_satan_urunler(self, limit=10):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT urun_id, urun_adi, SUM(adet) as toplam_satis, COUNT(*) as siparis_sayisi
                FROM siparisler WHERE durum = 'Teslim Edildi'
                GROUP BY urun_id ORDER BY toplam_satis DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def kullanici_kontrol(self, kullanici_adi, sifre):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sistem_kullanicilari WHERE kullanici_adi = ? AND sifre = ? AND durum = "Aktif"', (kullanici_adi, sifre))
            result = cursor.fetchone()
            return dict(result) if result else None

    def kullanicilari_getir(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sistem_kullanicilari ORDER BY kullanici_id')
            return [dict(row) for row in cursor.fetchall()]

    def kullanici_ekle(self, kullanici_adi, sifre, ad, soyad, rol='personel'):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO sistem_kullanicilari (kullanici_adi, sifre, ad, soyad, rol) VALUES (?, ?, ?, ?, ?)',
                          (kullanici_adi, sifre, ad, soyad, rol))
            return cursor.lastrowid

    def kullanici_sil(self, kullanici_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM sistem_kullanicilari WHERE kullanici_id = ?', (kullanici_id,))

    def kategorileri_getir(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT kategori_adi FROM kategoriler ORDER BY kategori_adi')
            return [row['kategori_adi'] for row in cursor.fetchall()]


# ============ LOGIN DIALOG ============

class LoginDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Depo ve Stok Yönetim Sistemi - Giriş")
        self.setGeometry(400, 300, 450, 400)
        self.setStyleSheet(DARK_STYLE)
        self.setModal(True)
        self.init_ui()
        self.kullanici = None

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 40, 30, 30)

        baslik = QLabel("🏪 DEPO & STOK YÖNETİM SİSTEMİ")
        baslik_font = QFont("Arial", 18, QFont.Bold)
        baslik.setFont(baslik_font)
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("color: #0077b6; margin-bottom: 10px;")

        alt_baslik = QLabel("Sisteme Giriş Yapın")
        alt_baslik.setFont(QFont("Arial", 12))
        alt_baslik.setAlignment(Qt.AlignCenter)
        alt_baslik.setStyleSheet("color: #e0e1dd; margin-bottom: 30px;")

        kadi_label = QLabel("Kullanıcı Adı")
        kadi_label.setFont(QFont("Arial", 11, QFont.Bold))
        kadi_label.setStyleSheet("color: #0077b6;")
        self.kadi_input = QLineEdit()
        self.kadi_input.setPlaceholderText("Kullanıcı adınızı girin")
        self.kadi_input.setStyleSheet("padding: 12px; font-size: 12px;")

        sifre_label = QLabel("Şifre")
        sifre_label.setFont(QFont("Arial", 11, QFont.Bold))
        sifre_label.setStyleSheet("color: #0077b6;")
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.sifre_input.setPlaceholderText("Şifrenizi girin")
        self.sifre_input.setStyleSheet("padding: 12px; font-size: 12px;")
        self.sifre_input.returnPressed.connect(self.giris_yap)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        giris_btn = QPushButton("🔐 Giriş Yap")
        giris_btn.setStyleSheet("background-color: #0077b6; padding: 12px; border-radius: 10px; font-weight: bold; font-size: 13px;")
        giris_btn.clicked.connect(self.giris_yap)

        iptal_btn = QPushButton("❌ Çıkış")
        iptal_btn.setObjectName("danger")
        iptal_btn.setStyleSheet("background-color: #e63946; padding: 12px; border-radius: 10px; font-weight: bold; font-size: 13px;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(giris_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(baslik)
        layout.addWidget(alt_baslik)
        layout.addWidget(kadi_label)
        layout.addWidget(self.kadi_input)
        layout.addWidget(sifre_label)
        layout.addWidget(self.sifre_input)
        layout.addSpacing(20)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def giris_yap(self):
        kadi = self.kadi_input.text().strip()
        sifre = self.sifre_input.text().strip()
        if not kadi or not sifre:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı ve şifre giriniz!")
            return
        kullanici = self.db.kullanici_kontrol(kadi, sifre)
        if kullanici:
            self.kullanici = kullanici
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre hatalı!")


# ============ URUN EKLE DIALOG ============

class UrunEkleDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Yeni Ürün Ekle")
        self.setGeometry(200, 200, 550, 650)
        self.setStyleSheet(DARK_STYLE)
        self.init_ui()
        self.result = None

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        baslik = QLabel("📦 Yeni Ürün Ekle")
        baslik.setFont(QFont("Arial", 16, QFont.Bold))
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("color: #0077b6; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(12)

        grid.addWidget(QLabel("Ürün Kodu:"), 0, 0)
        self.kod_input = QLineEdit()
        self.kod_input.setPlaceholderText("Otomatik oluşturulacak")
        grid.addWidget(self.kod_input, 0, 1)

        grid.addWidget(QLabel("Ürün Adı:*"), 1, 0)
        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Ürün adını girin")
        grid.addWidget(self.ad_input, 1, 1)

        grid.addWidget(QLabel("Kategori:*"), 2, 0)
        self.kategori_combo = QComboBox()
        self.kategori_combo.addItems(self.db.kategorileri_getir())
        self.kategori_combo.setEditable(True)
        grid.addWidget(self.kategori_combo, 2, 1)

        grid.addWidget(QLabel("Başlangıç Stok:"), 3, 0)
        self.stok_input = QSpinBox()
        self.stok_input.setMaximum(100000)
        self.stok_input.setValue(0)
        grid.addWidget(self.stok_input, 3, 1)

        grid.addWidget(QLabel("Minimum Stok Seviyesi:"), 4, 0)
        self.min_stok_input = QSpinBox()
        self.min_stok_input.setMaximum(10000)
        self.min_stok_input.setValue(10)
        grid.addWidget(self.min_stok_input, 4, 1)

        grid.addWidget(QLabel("Satış Fiyatı (TL):*"), 5, 0)
        self.fiyat_input = QDoubleSpinBox()
        self.fiyat_input.setMaximum(1000000)
        self.fiyat_input.setValue(0)
        grid.addWidget(self.fiyat_input, 5, 1)

        grid.addWidget(QLabel("Alış Fiyatı (TL):"), 6, 0)
        self.alis_input = QDoubleSpinBox()
        self.alis_input.setMaximum(1000000)
        self.alis_input.setValue(0)
        grid.addWidget(self.alis_input, 6, 1)

        grid.addWidget(QLabel("Birim:"), 7, 0)
        self.birim_combo = QComboBox()
        self.birim_combo.addItems(["adet", "kg", "litre", "paket", "kutu", "metre"])
        grid.addWidget(self.birim_combo, 7, 1)

        grid.addWidget(QLabel("Raf No:"), 8, 0)
        self.raf_input = QLineEdit()
        self.raf_input.setPlaceholderText("Örn: A-01, B-03")
        grid.addWidget(self.raf_input, 8, 1)

        grid.addWidget(QLabel("Açıklama:"), 9, 0)
        self.aciklama_input = QTextEdit()
        self.aciklama_input.setMaximumHeight(80)
        grid.addWidget(self.aciklama_input, 9, 1)

        layout.addWidget(baslik)
        layout.addLayout(grid)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        ekle_btn = QPushButton("✅ Ürün Ekle")
        ekle_btn.setStyleSheet("background-color: #2ec4b6; padding: 12px; border-radius: 10px; font-weight: bold;")
        ekle_btn.clicked.connect(self.ekle)
        iptal_btn = QPushButton("❌ İptal")
        iptal_btn.setObjectName("danger")
        iptal_btn.clicked.connect(self.reject)
        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(iptal_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def ekle(self):
        if self.ad_input.text().strip() and self.fiyat_input.value() > 0:
            kod = self.kod_input.text().strip()
            if not kod:
                import random
                kod = f"PRD{random.randint(10000, 99999)}"
            self.result = (
                kod, self.ad_input.text().strip(), self.kategori_combo.currentText(),
                self.stok_input.value(), self.min_stok_input.value(), self.fiyat_input.value(),
                self.alis_input.value() if self.alis_input.value() > 0 else None,
                self.birim_combo.currentText(), self.raf_input.text().strip(), self.aciklama_input.toPlainText()
            )
            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Ürün adı ve satış fiyatı zorunludur!")


# ============ SIPARIS OLUSTUR DIALOG ============

class SiparisOlusturDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Yeni Sipariş Oluştur")
        self.setGeometry(200, 200, 550, 600)
        self.setStyleSheet(DARK_STYLE)
        self.init_ui()
        self.result = None

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        baslik = QLabel("🛒 Yeni Sipariş Oluştur")
        baslik.setFont(QFont("Arial", 16, QFont.Bold))
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("color: #0077b6; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(12)

        grid.addWidget(QLabel("Ürün Seçin:*"), 0, 0)
        self.urun_combo = QComboBox()
        for urun in self.db.urunleri_getir():
            self.urun_combo.addItem(f"{urun['ad']} - Stok: {urun['stok']} - {urun['fiyat']:.2f} TL", urun['urun_id'])
        grid.addWidget(self.urun_combo, 0, 1)

        grid.addWidget(QLabel("Adet:*"), 1, 0)
        self.adet_input = QSpinBox()
        self.adet_input.setMinimum(1)
        self.adet_input.setMaximum(1000)
        self.adet_input.valueChanged.connect(self.fiyat_hesapla)
        grid.addWidget(self.adet_input, 1, 1)

        grid.addWidget(QLabel("Birim Fiyat (TL):"), 2, 0)
        self.fiyat_input = QDoubleSpinBox()
        self.fiyat_input.setMinimum(0)
        self.fiyat_input.setMaximum(1000000)
        self.fiyat_input.valueChanged.connect(self.fiyat_hesapla)
        grid.addWidget(self.fiyat_input, 2, 1)

        grid.addWidget(QLabel("Toplam Tutar (TL):"), 3, 0)
        self.toplam_label = QLabel("0.00 TL")
        self.toplam_label.setStyleSheet("color: #2ec4b6; font-weight: bold; font-size: 16px;")
        grid.addWidget(self.toplam_label, 3, 1)

        grid.addWidget(QLabel("Müşteri Adı:"), 4, 0)
        self.musteri_adi_input = QLineEdit()
        grid.addWidget(self.musteri_adi_input, 4, 1)

        grid.addWidget(QLabel("Müşteri Telefon:"), 5, 0)
        self.musteri_tel_input = QLineEdit()
        grid.addWidget(self.musteri_tel_input, 5, 1)

        grid.addWidget(QLabel("Notlar:"), 6, 0)
        self.notlar_input = QTextEdit()
        self.notlar_input.setMaximumHeight(80)
        grid.addWidget(self.notlar_input, 6, 1)

        layout.addWidget(baslik)
        layout.addLayout(grid)

        self.urun_combo.currentIndexChanged.connect(self.urun_fiyat_doldur)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        olustur_btn = QPushButton("✅ Sipariş Oluştur")
        olustur_btn.setStyleSheet("background-color: #2ec4b6; padding: 12px; border-radius: 10px; font-weight: bold;")
        olustur_btn.clicked.connect(self.siparis_olustur)
        iptal_btn = QPushButton("❌ İptal")
        iptal_btn.setObjectName("danger")
        iptal_btn.clicked.connect(self.reject)
        button_layout.addWidget(olustur_btn)
        button_layout.addWidget(iptal_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def urun_fiyat_doldur(self):
        index = self.urun_combo.currentIndex()
        if index >= 0:
            urun_id = self.urun_combo.itemData(index)
            urun = self.db.urun_getir(urun_id)
            if urun:
                self.fiyat_input.setValue(urun['fiyat'])

    def fiyat_hesapla(self):
        toplam = self.adet_input.value() * self.fiyat_input.value()
        self.toplam_label.setText(f"{toplam:,.2f} TL")

    def siparis_olustur(self):
        urun_id = self.urun_combo.currentData()
        adet = self.adet_input.value()
        fiyat = self.fiyat_input.value()
        if urun_id and adet > 0 and fiyat > 0:
            self.result = (urun_id, adet, fiyat, self.musteri_adi_input.text().strip(),
                          self.musteri_tel_input.text().strip(), self.notlar_input.toPlainText())
            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Ürün, adet ve fiyat zorunludur!")


# ============ STOK GUNCELLE DIALOG ============

class StokGuncelleDialog(QDialog):
    def __init__(self, db, urun, islem_tipi="arttir", parent=None):
        super().__init__(parent)
        self.db = db
        self.urun = urun
        self.islem_tipi = islem_tipi
        self.setWindowTitle(f"Stok {islem_tipi.capitalize()} - {urun['ad']}")
        self.setGeometry(400, 300, 400, 350)
        self.setStyleSheet(DARK_STYLE)
        self.init_ui()
        self.result = None

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        icon = "📈" if self.islem_tipi == "arttir" else "📉"
        baslik = QLabel(f"{icon} Stok {self.islem_tipi.capitalize()}")
        baslik.setFont(QFont("Arial", 16, QFont.Bold))
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("color: #0077b6; margin-bottom: 10px;")

        bilgi_frame = QFrame()
        bilgi_frame.setStyleSheet("background-color: #2a3a5c; border-radius: 10px; padding: 10px;")
        bilgi_layout = QVBoxLayout()
        bilgi_layout.addWidget(QLabel(f"📦 Ürün: {self.urun['ad']}"))
        bilgi_layout.addWidget(QLabel(f"📊 Mevcut Stok: {self.urun['stok']} {self.urun['birim']}"))
        bilgi_frame.setLayout(bilgi_layout)

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.addWidget(QLabel("Miktar:"), 0, 0)
        self.miktar_input = QSpinBox()
        self.miktar_input.setMinimum(1)
        self.miktar_input.setMaximum(100000)
        grid.addWidget(self.miktar_input, 0, 1)
        grid.addWidget(QLabel("Açıklama:"), 1, 0)
        self.aciklama_input = QTextEdit()
        self.aciklama_input.setMaximumHeight(80)
        grid.addWidget(self.aciklama_input, 1, 1)

        layout.addWidget(baslik)
        layout.addWidget(bilgi_frame)
        layout.addLayout(grid)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        islem_btn = QPushButton(f"✅ Stok {self.islem_tipi.capitalize()}")
        islem_btn.setStyleSheet("background-color: #2ec4b6; padding: 12px; border-radius: 10px; font-weight: bold;")
        islem_btn.clicked.connect(self.islem_yap)
        iptal_btn = QPushButton("❌ İptal")
        iptal_btn.setObjectName("danger")
        iptal_btn.clicked.connect(self.reject)
        button_layout.addWidget(islem_btn)
        button_layout.addWidget(iptal_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def islem_yap(self):
        miktar = self.miktar_input.value()
        if miktar > 0:
            self.result = (self.urun['urun_id'], miktar, self.aciklama_input.toPlainText())
            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Geçerli bir miktar giriniz!")


# ============ GRAFIK WIDGET ============

class WarehouseStatsWidget(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.figure = Figure(figsize=(14, 6), dpi=100, facecolor='#1b263b')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_charts(self):
        self.figure.clear()
        ax1 = self.figure.add_subplot(131)
        ax1.set_facecolor('#2a3a5c')
        kategoriler = self.db.kategori_dagilimi()
        if kategoriler:
            kate_adi = [k['kategori'][:10] for k in kategoriler[:5]]
            kate_sayi = [k['sayi'] for k in kategoriler[:5]]
            colors = ['#0077b6', '#2ec4b6', '#ff9f1c', '#e63946', '#9c27b0']
            ax1.bar(kate_adi, kate_sayi, color=colors[:len(kate_adi)], edgecolor='none', width=0.6)
            ax1.set_title('Kategori Dağılımı', fontsize=12, fontweight='bold', color='#0077b6', pad=15)
            ax1.set_ylabel('Ürün Sayısı', fontsize=10, color='#e0e1dd')
            ax1.tick_params(axis='y', colors='#e0e1dd')
            ax1.tick_params(axis='x', colors='#e0e1dd', labelsize=9, rotation=15)
        else:
            ax1.text(0.5, 0.5, 'Veri Yok', ha='center', va='center', fontsize=12, color='#e0e1dd')

        ax2 = self.figure.add_subplot(132)
        ax2.set_facecolor('#2a3a5c')
        urunler = self.db.urunleri_getir()
        dusuk_stok = sum(1 for u in urunler if u['stok'] <= u['minimum_stok'])
        normal_stok = len(urunler) - dusuk_stok
        if len(urunler) > 0:
            sizes = [normal_stok, dusuk_stok]
            labels = [f'Normal Stok\n{normal_stok}', f'Düşük Stok\n{dusuk_stok}']
            colors = ['#2ec4b6', '#e63946']
            ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, textprops={'fontsize': 10, 'color': '#e0e1dd'})
            ax2.set_title('Stok Durumu', fontsize=12, fontweight='bold', color='#0077b6', pad=15)
        else:
            ax2.text(0.5, 0.5, 'Veri Yok', ha='center', va='center', fontsize=12, color='#e0e1dd')

        ax3 = self.figure.add_subplot(133)
        ax3.set_facecolor('#2a3a5c')
        istatistikler = [self.db.toplam_urun_sayisi(), self.db.toplam_stok_adeti(),
                        len(self.db.siparisleri_getir()), len(self.db.dusuk_stoklu_urunler())]
        labels = ['📦 Ürünler', '📊 Toplam Stok', '🛒 Siparişler', '⚠️ Düşük Stok']
        colors_bar = ['#0077b6', '#2ec4b6', '#ff9f1c', '#e63946']
        ax3.bar(labels, istatistikler, color=colors_bar, edgecolor='none', width=0.6)
        ax3.set_title('Sistem İstatistikleri', fontsize=12, fontweight='bold', color='#0077b6', pad=15)
        ax3.set_ylabel('Sayı', fontsize=10, color='#e0e1dd')
        ax3.tick_params(axis='y', colors='#e0e1dd')
        ax3.tick_params(axis='x', colors='#e0e1dd', labelsize=9)

        self.figure.tight_layout()
        self.canvas.draw()


# ============ ANA PENCERE ============

class WarehouseMainWindow(QMainWindow):
    def __init__(self, kullanici, db):
        super().__init__()
        self.kullanici = kullanici
        self.db = db
        self.setWindowTitle(f"🏪 Depo ve Stok Yönetim Sistemi - Hoşgeldiniz, {kullanici['ad']} {kullanici['soyad']}")
        self.setGeometry(50, 50, 1400, 850)
        self.setStyleSheet(DARK_STYLE)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #1b263b; border-radius: 15px;")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(25, 15, 25, 15)

        left_header = QWidget()
        left_layout = QHBoxLayout()
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(0, 0, 0, 0)
        logo_label = QLabel("🏪")
        logo_label.setFont(QFont("Arial", 28))
        left_layout.addWidget(logo_label)
        header = QLabel("DEPO & STOK YÖNETİM SİSTEMİ")
        header_font = QFont("Arial", 18, QFont.Bold)
        header.setFont(header_font)
        header.setStyleSheet("color: #0077b6;")
        left_layout.addWidget(header)
        left_header.setLayout(left_layout)

        # Sağ taraf
        right_widget = QWidget()
        right_layout = QHBoxLayout()
        right_layout.setSpacing(15)
        right_layout.setContentsMargins(0, 0, 0, 0)

        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame { background-color: #2a3a5c; border: 1px solid #415a77; border-radius: 25px; padding: 2px; }
            QFrame:focus-within { border: 1px solid #0077b6; }
        """)
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)
        search_layout.setContentsMargins(12, 5, 12, 5)
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("color: #0077b6; font-size: 14px; background: transparent;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ürün ara...")
        self.search_input.setStyleSheet("background-color: transparent; border: none; color: #e0e1dd; font-size: 12px; padding: 5px 0; min-width: 250px;")
        self.search_input.textChanged.connect(self.arama_yap)
        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input)
        search_frame.setLayout(search_layout)

        kullanici_label = QLabel(f"👤 {self.kullanici['ad']} {self.kullanici['soyad']} [{self.kullanici['rol']}]")
        kullanici_label.setFont(QFont("Arial", 10, QFont.Bold))
        kullanici_label.setStyleSheet("color: #0077b6; background-color: #2a3a5c; padding: 8px 15px; border-radius: 20px;")

        cikis_btn = QPushButton("🚪 Çıkış")
        cikis_btn.setObjectName("danger")
        cikis_btn.clicked.connect(self.cikis_yap)

        right_layout.addWidget(search_frame)
        right_layout.addWidget(kullanici_label)
        right_layout.addWidget(cikis_btn)
        right_widget.setLayout(right_layout)

        header_layout.addWidget(left_header)
        header_layout.addStretch()
        header_layout.addWidget(right_widget)
        header_frame.setLayout(header_layout)

        # Dashboard Kartları
        dashboard_layout = QHBoxLayout()
        dashboard_layout.setSpacing(20)

        def create_card(title, value, color):
            card = QFrame()
            card.setStyleSheet(f"background-color: #1b263b; border-radius: 15px; padding: 20px; min-width: 180px;")
            layout = QVBoxLayout()
            layout.setSpacing(8)
            title_label = QLabel(title)
            title_label.setFont(QFont("Arial", 11, QFont.Bold))
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet(f"color: {color};")
            value_label = QLabel(value)
            value_label.setFont(QFont("Arial", 24, QFont.Bold))
            value_label.setAlignment(Qt.AlignCenter)
            value_label.setStyleSheet(f"color: {color};")
            value_label.setObjectName("value_label")
            layout.addWidget(title_label)
            layout.addWidget(value_label)
            card.setLayout(layout)
            return card

        urun_card = create_card("📦 Toplam Ürün", "0", "#0077b6")
        stok_card = create_card("📊 Toplam Stok", "0", "#2ec4b6")
        deger_card = create_card("💰 Stok Değeri", "0 TL", "#ff9f1c")
        siparis_card = create_card("🛒 Aktif Sipariş", "0", "#e63946")

        dashboard_layout.addWidget(urun_card)
        dashboard_layout.addWidget(stok_card)
        dashboard_layout.addWidget(deger_card)
        dashboard_layout.addWidget(siparis_card)

        self.urun_label = urun_card.findChild(QLabel, "value_label")
        self.stok_label = stok_card.findChild(QLabel, "value_label")
        self.deger_label = deger_card.findChild(QLabel, "value_label")
        self.siparis_label = siparis_card.findChild(QLabel, "value_label")

        # Sekmeler
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_urun_tab(), "📦 Ürünler")
        self.tabs.addTab(self.create_siparis_tab(), "🛒 Siparişler")
        self.tabs.addTab(self.create_hareket_tab(), "📊 Stok Hareketleri")
        self.tabs.addTab(WarehouseStatsWidget(self.db), "📈 İstatistikler")
        self.tabs.addTab(self.create_rapor_tab(), "📄 Raporlar")

        if self.kullanici['rol'] == 'admin':
            self.tabs.addTab(self.create_kullanici_tab(), "👤 Kullanıcılar")

        main_layout.addWidget(header_frame)
        main_layout.addLayout(dashboard_layout)
        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_all)
        self.timer.start(3000)

    def create_urun_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        filter_panel = QFrame()
        filter_panel.setStyleSheet("background-color: #1b263b; border-radius: 10px; padding: 10px;")
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        filter_layout.addWidget(QLabel("Kategori:"))
        self.kategori_filter = QComboBox()
        self.kategori_filter.addItem("Tüm Kategoriler")
        self.kategori_filter.addItems(self.db.kategorileri_getir())
        self.kategori_filter.currentTextChanged.connect(self.urunleri_filtrele)
        filter_layout.addWidget(self.kategori_filter)
        self.dusuk_stok_filter = QCheckBox("Sadece Düşük Stoklular")
        self.dusuk_stok_filter.stateChanged.connect(self.urunleri_filtrele)
        filter_layout.addWidget(self.dusuk_stok_filter)
        filter_layout.addStretch()
        filter_panel.setLayout(filter_layout)
        layout.addWidget(filter_panel)

        button_panel = QFrame()
        button_panel.setStyleSheet("background-color: #1b263b; border-radius: 10px; padding: 10px;")
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        ekle_btn = QPushButton("➕ Yeni Ürün Ekle")
        ekle_btn.clicked.connect(self.urun_ekle)
        stok_arttir_btn = QPushButton("📈 Stok Arttır")
        stok_arttir_btn.setObjectName("success")
        stok_arttir_btn.clicked.connect(self.stok_arttir)
        stok_azalt_btn = QPushButton("📉 Stok Azalt")
        stok_azalt_btn.setObjectName("warning")
        stok_azalt_btn.clicked.connect(self.stok_azalt)
        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.clicked.connect(self.urunleri_listele)
        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(stok_arttir_btn)
        button_layout.addWidget(stok_azalt_btn)
        button_layout.addWidget(yenile_btn)
        button_layout.addStretch()
        button_panel.setLayout(button_layout)
        layout.addWidget(button_panel)

        self.urun_table = QTableWidget()
        self.urun_table.setColumnCount(10)
        self.urun_table.setHorizontalHeaderLabels(["ID", "Ürün Kodu", "Ürün Adı", "Kategori", "Stok", "Min Stok", "Fiyat", "Birim", "Raf", "Durum"])
        self.urun_table.setAlternatingRowColors(True)
        self.urun_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.urun_table)
        widget.setLayout(layout)
        return widget

    def create_siparis_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        filter_panel = QFrame()
        filter_panel.setStyleSheet("background-color: #1b263b; border-radius: 10px; padding: 10px;")
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        filter_layout.addWidget(QLabel("Durum:"))
        self.siparis_filter = QComboBox()
        self.siparis_filter.addItems(["Tümü", "Beklemede", "Hazırlanıyor", "Teslim Edildi", "İptal Edildi"])
        self.siparis_filter.currentTextChanged.connect(self.siparisleri_listele)
        filter_layout.addWidget(self.siparis_filter)
        filter_layout.addStretch()
        filter_panel.setLayout(filter_layout)
        layout.addWidget(filter_panel)

        button_panel = QFrame()
        button_panel.setStyleSheet("background-color: #1b263b; border-radius: 10px; padding: 10px;")
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        siparis_olustur_btn = QPushButton("🛒 Yeni Sipariş")
        siparis_olustur_btn.setStyleSheet("background-color: #2ec4b6;")
        siparis_olustur_btn.clicked.connect(self.siparis_olustur)
        onayla_btn = QPushButton("✅ Sipariş Onayla")
        onayla_btn.clicked.connect(self.siparis_onayla)
        teslim_et_btn = QPushButton("🚚 Teslim Et")
        teslim_et_btn.setStyleSheet("background-color: #ff9f1c;")
        teslim_et_btn.clicked.connect(self.siparis_teslim_et)
        iptal_btn = QPushButton("❌ Sipariş İptal")
        iptal_btn.setObjectName("danger")
        iptal_btn.clicked.connect(self.siparis_iptal)
        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.clicked.connect(self.siparisleri_listele)
        button_layout.addWidget(siparis_olustur_btn)
        button_layout.addWidget(onayla_btn)
        button_layout.addWidget(teslim_et_btn)
        button_layout.addWidget(iptal_btn)
        button_layout.addWidget(yenile_btn)
        button_layout.addStretch()
        button_panel.setLayout(button_layout)
        layout.addWidget(button_panel)

        self.siparis_table = QTableWidget()
        self.siparis_table.setColumnCount(11)
        self.siparis_table.setHorizontalHeaderLabels(["ID", "Sipariş No", "Ürün", "Adet", "Birim Fiyat", "Toplam", "Tarih", "Teslim Tarihi", "Durum", "Müşteri", "Telefon"])
        self.siparis_table.setAlternatingRowColors(True)
        self.siparis_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.siparis_table)
        widget.setLayout(layout)
        return widget

    def create_hareket_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        self.hareket_table = QTableWidget()
        self.hareket_table.setColumnCount(8)
        self.hareket_table.setHorizontalHeaderLabels(["ID", "Ürün", "İşlem Tipi", "Miktar", "Önceki Stok", "Sonraki Stok", "Tarih", "Açıklama"])
        self.hareket_table.setAlternatingRowColors(True)
        self.hareket_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.clicked.connect(self.hareketleri_listele)
        layout.addWidget(yenile_btn)
        layout.addWidget(self.hareket_table)
        widget.setLayout(layout)
        return widget

    def create_rapor_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        button_panel = QFrame()
        button_panel.setStyleSheet("background-color: #1b263b; border-radius: 10px; padding: 10px;")
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        dusuk_stok_btn = QPushButton("⚠️ Düşük Stok Raporu")
        dusuk_stok_btn.clicked.connect(self.dusuk_stok_raporu)
        cok_satan_btn = QPushButton("🏆 En Çok Satan Ürünler")
        cok_satan_btn.clicked.connect(self.cok_satan_raporu)
        aylik_satis_btn = QPushButton("📊 Aylık Satış Özeti")
        aylik_satis_btn.clicked.connect(self.aylik_satis_raporu)
        kapsamli_btn = QPushButton("📋 Kapsamlı Rapor")
        kapsamli_btn.setStyleSheet("background-color: #0077b6;")
        kapsamli_btn.clicked.connect(self.kapsamli_rapor)
        button_layout.addWidget(dusuk_stok_btn)
        button_layout.addWidget(cok_satan_btn)
        button_layout.addWidget(aylik_satis_btn)
        button_layout.addWidget(kapsamli_btn)
        button_layout.addStretch()
        button_panel.setLayout(button_layout)
        layout.addWidget(button_panel)

        self.rapor_text = QTextEdit()
        self.rapor_text.setReadOnly(True)
        self.rapor_text.setStyleSheet("background-color: #1b263b; border: 1px solid #0077b6; border-radius: 10px; padding: 15px; font-family: 'Courier New', monospace; font-size: 11px;")
        layout.addWidget(self.rapor_text)
        widget.setLayout(layout)
        return widget

    def create_kullanici_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        button_panel = QFrame()
        button_panel.setStyleSheet("background-color: #1b263b; border-radius: 10px; padding: 10px;")
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        ekle_btn = QPushButton("➕ Yeni Kullanıcı Ekle")
        ekle_btn.clicked.connect(self.sistem_kullanici_ekle)
        sil_btn = QPushButton("🗑️ Kullanıcı Sil")
        sil_btn.setObjectName("danger")
        sil_btn.clicked.connect(self.sistem_kullanici_sil)
        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.clicked.connect(self.sistem_kullanici_listele)
        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(sil_btn)
        button_layout.addWidget(yenile_btn)
        button_layout.addStretch()
        button_panel.setLayout(button_layout)
        layout.addWidget(button_panel)

        self.kullanici_table = QTableWidget()
        self.kullanici_table.setColumnCount(6)
        self.kullanici_table.setHorizontalHeaderLabels(["ID", "Kullanıcı Adı", "Ad", "Soyad", "Rol", "Durum"])
        self.kullanici_table.setAlternatingRowColors(True)
        self.kullanici_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.kullanici_table)
        widget.setLayout(layout)
        return widget

    def load_data(self):
        self.urunleri_listele()
        self.siparisleri_listele()
        self.hareketleri_listele()
        if self.kullanici['rol'] == 'admin':
            self.sistem_kullanici_listele()

    def refresh_all(self):
        self.urunleri_listele()
        self.siparisleri_listele()
        self.hareketleri_listele()
        if self.kullanici['rol'] == 'admin':
            self.sistem_kullanici_listele()
        self.urun_label.setText(str(self.db.toplam_urun_sayisi()))
        self.stok_label.setText(str(self.db.toplam_stok_adeti()))
        self.deger_label.setText(f"{self.db.toplam_urun_degeri():,.2f} TL")
        aktif = len([s for s in self.db.siparisleri_getir() if s['durum'] in ['Beklemede', 'Hazırlanıyor']])
        self.siparis_label.setText(str(aktif))

    def arama_yap(self):
        metin = self.search_input.text().strip().lower()
        if not metin:
            self.urunleri_listele()
            return
        self.urun_table.setRowCount(0)
        for urun in self.db.urunleri_getir():
            if metin in urun['ad'].lower() or metin in urun['urun_kodu'].lower() or metin in urun['kategori'].lower():
                row = self.urun_table.rowCount()
                self.urun_table.insertRow(row)
                self.urun_table.setItem(row, 0, QTableWidgetItem(str(urun['urun_id'])))
                self.urun_table.setItem(row, 1, QTableWidgetItem(urun['urun_kodu']))
                self.urun_table.setItem(row, 2, QTableWidgetItem(urun['ad']))
                self.urun_table.setItem(row, 3, QTableWidgetItem(urun['kategori']))
                stok_item = QTableWidgetItem(str(urun['stok']))
                if urun['stok'] <= urun['minimum_stok']:
                    stok_item.setForeground(QColor("#e63946"))
                self.urun_table.setItem(row, 4, stok_item)
                self.urun_table.setItem(row, 5, QTableWidgetItem(str(urun['minimum_stok'])))
                self.urun_table.setItem(row, 6, QTableWidgetItem(f"{urun['fiyat']:,.2f} TL"))
                self.urun_table.setItem(row, 7, QTableWidgetItem(urun['birim']))
                self.urun_table.setItem(row, 8, QTableWidgetItem(urun['raf_no'] or "-"))
                self.urun_table.setItem(row, 9, QTableWidgetItem(urun['durum']))

    def urunleri_filtrele(self):
        kategori = self.kategori_filter.currentText()
        dusuk = self.dusuk_stok_filter.isChecked()
        if kategori == "Tüm Kategoriler":
            urunler = self.db.urunleri_getir(dusuk_stok=dusuk)
        else:
            urunler = [u for u in self.db.urunleri_getir(kategori=kategori) if not dusuk or u['stok'] <= u['minimum_stok']]
        self.urun_table.setRowCount(0)
        for urun in urunler:
            row = self.urun_table.rowCount()
            self.urun_table.insertRow(row)
            self.urun_table.setItem(row, 0, QTableWidgetItem(str(urun['urun_id'])))
            self.urun_table.setItem(row, 1, QTableWidgetItem(urun['urun_kodu']))
            self.urun_table.setItem(row, 2, QTableWidgetItem(urun['ad']))
            self.urun_table.setItem(row, 3, QTableWidgetItem(urun['kategori']))
            stok_item = QTableWidgetItem(str(urun['stok']))
            if urun['stok'] <= urun['minimum_stok']:
                stok_item.setForeground(QColor("#e63946"))
            self.urun_table.setItem(row, 4, stok_item)
            self.urun_table.setItem(row, 5, QTableWidgetItem(str(urun['minimum_stok'])))
            self.urun_table.setItem(row, 6, QTableWidgetItem(f"{urun['fiyat']:,.2f} TL"))
            self.urun_table.setItem(row, 7, QTableWidgetItem(urun['birim']))
            self.urun_table.setItem(row, 8, QTableWidgetItem(urun['raf_no'] or "-"))
            self.urun_table.setItem(row, 9, QTableWidgetItem(urun['durum']))

    def urunleri_listele(self):
        self.urunleri_filtrele()

    def urun_ekle(self):
        dialog = UrunEkleDialog(self.db, self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            try:
                self.db.urun_ekle(*dialog.result)
                QMessageBox.information(self, "Başarılı", "✅ Ürün başarıyla eklendi!")
                self.urunleri_listele()
                self.kategori_filter.clear()
                self.kategori_filter.addItem("Tüm Kategoriler")
                self.kategori_filter.addItems(self.db.kategorileri_getir())
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Hata", "Bu ürün kodu zaten kullanımda!")

    def stok_arttir(self):
        row = self.urun_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir ürün seçin!")
            return
        urun_id = int(self.urun_table.item(row, 0).text())
        urun = self.db.urun_getir(urun_id)
        if not urun:
            QMessageBox.warning(self, "Hata", "Ürün bulunamadı!")
            return
        dialog = StokGuncelleDialog(self.db, urun, "arttir", self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            try:
                self.db.stok_arttir(*dialog.result)
                QMessageBox.information(self, "Başarılı", "✅ Stok arttırıldı!")
                self.urunleri_listele()
                self.hareketleri_listele()
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))

    def stok_azalt(self):
        row = self.urun_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir ürün seçin!")
            return
        urun_id = int(self.urun_table.item(row, 0).text())
        urun = self.db.urun_getir(urun_id)
        if not urun:
            QMessageBox.warning(self, "Hata", "Ürün bulunamadı!")
            return
        dialog = StokGuncelleDialog(self.db, urun, "azalt", self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            try:
                self.db.stok_azalt(*dialog.result)
                QMessageBox.information(self, "Başarılı", "✅ Stok azaltıldı!")
                self.urunleri_listele()
                self.hareketleri_listele()
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))

    def siparis_olustur(self):
        dialog = SiparisOlusturDialog(self.db, self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            try:
                siparis_no = self.db.siparis_olustur(*dialog.result)
                QMessageBox.information(self, "Başarılı", f"✅ Sipariş oluşturuldu!\nSipariş No: {siparis_no}")
                self.siparisleri_listele()
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))

    def siparis_onayla(self):
        row = self.siparis_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir sipariş seçin!")
            return
        siparis_id = int(self.siparis_table.item(row, 0).text())
        if self.siparis_table.item(row, 8).text() != "Beklemede":
            QMessageBox.warning(self, "Uyarı", "Sadece bekleyen siparişler onaylanabilir!")
            return
        try:
            self.db.siparis_onayla(siparis_id)
            QMessageBox.information(self, "Başarılı", "✅ Sipariş onaylandı!")
            self.siparisleri_listele()
            self.urunleri_listele()
            self.hareketleri_listele()
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def siparis_teslim_et(self):
        row = self.siparis_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir sipariş seçin!")
            return
        siparis_id = int(self.siparis_table.item(row, 0).text())
        self.db.siparis_teslim_et(siparis_id)
        QMessageBox.information(self, "Başarılı", "✅ Sipariş teslim edildi!")
        self.siparisleri_listele()

    def siparis_iptal(self):
        row = self.siparis_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir sipariş seçin!")
            return
        siparis_id = int(self.siparis_table.item(row, 0).text())
        if self.siparis_table.item(row, 8).text() == "Teslim Edildi":
            QMessageBox.warning(self, "Uyarı", "Teslim edilmiş sipariş iptal edilemez!")
            return
        if QMessageBox.question(self, "Onay", "Siparişi iptal etmek istediğinize emin misiniz?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            try:
                self.db.siparis_iptal(siparis_id)
                QMessageBox.information(self, "Başarılı", "❌ Sipariş iptal edildi!")
                self.siparisleri_listele()
                self.urunleri_listele()
                self.hareketleri_listele()
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))

    def siparisleri_listele(self):
        durum = self.siparis_filter.currentText()
        siparisler = self.db.siparisleri_getir() if durum == "Tümü" else self.db.siparisleri_getir(durum=durum)
        self.siparis_table.setRowCount(0)
        for s in siparisler:
            row = self.siparis_table.rowCount()
            self.siparis_table.insertRow(row)
            self.siparis_table.setItem(row, 0, QTableWidgetItem(str(s['siparis_id'])))
            self.siparis_table.setItem(row, 1, QTableWidgetItem(s['siparis_no']))
            self.siparis_table.setItem(row, 2, QTableWidgetItem(s['urun_adi']))
            self.siparis_table.setItem(row, 3, QTableWidgetItem(str(s['adet'])))
            self.siparis_table.setItem(row, 4, QTableWidgetItem(f"{s['birim_fiyat']:,.2f} TL"))
            self.siparis_table.setItem(row, 5, QTableWidgetItem(f"{s['toplam_tutar']:,.2f} TL"))
            tarih = datetime.fromisoformat(s['siparis_tarihi'].replace(' ', 'T')) if s['siparis_tarihi'] else None
            self.siparis_table.setItem(row, 6, QTableWidgetItem(tarih.strftime("%d.%m.%Y %H:%M") if tarih else "-"))
            teslim = datetime.fromisoformat(s['teslim_tarihi'].replace(' ', 'T')) if s['teslim_tarihi'] else None
            self.siparis_table.setItem(row, 7, QTableWidgetItem(teslim.strftime("%d.%m.%Y") if teslim else "-"))
            durum_item = QTableWidgetItem(s['durum'])
            if s['durum'] == 'Beklemede':
                durum_item.setForeground(QColor("#ff9f1c"))
            elif s['durum'] == 'Hazırlanıyor':
                durum_item.setForeground(QColor("#0077b6"))
            elif s['durum'] == 'Teslim Edildi':
                durum_item.setForeground(QColor("#2ec4b6"))
            else:
                durum_item.setForeground(QColor("#e63946"))
            self.siparis_table.setItem(row, 8, durum_item)
            self.siparis_table.setItem(row, 9, QTableWidgetItem(s['musteri_adi'] or "-"))
            self.siparis_table.setItem(row, 10, QTableWidgetItem(s['musteri_tel'] or "-"))

    def hareketleri_listele(self):
        hareketler = self.db.stok_hareketlerini_getir(limit=100)
        self.hareket_table.setRowCount(0)
        for h in hareketler:
            row = self.hareket_table.rowCount()
            self.hareket_table.insertRow(row)
            self.hareket_table.setItem(row, 0, QTableWidgetItem(str(h['hareket_id'])))
            self.hareket_table.setItem(row, 1, QTableWidgetItem(h['urun_adi']))
            tip = QTableWidgetItem(h['hareket_tipi'])
            tip.setForeground(QColor("#2ec4b6") if h['hareket_tipi'] == 'Giriş' else QColor("#e63946"))
            self.hareket_table.setItem(row, 2, tip)
            self.hareket_table.setItem(row, 3, QTableWidgetItem(str(h['miktar'])))
            self.hareket_table.setItem(row, 4, QTableWidgetItem(str(h['onceki_stok'])))
            self.hareket_table.setItem(row, 5, QTableWidgetItem(str(h['sonraki_stok'])))
            tarih = datetime.fromisoformat(h['islem_tarihi'].replace(' ', 'T')) if h['islem_tarihi'] else None
            self.hareket_table.setItem(row, 6, QTableWidgetItem(tarih.strftime("%d.%m.%Y %H:%M") if tarih else "-"))
            self.hareket_table.setItem(row, 7, QTableWidgetItem(h['aciklama'] or "-"))

    def dusuk_stok_raporu(self):
        urunler = self.db.dusuk_stoklu_urunler()
        if not urunler:
            self.rapor_text.setText("✅ Tüm ürünlerin stoğu yeterli seviyede!")
        else:
            rapor = "╔═════════════════════════════════════════════════════════════════╗\n"
            rapor += "║                    ⚠️ DÜŞÜK STOK RAPORU                        ║\n"
            rapor += "╚═════════════════════════════════════════════════════════════════╝\n\n"
            for u in urunler:
                eksik = u['minimum_stok'] - u['stok']
                rapor += f"📦 {u['ad']}\n"
                rapor += f"   ├─ Stok: {u['stok']} / {u['minimum_stok']} (Eksik: {eksik})\n"
                rapor += f"   ├─ Raf No: {u['raf_no'] or 'Belirtilmemiş'}\n"
                rapor += f"   └─ Acil Sipariş Verilmeli!\n\n"
            self.rapor_text.setText(rapor)
        self.tabs.setCurrentIndex(4)

    def cok_satan_raporu(self):
        urunler = self.db.en_cok_satan_urunler(10)
        if not urunler:
            self.rapor_text.setText("Henüz satış verisi bulunmamaktadır!")
        else:
            rapor = "╔═════════════════════════════════════════════════════════════════╗\n"
            rapor += "║                  🏆 EN ÇOK SATAN ÜRÜNLER                       ║\n"
            rapor += "╚═════════════════════════════════════════════════════════════════╝\n\n"
            for i, u in enumerate(urunler, 1):
                rapor += f"{i}. {u['urun_adi']}\n"
                rapor += f"   ├─ Toplam Satış: {u['toplam_satis']} adet\n"
                rapor += f"   └─ Sipariş Sayısı: {u['siparis_sayisi']}\n\n"
            self.rapor_text.setText(rapor)
        self.tabs.setCurrentIndex(4)

    def aylik_satis_raporu(self):
        aylik = self.db.aylik_siparis_ozeti()
        if not aylik:
            self.rapor_text.setText("Henüz satış verisi bulunmamaktadır!")
        else:
            rapor = "╔═════════════════════════════════════════════════════════════════╗\n"
            rapor += "║                    📊 AYLIK SATIŞ ÖZETİ                        ║\n"
            rapor += "╚═════════════════════════════════════════════════════════════════╝\n\n"
            for a in aylik:
                rapor += f"📅 {a['ay']}\n"
                rapor += f"   ├─ Sipariş Sayısı: {a['siparis_sayisi']}\n"
                rapor += f"   ├─ Toplam Ürün: {a['toplam_urun']} adet\n"
                rapor += f"   └─ Toplam Ciro: {a['toplam_ciro']:,.2f} TL\n\n"
            self.rapor_text.setText(rapor)
        self.tabs.setCurrentIndex(4)

    def kapsamli_rapor(self):
        rapor = "╔════════════════════════════════════════════════════════════════════════════╗\n"
        rapor += "║                 🏪 DEPO VE STOK YÖNETİM SİSTEMİ RAPORU                   ║\n"
        rapor += "╚════════════════════════════════════════════════════════════════════════════╝\n\n"
        rapor += "┌────────────────────────────────────────────────┐\n"
        rapor += "│                 📊 GENEL İSTATİSTİKLER          │\n"
        rapor += "├────────────────────────────────────────────────┤\n"
        rapor += f"│ Toplam Ürün Sayısı           : {self.db.toplam_urun_sayisi():>15} │\n"
        rapor += f"│ Toplam Stok Adeti            : {self.db.toplam_stok_adeti():>15} │\n"
        rapor += f"│ Toplam Stok Değeri           : {self.db.toplam_urun_degeri():>15,.2f} TL │\n"
        rapor += f"│ Düşük Stoklu Ürün Sayısı     : {len(self.db.dusuk_stoklu_urunler()):>15} │\n"
        rapor += f"│ Toplam Sipariş Sayısı        : {len(self.db.siparisleri_getir()):>15} │\n"
        rapor += "└────────────────────────────────────────────────┘\n\n"
        rapor += "┌────────────────────────────────────────────────┐\n"
        rapor += "│                  🏆 EN ÇOK SATAN 5 ÜRÜN         │\n"
        rapor += "├────────────────────────────────────────────────┤\n"
        for i, u in enumerate(self.db.en_cok_satan_urunler(5), 1):
            rapor += f"│ {i}. {u['urun_adi'][:25]:<25} : {u['toplam_satis']:>3} adet │\n"
        rapor += "└────────────────────────────────────────────────┘\n"
        self.rapor_text.setText(rapor)
        self.tabs.setCurrentIndex(4)

    def sistem_kullanici_ekle(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Kullanıcı Ekle")
        dialog.setGeometry(400, 300, 400, 400)
        dialog.setStyleSheet(DARK_STYLE)
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.addWidget(QLabel("Kullanıcı Adı:"), 0, 0)
        kadi = QLineEdit()
        grid.addWidget(kadi, 0, 1)
        grid.addWidget(QLabel("Şifre:"), 1, 0)
        sifre = QLineEdit()
        sifre.setEchoMode(QLineEdit.Password)
        grid.addWidget(sifre, 1, 1)
        grid.addWidget(QLabel("Ad:"), 2, 0)
        ad = QLineEdit()
        grid.addWidget(ad, 2, 1)
        grid.addWidget(QLabel("Soyad:"), 3, 0)
        soyad = QLineEdit()
        grid.addWidget(soyad, 3, 1)
        grid.addWidget(QLabel("Rol:"), 4, 0)
        rol = QComboBox()
        rol.addItems(["personel", "admin"])
        grid.addWidget(rol, 4, 1)
        layout.addLayout(grid)
        btn_layout = QHBoxLayout()
        ekle_btn = QPushButton("✅ Ekle")
        iptal_btn = QPushButton("❌ İptal")
        iptal_btn.setObjectName("danger")

        def ekle():
            if kadi.text().strip() and sifre.text().strip() and ad.text().strip() and soyad.text().strip():
                try:
                    self.db.kullanici_ekle(kadi.text().strip(), sifre.text().strip(), ad.text().strip(), soyad.text().strip(), rol.currentText())
                    QMessageBox.information(dialog, "Başarılı", "Kullanıcı eklendi!")
                    dialog.accept()
                    self.sistem_kullanici_listele()
                except sqlite3.IntegrityError:
                    QMessageBox.warning(dialog, "Hata", "Bu kullanıcı adı zaten var!")
            else:
                QMessageBox.warning(dialog, "Uyarı", "Tüm alanları doldurun!")

        ekle_btn.clicked.connect(ekle)
        iptal_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(ekle_btn)
        btn_layout.addWidget(iptal_btn)
        layout.addLayout(btn_layout)
        dialog.setLayout(layout)
        dialog.exec_()

    def sistem_kullanici_sil(self):
        row = self.kullanici_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek kullanıcıyı seçin!")
            return
        kullanici_id = int(self.kullanici_table.item(row, 0).text())
        kullanici_adi = self.kullanici_table.item(row, 1).text()
        if kullanici_adi == "admin":
            QMessageBox.warning(self, "Hata", "Admin kullanıcısı silinemez!")
            return
        if kullanici_adi == self.kullanici['kullanici_adi']:
            QMessageBox.warning(self, "Hata", "Kendi hesabınızı silemezsiniz!")
            return
        if QMessageBox.question(self, "Onay", f"'{kullanici_adi}' kullanıcısını silmek istediğinize emin misiniz?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.kullanici_sil(kullanici_id)
            QMessageBox.information(self, "Başarılı", "Kullanıcı silindi!")
            self.sistem_kullanici_listele()

    def sistem_kullanici_listele(self):
        self.kullanici_table.setRowCount(0)
        for k in self.db.kullanicilari_getir():
            row = self.kullanici_table.rowCount()
            self.kullanici_table.insertRow(row)
            self.kullanici_table.setItem(row, 0, QTableWidgetItem(str(k['kullanici_id'])))
            self.kullanici_table.setItem(row, 1, QTableWidgetItem(k['kullanici_adi']))
            self.kullanici_table.setItem(row, 2, QTableWidgetItem(k['ad']))
            self.kullanici_table.setItem(row, 3, QTableWidgetItem(k['soyad']))
            self.kullanici_table.setItem(row, 4, QTableWidgetItem(k['rol']))
            durum = QTableWidgetItem(k['durum'])
            durum.setForeground(QColor("#2ec4b6") if k['durum'] == 'Aktif' else QColor("#e63946"))
            self.kullanici_table.setItem(row, 5, durum)

    def cikis_yap(self):
        if QMessageBox.question(self, "Çıkış", "Oturumu kapatmak istediğinize emin misiniz?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.close()
            self.yeni_giris()

    def yeni_giris(self):
        login = LoginDialog(self.db)
        if login.exec_() == QDialog.Accepted and login.kullanici:
            self.kullanici = login.kullanici
            self.setWindowTitle(f"🏪 Depo ve Stok Yönetim Sistemi - Hoşgeldiniz, {self.kullanici['ad']} {self.kullanici['soyad']}")
            for widget in self.centralWidget().findChildren(QLabel):
                if "👤" in widget.text() and "[" in widget.text():
                    widget.setText(f"👤 {self.kullanici['ad']} {self.kullanici['soyad']} [{self.kullanici['rol']}]")
            admin_var = any("Kullanıcılar" in self.tabs.tabText(i) for i in range(self.tabs.count()))
            if self.kullanici['rol'] == 'admin' and not admin_var:
                self.tabs.addTab(self.create_kullanici_tab(), "👤 Kullanıcılar")
            elif self.kullanici['rol'] != 'admin' and admin_var:
                for i in range(self.tabs.count()):
                    if "Kullanıcılar" in self.tabs.tabText(i):
                        self.tabs.removeTab(i)
                        break
            self.load_data()
            self.show()
        else:
            sys.exit()


# ============ MAIN ============

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    db = DatabaseManager()
    login = LoginDialog(db)
    if login.exec_() == QDialog.Accepted:
        window = WarehouseMainWindow(login.kullanici, db)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()


if __name__ == "__main__":
    main()
