import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLabel,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox,
    QTabWidget, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ===================== ÜRÜN SINIFI =====================
class Urun:
    _id_counter = 1

    def __init__(self, ad, stok, fiyat):
        self.urun_id = Urun._id_counter
        Urun._id_counter += 1
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
        return f"[{self.urun_id}] {self.ad} | Stok: {self.stok} | Fiyat: {self.fiyat} TL"


# ===================== SİPARİŞ SINIFI =====================
class Siparis:
    _id_counter = 1

    def __init__(self, urun, adet):
        self.siparis_id = Siparis._id_counter
        Siparis._id_counter += 1
        self.urun = urun
        self.adet = adet
        self.toplam_fiyat = urun.fiyat * adet

    def siparis_olustur(self):
        if self.urun.stok_azalt(self.adet):
            return True, f"Sipariş oluşturuldu -> {self.urun.ad} x {self.adet}"
        else:
            return False, "Yetersiz stok"

    def __str__(self):
        return f"[{self.siparis_id}] {self.urun.ad} | Adet: {self.adet} | Toplam: {self.toplam_fiyat:.2f} TL"


# ===================== SİSTEM SINIFI =====================
class Sistem:
    def __init__(self):
        self.urunler = []
        self.siparisler = []

    def urun_ekle(self, urun):
        self.urunler.append(urun)

    def urun_bul(self, uid):
        return next((u for u in self.urunler if u.urun_id == uid), None)

    def urun_sil(self, uid):
        self.urunler = [u for u in self.urunler if u.urun_id != uid]

    def siparis_ekle(self, siparis):
        self.siparisler.append(siparis)

    def toplam_stok_degeri(self):
        return sum(u.stok * u.fiyat for u in self.urunler)

    def toplam_siparis_tutari(self):
        return sum(s.toplam_fiyat for s in self.siparisler)


# ===================== DIALOG PENCERELERI =====================

class UrunEkleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ürün Ekle")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.result = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Ad
        ad_label = QLabel("Ürün Adı:")
        ad_label.setFont(QFont("Arial", 10))
        self.ad_input = QLineEdit()
        self.ad_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Stok
        stok_label = QLabel("Stok:")
        stok_label.setFont(QFont("Arial", 10))
        self.stok_input = QSpinBox()
        self.stok_input.setMinimum(0)
        self.stok_input.setMaximum(1000000)
        self.stok_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Fiyat
        fiyat_label = QLabel("Fiyat (TL):")
        fiyat_label.setFont(QFont("Arial", 10))
        self.fiyat_input = QDoubleSpinBox()
        self.fiyat_input.setMinimum(0.0)
        self.fiyat_input.setMaximum(1000000.0)
        self.fiyat_input.setDecimals(2)
        self.fiyat_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("✓ Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.ekle)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(ad_label)
        layout.addWidget(self.ad_input)
        layout.addWidget(stok_label)
        layout.addWidget(self.stok_input)
        layout.addWidget(fiyat_label)
        layout.addWidget(self.fiyat_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def ekle(self):
        try:
            if not self.ad_input.text().strip():
                QMessageBox.warning(self, "Hata", "Ürün adı boş olamaz!")
                return

            if self.stok_input.value() < 0:
                QMessageBox.warning(self, "Hata", "Stok negatif olamaz!")
                return

            if self.fiyat_input.value() < 0:
                QMessageBox.warning(self, "Hata", "Fiyat negatif olamaz!")
                return

            self.result = (
                self.ad_input.text().strip(),
                self.stok_input.value(),
                self.fiyat_input.value()
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")


class StokArttirDialog(QDialog):
    def __init__(self, urun, parent=None):
        super().__init__(parent)
        self.urun = urun
        self.setWindowTitle(f"Stok Arttır - {urun.ad}")
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.result = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Bilgi
        info_label = QLabel(f"Ürün: {self.urun.ad}\nMevcut Stok: {self.urun.stok}")
        info_label.setFont(QFont("Arial", 10))

        # Miktar
        miktar_label = QLabel("Eklenecek Miktar:")
        miktar_label.setFont(QFont("Arial", 10))
        self.miktar_input = QSpinBox()
        self.miktar_input.setMinimum(1)
        self.miktar_input.setMaximum(1000000)
        self.miktar_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("✓ Arttır")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.arttir)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(info_label)
        layout.addWidget(miktar_label)
        layout.addWidget(self.miktar_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def arttir(self):
        try:
            self.result = self.miktar_input.value()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")


class StokAzaltDialog(QDialog):
    def __init__(self, urun, parent=None):
        super().__init__(parent)
        self.urun = urun
        self.setWindowTitle(f"Stok Azalt - {urun.ad}")
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.result = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Bilgi
        info_label = QLabel(f"Ürün: {self.urun.ad}\nMevcut Stok: {self.urun.stok}")
        info_label.setFont(QFont("Arial", 10))

        # Miktar
        miktar_label = QLabel("Azaltılacak Miktar:")
        miktar_label.setFont(QFont("Arial", 10))
        self.miktar_input = QSpinBox()
        self.miktar_input.setMinimum(1)
        self.miktar_input.setMaximum(self.urun.stok)
        self.miktar_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Butonlar
        button_layout = QHBoxLayout()
        azalt_btn = QPushButton("✓ Azalt")
        azalt_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        azalt_btn.clicked.connect(self.azalt)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(azalt_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(info_label)
        layout.addWidget(miktar_label)
        layout.addWidget(self.miktar_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def azalt(self):
        try:
            self.result = self.miktar_input.value()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")


class SiparisOlusturDialog(QDialog):
    def __init__(self, sistem, parent=None):
        super().__init__(parent)
        self.sistem = sistem
        self.setWindowTitle("Sipariş Oluştur")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.result = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Ürün seçimi
        urun_label = QLabel("Ürün Seçin:")
        urun_label.setFont(QFont("Arial", 10))
        self.urun_combo = QComboBox()
        self.urun_combo.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        if self.sistem.urunler:
            for u in self.sistem.urunler:
                self.urun_combo.addItem(f"{u.ad} (Stok: {u.stok}, Fiyat: {u.fiyat} TL)", u.urun_id)
        else:
            self.urun_combo.addItem("Ürün yok", None)
            self.urun_combo.setEnabled(False)

        # Adet
        adet_label = QLabel("Adet:")
        adet_label.setFont(QFont("Arial", 10))
        self.adet_input = QSpinBox()
        self.adet_input.setMinimum(1)
        self.adet_input.setMaximum(1000000)
        self.adet_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Toplam Fiyat Etiketi
        self.toplam_label = QLabel("Toplam: 0.00 TL")
        self.toplam_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.toplam_label.setStyleSheet("color: #2196F3;")

        # Bağlantılar
        self.urun_combo.currentIndexChanged.connect(self.guncelle_toplam)
        self.adet_input.valueChanged.connect(self.guncelle_toplam)

        # Butonlar
        button_layout = QHBoxLayout()
        olustur_btn = QPushButton("✓ Sipariş Oluştur")
        olustur_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        olustur_btn.clicked.connect(self.olustur)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(olustur_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(urun_label)
        layout.addWidget(self.urun_combo)
        layout.addWidget(adet_label)
        layout.addWidget(self.adet_input)
        layout.addWidget(self.toplam_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def guncelle_toplam(self):
        try:
            urun_id = self.urun_combo.currentData()
            if urun_id:
                urun = self.sistem.urun_bul(urun_id)
                if urun:
                    toplam = urun.fiyat * self.adet_input.value()
                    self.toplam_label.setText(f"Toplam: {toplam:.2f} TL")
        except Exception as e:
            pass

    def olustur(self):
        try:
            urun_id = self.urun_combo.currentData()
            if not urun_id:
                QMessageBox.warning(self, "Hata", "Lütfen bir ürün seçin!")
                return

            urun = self.sistem.urun_bul(urun_id)
            if not urun:
                QMessageBox.warning(self, "Hata", "Ürün bulunamadı!")
                return

            adet = self.adet_input.value()
            if adet <= 0:
                QMessageBox.warning(self, "Hata", "Adet 0'dan büyük olmalı!")
                return

            if adet > urun.stok:
                QMessageBox.warning(self, "Hata", f"Yetersiz stok! Mevcut stok: {urun.stok}")
                return

            self.result = (urun_id, adet)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")


# ===================== GRAFIKLER =====================

class StatisticsWidget(QWidget):
    def __init__(self, sistem, parent=None):
        super().__init__(parent)
        self.sistem = sistem
        self.figure = Figure(figsize=(12, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_charts(self):
        try:
            self.figure.clear()

            # Stok Grafik
            ax1 = self.figure.add_subplot(121)
            if self.sistem.urunler:
                urun_adlari = [u.ad for u in self.sistem.urunler]
                stok_miktarlari = [u.stok for u in self.sistem.urunler]
                colors = ['#4CAF50', '#2196F3', '#FF9800', '#f44336', '#9C27B0', '#00BCD4']
                colors = colors * (len(urun_adlari) // len(colors) + 1)

                bars1 = ax1.bar(range(len(urun_adlari)), stok_miktarlari, color=colors[:len(urun_adlari)], edgecolor='black', linewidth=1.5)
                ax1.set_xticks(range(len(urun_adlari)))
                ax1.set_xticklabels(urun_adlari, rotation=45, ha='right')
                ax1.set_title('📦 Ürün Stok Dağılımı', fontsize=12, fontweight='bold')
                ax1.set_ylabel('Stok Miktarı', fontsize=10)

                for bar in bars1:
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}',
                            ha='center', va='bottom', fontweight='bold')
            else:
                ax1.text(0.5, 0.5, 'Ürün Yok', ha='center', va='center', fontsize=14)
                ax1.set_title('📦 Ürün Stok Dağılımı', fontsize=12, fontweight='bold')

            # Fiyat Grafik
            ax2 = self.figure.add_subplot(122)
            if self.sistem.urunler:
                urun_adlari = [u.ad for u in self.sistem.urunler]
                fiyatlar = [u.fiyat for u in self.sistem.urunler]
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
                colors = colors * (len(urun_adlari) // len(colors) + 1)

                bars2 = ax2.bar(range(len(urun_adlari)), fiyatlar, color=colors[:len(urun_adlari)], edgecolor='black', linewidth=1.5)
                ax2.set_xticks(range(len(urun_adlari)))
                ax2.set_xticklabels(urun_adlari, rotation=45, ha='right')
                ax2.set_title('💰 Ürün Fiyat Dağılımı', fontsize=12, fontweight='bold')
                ax2.set_ylabel('Fiyat (TL)', fontsize=10)

                for bar in bars2:
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:.2f} TL',
                            ha='center', va='bottom', fontweight='bold', fontsize=9)
            else:
                ax2.text(0.5, 0.5, 'Ürün Yok', ha='center', va='center', fontsize=14)
                ax2.set_title('💰 Ürün Fiyat Dağılımı', fontsize=12, fontweight='bold')

            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Grafik hatası: {str(e)}")


# ===================== MAIN WINDOW =====================

class DepoMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sistem = Sistem()
        self.setWindowTitle("📦 DEPO VE STOK YÖNETİM SİSTEMİ")
        self.setGeometry(0, 0, 1400, 800)
        self.setStyleSheet("background-color: #ffffff;")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # Başlık
        header = QLabel("📦 DEPO VE STOK YÖNETİM SİSTEMİ")
        header_font = QFont()
        header_font.setPointSize(20)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #4CAF50; padding: 20px;")

        # Dashboard
        dashboard_layout = QHBoxLayout()

        urun_card = self.create_stat_card("📦 Toplam Ürün", "0", "#4CAF50")
        stok_card = self.create_stat_card("📊 Stok Değeri", "0.00 TL", "#2196F3")
        siparis_card = self.create_stat_card("🛒 Sipariş Tutarı", "0.00 TL", "#FF9800")

        dashboard_layout.addWidget(urun_card)
        dashboard_layout.addWidget(stok_card)
        dashboard_layout.addWidget(siparis_card)

        self.urun_label = urun_card.findChild(QLabel, "value_label")
        self.stok_label = stok_card.findChild(QLabel, "value_label")
        self.siparis_label = siparis_card.findChild(QLabel, "value_label")

        # Sekme Penceresi
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)

        # Ürünler Sekmesi
        self.urun_tab = self.create_urun_tab()
        self.tabs.addTab(self.urun_tab, "📦 Ürünler")

        # Siparişler Sekmesi
        self.siparis_tab = self.create_siparis_tab()
        self.tabs.addTab(self.siparis_tab, "🛒 Siparişler")

        # Grafikler Sekmesi
        self.stats_widget = StatisticsWidget(self.sistem)
        self.tabs.addTab(self.stats_widget, "📊 Grafikler")

        main_layout.addWidget(header)
        main_layout.addLayout(dashboard_layout)
        main_layout.addWidget(self.tabs)

        central_widget.setLayout(main_layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_all)
        self.timer.start(500)

    def create_stat_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                padding: 20px;
                color: white;
            }}
        """)

        layout = QVBoxLayout()
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(18)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setObjectName("value_label")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)

        return card

    def create_urun_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("➕ Ürün Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.urun_ekle)

        arttir_btn = QPushButton("📈 Stok Arttır")
        arttir_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        arttir_btn.clicked.connect(self.stok_arttir)

        azalt_btn = QPushButton("📉 Stok Azalt")
        azalt_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        azalt_btn.clicked.connect(self.stok_azalt)

        sil_btn = QPushButton("🗑️ Ürün Sil")
        sil_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        sil_btn.clicked.connect(self.urun_sil)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        yenile_btn.clicked.connect(self.urunleri_goster)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(arttir_btn)
        button_layout.addWidget(azalt_btn)
        button_layout.addWidget(sil_btn)
        button_layout.addWidget(yenile_btn)

        # Tablo
        self.urun_table = QTableWidget()
        self.urun_table.setColumnCount(4)
        self.urun_table.setHorizontalHeaderLabels(["ID", "Ürün Adı", "Stok", "Fiyat (TL)"])
        self.urun_table.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")

        layout.addLayout(button_layout)
        layout.addWidget(self.urun_table)
        widget.setLayout(layout)

        return widget

    def create_siparis_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Butonlar
        button_layout = QHBoxLayout()
        olustur_btn = QPushButton("➕ Sipariş Oluştur")
        olustur_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        olustur_btn.clicked.connect(self.siparis_olustur)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        yenile_btn.clicked.connect(self.siparisleri_goster)

        button_layout.addWidget(olustur_btn)
        button_layout.addWidget(yenile_btn)

        # Tablo
        self.siparis_table = QTableWidget()
        self.siparis_table.setColumnCount(5)
        self.siparis_table.setHorizontalHeaderLabels(["ID", "Ürün Adı", "Adet", "Birim Fiyat", "Toplam (TL)"])
        self.siparis_table.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")

        layout.addLayout(button_layout)
        layout.addWidget(self.siparis_table)
        widget.setLayout(layout)

        return widget

    # ============ ÜRÜN METODLARI ==========

    def urun_ekle(self):
        try:
            dialog = UrunEkleDialog(self)
            if dialog.exec_() == QDialog.Accepted and dialog.result:
                ad, stok, fiyat = dialog.result
                self.sistem.urun_ekle(Urun(ad, stok, fiyat))
                QMessageBox.information(self, "Başarılı", "Ürün eklendi!")
                self.urunleri_goster()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ürün eklenirken hata oluştu: {str(e)}")

    def stok_arttir(self):
        try:
            row = self.urun_table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Hata", "Lütfen bir ürün seçin!")
                return

            urun_id = int(self.urun_table.item(row, 0).text())
            urun = self.sistem.urun_bul(urun_id)

            if not urun:
                QMessageBox.warning(self, "Hata", "Ürün bulunamadı!")
                return

            dialog = StokArttirDialog(urun, self)
            if dialog.exec_() == QDialog.Accepted and dialog.result:
                urun.stok_arttir(dialog.result)
                QMessageBox.information(self, "Başarılı", "Stok arttırıldı!")
                self.urunleri_goster()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Stok arttırılırken hata oluştu: {str(e)}")

    def stok_azalt(self):
        try:
            row = self.urun_table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Hata", "Lütfen bir ürün seçin!")
                return

            urun_id = int(self.urun_table.item(row, 0).text())
            urun = self.sistem.urun_bul(urun_id)

            if not urun:
                QMessageBox.warning(self, "Hata", "Ürün bulunamadı!")
                return

            dialog = StokAzaltDialog(urun, self)
            if dialog.exec_() == QDialog.Accepted and dialog.result:
                if urun.stok_azalt(dialog.result):
                    QMessageBox.information(self, "Başarılı", "Stok azaltıldı!")
                    self.urunleri_goster()
                else:
                    QMessageBox.warning(self, "Hata", "Yetersiz stok!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Stok azaltılırken hata oluştu: {str(e)}")

    def urun_sil(self):
        try:
            row = self.urun_table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Hata", "Lütfen bir ürün seçin!")
                return

            urun_id = int(self.urun_table.item(row, 0).text())
            urun = self.sistem.urun_bul(urun_id)

            if not urun:
                QMessageBox.warning(self, "Hata", "Ürün bulunamadı!")
                return

            reply = QMessageBox.question(self, "Onay", f"'{urun.ad}' silinsin mi?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.sistem.urun_sil(urun_id)
                QMessageBox.information(self, "Başarılı", "Ürün silindi!")
                self.urunleri_goster()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ürün silinirken hata oluştu: {str(e)}")

    def urunleri_goster(self):
        try:
            self.urun_table.setRowCount(0)
            for u in self.sistem.urunler:
                row = self.urun_table.rowCount()
                self.urun_table.insertRow(row)
                self.urun_table.setItem(row, 0, QTableWidgetItem(str(u.urun_id)))
                self.urun_table.setItem(row, 1, QTableWidgetItem(u.ad))
                self.urun_table.setItem(row, 2, QTableWidgetItem(str(u.stok)))
                self.urun_table.setItem(row, 3, QTableWidgetItem(f"{u.fiyat:.2f}"))
        except Exception as e:
            print(f"Ürünler gösterilirken hata: {str(e)}")

    # ============ SİPARİŞ METODLARI ==========

    def siparis_olustur(self):
        try:
            if not self.sistem.urunler:
                QMessageBox.warning(self, "Hata", "Önce ürün ekleyin!")
                return

            dialog = SiparisOlusturDialog(self.sistem, self)
            if dialog.exec_() == QDialog.Accepted and dialog.result:
                urun_id, adet = dialog.result
                urun = self.sistem.urun_bul(urun_id)

                if not urun:
                    QMessageBox.warning(self, "Hata", "Ürün bulunamadı!")
                    return

                siparis = Siparis(urun, adet)
                basarili, mesaj = siparis.siparis_olustur()

                if basarili:
                    self.sistem.siparis_ekle(siparis)
                    QMessageBox.information(self, "Başarılı", mesaj)
                    self.siparisleri_goster()
                    self.urunleri_goster()
                else:
                    QMessageBox.warning(self, "Hata", mesaj)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Sipariş oluşturulurken hata oluştu: {str(e)}")

    def siparisleri_goster(self):
        try:
            self.siparis_table.setRowCount(0)
            for s in self.sistem.siparisler:
                row = self.siparis_table.rowCount()
                self.siparis_table.insertRow(row)
                self.siparis_table.setItem(row, 0, QTableWidgetItem(str(s.siparis_id)))
                self.siparis_table.setItem(row, 1, QTableWidgetItem(s.urun.ad))
                self.siparis_table.setItem(row, 2, QTableWidgetItem(str(s.adet)))
                self.siparis_table.setItem(row, 3, QTableWidgetItem(f"{s.urun.fiyat:.2f}"))
                self.siparis_table.setItem(row, 4, QTableWidgetItem(f"{s.toplam_fiyat:.2f}"))
        except Exception as e:
            print(f"Siparişler gösterilirken hata: {str(e)}")

    # ============ REFRESH METODU ==========

    def refresh_all(self):
        try:
            self.urun_label.setText(str(len(self.sistem.urunler)))
            self.stok_label.setText(f"{self.sistem.toplam_stok_degeri():.2f} TL")
            self.siparis_label.setText(f"{self.sistem.toplam_siparis_tutari():.2f} TL")
            self.stats_widget.update_charts()
        except Exception as e:
            print(f"Yenileme hatası: {str(e)}")


# ===================== MAIN ==========

def main():
    try:
        app = QApplication(sys.argv)
        window = DepoMainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Uygulama başlatılırken hata: {str(e)}")


if __name__ == "__main__":
    main()
