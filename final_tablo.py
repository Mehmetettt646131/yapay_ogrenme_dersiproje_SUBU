import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
from datetime import datetime

# Dosya adi (calisma dizininde aranir)
INPUT_XLSX = "kapasiteli_dagitim_ozeti.xlsx"

print("Aranan dosya:", INPUT_XLSX)

if not os.path.exists(INPUT_XLSX):
    print("\nHATA: input dosyasi bulunamadi:", INPUT_XLSX)
    print("Lutfen once 'yukleme_stratejisi.py' ile Excel olusturun.")
    sys.exit(1)

# Excel oku (ilk sayfa)
try:
    df = pd.read_excel(INPUT_XLSX)
except Exception as e:
    print("Excel okuma hatasi:", repr(e))
    sys.exit(1)

# Beklenen en az 4 sutun var mi kontrolu
if df.shape[1] < 4:
    print("UYARI: Excel dosyasinda en az 4 sutun bekleniyor.")
    print("Mevcut sutun sayisi:", df.shape[1])
    print("Ilk satirlar:")
    print(df.head().to_string(index=False))
    sys.exit(1)

# Ilk 4 sutunu kullan ve ASCII uyumlu isimlendir
df = df.iloc[:, :4].copy()
df.columns = ["Bolge", "Top_Talep", "Sefer_Sayisi", "Top_Mesafe"]

# Sayisal sutunlari numeric'e cevir (gerekirse)
for c in ["Top_Talep", "Sefer_Sayisi", "Top_Mesafe"]:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

# Konsolda ozeti yaz
print("\n=== OZET TABLO ===")
print(df.to_string(index=False))
print("==================\n")

# Genel toplamlar
total_bolge = df["Bolge"].nunique()
total_talep = int(df["Top_Talep"].sum())
total_sefer = int(df["Sefer_Sayisi"].sum())
total_mesafe = float(df["Top_Mesafe"].sum())

summary_df = pd.DataFrame([{
    "Toplam_Bolge": total_bolge,
    "Toplam_Talep": total_talep,
    "Toplam_Sefer": total_sefer,
    "Toplam_Mesafe": total_mesafe
}])

print("=== GENEL OZET ===")
print(summary_df.to_string(index=False))
print("==================\n")

# Gorsel tablo olusturma
rows = len(df)
fig_h = 2.5 + 0.4 * rows
fig, ax = plt.subplots(figsize=(10, fig_h))
ax.axis("off")

table = ax.table(cellText=df.values,
                 colLabels=df.columns,
                 cellLoc="center",
                 loc="center")

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.4)

header_color = "#2c3e50"
row_colors = ["#ecf0f1", "white"]
edge_color = "#bdc3c7"

for (r, c), cell in table.get_celld().items():
    cell.set_edgecolor(edge_color)
    if r == 0:
        cell.set_facecolor(header_color)
        cell.set_text_props(weight="bold", color="white")
        cell.set_height(0.18)
    else:
        cell.set_facecolor(row_colors[(r - 1) % len(row_colors)])
        cell.set_text_props(color="black")
        cell.set_height(0.14)

plt.title("Insani Yardim Dagitim - Operasyonel Ozet", fontsize=14, weight="bold", color="#34495e", pad=10)

# Zaman damgali cikti isimleri
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
png_name = f"proje_ozet_tablosu_{ts}.png"
xlsx_name = f"proje_ozet_tablosu_{ts}.xlsx"
summary_xlsx = f"proje_ozet_genel_{ts}.xlsx"

# Kaydet
plt.savefig(png_name, dpi=300, bbox_inches="tight")
print("Tablo resmi kaydedildi:", os.path.abspath(png_name))

try:
    df.to_excel(xlsx_name, index=False)
    print("Tablo Excel olarak kaydedildi:", os.path.abspath(xlsx_name))
except Exception as e:
    print("Excel kaydetme hatasi:", repr(e))

try:
    summary_df.to_excel(summary_xlsx, index=False)
    print("Genel ozet kaydedildi:", os.path.abspath(summary_xlsx))
except Exception as e:
    print("Genel ozet kaydetme hatasi:", repr(e))

plt.show()