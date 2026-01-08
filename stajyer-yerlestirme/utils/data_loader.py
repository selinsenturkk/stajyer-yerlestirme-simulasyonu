import json
import os       #Kodun taşınabilirliğini (portability) sağlamak için bu kütüphaneyi ekledik.

class Student:
    def __init__(self, id, name, gpa, preferences):  #Constructor fonksiyonu:Bir öğrenci yaratıldığı anda (örneğin JSON'dan okunurken) ilk bu bölüm çalışır.
        self.id = id                                 #self=Oluşturulan nesnenin kendisini temsil eder
        self.name = name
        self.gpa = gpa
        self.preferences = preferences
        # Simülasyon sırasında güncellenecek dinamik bilgiler
        self.is_placed = False     #Yerleşme durumu(Başlangıçta false yaptık)
        self.assigned_firm = None  #Yerleştiği firma ismi
        self.choice_rank = 0       # Kaçıncı tercihine yerleştiği

    #print(student) dediğimizde,ekranda anlamsız bir bilgisayar kodu almamak için bu fonksiyonu tanımladık:
    def __repr__(self):
        return f"Student({self.name}, GPA: {self.gpa})"

class Company:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.interns = []  # Bu şirkete yerleşen öğrenci nesnelerini bu listenin içine atacağız.

    #Bu dekoratör, aslında bir fonksiyon olan bir yapıyı, dışarıdan bakıldığında sanki basit bir değişken (özellik) gibi kullanmamızı sağlar.
    @property       #Manuel azaltmıyoruz.Biz sadece "Kapasiteden, içerideki stajyer listesinin uzunluğunu çıkar" diyoruz.
    def remaining_capacity(self):
        return self.capacity - len(self.interns)

    #print(company) dediğimizde,ekranda anlamsız bir bilgisayar kodu almamak için bu fonksiyonu tanımladık:
    def __repr__(self):
        return f"Company({self.name}, Capacity: {len(self.interns)}/{self.capacity})"


#Data klasöründeki JSON dosyalarını okur ve nesne listeleri döndürür.
def load_all_data():
    # Dosya yollarını projenin ana dizinine göre ayarlıyoruz
    base_path = os.path.dirname(os.path.dirname(__file__))  # Birinci dirname bizi utils klasörüne, ikinci dirname ise projenin ana dizinine (Root) götürür.
    students_path = os.path.join(base_path, 'data', 'students.json') #Bu os.path.join ile biz sadece klasör isimlerini veririz,Python aradaki işaretleri bilgisayara göre otomatik ayarlar.
    firms_path = os.path.join(base_path, 'data', 'firms.json')

    # 2. Öğrenci Verilerini Yükle
    with open(students_path, 'r', encoding='utf-8') as f:
        students_raw = json.load(f)  # Metin dosyasını Python listesine çevir
        # Her bir sözlüğü (dict) alıp Student sınıfına 'fırlat' ve nesne oluştur
        students = [Student(**s) for s in students_raw]

    # 3. Firma Verilerini Yükle
    with open(firms_path, 'r', encoding='utf-8') as f:
        firms_raw = json.load(f)  # Ham firma verilerini oku
        # Ham veriyi alıp kapasite takibi yapabilen Company nesnelerine dönüştür
        companies = [Company(**c) for c in firms_raw]

    # Hazırlanan listeleri algoritmanın kullanması için geri gönder
    return students, companies


# SONUÇLARI KAYDETME FONKSİYONU (Bunu main.py kullanıyor)
# data_loader.py içindeki bu fonksiyonu bul ve şu şekilde değiştir:
def save_results(students, dosya_adi="sonuc_tablosu.json"):  # dosya_adi parametresi eklendi
    output_list = []
    for s in students:
        # Firmayı güvenli bir şekilde metin olarak al (Nesne veya String kontrolü)
        if s.assigned_firm:
            firm_name = s.assigned_firm if isinstance(s.assigned_firm, str) else s.assigned_firm.name
        else:
            firm_name = "YERLESEMEDI"

        durum = "Tercihine Yerlesti" if s.choice_rank > 0 else "Rastgele Atandi"
        if firm_name == "YERLESEMEDI": durum = "Bosta"

        output_list.append({
            "ogrenci_id": s.id,
            "isim": s.name,
            "gpa": s.gpa,
            "yerlestigi_firma": firm_name,
            "tercih_sirasi": s.choice_rank,
            "durum": durum
        })

    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(current_dir)
    # Sabit 'sonuc_tablosu.json' yerine artık 'dosya_adi' değişkenini kullanıyoruz
    output_path = os.path.join(base_path, dosya_adi)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_list, f, indent=4, ensure_ascii=False)
    print(f">>> Sonuçlar '{output_path}' dosyasına kaydedildi.")