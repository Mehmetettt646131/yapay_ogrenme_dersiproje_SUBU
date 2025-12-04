import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os
import math
import sys

# --- 1. AYARLAR ---
# Klasor yolu
target_folder = r"C:\Users\VICTUS\Desktop\depremodevvvvvv\Dersodevv"
MAX_CAPACITY = 30  # Drone kapasitesi

print("Calisma Klasoru:", target_folder)

# Dosya yollari
coord_file = os.path.join(target_folder, 'koordinatlar.xlsx')
demand_file = os.path.join(target_folder, 'talepler.xlsx')

# Dosya kontrolu
if not os.path.exists(coord_file) or not os.path.exists(demand_file):
    print("HATA: Excel dosyalari bulunamadi!")
    print("Lutfen once veri_hazirlik.py dosyasini calistir.")
    sys.exit()

# Verileri Yukle
df_coords = pd.read_excel(coord_file)
df_demands = pd.read_excel(demand_file)

print("Veriler yuklendi. Kapasite hesaplamasi basliyor...")

# --- 2. VERI BIRLESTIRME ---
customers = df_coords[df_coords['tip'] == 'Musteri'].copy()

# Talepler dosyasindaki Nokta_ID ile Koordinatlardaki id eslesmeli
customers = pd.merge(customers, df_demands, left_on='id', right_on='Nokta_ID', how='left')

# Toplam Talep (Tibbi + Yiyecek)
customers['Total_Demand'] = customers['Tibbi_Malzeme'] + customers['Yiyecek']
customers['Total_Demand'] = customers['Total_Demand'].fillna(0)

depots = df_coords[df_coords['tip'] == 'Depo'].copy()

# --- 3. K-MEANS KUMELEME ---
coords_xy = customers[['x', 'y']]
kmeans = KMeans(n_clusters=3, random_state=42)
customers['cluster_no'] = kmeans.fit_predict(coords_xy)

# --- 4. KAPASITELI ROTA ALGORITMASI (Core Logic) ---
def calculate_capacity_route(start_node, customer_df, max_cap):
    # Baslangic (Depo)
    route_coords_x = [start_node.iloc[0]['x']]
    route_coords_y = [start_node.iloc[0]['y']]
    route_ids = [start_node.index[0]] # Depo ID
    
    current_load = 0
    current_pos = start_node
    
    unvisited = customer_df.copy()
    
    depot_x = start_node.iloc[0]['x']
    depot_y = start_node.iloc[0]['y']
    depot_id = start_node.index[0]
    
    trips = 0 # Kac sefer yapti
    
    while len(unvisited) > 0:
        # Mevcut konumdan en yakin musteriyi bul
        dists = np.sqrt(((unvisited[['x', 'y']] - current_pos[['x', 'y']].iloc[0])**2).sum(axis=1))
        nearest_idx = dists.idxmin()
        nearest_node = unvisited.loc[nearest_idx]
        
        demand = nearest_node['Total_Demand']
        
        # --- KAPASITE KONTROLU ---
        # Eger mevcut yuk + yeni talep kapasiteyi asiyorsa -> DEPOYA DON
        if current_load + demand > max_cap:
            # Depoya git
            route_coords_x.append(depot_x)
            route_coords_y.append(depot_y)
            route_ids.append(depot_id)
            
            # Yuku bosalt
            current_load = 0
            trips += 1
            
            # Konumu depo yap
            current_pos = start_node
            
            # Dongu devam eder, bu musteriye bir sonraki turda depodan gidilecek
            continue
            
        # Kapasite yetiyorsa -> MUSTERIYE GIT
        route_coords_x.append(nearest_node['x'])
        route_coords_y.append(nearest_node['y'])
        route_ids.append(nearest_idx)
        
        current_load += demand
        current_pos = pd.DataFrame([nearest_node]) 
        
        # Listeden sil
        unvisited = unvisited.drop(nearest_idx)
        
    # Tum musteriler bitti, Depoya Don
    route_coords_x.append(depot_x)
    route_coords_y.append(depot_y)
    route_ids.append(depot_id)
    
    return route_coords_x, route_coords_y, route_ids, trips

# --- 5. CIZIM VE RAPORLAMA ---
plt.figure(figsize=(15, 6))
colors = ['red', 'green', 'blue']

summary_data = []

for i in range(3):
    cluster_data = customers[customers['cluster_no'] == i].copy()
    
    # En yakin depoyu sec
    center = cluster_data[['x', 'y']].mean()
    dists_to_depot = np.sqrt(((depots[['x', 'y']] - center)**2).sum(axis=1))
    selected_depot = depots.loc[[dists_to_depot.idxmin()]]
    
    # Algoritmayi Calistir
    rx, ry, r_ids, n_trips = calculate_capacity_route(selected_depot, cluster_data, MAX_CAPACITY)
    
    # Cizim
    plt.subplot(1, 3, i+1)
    plt.scatter(cluster_data['x'], cluster_data['y'], s=50, c=colors[i], label='Musteri')
    plt.scatter(selected_depot['x'], selected_depot['y'], s=200, c='black', marker='s', label='Depo')
    plt.plot(rx, ry, c=colors[i], linestyle='-', linewidth=1.5, alpha=0.7)
    
    plt.title(f"Bolge {i+1} (Kapasite Kontrollu)\nSefer Sayisi: {n_trips}")
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Excel Kayitlari
    route_rows = []
    for step, rid in enumerate(r_ids):
        if rid in depots.index:
            row = depots.loc[rid]
            tip = "DEPO (Dolum)"
            yuk = 0
        else:
            row = customers.loc[rid]
            tip = "Musteri"
            yuk = row['Total_Demand']
            
        route_rows.append({
            'Adim': step, 
            'ID': str(rid), 
            'Tip': tip, 
            'Talep': yuk,
            'X': float(row['x']), 
            'Y': float(row['y'])
        })
        
    df_route = pd.DataFrame(route_rows)
    excel_name = f'kapasiteli_rota_bolge_{i+1}.xlsx'
    df_route.to_excel(os.path.join(target_folder, excel_name), index=False)
    print(f"OK: {excel_name} olusturuldu.")
    
    summary_data.append({
        'Bolge': i+1,
        'Depo_ID': str(selected_depot.index[0]),
        'Musteri_Sayisi': len(cluster_data),
        'Toplam_Talep': cluster_data['Total_Demand'].sum(),
        'Sefer_Sayisi': n_trips
    })

plt.tight_layout()

# Grafik Kaydet
img_path = os.path.join(target_folder, 'kapasiteli_dagitim_grafigi.png')
plt.savefig(img_path, dpi=150)
print(f"Grafik kaydedildi: {img_path}")

# Ozet Rapor Kaydet
df_summary = pd.DataFrame(summary_data)
summary_path = os.path.join(target_folder, 'kapasiteli_dagitim_ozeti.xlsx')
df_summary.to_excel(summary_path, index=False)
print(f"Ozet rapor kaydedildi: {summary_path}")

print("-----------------------------------------")
print("ISLEM BASARIYLA TAMAMLANDI!")
print("-----------------------------------------")

plt.show()
