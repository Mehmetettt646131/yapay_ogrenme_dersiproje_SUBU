import os
import sys
import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Sadece ACO uygulanacak versiyon — tek seçim yapıldı.
hedef_klasor = r"C:\Users\VICTUS\Desktop\depremodevvvvvv\Dersodevv"
print("Çalışma klasörü:", hedef_klasor)

dosya_yolu = os.path.join(hedef_klasor, 'koordinatlar.xlsx')
if not os.path.exists(dosya_yolu):
    print("HATA: 'koordinatlar.xlsx' bulunamadı. Önce veri_hazirlik.py çalıştır.")
    sys.exit(1)

# Parametreler (isteğe göre ayarlanabilir)
KUME_SAYISI = 3
ACO_ANTS = 40
ACO_ITER = 120
ALPHA = 1.0   # pheromone etkisi
BETA = 6.0    # heuristic etkisi (1/distance)
RHO = 0.15    # buharlaşma oranı
Q = 1.0       # depozit miktarı

# Veri yükle ve kümelendir
df = pd.read_excel(dosya_yolu)
musteriler = df[df['tip'] == 'Musteri'].copy()
koordinatlar = musteriler[['x', 'y']].astype(float)
kmeans = KMeans(n_clusters=KUME_SAYISI, random_state=42)
musteriler['kume_no'] = kmeans.fit_predict(koordinatlar)
depolar = df[df['tip'] == 'Depo'].copy()

def euclid(a, b):
    return math.hypot(a['x'] - b['x'], a['y'] - b['y'])

def build_distance_matrix(nodes_df):
    idx = list(nodes_df.index)
    n = len(idx)
    dist = pd.DataFrame(np.zeros((n, n)), index=idx, columns=idx)
    for i in idx:
        for j in idx:
            if i == j:
                dist.loc[i, j] = 0.0
            else:
                dist.loc[i, j] = euclid(nodes_df.loc[i], nodes_df.loc[j])
    return dist

def aco_tsp(start_idx, nodes_df, n_ants=ACO_ANTS, n_iter=ACO_ITER,
            alpha=ALPHA, beta=BETA, rho=RHO, q=Q):
    """
    Basit ACO ile TSP benzeri tur bulma.
    nodes_df: index'leri route id olacak (depo dahil)
    start_idx: başlangıç (depo) index'i (mutlaka nodes_df içinde olmalı)
    Döner: (best_tour_list, best_length)
    """
    idx = list(nodes_df.index)
    if start_idx not in idx:
        raise ValueError("start_idx nodes_df içinde değil")
    dist = build_distance_matrix(nodes_df)
    n = len(idx)
    # Başlangıç pheromone
    tau = pd.DataFrame(np.ones((n, n)), index=idx, columns=idx)
    best_tour = None
    best_len = float('inf')

    for iteration in range(n_iter):
        all_tours = []
        for ant in range(n_ants):
            unvisited = set(idx)
            current = start_idx
            tour = [current]
            unvisited.discard(current)
            while unvisited:
                # olasılıkları hesapla
                probs = []
                denom = 0.0
                for j in unvisited:
                    t = tau.loc[current, j] ** alpha
                    heur = (1.0 / (dist.loc[current, j] + 1e-9)) ** beta
                    val = t * heur
                    probs.append((j, val))
                    denom += val
                if denom == 0:
                    nxt = random.choice(list(unvisited))
                else:
                    r = random.random()
                    acc = 0.0
                    nxt = probs[-1][0]
                    for j, val in probs:
                        acc += val / denom
                        if r <= acc:
                            nxt = j
                            break
                tour.append(nxt)
                unvisited.discard(nxt)
                current = nxt
            # turun uzunluğunu hesapla (tur bitip başlangıca döner)
            length = 0.0
            for a, b in zip(tour[:-1], tour[1:]):
                length += dist.loc[a, b]
            length += dist.loc[tour[-1], start_idx]
            all_tours.append((tour, length))
            if length < best_len:
                best_len = length
                best_tour = tour.copy()
        # pheromone güncellemesi
        tau *= (1 - rho)
        for tour, length in all_tours:
            deposit = q / (length + 1e-9)
            for a, b in zip(tour[:-1], tour[1:]):
                tau.loc[a, b] += deposit
                tau.loc[b, a] += deposit
            # dönüş kenarı
            tau.loc[tour[-1], start_idx] += deposit
            tau.loc[start_idx, tour[-1]] += deposit
    return best_tour, best_len

summary = []
for k in sorted(musteriler['kume_no'].unique()):
    cluster_df = musteriler[musteriler['kume_no'] == k].copy()
    if cluster_df.empty:
        continue
    centroid = {'x': cluster_df['x'].mean(), 'y': cluster_df['y'].mean()}
    nearest_depo_idx = depolar.apply(lambda r: euclid(r, centroid), axis=1).idxmin()
    start_idx = nearest_depo_idx
    # nodes_df: depo + müşteriler (index korunur)
    nodes_df = pd.concat([depolar.loc[[nearest_depo_idx]], cluster_df])
    nodes_df[['x','y']] = nodes_df[['x','y']].astype(float)
    print(f"\nKüme {k}: başlangıç depo: {start_idx}, müşteri sayısı: {len(cluster_df)}")

    # ACO ile rota
    best_tour, best_len = aco_tsp(start_idx, nodes_df)
    if best_tour is None:
        print("ACO sonuç vermedi, greedy fallback uygulanıyor.")
        # basit greedy fallback
        unv = set(nodes_df.index)
        cur = start_idx
        tour = [cur]
        unv.discard(cur)
        while unv:
            nxt = min(unv, key=lambda nid: euclid(nodes_df.loc[cur], nodes_df.loc[nid]))
            tour.append(nxt); unv.discard(nxt); cur = nxt
        best_tour = tour
        best_len = sum(euclid(nodes_df.loc[a], nodes_df.loc[b]) for a,b in zip(best_tour[:-1], best_tour[1:])) + euclid(nodes_df.loc[best_tour[-1]], nodes_df.loc[start_idx])

    route_with_return = best_tour + [start_idx]
    print(f"Rota bulundu. Toplam mesafe: {best_len:.2f}")

    # rota DataFrame ve kaydetme
    rota_list = []
    order = 0
    for nid in route_with_return:
        row = nodes_df.loc[nid]
        rota_list.append({'order': order, 'id': str(nid), 'x': row['x'], 'y': row['y']})
        order += 1
    rota_df = pd.DataFrame(rota_list)
    rota_path = os.path.join(hedef_klasor, f'rota_kume_{k}_aco.xlsx')
    rota_df.to_excel(rota_path, index=False)
    print("Rota kaydedildi:", rota_path)

    # grafik
    plt.figure(figsize=(7,6))
    plt.scatter(cluster_df['x'], cluster_df['y'], c='tab:orange', label='Müşteri', s=40)
    dp = depolar.loc[nearest_depo_idx]
    plt.scatter([dp['x']], [dp['y']], c='black', marker='s', s=150, label='Depo')
    xs = [nodes_df.loc[i]['x'] for i in route_with_return]
    ys = [nodes_df.loc[i]['y'] for i in route_with_return]
    plt.plot(xs, ys, '-o', color='tab:blue')
    plt.title(f'Küme {k} Rota (ACO)')
    plt.xlabel('x'); plt.ylabel('y'); plt.grid(alpha=0.4); plt.legend()
    fig_path = os.path.join(hedef_klasor, f'rota_kume_{k}_aco.png')
    plt.savefig(fig_path, dpi=150)
    plt.close()
    print("Rota grafik kaydedildi:", fig_path)

    summary.append({'kume': k, 'depo': str(nearest_depo_idx), 'n_musteri': len(cluster_df), 'metod': 'ACO', 'toplam_mesafe': round(best_len, 2)})

# özet kaydet
summary_df = pd.DataFrame(summary)
summary_path = os.path.join(hedef_klasor, 'rota_ozeti_aco.xlsx')
summary_df.to_excel(summary_path, index=False)
print("\nİşlem tamam. Özet kaydedildi:", summary_path)