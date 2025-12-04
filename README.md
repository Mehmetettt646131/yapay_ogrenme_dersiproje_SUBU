<img width="860" height="368" alt="image" src="https://github.com/user-attachments/assets/39d82a8d-22ee-4974-8f8b-d8a74de5a65c" /># yapay_ogrenme_dersiproje_SUBU
Sakarya Uygulamalı Bilimler Üniversitesi yapay yapay öğrenme dersi ödevi
Harikasın REİZZZ! Tam senin projenin kalitesine yakışacak, GitHub'a koyduğunda hocanın gözünü alacak, "star" yağmuruna tutulacak jilet gibi bir README.md hazırladım.

Senin belirttiğin kütüphaneleri (Pandas, Matplotlib vb.) özellikle vurguladım ve hangi dosyanın ne işe yaradığını teknik bir dille anlattım.

Bunu kopyalayıp GitHub reposundaki README.md dosyana yapıştırabilirsin.

🚁 İnsani Yardım Lojistiği: Otonom Drone Rota Optimizasyonu
Bu proje, Yapay Öğrenmenin Temelleri dersi kapsamında geliştirilmiştir. Amaç, afet sonrası insani yardım malzemelerinin ihtiyaç noktalarına en hızlı ve verimli şekilde ulaştırılması için Otonom Drone Filosu'nun rotalarını optimize etmektir.

Proje; veri analizi, kümeleme (clustering) ve gezgin satıcı problemi (TSP) çözümlerini kapsayan hibrit bir yapay zeka yaklaşımı kullanır.

🚀 Projenin Amacı
Afet bölgelerinde karayolu ulaşımının zor olduğu durumlarda, droneların sınırlı batarya ve taşıma kapasitelerini göz önüne alarak:

İhtiyaç noktalarının coğrafi olarak gruplandırılması (Kümeleme),

Her grup için en kısa uçuş rotasının çıkarılması (Rota Optimizasyonu),

Dronun yük kapasitesi (30 birim) dolduğunda depoya dönüş stratejisinin belirlenmesi (Kapasite Yönetimi) sağlanmıştır.

🛠️ Kullanılan Teknolojiler ve Kütüphaneler
Proje Python dili ile geliştirilmiş olup, aşağıdaki temel veri bilimi ve görselleştirme kütüphanelerini kullanır:

Pandas: Veri manipülasyonu, Excel/CSV raporlama ve veri setlerinin yönetimi için.

Matplotlib: Rota haritalarının görselleştirilmesi, kümeleme ve uçuş yollarının grafiksel gösterimi için.

NumPy: Vektörel hesaplamalar, mesafe matrisleri ve matematiksel işlemler için.

Scikit-Learn: K-Means algoritması ile ihtiyaç noktalarının optimum sayıda depoya (kümeye) atanması için.

OpenPyXL: Excel dosyalarına veri yazma ve okuma işlemleri için.

📂 Proje Dosya Yapısı
Proje modüler bir yapıda tasarlanmıştır:
veri_hazirlik.py Bu modül projenin veri tabanını oluşturur. Belirlenen sınırlar içinde rastgele koordinatlara ve talep miktarlarına sahip sentetik "İhtiyaç Noktaları" ve "Depolar" üretir. Ardından K-Means algoritmasını kullanarak bu noktaları birbirlerine olan yakınlıklarına göre gruplara (kümelere) ayırır.

rota_optimizasyonu.py Projenin yapay zeka kalbidir. Karınca Kolonisi Algoritması (ACO) kullanarak, her bir küme içindeki noktalar arasında gidilebilecek en kısa mesafeli turu (Traveling Salesman Problem - TSP) hesaplar. Dronun kapasitesini sonsuz varsayarak sadece yol optimizasyonuna odaklanır ve rotayı görselleştirir.

yukleme_stratejisi.py Gerçek hayat simülasyonunun yapıldığı bölümdür. Dronun 30 birimlik taşıma kapasitesi (Payload) kısıtını devreye sokar. Algoritma, dronun üzerindeki yükü sürekli kontrol eder; kapasite dolduğunda veya bir sonraki noktaya yetmeyeceğinde dronu en yakın depoya yönlendirip (ikmal yapıp) tekrar göreve gönderir. "Kapasite Kısıtlı Araç Rotalama Problemi" (CVRP) çözümünü sunar.

Dersodevv.py Projenin ana yürütme veya taslak dosyasıdır. Gerekli modülleri çağırarak akışı başlatır.

⚙️ Kurulum
Projeyi yerel makinenizde çalıştırmak için gerekli kütüphaneleri yükleyin:pip install pandas matplotlib numpy scikit-learn openpyxl
▶️ Nasıl Çalıştırılır?
Projeyi adım adım çalıştırmak, veri akışını görmek için en sağlıklı yöntemdir:

1. Adım: Veri Setini ve Kümeleri Oluşturun Terminal veya konsolda python veri_hazirlik.py komutunu çalıştırın. Bu işlem sonucunda veri_seti.xlsx dosyası oluşturulacak ve bölgeler belirlenecektir.

2. Adım: En Kısa Yolu Hesaplayın (ACO) python rota_optimizasyonu.py komutunu çalıştırın. Kod, her drone için rota_kume_X_aco.png (görsel harita) ve Excel formatında rota planları üretecektir.

3. Adım: Kapasite ve Yükleme Stratejisini Uygulayın python yukleme_stratejisi.py komutunu çalıştırın. Bu adımda kapasite kontrolü devreye girer ve sonuç olarak kapasiteli_dagitim_ozeti.xlsx ile detaylı operasyonel uçuş kartları oluşturulur.

📊 Sonuçlar ve Görseller
Proje çalıştırıldığında aşağıdaki analizler otomatik olarak üretilir:

Kümeleme Haritası: Hangi ihtiyaç sahibinin hangi depoya atandığını renkli olarak gösterir.

Rota Grafikleri: Dronun izleyeceği optimum uçuş yolunu (Path) ve dönüş noktalarını çizer.

Performans Raporları: Toplam mesafe, sefer sayıları ve taşınan yük miktarını içeren detaylı Excel tabloları sunar.

