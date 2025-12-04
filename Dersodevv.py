import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os

# --- 1. DOSYA YOLLARI ---
# Dosyalarin oldugu klasor
hedef_klasor = r"C:\Users\VICTUS\Desktop\depremodevvvvvv\Dersodevv"

print("Calisma Klasoru:", hedef_klasor)

# Koordinat dosyasini oku
dosya_yolu = os.path.join(hedef_klasor, 'koordinatlar.xlsx')

# Dosya kontrolu
if not os.path.exists(dosya_yolu):
    print("HATA: 'koordinatlar.xlsx' bulunamadi! Once veri_hazirlik.py dosyasini calistir.")
    exit()

# Veriyi Yukle
df = pd.read_excel(dosya_yolu)
print("Veriler yuklendi.")

# --- 2. K-MEANS KUMELEME ISLEMI ---
# [cite_start]Sadece 'Musteri' (Ihtiyac Noktasi) olanlari aliyoruz [cite: 22, 25]
musteriler = df[df['tip'] == 'Musteri'].copy()
koordinatlar = musteriler[['x', 'y']]

# 3 Depo oldugu icin 3 farkli kume olusturuyoruz
kmeans = KMeans(n_clusters=3, random_state=42)

# Her noktaya kume numarasi ata (0, 1 veya 2)
musteriler['kume_no'] = kmeans.fit_predict(koordinatlar)

# --- 3. SONUCLARI KAYDETME ---
depolar = df[df['tip'] == 'Depo'].copy()
depolar['kume_no'] = -1 

sonuc_df = pd.concat([depolar, musteriler])

# Excel'e yaz
kayit_yolu = os.path.join(hedef_klasor, 'kumelenmis_veri.xlsx')
sonuc_df.to_excel(kayit_yolu, index=False)
print("Kumeleme bitti! Sonuclar suraya kaydedildi:", kayit_yolu)

# [cite_start]--- 4. GORSELLESTIRME (HARITA CIZIMI) [cite: 44] ---
plt.figure(figsize=(10, 8))

renkler = ['red', 'green', 'blue']
bolge_isimleri = ['1. Bolge', '2. Bolge', '3. Bolge']

# Kumeleri Ciz
for i in range(3):
    bolge = musteriler[musteriler['kume_no'] == i]
    plt.scatter(bolge['x'], bolge['y'], s=50, c=renkler[i], label=bolge_isimleri[i], alpha=0.7)

# Depolari Ciz (Siyah Kare)
plt.scatter(depolar['x'], depolar['y'], s=200, c='black', marker='s', label='Depolar (Merkez)')

# Grafik Ayarlari
plt.title('Deprem Yardim Dagitim Bolgeleri (K-Means Sonucu)')
plt.xlabel('X Koordinati (km)')
plt.ylabel('Y Koordinati (km)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

# Haritayi Kaydet
resim_yolu = os.path.join(hedef_klasor, 'kumeleme_haritasi.png')
plt.savefig(resim_yolu)
print("Harita resmi olusturuldu:", resim_yolu)

# Ekranda Goster
plt.show()