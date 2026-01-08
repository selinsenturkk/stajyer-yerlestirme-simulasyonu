from algorithms.greedy import greedy_step
from simulation.rejection import reject_students

def run_simulation(students, companies):
    iteration = 1
    max_iterations = 20 
    base_rejection_rate = 0.20 
    history = [] 

    print(f"\n{'='*20} SİMÜLASYON BAŞLIYOR {'='*20}")

    while iteration <= max_iterations:
        pool_size = sum(1 for s in students if not s.is_placed)
        print(f"\n>>> TUR {iteration} (Havuzda Bekleyen: {pool_size} Kişi) <<<")
        
        if pool_size == 0:
            print("  Herkes yerleşti! Simülasyon erken tamamlandı.")
            break

        # 1. ADIM: Greedy'ye tur sayısını gönderiyoruz
        students, companies, results = greedy_step(students, companies, round_number=iteration)
        
        placed_in_round = results['total_placed']     
        current_unplaced = results['total_unplaced'] 
        
        print(f"  [Atama] {placed_in_round} kişi yerleştirildi. (Hala Açıkta: {current_unplaced})")
        
        if current_unplaced == 0:
            print("  Tüm öğrenciler yerleşti! Simülasyon tamamlandı.")
            break
            
        # 2. ADIM: Reddetme fonksiyonuna tur sayısını gönderiyoruz
        current_rate = max(0, base_rejection_rate - (iteration * 0.01))
        
        # reject_students artık 'iteration' parametresini alıyor
        rejected_count = reject_students(companies, current_round=iteration, rejection_rate=current_rate)
        
        history.append({
            "round": iteration,
            "pool_start": pool_size,
            "placed": placed_in_round,
            "rejected": rejected_count,
            "left_unplaced": current_unplaced
        })
        
        if rejected_count == 0 and placed_in_round == 0:
            print("  Sistem stabil hale geldi (Değişiklik yok).")
            break

        iteration += 1

    print(f"\n{'='*20} SİMÜLASYON BİTTİ {'='*20}")
    
    return students, companies, history