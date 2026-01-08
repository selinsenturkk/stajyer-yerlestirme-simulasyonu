import random

def reject_students(companies, current_round, rejection_rate=0.2):
    """
    Sadece BU TURDA (current_round) yerleşen öğrencileri değerlendirir.
    Eski turlarda yerleşmiş olanlar 'güvendedir'.
    """
    total_rejected = 0
    stats = {"Popüler": 0, "Standart": 0, "Alt Segment": 0}

    print(f"\n--- Reddetme Süreci (Sadece Yeni Gelenler İçin - Baz Oran: %{int(rejection_rate * 100)}) ---")

    for company in companies:
        if len(company.interns) > 0:

            # Prestij Çarpanları
            if company.capacity == 2:
                firm_type = "Popüler"
                multiplier = 2.5
            elif company.capacity == 3:
                firm_type = "Standart"
                multiplier = 1.5
            else:
                firm_type = "Alt Segment"
                multiplier = 0.4

            current_firm_rate = rejection_rate * multiplier

            # Listeyi kopyala
            current_interns = list(company.interns)

            for student in current_interns:

                # --- KRİTİK KONTROL ---
                # Öğrencinin yerleştiği tur, şimdiki tur değilse (yani eskiyse) KORU.
                # getattr kullanıyoruz ki 'placed_round' yoksa hata vermesin (0 varsayalım)
                student_round = getattr(student, 'placed_round', 0)

                if student_round != current_round:
                    continue  # Bu öğrenci eski toprak, dokunma.

                # Sadece YENİLER için zar at
                if random.random() < current_firm_rate:
                    company.interns.remove(student)

                    student.is_placed = False
                    student.assigned_firm = None
                    student.choice_rank = 0
                    student.placed_round = 0  # Bilgiyi sıfırla

                    total_rejected += 1
                    stats[firm_type] += 1

    print(f"--- Toplam {total_rejected} yeni aday reddedildi. ---")
    print(f"    (Popüler: {stats['Popüler']}, Standart: {stats['Standart']}, Alt Segment: {stats['Alt Segment']})")

    return total_rejected