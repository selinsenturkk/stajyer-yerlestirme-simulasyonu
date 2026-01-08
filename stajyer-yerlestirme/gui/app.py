import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time

# YOL AYARI (PATH FIX)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from data import dataset_hazirlayici
from utils.data_loader import load_all_data, save_results
from utils.metrics import calculate_happiness
from simulation.simulation import run_simulation
from algorithms import heuristic_local, heuristic_scoring


class InternshipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stajyer Yerleştirme Simülasyonu 2025-2026")
        self.root.geometry("1000x700")
        
        # STİL VE TEMA AYARLARI
        self.setup_styles()
        self.root.configure(bg="#f0f2f5") # Arka plan rengi

        # ANA KONTEYNER
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ÜST PANEL (BAŞLIK & KONTROLLER)
        header_frame = ttk.LabelFrame(main_frame, text=" Kontrol Paneli ", padding=15)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        # Butonlar ve Giriş Alanları
        self.btn_create_data = ttk.Button(header_frame, text=" 1. Veri Seti Oluştur", command=self.create_data, style="Accent.TButton")
        self.btn_create_data.pack(side=tk.LEFT, padx=5)

        self.btn_run_sim = ttk.Button(header_frame, text=" 2. Simülasyonu Başlat", command=self.start_simulation_thread, style="Success.TButton")
        self.btn_run_sim.pack(side=tk.LEFT, padx=5)

        # Ayırıcı Çizgi
        ttk.Separator(header_frame, orient="vertical").pack(side=tk.LEFT, fill="y", padx=15)

        ttk.Label(header_frame, text="Öğrenci Sayısı:", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.ent_student_count = ttk.Entry(header_frame, width=8, font=("Segoe UI", 10))
        self.ent_student_count.insert(0, "130")
        self.ent_student_count.config(state='readonly')
        self.ent_student_count.pack(side=tk.LEFT)

        # İlerleme Çubuğu
        self.progress = ttk.Progressbar(header_frame, mode='indeterminate', length=220)
        self.progress.pack(side=tk.RIGHT, padx=10)

        # ORTA PANEL (SONUÇ TABLOSU)
        table_frame = ttk.LabelFrame(main_frame, text=" Karşılaştırma Sonuçları ", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ("yontem", "sure", "detay", "skor")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
        
        # Sütun Başlıkları
        self.tree.heading("yontem", text="Algoritma Yöntemi")
        self.tree.heading("sure", text="Süre (sn)")
        self.tree.heading("detay", text="İşlem Detayı")
        self.tree.heading("skor", text="Mutluluk Skoru")
        
        self.tree.column("yontem", width=250, anchor="w")
        self.tree.column("sure", width=100, anchor="center")
        self.tree.column("detay", width=150, anchor="center")
        self.tree.column("skor", width=150, anchor="center")
        
        # Zebra Çizgili Satırlar için Tag
        self.tree.tag_configure('odd', background='#f9f9f9')
        self.tree.tag_configure('even', background='#eef2f3')
        
        # Scrollbar ekle
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # ALT PANEL (TERMİNAL LOGLARI)
        log_frame = ttk.LabelFrame(main_frame, text=" Sistem Logları ", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))

        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, state='disabled', 
                                                  font=("Consolas", 12), bg="#1e1e1e", fg="#00ff00") # Matrix Stili
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Konsol yönlendirme
        sys.stdout = self

    def setup_styles(self):
        """Arayüzü güzelleştiren stil tanımları"""
        style = ttk.Style()
        style.theme_use("clam")

        # Genel Renkler
        bg_color = "#f0f2f5"
        primary_color = "#2c3e50"
        
        style.configure("TFrame", background=bg_color)
        style.configure("TLabelframe", background=bg_color, borderwidth=2, relief="groove")
        style.configure("TLabelframe.Label", font=("Segoe UI", 12, "bold"), foreground=primary_color, background=bg_color)
        
        style.configure("TLabel", background=bg_color, font=("Segoe UI", 11))
        
        # Buton Stilleri
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        
        # Mavi Buton
        style.configure("Accent.TButton", background="#3498db", foreground="white", borderwidth=0)
        style.map("Accent.TButton", background=[("active", "#2980b9")])
        
        # Yeşil Buton
        style.configure("Success.TButton", background="#27ae60", foreground="white", borderwidth=0)
        style.map("Success.TButton", background=[("active", "#219150")])

        # Tablo Stili
        style.configure("Treeview", 
                        background="white",
                        foreground="black", 
                        rowheight=30, 
                        fieldbackground="white",
                        font=("Segoe UI", 12))
        
        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 12, "bold"), 
                        background="#bdc3c7", 
                        foreground="#2c3e50")
        
    def write(self, text):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()

    def flush(self):
        pass

    def create_data(self):
        try:
            count = int(self.ent_student_count.get())
            self.write(f"\n--- {count} Öğrenci İçin Veri Seti Hazırlanıyor ---\n")
            dataset_hazirlayici.generate_realistic_data(count)

            if not os.path.exists('data'):
                os.makedirs('data')

            if os.path.exists("students.json"):
                os.replace("students.json", "data/students.json")
            if os.path.exists("firms.json"):
                os.replace("firms.json", "data/firms.json")

            self.write(">>> Veri seti başarıyla oluşturuldu!\n")
            messagebox.showinfo("Başarılı", "Veri seti 'data' klasörüne kaydedildi.")

        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin.")
        except Exception as e:
            self.write(f" HATA: {e}\n")

    def start_simulation_thread(self):
        # Butonları devre dışı bırak, progress barı başlat
        self.btn_run_sim.config(state="disabled")
        self.btn_create_data.config(state="disabled")
        self.progress.start(10) 
        
        threading.Thread(target=self.run_simulations, daemon=True).start()

    def run_simulations(self):
        # Tabloyu temizle
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            self.write("\n" + "="*40 + "\n SİMÜLASYON SÜRECİ BAŞLATILIYOR \n" + "="*40 + "\n")

            # Greedy
            self.write("\n Deney 1: Greedy + Rejection Modeli\n")
            s_greedy, c_greedy = load_all_data()
            basla = time.time()

            s_greedy, c_greedy, gecmis_greedy = run_simulation(s_greedy, c_greedy)

            sure_g = round(time.time() - basla, 4)
            skor_g = calculate_happiness(s_greedy)

            self.tree.insert("", tk.END, values=("Greedy (Açgözlü)", f"{sure_g} sn", f"{len(gecmis_greedy)} Tur", skor_g), tags=('odd',))
            save_results(s_greedy, "sonuc_greedy.json")
            time.sleep(0.5) # Görsellik için çok kısa bekleme

            # Scoring Heuristic
            
            self.write("\n Deney 2: Scoring Heuristic (Puanlama)\n")
            s_score, c_score = load_all_data()
            basla = time.time()

            yerlesen_sayisi, tur_sayisi = heuristic_scoring.apply_scoring_heuristic(s_score, c_score)

            sure_s = round(time.time() - basla, 4)
            skor_s = calculate_happiness(s_score)

            self.tree.insert("", tk.END, values=("Scoring Heuristic", f"{sure_s} sn", f"{tur_sayisi} Tur", skor_s), tags=('even',))
            save_results(s_score, "sonuc_scoring.json")
            time.sleep(0.5)

            # Local Search
            self.write("\n Deney 3: Local Search (Tepe Tırmanma)\n")
            s_local, c_local = load_all_data()
            basla = time.time()
            
            sonuc_paketi = heuristic_local.run(s_local, c_local)
            
            sure_l = round(time.time() - basla, 4)
            skor_l = sonuc_paketi.get('final_skor', 0)
            gercek_islem = sonuc_paketi.get('islem_sayisi', 5000)
            
            self.tree.insert("", tk.END, values=("Local Search (Optimizasyon)", f"{sure_l} sn", f"{gercek_islem} Takas", skor_l), tags=('odd',))
            save_results(s_local, "sonuc_local.json")

            self.write("\n TÜM İŞLEMLER BAŞARIYLA TAMAMLANDI.\n")
            messagebox.showinfo("Tamamlandı", "Tüm simülasyonlar bitti ve sonuçlar kaydedildi.")

        except FileNotFoundError:
            messagebox.showerror("Hata", "Veri dosyaları bulunamadı! Önce 'Veri Seti Oluştur' butonuna basın.")
        except Exception as e:
            messagebox.showerror("Hata", f"Beklenmedik bir hata oluştu:\n{e}")
            print(e)
        finally:
            # İşlem bitince butonları aç ve barı durdur
            self.root.after(0, self.stop_progress)

    def stop_progress(self):
        self.progress.stop()
        self.btn_run_sim.config(state="normal")
        self.btn_create_data.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    # Windows'ta ikonun net görünmesi için
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
        
    app = InternshipApp(root)
    root.mainloop()