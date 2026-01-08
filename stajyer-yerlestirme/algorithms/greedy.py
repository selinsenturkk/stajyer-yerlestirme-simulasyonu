import time

def greedy_step(students, companies, round_number=1):

    # Performans ölçümü için süreyi başlatıyoruz
    start_time = time.time()
    
    # Firma isminden nesneye hızlı erişim için map (sözlük) kullanıyoruz. 
    # Yoksa her seferinde 40 firmayı döngüyle aramak çok yavaşlatır.
    company_map = {c.name: c for c in companies}
    
    # En yüksek ortalamalı öğrenciye öncelik veriyoruz (Büyükten küçüğe sırala)
    sorted_students = sorted(students, key=lambda x: x.gpa, reverse=True)

    placed_in_this_round = 0 
    total_satisfaction = 0

    print(f"\n--- Greedy Atama Başlıyor (Tur {round_number}) ---")

    for student in sorted_students:
        
        # Öğrenci zaten bir yere yerleştiyse onu atlıyoruz, tekrar işlem yapmaya gerek yok.
        if student.is_placed:
            continue

        # Öğrencinin tercih listesini sırayla (1. tercihten başlayarak) geziyoruz
        for index, pref_firm_name in enumerate(student.preferences):
            company = company_map.get(pref_firm_name)
            
            if company:
                # Eğer firmada boş kontenjan varsa atamayı yapıyoruz
                if len(company.interns) < company.capacity:
                    
                    # ATAMA İŞLEMLERİ
                    company.interns.append(student) 
                    student.assigned_firm = company.name 
                    student.is_placed = True
                    student.choice_rank = index + 1
                    
                    # Rejection algoritması için: Öğrencinin hangi turda yerleştiğini kaydediyoruz.
                    # Böylece eski turlarda yerleşenleri koruyabileceğiz.
                    student.placed_round = round_number 
                    
                    placed_in_this_round += 1
                    total_satisfaction += (5 - index) # 1. tercih 5 puan, 5. tercih 1 puan katkı sağlar
                    
                    # Öğrenci yerleştiği için diğer tercihlerine bakmayı bırakıyoruz
                    break 
        
    end_time = time.time()
    
    # Gerçekten kaç kişi açıkta kaldı? Onu hesaplıyoruz.
    actual_unplaced_count = sum(1 for s in students if not s.is_placed)
    
    if placed_in_this_round > 0:
        avg_satisfaction = total_satisfaction / placed_in_this_round
    else:
        avg_satisfaction = 0

    # Sonuçları paketleyip simülasyona geri gönderiyoruz
    results = {
        "total_placed": placed_in_this_round,
        "total_unplaced": actual_unplaced_count,
        "execution_time": end_time - start_time,
        "average_satisfaction": avg_satisfaction
    }

    return sorted_students, companies, results