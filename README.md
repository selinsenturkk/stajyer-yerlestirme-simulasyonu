# stajyer-yerlestirme-simulasyonu

[cite_start]Bu proje, **Python Programlama** dersi kapsamında geliştirilmiş; kısıtlı kaynakların (staj kontenjanları) yoğun talep altındaki birimlere (öğrenciler) atanması problemini (**Resource Constrained Assignment Problem**) çözen kapsamlı bir simülasyon uygulamasıdır[cite: 9].

[cite_start]Sistem, sadece akademik başarıyı değil, **"Toplam Mutluluk Skoru"nu (Global Happiness Score)** maksimize etmeyi hedeflerken; gerçek hayattaki **reddedilme** ve **mülakat uyumsuzluğu** senaryolarını da simüle eder[cite: 11, 15].

## Projenin Amacı ve Kapsamı

Gerçek hayatta firmaların kapasiteleri sınırlıdır ve öğrencilerin tercihleri genellikle popüler firmalarda çakışır. Bu proje, bu kaotik süreci yönetmek için **3 farklı algoritma** geliştirerek performanslarını karşılaştırır.

Simülasyonun temel özellikleri şunlardır:
* **Stokastik Reddetme Mekanizması:** Firmalar, popülaritelerine göre belirli olasılıklarla öğrencileri reddedebilir. [cite_start]Bu süreçte **Simulated Annealing** (Tavlama Benzetimi) yaklaşımından esinlenen bir "soğuma takvimi" kullanılır[cite: 131, 132].
* [cite_start]**Döngüsel (Iterative) Simülasyon:** Yerleştirme tek seferde olmaz; reddedilen öğrenciler havuza döner ve sistem kararlı hale (stable state) gelene kadar döngü devam eder[cite: 119].
* [cite_start]**Sentetik Veri Üretimi:** 130 öğrenci ve 40 firma (Trendyol, Aselsan vb. temsili) içeren gerçekçi bir veri seti, `dataset_hazirlayici.py` modülü ile akademik gerçekliğe uygun (GNO 1.50-4.00 arası) üretilir[cite: 20, 26, 30].

---

## ⚙️ Kullanılan Algoritmalar

Projede, çözüm uzayını taramak ve optimum eşleşmeyi bulmak için üç farklı yaklaşım geliştirilmiştir:

### 1. Açgözlü Yaklaşım (Greedy Algorithm)
*"Bireysel Liyakat Önceliği"*

[cite_start]Bu algoritma, deterministik bir yaklaşımla öğrencileri **Genel Not Ortalamasına (GNO)** göre büyükten küçüğe sıralar[cite: 68].
* **Mantık:** En başarılı öğrenci, tercih listesindeki en üst sıradaki boş firmaya yerleşir.
* [cite_start]**Karmaşıklık:** $O(N \log N)$ (Sıralama maliyeti)[cite: 75].
* **Sonuç:** Hızlıdır ancak "toplam mutluluğu" garanti etmez, sadece yüksek puanlıları mutlu eder.

### 2. Puan Bazlı Sezgisel (Scoring Heuristic)
*"Hibrit Karar Mekanizması"*

[cite_start]Bu yöntem, problemi sadece GNO değil, öğrencinin isteğini de katan çok boyutlu bir optimizasyon olarak ele alır[cite: 199]. Her eşleşme için bir **"Uygunluk Skoru"** hesaplar:

$$S_{i,j} = (\alpha \times GNO_{i}) + (\beta - \gamma \times Rank_{i,j})$$

* **Mantık:** Öğrencinin tercih listesinde aşağı inmesi ceza puanı oluşturur. [cite_start]Bu algoritma, "Çok İsteyen" öğrencilere, "Puanı Biraz Yüksek Olan" öğrencilere karşı stratejik avantaj sağlar[cite: 204, 207].
* **Avantaj:** Akademik başarı ile bireysel tatmin arasında denge kurar.

### 3. Yerel Arama (Local Search - Hill Climbing)
*"İleri Optimizasyon"*

[cite_start]Rastgele bir başlangıç çözümünü, **takas (swap)** işlemleriyle adım adım iyileştiren sezgisel yöntemdir[cite: 270].
* **Mantık:** Rastgele iki öğrenci seçilir ve firmaları değiştirilir. [cite_start]Eğer yeni durumdaki **Toplam Mutluluk Skoru** artıyorsa değişiklik kabul edilir, artmıyorsa geri alınır[cite: 280, 285].
* [cite_start]**Durdurma Kriteri:** "Sabır" (Patience) mekanizması ile 400 iterasyon boyunca iyileşme olmazsa algoritma durur[cite: 293].
* [cite_start]**Performans:** Deneylerde **10.750 puan** ile en yüksek skoru ve kararlılığı bu algoritma sağlamıştır[cite: 358].

---

## Mutluluk Skoru (Metric)

[cite_start]Algoritmaların başarısı aşağıdaki puanlama sistemine göre ölçülür[cite: 58, 57]:

| Durum | Puan Etkisi |
| :--- | :--- |
| **1. Tercihe Yerleşme** | +100 Puan |
| **2. Tercihe Yerleşme** | +85 Puan |
| **3. Tercihe Yerleşme** | +70 Puan |
| **4. Tercihe Yerleşme** | +55 Puan |
| **5. Tercihe Yerleşme** | +40 Puan |
| **Tercih Dışı Yerleşme** | +10 Puan |
| **Açıkta Kalma (Ceza)** | **-500 Puan** |

---

## Arayüz ve Teknik Detaylar

Uygulama, kullanıcı dostu bir deneyim için **Python Tkinter** kütüphanesi ile geliştirilmiştir.

* [cite_start]**Multi-Threading:** Arayüzün donmasını engellemek için hesaplama işlemleri arka planda (worker threads) çalıştırılır[cite: 375].
* [cite_start]**Log Terminali:** Kullanıcı, algoritmaların adımlarını (yerleşen sayısı, reddedilen sayısı, tur döngüleri) anlık olarak kaydırılabilir terminalden izleyebilir[cite: 374].
* [cite_start]**Veri Yönetimi:** Sonuçlar ve öğrenci verileri JSON formatında tutularak simülasyonlar arası veri bütünlüğü sağlanır[cite: 39].

## Ekran Görüntüleri

| Kontrol Paneli | Sonuç Karşılaştırma |
| :---: | :---: |
| *Simülasyon ayarları ve başlatma butonları* | *Algoritmaların süre ve skor karşılaştırması* |

*(Not: Buraya rapordaki ekran görüntülerini ekleyebilirsiniz.)*

## Takım Üyeleri

[cite_start]Bu proje aşağıdaki ekip tarafından geliştirilmiştir[cite: 2, 3, 4]:

* **Selin Şentürk**
* **Pınar Nida Tunca**
* **Selen Yakın**

---
*Bu proje akademik amaçla hazırlanmış olup, İMEP staj süreçlerine algoritmik bir bakış açısı getirmeyi amaçlamaktadır.*
