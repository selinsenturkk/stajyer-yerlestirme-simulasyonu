"""
Scoring-based (Puanlama tabanlı) heuristiği yaparken asıl amacın: GNO’su düşük olsa bile,
bir firmayı çok isteyen (1. sıraya yazan) öğrenciyi, o firmayı 5. sıraya yazan yüksek GNO'lu
öğrencinin önüne geçirebilecek bir "Karma Puan" (Hybrid Score) sistemi kurmaktır.
"""
from simulation.rejection import reject_students  # Red fonksiyonunu çağırıyoruz

def apply_scoring_heuristic(ogrenciler, firmalar):
    tur_sayisi = 1
    maksimum_tur = 10  # Sonsuz döngüden kaçınmak için bir limit belirledik.

    print(f"\n>>> [SCORING HEURISTIC] Yerleştirme Başlatılıyor ...")

    while tur_sayisi <= maksimum_tur:
        print(f"\n--- TUR {tur_sayisi} BAŞLIYOR ---")

        # AÇIKTA KALANLARI BELİRLE
        yerlesmemis_ogrenciler = [ogr for ogr in ogrenciler if not ogr.is_placed]

        if not yerlesmemis_ogrenciler:       #Yerleşmemiş öğrenci kalmadıysa döngüden çıkabiliriz.
            print("-> [BİLGİ] Tüm öğrenciler yerleşti! Döngü sonlanıyor.")
            break

        print(f">>> [ADIM 1] {len(yerlesmemis_ogrenciler)} öğrenci için hibrit puanlar hesaplanıyor...")

        # PUANLAMA
        olasi_eslesmeler = []

        for ogrenci in yerlesmemis_ogrenciler:
            for tercih_sirasi, firma_adi in enumerate(ogrenci.preferences, 1): #1.X Firması ,2.Y Firması.... diye numaralandırarak alıyoruz.
                # Formül: (GNO * 10) + (60 - Tercih Sırası * 10)
                tercih_bonusu = 60 - (tercih_sirasi * 10)  #1. tercih =50, 2.tercih=40... şeklinde tercih sırasına göre bir tercih bonusu alıyorlar.
                eslesme_puani = (ogrenci.gpa * 10) + tercih_bonusu

                olasi_eslesmeler.append({
                    'ogrenci': ogrenci,
                    'hedef_firma': firma_adi,
                    'puan': eslesme_puani,
                    'sira': tercih_sirasi
                })

        print(f">>> [ADIM 2] {len(olasi_eslesmeler)} olası eşleşme kombinasyonu oluşturuldu.")

        # SIRALAMA
        olasi_eslesmeler.sort(key=lambda x: x['puan'], reverse=True)

        # En iyi öğrencinin bilgilerine bak
        if tur_sayisi == 1 and olasi_eslesmeler:
            en_iyi = olasi_eslesmeler[0]
            print(
                f"    -> Örnek En Yüksek Skor: {en_iyi['ogrenci'].name} | {en_iyi['hedef_firma']} | Skor: {en_iyi['puan']:.2f}")

        # YERLEŞTİRME
        print(">>> [ADIM 3] Sıralı liste üzerinden yerleştirme yapılıyor...")

        bu_tur_yerlesen_sayisi = 0

        # Puan sırasına göre (Yüksekten Düşüğe) dizilmiş aday listesini geziyoruz.
        # Bu, "En yüksek puanlı (en hak eden) adaya öncelik ver" demektir (Greedy Mantığı).
        for eslesme in olasi_eslesmeler:
            aday_ogrenci = eslesme['ogrenci']
            aranan_firma_adi = eslesme['hedef_firma']

            if aday_ogrenci.is_placed:
                continue

            # Hedef firmayı bul
            bulunan_firma_nesnesi = None

            for firma in firmalar:
                # Veri setindeki görünmez boşluk hatalarını .strip() temizler.(Örn: "Trendyol " vs "Trendyol")
                if firma.name.strip() == aranan_firma_adi.strip():
                    bulunan_firma_nesnesi = firma
                    break

            if bulunan_firma_nesnesi and bulunan_firma_nesnesi.remaining_capacity > 0:
                bulunan_firma_nesnesi.interns.append(aday_ogrenci)
                # Öğrenci bilgilerini güncelle
                aday_ogrenci.is_placed = True
                aday_ogrenci.assigned_firm = bulunan_firma_nesnesi.name
                aday_ogrenci.choice_rank = eslesme['sira']

                #rejection.py burayı okuyor,bir sonraki adımda rejection fonksiyonu "Bu öğrenci yeni gelmiş,bir değerlendirelim" der.
                aday_ogrenci.placed_round = tur_sayisi

                bu_tur_yerlesen_sayisi += 1

        print(f">>> [ADIM 4] Bu turda {bu_tur_yerlesen_sayisi} öğrenci yerleştirildi.")

        # REDDETME SİMÜLASYONU
        reddedilen_sayisi = reject_students(firmalar, tur_sayisi, rejection_rate=0.20)

        # KONTROL
        if bu_tur_yerlesen_sayisi == 0 and reddedilen_sayisi == 0:
            print("\n>>> [BİTİŞ] Sistem stabil hale geldi (Hareket yok).")
            break

        tur_sayisi += 1

    # SONUÇ
    sayac = 0  # Başlangıçta kimse yok
    for ogr in ogrenciler:
        if ogr.is_placed == True:
            sayac = sayac + 1

    toplam_yerlesen = sayac

    print(f"\n>>> [SONUÇ] Scoring Heuristic Tamamlandı. Toplam Yerleşen: {toplam_yerlesen}")
    return toplam_yerlesen, tur_sayisi