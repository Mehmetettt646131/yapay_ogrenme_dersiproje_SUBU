import os
import sys
import pandas as pd
import numpy as np
import random

# openpyxl kontrolü (pandas .xlsx için kullanır)
try:
    import openpyxl  # noqa: F401
except ImportError:
    print("UYARI: openpyxl yüklü değil. Yüklemek için: pip install openpyxl")

# Hedef klasör — masaüstündeki depremodevvvvvv içindeki Dersodevv
target_dir = r"C:\Users\VICTUS\Desktop\depremodevvvvvv\Dersodevv"
os.makedirs(target_dir, exist_ok=True)
print("Dosyalar bu klasöre yazılacak:", target_dir)

# --- PROJE AYARLARI ---
nokta_sayisi = 45
depo_sayisi = 3
toplam_konum = nokta_sayisi + depo_sayisi

# --- 1. ADIM: SANAL KOORDINATLAR URETME ---
koordinatlar = {
    'id': [f'Depo_{i+1}' for i in range(depo_sayisi)] + [f'Nokta_{i+1}' for i in range(nokta_sayisi)],
    'x': [random.randint(0, 100) for _ in range(toplam_konum)],
    'y': [random.randint(0, 100) for _ in range(toplam_konum)],
    'tip': ['Depo'] * depo_sayisi + ['Musteri'] * nokta_sayisi
}
df_konum = pd.DataFrame(koordinatlar)

def safe_to_excel(df, filename, index=False):
    path = os.path.join(target_dir, filename)
    try:
        df.to_excel(path, index=index)
        print(f"OK: '{filename}' oluşturuldu -> {path}")
    except Exception as e:
        print(f"HATA: '{filename}' oluşturulamadı. Yol: {path}")
        print("İstisna:", repr(e))

# Kaydetme
safe_to_excel(df_konum, 'koordinatlar.xlsx', index=False)

# --- 2. ADIM: IHTIYAC NOKTALARI MESAFELERI DOSYASI ---
mesafeler = np.zeros((toplam_konum, toplam_konum))
for i in range(toplam_konum):
    for j in range(toplam_konum):
        x1, y1 = df_konum.iloc[i]['x'], df_konum.iloc[i]['y']
        x2, y2 = df_konum.iloc[j]['x'], df_konum.iloc[j]['y']
        dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        mesafeler[i][j] = round(dist, 2)

df_mesafeler = pd.DataFrame(mesafeler, index=df_konum['id'], columns=df_konum['id'])
safe_to_excel(df_mesafeler, 'mesafeler.xlsx', index=True)

# --- 3. ADIM: YARDIM TALEP DOSYASI ---
talepler = {
    'Nokta_ID': [f'Nokta_{i+1}' for i in range(nokta_sayisi)],
    'Tibbi_Malzeme': [random.randint(1, 10) for _ in range(nokta_sayisi)],
    'Yiyecek': [random.randint(1, 15) for _ in range(nokta_sayisi)]
}
df_talepler = pd.DataFrame(talepler)
safe_to_excel(df_talepler, 'talepler.xlsx', index=False)

print("\nISLEM TAMAM! Hedef klasörü açıp dosyaların oluştuğunu kontrol et.")