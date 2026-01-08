import sys
import io
import time

# Türkçe karakterler konsolda düzgün çıksın diye
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Kendi yazdığımız dosyaları içeri alıyoruz
from utils.data_loader import load_all_data, save_results
from utils.metrics import calculate_happiness
from simulation.simulation import run_simulation
from algorithms import heuristic_local, heuristic_scoring


def main():
    # Sonuçları burada toplayıp en son tablo yapacağım
    rapor_verileri = []

    print("--- Stajyer Yerleştirme Programı Başlatılıyor ---")
    print("Not: Dosyaların 'data' klasöründe olduğundan emin olun.\n")

    # Greedy ve Reddetme Simülasyonu
    
    print("-" * 30)
    print("Deney 1: Greedy + Rejection Simülasyonu")
    s_greedy, c_greedy = load_all_data()
    basla = time.time()

    # Bu fonksiyon kendi içinde döngüyle atama ve red yapıyor
    s_greedy, c_greedy, gecmis = run_simulation(s_greedy, c_greedy)
    sure_g = round(time.time() - basla, 4)
    skor_g = calculate_happiness(s_greedy)

    rapor_verileri.append(["Greedy (Simülasyon)", sure_g, f"{len(gecmis)} Tur", skor_g])
    save_results(s_greedy, "sonuc_greedy.json")  # Greedy sonucunu kaydet

    # Scoring Heuristic (Hibrit Puanlama)

    print("\n" + "-" * 30)
    print("Deney 2: Scoring Heuristic")
    s_score, c_score = load_all_data()
    basla = time.time()

    # Fonksiyon iki değer dönüyor, ikisini de alıyoruz:
    yerlesen_sayisi, kac_tur_surdu = heuristic_scoring.apply_scoring_heuristic(s_score, c_score)

    sure_s = round(time.time() - basla, 4)
    skor_s = calculate_happiness(s_score)

    rapor_verileri.append(["Scoring Heuristic", sure_s, f"{kac_tur_surdu} Tur", skor_s])

    save_results(s_score, "sonuc_scoring.json")

    # Local Search

    print("\n" + "-" * 30)
    print("Deney 3: Local Search (Hill Climbing)")
    s_local, c_local = load_all_data()
    basla = time.time()

    # Algoritmayı çalıştır ve dönen paketi al
    sonuc_l = heuristic_local.run(s_local, c_local)

    sure_l = round(time.time() - basla, 4)
    skor_l = sonuc_l.get('final_skor')

    # Tabloya algoritmanın durduğu turu (islem_sayisi) yazdırıyoruz
    gercek_tur = sonuc_l.get('islem_sayisi', 5000)

    rapor_verileri.append(["Local Search", sure_l, f"{gercek_tur} Takas", skor_l])
    save_results(s_local, "sonuc_local.json")

    print("\n\n" + "=" * 80)
    print(f"{'ALGORİTMA KARŞILAŞTIRMA SONUÇLARI':^80}")
    print("=" * 80)
    print(f"{'Yöntem':<25} | {'Süre (sn)':<12} | {'İşlem Detayı':<18} | {'Mutluluk Skoru'}")
    print("-" * 80)
    for r in rapor_verileri:
        print(f"{r[0]:<25} | {r[1]:<12} | {r[2]:<18} | {r[3]}")

    print("-" * 80)
    print("\n>>> Tüm algoritmaların sonuçları ayrı ayrı JSON dosyalarına yazdırıldı.")


if __name__ == "__main__":
    main()