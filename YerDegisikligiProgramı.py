import random
import tkinter as tk
from tkinter import messagebox

#Ertuğrul Yıldız
class ProgramHakkindaPenceresi:
    def __init__(self, root):
        self.root = root
        self.root.title("Program Hakkında")
        self.root.iconbitmap('data_dosyaları/bin/hakkında.ico')

        tk.Label(root, text="Yer Değişikliği Uygulaması", font=('Helvetica', 12, 'bold'),fg="orange").pack(pady=20)

        aciklama = ("Bu uygulama, öğrencilerin sıralarını rasgele oluşturarak oturma düzeni oluşturmayı sağlar.\n"
                    "Ayrıca, kızlı-erkekli oturma, karışık oturma gibi modları vardır.\n"
                    "12.02.2024'te Ertuğrul Yıldız tarafından yapılmıştır.")
        tk.Label(root, text=aciklama, font=('Helvetica', 10)).pack(padx=20, pady=10)

        tk.Button(root, text="Kapat", command=self.kapat, bg="orange",fg="white").pack(pady=20)

    def kapat(self):
        self.root.destroy()

class AyarlarPenceresi:
    def __init__(self, root, ana_pencere):
        self.root = root
        self.root.title("Ayarlar")
        self.root.iconbitmap('data_dosyaları/bin/ayar.ico')

        self.ana_pencere = ana_pencere
        self.karisik_mod = tk.BooleanVar()
        self.kiz_erkek_mod = tk.BooleanVar()

        tk.Label(root, text="Oturma Düzeni Ayarları", font=('Helvetica', 12, 'bold'),fg="orange").pack(pady=20)

        tk.Checkbutton(root, text="Karışık Mod", variable=self.karisik_mod).pack()
        tk.Checkbutton(root, text="Kız-Erkek Mod", variable=self.kiz_erkek_mod).pack()

        tk.Button(root, text="Uygula", command=self.uygula,bg="orange",fg="white").pack(pady=10)

    def uygula(self):
        self.ana_pencere.karisik_mod = self.karisik_mod.get()
        self.ana_pencere.kiz_erkek_mod = self.kiz_erkek_mod.get()
        self.root.destroy()


class OgrenciSiralamaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rasgele Sıra Düzeni - Ertuğrul Yıldız")

        self.kizlar = []
        self.erkekler = []

        try:
            with open("data_dosyaları/bin/kizlar.txt", "r", encoding="utf-8") as kiz_dosya:
                self.kizlar = [isim.strip() for isim in kiz_dosya.readline().split(',')]
        except FileNotFoundError:
            print("Daha önce kaydedilmiş bir kız öğrenci txt dosyası bulunamadı. kizlar.txt adında yeni bir txt dosyası oluşturun.")

        try:
            with open("data_dosyaları/bin/erkekler.txt", "r", encoding="utf-8") as erkek_dosya:
                self.erkekler = [isim.strip() for isim in erkek_dosya.readline().split(',')]
        except FileNotFoundError:
            print("Daha önce kaydedilmiş bir erkek öğrenci txt dosyası bulunamadı. erkekler.txt adında yeni bir txt dosyası oluşturun.")

        self.root.iconbitmap('data_dosyaları/bin/icon.ico')

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        ayarlar_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayarlar", menu=ayarlar_menu)
        ayarlar_menu.add_command(label="Oturma Düzeni Ayarları", command=self.ayarlar_ac)
        ayarlar_menu.add_command(label="Program Hakkında", command=self.program_hakkinda_ac)

        self.label_main = tk.Label(root, text="10-B Sıra Düzeni Uygulaması", font=('Helvetica', 12, 'bold'), fg="orange")
        self.label_main.pack(pady=40)

        self.entry_default_text = ""
        self.entry = tk.Entry(root, font=('italic', 8), bd=5, width=40)
        self.entry.insert(tk.END, self.entry_default_text)
        self.entry.bind("<FocusIn>", self.clear_entry_default_text)
        self.entry.bind("<FocusOut>", self.restore_entry_default_text)
        self.entry.pack()

        self.label_instruction = tk.Label(root, text="Öğrenci Ekle(isimlerin arasına virgül koyunuz)", font=('Helvetica', 7))
        self.label_instruction.pack()

        self.button = tk.Button(root, text="Öğrencileri Sırala ve kaydet", command=self.sirala_ve_kaydet, bg='orange', fg='white', font=('Helvetica', 12, 'bold'))
        self.button.pack(pady=8)

        self.create_text_widgets()

       
        self.karisik_mod = True
        self.kiz_erkek_mod = False

        self.root.geometry("735x480")
        self.root.update_idletasks() 
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) // 2
        self.root.geometry("+{}+{}".format(x, y))

    def create_text_widgets(self):
        self.text_widgets = []
        for i in range(4):
            text_widget = tk.Text(self.root, height=13, width=23, font=('Helvetica', 10, 'italic'))
            text_widget.pack(side=tk.LEFT, padx=10, pady=10)
            self.text_widgets.append(text_widget)

    def sirala_ve_kaydet(self):
        ekstra_ogrenci_listesi = self.entry.get().split(',')

        if ekstra_ogrenci_listesi != ['']:
            for ogrenci in ekstra_ogrenci_listesi:
                cinsiyet = self.cinsiyet_sor(ogrenci)
                if cinsiyet.lower() == 'k':
                    self.kizlar.append(ogrenci)
                elif cinsiyet.lower() == 'e':
                    self.erkekler.append(ogrenci)

        random.shuffle(self.kizlar)
        random.shuffle(self.erkekler)

        if self.kiz_erkek_mod:
            karisik_ogrenciler = []

          
            for i in range(0, max(len(self.kizlar), len(self.erkekler)), 2):
                if i < len(self.kizlar):
                    karisik_ogrenciler.append(self.kizlar[i])
                if i < len(self.erkekler):
                    karisik_ogrenciler.append(self.erkekler[i])

                if i + 1 < len(self.kizlar):
                    karisik_ogrenciler.append(self.kizlar[i + 1])
                if i + 1 < len(self.erkekler):
                    karisik_ogrenciler.append(self.erkekler[i + 1])

            sirali_ogrenciler = [
                tuple(karisik_ogrenciler[i:i + 2]) for i in range(0, len(karisik_ogrenciler), 2)
            ]
        else:
            karisik_ogrenciler = self.kizlar + self.erkekler
            random.shuffle(karisik_ogrenciler)

            sirali_ogrenciler = [
                tuple(karisik_ogrenciler[i:i + 2]) for i in range(0, len(karisik_ogrenciler), 2)
            ]

        for text_widget in self.text_widgets:
            text_widget.delete("1.0", tk.END)

        text_index = 0
        for i, siradaki_ogrenciler in enumerate(sirali_ogrenciler):
            sira = f"Sıra {i + 1}: {', '.join(ogrenci if ogrenci else ' ' for ogrenci in siradaki_ogrenciler)}\n\n"
            self.text_widgets[text_index].insert(tk.END, sira)

            if (i + 1) % 5 == 0:
                text_index += 1

        with open("data_dosyaları/bin/kizlar.txt", "w", encoding="utf-8") as kiz_dosya:
            kiz_dosya.write(','.join(self.kizlar))

        with open("data_dosyaları/bin/erkekler.txt", "w", encoding="utf-8") as erkek_dosya:
            erkek_dosya.write(','.join(self.erkekler))

        messagebox.showinfo("Başarı", "Öğrenciler başarıyla sıralandı ve kaydedildi.")

        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.entry_default_text)

    def clear_entry_default_text(self, event):
        if self.entry.get() == self.entry_default_text:
            self.entry.delete(0, tk.END)

    def restore_entry_default_text(self, event):
        if not self.entry.get():
            self.entry.insert(tk.END, self.entry_default_text)

    def cinsiyet_sor(self, ogrenci):
        cevap = messagebox.askquestion("Cinsiyet Seçimi", f"{ogrenci} ismi Erkek mi ?", icon='info')
        if cevap.lower() == 'yes':
            return 'e'
        else:
            return 'k'

    def ayarlar_ac(self):
        ayarlar_pencere = tk.Toplevel(self.root)
        AyarlarPenceresi(ayarlar_pencere, self)

    def program_hakkinda_ac(self):
        program_hakkinda_pencere = tk.Toplevel(self.root)
        ProgramHakkindaPenceresi(program_hakkinda_pencere)

if __name__ == "__main__":
    root = tk.Tk()
    app = OgrenciSiralamaApp(root)
    root.mainloop()
