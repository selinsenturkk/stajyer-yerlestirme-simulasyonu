import json
import random    # Rastgele isim, GNO ve tercih seçimi yapmak için random kütüphanesinden yararlandık.

def generate_realistic_data(student_count=130):
    # Okulumuzun anlaşmalı olduğu 40 adet firma ismi
    firm_names_list = [
        "Doğuş", "BEYÇELİK", "Trendyol", "HepsiBurada", "Getir", "BİLGE Teknoloji", "NESTLE",
        "TOFAŞ", "CITS Bilişim", "Datayaz Bilişim", "Diniz Donanım",
        "Dista Yazılım", "Nette", "ECS Elektrik", "Borçelik",
        "EMKO Elektronik", "Eruslu Tekstil", "EXİM TEKSTİL",
        "GÖRSENTAM", "Güncel Yazılım", "Harput Tekstil",
        "İnvio Bilişim", "İbraş Kauçuk", "Kentkart Teknoloji", "MOBGE Yazılım",
        "BODO", "Orcas Otomotiv", "ORTEM Elektronik", "Ottomotive Mühendislik",
        "PENTECH Bilişim", "Rabek Tekstil", "Rudolf Duraner",
        "Sorsware Bilişim", "Şahince Otomotiv", "Teracity Yazılım", "Vesium",
        "Virgasol Bilişim", "Wiome Elektronik", "ADASTEC", "Skyfood Gıda"
    ]

    firm_pool = []
    for i, name in enumerate(firm_names_list):  #Kapasiteyi sıraya göre belirlemek için enumerate kullandık.(0.Şirket=prestijli....)
        if i < 10:   # İlk 10 firma "popüler" (Az kontenjan)
            capacity = 2
        elif i < 30:  # "standart" firmalar
            capacity = 3
        else:         # Son 10 firma "alt segmentli" (Yüksek kontenjan)
            capacity = 5


        firm_pool.append({        #Veriyi JSON formatına uygun hale getirmek için bellekte bir dictionary oluşturur.
            "name": name,
            "capacity": capacity
        })

    #Firmaları 3 segmente ayırdık
    popular_firms = [f["name"] for f in firm_pool[:10]]  # En çok istenenler (Kapasite: 2)
    standard_firms = [f["name"] for f in firm_pool[10:30]]  # Standart  (Kapasite: 3)
    bottom_firms = [f["name"] for f in firm_pool[30:]]  # Alt Segment (Kapasite: 5)

    # 80 * 80 = 6400 farklı kombinasyon demektir.Bu da isim-soyisim çeşitliliğini ciddi ölçüde arttırır.
    first_names = [
        "Ahmet", "Mehmet", "Mustafa", "Ali", "Hüseyin", "Hasan", "İbrahim", "İsmail", "Osman", "Yusuf",
        "Murat", "Ömer", "Ramazan", "Halil", "Süleyman", "Abdullah", "Mahmut", "Salih", "Kemal", "Recep",
        "Fatma", "Ayşe", "Emine", "Hatice", "Zeynep", "Elif", "Meryem", "Şerife", "Zehra", "Sultan",
        "Hanife", "Merve", "Havva", "Zeliha", "Esra", "Fadime", "Özlem", "Hacer", "Yasemin", "Hülya",
        "Cem", "Deniz", "Ege", "Umut", "Arda", "Bora", "Can", "Efe", "Kağan", "Mert",
        "Selin", "Pelin", "Melis", "Damla", "Gizem", "İrem", "Simge", "Buse", "Duygu", "Ezgi",
        "Barış", "Savaş", "Volkan", "Serkan", "Gökhan", "Hakan", "Okan", "Erkan", "Tolga", "Koray",
        "Burak", "Berk", "Berkay", "Batuhan", "Buğra", "Alp", "Alper", "Göktuğ", "Yiğit", "Kerem"
    ]

    last_names = [
        "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Yıldırım", "Öztürk", "Aydın", "Özdemir",
        "Arslan", "Doğan", "Kılıç", "Aslan", "Çetin", "Kara", "Koç", "Kurt", "Özkan", "Şimşek",
        "Polat", "Özçelik", "Korkmaz", "Çakır", "Erdoğan", "Yavuz", "Can", "Acar", "Şen", "Aktaş",
        "Güler", "Yalçın", "Güneş", "Bozkurt", "Bulut", "Keskin", "Ünal", "Turan", "Gül", "Avcı",
        "Işık", "Kaplan", "Tekin", "Taş", "Köse", "Yüksel", "Ateş", "Aksoy", "Coşkun", "Sarı",
        "Uçar", "Duran", "Türk", "Yaman", "Çalışkan", "Karataş", "Çam", "Ceylan", "Bayram", "Vural",
        "Ergin", "Genç", "Çakmak", "Korkut", "Duman", "Parlak", "Uysal", "Şeker", "Mutlu", "Baş",
        "Toprak", "Kocaman", "Sönmez", "Bilgin", "Uslu", "Esen", "Tezel", "Önal", "Gedik", "Varol"
    ]

    students = []
    generated_names = set()

    while len(students) < student_count:
        f_name = random.choice(first_names)
        l_name = random.choice(last_names)
        full_name = f"{f_name} {l_name}"

        if full_name in generated_names:  #Daha önce oluşturulmuş bir isimse atla
            continue
        generated_names.add(full_name)

        # Oluşturulan öğrencilerin gno aralığı: 1.50 - 4.00 arası oluşturulacak.
        gpa = round(random.uniform(1.50, 4.00), 2)


        # GNO'ya göre 3'lü Segment Tercih Stratejisi
        if gpa >= 3.50:
            # ÜST SEGMENT: 3 Popüler + 1 Standart + 1 Alt (Risk yönetimi yapar)
            # 3.95'lik öğrenci örneğin: 3 Popüler seçer, 2 tane de 'ne olur ne olmaz' der.
            prefs = random.sample(popular_firms, 3) + random.sample(standard_firms, 1) + random.sample(bottom_firms, 1)
        elif gpa >= 2.50:
            # ORTA SEGMENT: 1 Popüler + 2 Standart + 2 Alt
            prefs = random.sample(popular_firms, 1) + random.sample(standard_firms, 2) + random.sample(bottom_firms, 2)
        else:
            # ALT SEGMENT (1.5 - 2.5): 0 Popüler (Yazsa da giremez) + 2 Standart + 3 Alt
            # Bu grup tamamen yerleşme odaklı davranır.
            prefs = random.sample(standard_firms, 2) + random.sample(bottom_firms, 3)

        random.shuffle(prefs)  # Kimin neyi 1. sıraya yazacağı hala sürpriz kalsın

        students.append({
            "id": 1000 + len(students) + 1,
            "name": full_name,
            "gpa": gpa,
            "preferences": prefs
        })

    # JSON Kayıt
    with open('firms.json', 'w', encoding='utf-8') as f:
        json.dump(firm_pool, f, indent=4, ensure_ascii=False)

    with open('students.json', 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=4, ensure_ascii=False)

    total_capacity = sum(f['capacity'] for f in firm_pool) #Sistemde toplam kaç öğrenci yerleştirilebilir görmek için
    print(f"Veri Seti Hazır! GNO: 1.50 - 4.00 | Toplam Kontenjan: {total_capacity}")


if __name__ == "__main__":
    generate_realistic_data(130)