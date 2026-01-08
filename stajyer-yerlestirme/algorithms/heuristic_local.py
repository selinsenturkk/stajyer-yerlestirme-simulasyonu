import random
import time
from utils.metrics import calculate_happiness

def run(ogrenciler, firmalar):
    """ 
    Yerel Arama (Local Search)
    --> İlk olarak herkesi rastgele bir yere atıyoruz sonra 'kimle kimi değiştirirsek
        toplam mutluluk artar?' diye 5000 kere deniyoruz"""
    print("\n--- Local Search Başlatılıyor ---")
    baslangic_zamani = time.time()
    
    # Firma isimlerinden nesnelere hızlı ulaşmak için bir sözlük (Map) oluşturuyoruz.
    # Böylece string olarak tuttuğumuz isimle, firmanın kendisine ulaşabileceğiz.
    company_map = {f.name: f for f in firmalar}

    # RASTGELE İLK YERLEŞTİRME
    #Başlangıçta kimin nereye gitiiği önemli değil çünkü birazdan takaslarla düzelteceğiz
    print(">>> [ADIM 1] Rastgele ilk yerleştirme yapılıyor...")
    bos_yer_havuzu = []
    
    # Havuzu firma nesneleriyle doldur
    for tek_firma in firmalar:
        tek_firma.interns = [] #üstten kalan veri varsa temizle
        for i in range(tek_firma.capacity):
            bos_yer_havuzu.append(tek_firma)
    
    random.shuffle(bos_yer_havuzu) # rastgeleliği sağlamak için havuzu karıştır
    
    for tek_ogrenci in ogrenciler:
        if len(bos_yer_havuzu) > 0:
            secilen_firma = bos_yer_havuzu.pop() # havuzdan bir firma nesnesi çektik
            
            #Öğrenciye firmanın kendisini değil, ADINI (String) atıyoruz.
            tek_ogrenci.assigned_firm = secilen_firma.name   
            secilen_firma.interns.append(tek_ogrenci) # Firmaya ise öğrencinin kendisini (Nesne) ekliyoruz.
            tek_ogrenci.is_placed = True

    #Rastgele attığımızda ne kadar 'mutsuz' tablo oluştu?
    mevcut_puan = calculate_happiness(ogrenciler)
    print(f"    Başlangıç Mutluluk Skoru: {mevcut_puan}")
    
    # TAKAS (SWAP) İLE İYİLEŞTİRME 
    print(f">>> [ADIM 2] Maksimum 5000 iterasyonluk optimizasyon döngüsü başlatıldı...")
    
    toplam_deneme = 5000
    basarili_takaslar = 0
    sabir=400 #EARLY STOPPİNG
    son_iyilesmeden_beri_gecen_tur = 0
    en_iyi_tur=0

    for tur in range(1, toplam_deneme + 1):
        #Listeden 2 tane öğrenci seçiyoruz, yerlerini değiştirirsek ne olur?
        o1 = random.choice(ogrenciler)
        o2 = random.choice(ogrenciler)
        
        # Eğer öğrencilerden biri yerleşmemişse (Nadir durum ama güvenlik için) pas geç
        if not o1.assigned_firm or not o2.assigned_firm:
            continue

        # Eğer ikisi zaten aynı firmada ise değiştirmek bir şeyi etkilemez, pas geçelim
        if o1.assigned_firm == o2.assigned_firm:
            son_iyilesmeden_beri_gecen_tur += 1
            continue
         
        # String olan isimlerden Firma Nesnelerine ulaşıyoruz
        f1_name = o1.assigned_firm
        f2_name = o2.assigned_firm
        # Takas yapmadan önce kimin nerede olduğunu kopyalıyoruz  
        f1 = company_map[f1_name]
        f2 = company_map[f2_name]
        
        # TAKAS: Öğrencileri eski firmalarının stajyer listelerinden siliyoruz.
        f1.interns.remove(o1)
        f2.interns.remove(o2)
        
        # Öğrencilerin atandığı firma İSİMLERİNİ değiştiriyoruz
        o1.assigned_firm = f2.name
        o2.assigned_firm = f1.name
        
        # Firmaların listesine öğrencileri ekliyoruz
        f2.interns.append(o1)
        f1.interns.append(o2)
        
        # Yaptığımız değişiklik toplam mutluluk puanını artırdı mı?
        yeni_puan = calculate_happiness(ogrenciler)
        
        if yeni_puan > mevcut_puan:
            # Puan arttı, o zaman bu takas kalıcı olsun
            mevcut_puan = yeni_puan
            basarili_takaslar += 1
            son_iyilesmeden_beri_gecen_tur = 0
            en_iyi_tur=tur

        else:
            # Puan azaldı ya da aynı kaldı. Yaptığımız değişikliği geri almalıyız.
            # Geri Al (Undo) - İşlemlerin tam tersini yap
            f2.interns.remove(o1)
            f1.interns.remove(o2)
            
            # İsimleri eski haline (kopyaladığımız) haline getiririyoruz
            o1.assigned_firm = f1_name
            o2.assigned_firm = f2_name
            
            # Listeleri eski haline getir
            f1.interns.append(o1)
            f2.interns.append(o2)

            son_iyilesmeden_beri_gecen_tur += 1
        
        # --- ERKEN DURDURMA (EARLY STOPPING) KONTROLÜ ---
        if son_iyilesmeden_beri_gecen_tur >= sabir:
            print(f"\n>>> [BİLGİ] {sabir} tur boyunca gelişim olmadığı için durduruldu.")
            break

    # SONUÇ RAPORU
    bitis_zamani = time.time()
    
    print(f"\n>>> [ANALİZ] Algoritma en iyi skoru({mevcut_puan}) {en_iyi_tur}. turda yakaladı.")
    print(f">>> [ANALİZ] Toplamda {tur} takas denemesi gerçekleştirildi.")
    return {
        "final_skor": mevcut_puan,
        "en_iyi_tur": en_iyi_tur,    
        "islem_sayisi": tur,           
        "cozum_suresi": round(bitis_zamani - baslangic_zamani, 4)
    }