def calculate_happiness(students):
    total_score = 0
    for s in students:
        if s.assigned_firm is None:
            total_score -= 500 # Boşta kalana büyük ceza
        else:
            # --- DÜZELTME BURADA ---
            # Eğer greedy.py firmayı isim (str) olarak kaydettiyse direkt onu al
            # Eğer nesne olarak kaydettiyse .name özelliğini al
            if isinstance(s.assigned_firm, str):
                firm_name = s.assigned_firm
            else:
                firm_name = s.assigned_firm.name
            
            if firm_name in s.preferences:
                rank = s.preferences.index(firm_name)
                # 1. tercih 100 puan, her sırada 15 puan düşer
                score = 100 - (rank * 15)
                total_score += score
                s.choice_rank = rank + 1
            else:
                total_score += 10 # Rastgele atama puanı
                s.choice_rank = -1
    return total_score

def print_status(students, companies, title="DURUM RAPORU"):
    placed = [s for s in students if s.assigned_firm]
    unplaced = [s for s in students if not s.assigned_firm]
    score = calculate_happiness(students)

    print(f"\n--- {title} ---")
    print(f"Toplam Öğrenci : {len(students)}")
    print(f"Yerleşen       : {len(placed)}")
    print(f"Açıkta Kalan   : {len(unplaced)}")
    print(f"Mutluluk Skoru : {score}")
    print("-" * 30)