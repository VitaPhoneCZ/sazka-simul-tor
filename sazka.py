import tkinter as tk
from tkinter import messagebox, Toplevel, Button, Label, Checkbutton, Radiobutton, IntVar, BooleanVar, Spinbox, Text, Scrollbar, ttk
import random
from itertools import combinations
from math import comb
import os
from datetime import datetime
import threading
import time

# ─────────────────────── NASTAVENÍ ───────────────────────
SOUBOR_TICKET = "ticket.txt"
CENA_KOMBINACE = 20
CENA_SANCE = 20

# ─────────────────────── HLAVNÍ APLIKACE ───────────────────────
class SportkaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.tk.call("tk", "scaling", 2.0)
        self.root.title("Sportka od Sazky")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Moderní barevné schéma
        self.bg_color = "#1a1a1a"
        self.primary_color = "#FF8C00"
        self.secondary_color = "#FFD700"
        self.accent_blue = "#0078D4"
        self.accent_green = "#107C10"
        self.accent_red = "#D13438"
        self.text_color = "#ffffff"
        self.card_bg = "#2d2d2d"
        
        self.root.config(bg=self.bg_color)

        # Hlavní nadpis s lepším designem
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(pady=(50, 30))
        
        tk.Label(header_frame, text="🎲 SPORTKA", font=("Arial", 32, "bold"), 
                bg=self.bg_color, fg=self.primary_color).pack()
        tk.Label(header_frame, text="SAZKA", font=("Arial", 18, "bold"), 
                bg=self.bg_color, fg=self.text_color).pack(pady=(5, 0))

        # Tlačítka s modernějším designem
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(pady=20)
        
        self.create_modern_button(buttons_frame, "🎫 Ticket", self.primary_color, 
                                 self.otevri_ticket, width=40, height=3).pack(pady=15)
        
        # Rámeček pro Slosovat a Auto Jackpot
        slosovani_frame = tk.Frame(buttons_frame, bg=self.bg_color)
        slosovani_frame.pack(pady=15)
        
        self.create_modern_button(slosovani_frame, "🎰 Slosovat", self.accent_blue, 
                                 self.slosovani, width=30, height=3).pack(side="left", padx=(0, 5))
        self.create_modern_button(slosovani_frame, "🎯", self.secondary_color, 
                                 self.slosuj_do_jackpotu, width=5, height=3).pack(side="left", padx=(0, 5))
        self.create_modern_button(slosovani_frame, "⚡", "#9C27B0", 
                                 self.benchmark_rychlost, width=5, height=3).pack(side="left")
        
        self.create_modern_button(buttons_frame, "🖨️ Tisk", self.accent_green, 
                                 self.tisk, width=40, height=3).pack(pady=15)
        self.create_modern_button(buttons_frame, "🔄 Reset", self.accent_red, 
                                 self.reset, width=40, height=3).pack(pady=15)
        
        # Flag pro zastavení auto slosování
        self.stop_auto_slosovani = False

        self.root.mainloop()
    
    def create_modern_button(self, parent, text, bg_color, command, width=30, height=2):
        """Vytvoří moderní tlačítko s hover efektem"""
        btn = Button(parent, text=text, font=("Arial", 12, "bold"), 
                    width=width, height=height, bg=bg_color, fg="white", 
                    relief="flat", bd=0, cursor="hand2", command=command,
                    activebackground=self.lighten_color(bg_color),
                    activeforeground="white")
        
        def on_enter(e):
            btn.config(bg=self.lighten_color(bg_color))
        def on_leave(e):
            btn.config(bg=bg_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn
    
    def lighten_color(self, color):
        """Zesvětlí barvu pro hover efekt"""
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        rgb = tuple(min(255, c + 30) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    # ─────────────────────── OTEVŘENÍ TICKETU ───────────────────────
    def otevri_ticket(self):
        if hasattr(self, 'ticket_window') and self.ticket_window.winfo_exists():
            self.ticket_window.lift()
            return

        self.ticket_window = Toplevel(self.root)
        self.ticket_window.title("Vyplň ticket Sportky")
        self.ticket_window.geometry("1800x1200")
        self.ticket_window.resizable(True, True)
        self.ticket_window.config(bg="#f5f5f5")

        canvas = tk.Canvas(self.ticket_window, bg="#f5f5f5", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.ticket_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.main_container = tk.Frame(canvas, bg="#f5f5f5")
        canvas.create_window((0, 0), window=self.main_container, anchor="nw")

        def nastav_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.main_container.bind("<Configure>", nastav_scrollregion)

        # Kolečko myši
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        # Nadpisy
        header_card = tk.Frame(self.main_container, bg=self.primary_color, relief="flat", bd=0)
        header_card.pack(fill="x", pady=(20, 30), padx=20)
        tk.Label(header_card, text="🎲 SPORTKA", font=("Arial", 28, "bold"), 
                bg=self.primary_color, fg="white").pack(pady=(15, 5))
        tk.Label(header_card, text="SAZKA", font=("Arial", 18, "bold"), 
                bg=self.primary_color, fg="white").pack(pady=(0, 15))

        self.vars = [{} for _ in range(10)]
        self.pocet_labels = []
        self.cena_label_var = tk.StringVar(value="Celková cena: 0 Kč")

        # Zobrazení ceny
        cena_frame = tk.Frame(self.main_container, bg="#f5f5f5")
        cena_frame.pack(pady=(0, 20))
        tk.Label(cena_frame, textvariable=self.cena_label_var, 
                font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#2d2d2d").pack()

        # 5 řádků × 2 sloupce
        for radek in range(5):
            row_frame = tk.Frame(self.main_container, bg="#f5f5f5")
            row_frame.pack(pady=20)

            for pozice in range(2):
                idx = radek * 2 + pozice
                # Karta pro každý sloupec
                sloupec_frame = tk.Frame(row_frame, bg="white", relief="flat", bd=0)
                sloupec_frame.pack(side="left", padx=30, pady=10, fill="both", expand=True)
                
                # Stínový efekt pomocí rámečku
                shadow = tk.Frame(sloupec_frame, bg="#e0e0e0")
                shadow.place(x=3, y=3, relwidth=1, relheight=1)
                sloupec_frame.lift()

                inner_frame = tk.Frame(sloupec_frame, bg="white")
                inner_frame.pack(fill="both", expand=True, padx=10, pady=10)

                tk.Label(inner_frame, text=f"Sloupec {idx+1}", 
                        font=("Arial", 12, "bold"), bg="white", fg="#2d2d2d").pack(pady=(5, 0))

                var_pocet = tk.StringVar(value="0 čísel vybráno")
                self.pocet_labels.append(var_pocet)
                tk.Label(inner_frame, textvariable=var_pocet, 
                        font=("Arial", 9), bg="white", fg="#666666").pack(pady=5)

                btns = tk.Frame(inner_frame, bg="white")
                btns.pack(pady=5)
                Button(btns, text="🎲 Náhodný", font=("Arial", 8), bg="#0078D4", fg="white",
                       relief="flat", bd=0, cursor="hand2",
                       command=lambda s=idx: self.nahodny_tip(s),
                       activebackground="#005a9e", activeforeground="white").pack(side="left", padx=3)
                Button(btns, text="🗑️ Smazat", font=("Arial", 8), bg="#D13438", fg="white",
                       relief="flat", bd=0, cursor="hand2",
                       command=lambda s=idx: self.clear_sloupec(s),
                       activebackground="#a0262a", activeforeground="white").pack(side="left", padx=3)

                grid = tk.Frame(inner_frame, bg="white")
                grid.pack(pady=10)
                for r in range(7):
                    for c in range(7):
                        cislo = r * 7 + c + 1
                        if cislo > 49: continue
                        var = tk.IntVar()
                        self.vars[idx][cislo] = var
                        chk = tk.Checkbutton(grid,
                                           text=str(cislo).zfill(2),
                                           variable=var,
                                           indicatoron=False,
                                           bg="#f0f0f0", fg="#2d2d2d",
                                           selectcolor="#4CAF50",
                                           font=("Arial", 9, "bold"),
                                           width=4, height=2,
                                           bd=1, relief="flat",
                                           cursor="hand2",
                                           activebackground="#4CAF50",
                                           activeforeground="white",
                                           command=lambda s=idx: self.update_count(s))
                        chk.grid(row=r, column=c, padx=2, pady=2)

        # Dolní lišta s nastavením
        dolni_card = tk.Frame(self.main_container, bg="white", relief="flat", bd=0)
        dolni_card.pack(fill="x", pady=(30, 20), padx=20)
        
        shadow_dolni = tk.Frame(dolni_card, bg="#e0e0e0")
        shadow_dolni.place(x=3, y=3, relwidth=1, relheight=1)
        dolni_card.lift()
        
        dolni = tk.Frame(dolni_card, bg="white")
        dolni.pack(fill="both", expand=True, padx=20, pady=20)

        # Slosování
        slos_frame = tk.LabelFrame(dolni, text="📅 Slosování", font=("Arial", 11, "bold"),
                                   bg="white", fg="#2d2d2d", relief="flat", bd=1)
        slos_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.streda_var = BooleanVar(value=True)
        self.patek_var = BooleanVar(value=True)
        self.nedele_var = BooleanVar(value=True)

        dni = tk.Frame(slos_frame, bg="white")
        dni.pack(pady=10)
        Checkbutton(dni, text="Středeční", variable=self.streda_var, bg="white", 
                   font=("Arial", 10), selectcolor="#4CAF50").pack(side="left", padx=10)
        Checkbutton(dni, text="Páteční", variable=self.patek_var, bg="white", 
                   font=("Arial", 10), selectcolor="#4CAF50").pack(side="left", padx=10)
        Checkbutton(dni, text="Nedělní", variable=self.nedele_var, bg="white", 
                   font=("Arial", 10), selectcolor="#4CAF50").pack(side="left", padx=10)

        pocet_frame = tk.Frame(slos_frame, bg="white")
        pocet_frame.pack(pady=10)
        tk.Label(pocet_frame, text="Počet slosování:", font=("Arial", 10), bg="white").pack(side="left", padx=5)
        self.pocet_slos_var = IntVar(value=1)
        Spinbox(pocet_frame, from_=1, to=52, width=8, font=("Arial", 10), 
               textvariable=self.pocet_slos_var, command=self.update_cena).pack(side="left", padx=5)

        # Šance
        sance_frame = tk.LabelFrame(dolni, text="🎯 Šance", font=("Arial", 11, "bold"),
                                    bg="white", fg="#2d2d2d", relief="flat", bd=1)
        sance_frame.pack(side="right", fill="both", expand=True, padx=10)
        self.sance_var = IntVar(value=0)
        rb = tk.Frame(sance_frame, bg="white")
        rb.pack(pady=20)
        Radiobutton(rb, text="Ano", variable=self.sance_var, value=1, bg="white", 
                   selectcolor="#4CAF50", font=("Arial", 10, "bold"),
                   command=self.update_cena).pack(side="left", padx=15)
        Radiobutton(rb, text="Ne", variable=self.sance_var, value=0, bg="white", 
                   selectcolor="#4CAF50", font=("Arial", 10, "bold"),
                   command=self.update_cena).pack(side="left", padx=15)

        # Tlačítka
        buttons_bottom = tk.Frame(dolni, bg="white")
        buttons_bottom.pack(fill="x", pady=(20, 0))
        
        Button(buttons_bottom, text="🎲 NÁHODNÝ CELÝ TICKET", font=("Arial", 10, "bold"),
               bg=self.secondary_color, fg="black", relief="flat", bd=0, cursor="hand2",
               command=self.nahodny_cely_ticket,
               activebackground="#e6c200", activeforeground="black").pack(side="left", padx=5, fill="x", expand=True)
        
        Button(buttons_bottom, text="💾 ULOŽIT SÁZKU", font=("Arial", 12, "bold"), 
               bg="#107C10", fg="white", relief="flat", bd=0, cursor="hand2",
               command=self.uloz_ticket,
               activebackground="#0d630d", activeforeground="white").pack(side="left", padx=5, fill="x", expand=True)
        
        # Aktualizace ceny při změně
        for var in [self.streda_var, self.patek_var, self.nedele_var]:
            try:
                var.trace_add("write", lambda *args: self.update_cena())
            except AttributeError:
                # Fallback pro starší verze Pythonu (< 3.8)
                var.trace("w", lambda *args: self.update_cena())

    # ───── NÁHODNÝ CELÝ TICKET (nezasahuje do Šance) ─────
    def nahodny_cely_ticket(self):
        for sl in range(10):
            for var in self.vars[sl].values():
                var.set(0)
            for c in random.sample(range(1, 50), 6):
                self.vars[sl][c].set(1)
            self.update_count(sl)

        self.streda_var.set(True)
        self.patek_var.set(True)
        self.nedele_var.set(True)
        self.pocet_slos_var.set(1)
        self.sance_var.set(0)
        self.update_cena()

        self.ticket_window.title("Vyplň ticket Sportky – HOTOVO!")
        self.ticket_window.after(800, lambda: self.ticket_window.title("Vyplň ticket Sportky"))
        self.ticket_window.lift()

    # ───── POMOCNÉ FUNKCE ─────
    def update_count(self, sloupec):
        pocet = sum(v.get() for v in self.vars[sloupec].values())
        if pocet > 12:
            # Automaticky odznačit poslední vybrané číslo
            for cislo, var in reversed(list(self.vars[sloupec].items())):
                if var.get() == 1:
                    var.set(0)
                    break
            pocet = 12
            messagebox.showwarning("Limit", "Maximálně 12 čísel na sloupec!")
        
        self.pocet_labels[sloupec].set(f"{pocet} čísel vybráno")
        self.update_cena()
    
    def update_cena(self, *args):
        """Aktualizuje zobrazení ceny v reálném čase"""
        try:
            sloupce = []
            for sl in self.vars:
                vybrana = [c for c, v in sl.items() if v.get()]
                if len(vybrana) >= 6:
                    sloupce.append(vybrana)
            
            pocet_kombinaci = sum(comb(len(tip), 6) if len(tip) >= 6 else 0 for tip in sloupce)
            pocet_slos = self.pocet_slos_var.get() if hasattr(self, 'pocet_slos_var') else 1
            sance = self.sance_var.get() if hasattr(self, 'sance_var') else 0
            
            cena_celkem = pocet_kombinaci * CENA_KOMBINACE * pocet_slos + (CENA_SANCE if sance else 0) * pocet_slos
            self.cena_label_var.set(f"💰 Celková cena: {cena_celkem:,} Kč")
        except:
            pass

    def nahodny_tip(self, sloupec):
        for var in self.vars[sloupec].values():
            var.set(0)
        for c in random.sample(range(1, 50), 6):
            self.vars[sloupec][c].set(1)
        self.update_count(sloupec)
        self.update_cena()

    def clear_sloupec(self, sloupec):
        for var in self.vars[sloupec].values():
            var.set(0)
        self.update_count(sloupec)
        self.update_cena()

    # ───── ULOŽENÍ – OPRAVENÁ ZÁVORKA! ─────
    def uloz_ticket(self):
        if not any(len([c for c, v in sl.items() if v.get()]) >= 6 for sl in self.vars):
            messagebox.showwarning("Chyba", "Vyplň alespoň jeden sloupec (min. 6 čísel)!")
            return

        with open(SOUBOR_TICKET, "w", encoding="utf-8") as f:
            for i, sl in enumerate(self.vars, 1):
                vybrana = [c for c, v in sl.items() if v.get()]
                if len(vybrana) >= 6:
                    f.write(f"Sloupec {i}: {','.join(map(str, sorted(vybrana)))}\n")  # ←←← opraveno!
            f.write(f"Středeční: {'Ano' if self.streda_var.get() else 'Ne'}\n")
            f.write(f"Páteční: {'Ano' if self.patek_var.get() else 'Ne'}\n")
            f.write(f"Nedělní: {'Ano' if self.nedele_var.get() else 'Ne'}\n")
            f.write(f"Počet slosování: {self.pocet_slos_var.get()}\n")
            f.write(f"Šance: {'Ano' if self.sance_var.get() else 'Ne'}\n")
            if self.sance_var.get():
                f.write(f"Šance_číslo: {random.randint(0, 999999):06d}\n")

        messagebox.showinfo("✅ Hotovo", f"Ticket uložen!\n\nCelková cena: {self.vypocitej_cenu():,} Kč")
        self.ticket_window.destroy()
    
    def vypocitej_cenu(self):
        """Vypočítá celkovou cenu ticketu"""
        sloupce = []
        for sl in self.vars:
            vybrana = [c for c, v in sl.items() if v.get()]
            if len(vybrana) >= 6:
                sloupce.append(vybrana)
        pocet_kombinaci = sum(comb(len(tip), 6) if len(tip) >= 6 else 0 for tip in sloupce)
        pocet_slos = self.pocet_slos_var.get()
        sance = self.sance_var.get()
        return pocet_kombinaci * CENA_KOMBINACE * pocet_slos + (CENA_SANCE if sance else 0) * pocet_slos

    def zobraz_progress(self, celkem):
        """Zobrazí progress okno pro dlouhé slosování"""
        progress_window = Toplevel(self.root)
        progress_window.title("Slosování...")
        progress_window.geometry("400x120")
        progress_window.config(bg="#f5f5f5")
        progress_window.resizable(False, False)
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Centrování okna
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (120 // 2)
        progress_window.geometry(f"400x120+{x}+{y}")
        
        label = tk.Label(progress_window, text=f"Slosování 0 / {celkem:,}...", 
                        font=("Arial", 10), bg="#f5f5f5")
        label.pack(pady=(20, 10))
        
        progress = ttk.Progressbar(progress_window, length=350, mode='determinate', maximum=100)
        progress.pack(pady=10)
        
        progress_window.progress = progress
        progress_window.label = label
        progress_window.window = progress_window
        
        return progress_window

    # ───── BENCHMARK RYCHLOSTI ─────
    def benchmark_rychlost(self):
        """Změří rychlost slosování (slosování za sekundu)"""
        if not os.path.exists(SOUBOR_TICKET):
            messagebox.showerror("Chyba", "Nejprve vyplň a ulož ticket!")
            return
        
        # Načtení ticketu
        sloupce = []
        sance = False
        sance_cislo = None
        
        with open(SOUBOR_TICKET, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("Sloupec"):
                    cisla = [int(x) for x in line.split(":")[1].split(",") if x.strip().isdigit()]
                    if len(cisla) >= 6:
                        sloupce.append(sorted(cisla))
                elif "Šance: Ano" in line:
                    sance = True
                elif line.startswith("Šance_číslo:"):
                    sance_cislo = int(line.split(":")[1].strip())
        
        if not sloupce:
            messagebox.showerror("Chyba", "Ticket neobsahuje žádné sloupce!")
            return
        
        # Progress okno
        progress_window = Toplevel(self.root)
        progress_window.title("⚡ Benchmark rychlosti")
        progress_window.geometry("500x200")
        progress_window.config(bg="#f5f5f5")
        progress_window.resizable(False, False)
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Centrování okna
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (200 // 2)
        progress_window.geometry(f"500x200+{x}+{y}")
        
        label = tk.Label(progress_window, text="Měření rychlosti...", 
                        font=("Arial", 12, "bold"), bg="#f5f5f5")
        label.pack(pady=(20, 10))
        
        status_label = tk.Label(progress_window, text="Připravuji...", 
                               font=("Arial", 10), bg="#f5f5f5")
        status_label.pack(pady=5)
        
        # Předpočítání kombinací a setů
        kombinace_sloupcu = []
        kombinace_sety = []
        for tip in sloupce:
            if len(tip) > 6:
                komb_list = list(combinations(tip, 6))
                kombinace_sloupcu.append(komb_list)
                kombinace_sety.append([set(k) for k in komb_list])
            else:
                komb_tuple = tuple(sorted(tip))
                kombinace_sloupcu.append([komb_tuple])
                kombinace_sety.append([set(komb_tuple)])
        
        cisla_1_49 = list(range(1, 50))
        sance_mods = [10**k for k in range(1, 7)]
        sance_vyhry = {2:40, 3:100, 4:500, 5:10000, 6:200000}
        
        # Benchmark - 3 sekundy měření
        status_label.config(text="Měření rychlosti (3 sekundy)...")
        progress_window.update()
        
        pocet_slos = 0
        start_time = time.time()
        end_time = start_time + 3.0  # 3 sekundy
        
        while time.time() < end_time:
            pocet_slos += 1
            
            # Rychlejší slosování
            tah1 = random.sample(cisla_1_49, 7)
            tah2 = random.sample(cisla_1_49, 7)
            hlavni1_set = set(tah1[:6])
            dod1 = tah1[6]
            hlavni2_set = set(tah2[:6])
            dod2 = tah2[6]
            sance_los = random.randint(0, 999999)
            
            vyhra_slos = 0
            
            # Optimalizovaná kontrola výher
            for komb_sety in kombinace_sety:
                for k_set in komb_sety:
                    # Kontrola prvního tahu
                    shoda = len(k_set & hlavni1_set)
                    if shoda == 6:
                        vyhra_slos += 10_000_000
                    elif shoda == 5:
                        if dod1 in k_set:
                            vyhra_slos += 500_000
                        else:
                            vyhra_slos += 50_000
                    elif shoda == 4:
                        vyhra_slos += 2_000
                    elif shoda == 3:
                        vyhra_slos += 300
                    
                    # Kontrola druhého tahu
                    shoda = len(k_set & hlavni2_set)
                    if shoda == 6:
                        vyhra_slos += 10_000_000
                    elif shoda == 5:
                        if dod2 in k_set:
                            vyhra_slos += 500_000
                        else:
                            vyhra_slos += 50_000
                    elif shoda == 4:
                        vyhra_slos += 2_000
                    elif shoda == 3:
                        vyhra_slos += 300
            
            # Optimalizovaná Šance
            if sance and sance_cislo is not None:
                for k in range(5, -1, -1):
                    mod = sance_mods[k]
                    if (sance_cislo % mod) == (sance_los % mod):
                        shodnych = k + 1
                        if shodnych >= 2:
                            vyhra_slos += sance_vyhry.get(shodnych, 0)
                        break
        
        elapsed_time = time.time() - start_time
        rychlost = pocet_slos / elapsed_time
        
        # Zobrazení výsledků
        result_text = f"⚡ BENCHMARK RYCHLOSTI ⚡\n\n"
        result_text += f"Čas měření: {elapsed_time:.2f} sekund\n"
        result_text += f"Počet slosování: {pocet_slos:,}\n"
        result_text += f"Rychlost: {rychlost:,.0f} slosování/sekundu\n\n"
        result_text += f"To je {rychlost/1000:.1f} tisíc slosování za sekundu!"
        
        label.config(text=result_text, justify="left")
        status_label.config(text="Hotovo!")
        
        # Tlačítko pro zavření
        Button(progress_window, text="Zavřít", font=("Arial", 10, "bold"),
              bg="#0078D4", fg="white", relief="flat", bd=0, cursor="hand2",
              command=progress_window.destroy,
              activebackground="#005a9e", activeforeground="white").pack(pady=15)

    # ───── AUTO SLOSOVÁNÍ DO JACKPOTU ─────
    def slosuj_do_jackpotu(self):
        """Automaticky slosuje dokud nevyhraje jackpot"""
        if not os.path.exists(SOUBOR_TICKET):
            messagebox.showerror("Chyba", "Nejprve vyplň a ulož ticket!")
            return
        
        # Načtení ticketu
        sloupce = []
        sance = False
        sance_cislo = None
        
        with open(SOUBOR_TICKET, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("Sloupec"):
                    cisla = [int(x) for x in line.split(":")[1].split(",") if x.strip().isdigit()]
                    if len(cisla) >= 6:
                        sloupce.append(sorted(cisla))
                elif "Šance: Ano" in line:
                    sance = True
                elif line.startswith("Šance_číslo:"):
                    sance_cislo = int(line.split(":")[1].strip())
        
        if not sloupce:
            messagebox.showerror("Chyba", "Ticket neobsahuje žádné sloupce!")
            return
        
        # Progress okno
        progress_window = Toplevel(self.root)
        progress_window.title("Auto slosování do Jackpotu")
        progress_window.geometry("450x180")
        progress_window.config(bg="#f5f5f5")
        progress_window.resizable(False, False)
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Centrování okna
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (180 // 2)
        progress_window.geometry(f"450x180+{x}+{y}")
        
        label = tk.Label(progress_window, text="Hledám jackpot...", 
                        font=("Arial", 12, "bold"), bg="#f5f5f5")
        label.pack(pady=(20, 10))
        
        pocet_label = tk.Label(progress_window, text="Pokusů: 0", 
                               font=("Arial", 10), bg="#f5f5f5")
        pocet_label.pack(pady=5)
        
        stop_button = Button(progress_window, text="⏹️ Zastavit", 
                            font=("Arial", 10, "bold"), bg="#D13438", fg="white",
                            relief="flat", bd=0, cursor="hand2",
                            command=lambda: setattr(self, 'stop_auto_slosovani', True),
                            activebackground="#a0262a", activeforeground="white")
        stop_button.pack(pady=10)
        
        self.stop_auto_slosovani = False
        
        # Předpočítání kombinací a setů pro rychlejší výpočet
        kombinace_sloupcu = []
        kombinace_sety = []  # Předpočítané sety pro rychlejší operace
        for tip in sloupce:
            if len(tip) > 6:
                komb_list = list(combinations(tip, 6))
                kombinace_sloupcu.append(komb_list)
                kombinace_sety.append([set(k) for k in komb_list])
            else:
                komb_tuple = tuple(sorted(tip))
                kombinace_sloupcu.append([komb_tuple])
                kombinace_sety.append([set(komb_tuple)])
        
        pocet_kombinaci = sum(comb(len(tip), 6) if len(tip) >= 6 else 0 for tip in sloupce)
        cena_na_slos = pocet_kombinaci * CENA_KOMBINACE + (CENA_SANCE if sance else 0)
        
        # Předpočítání pro rychlejší random generování
        cisla_1_49 = list(range(1, 50))
        
        # Předpočítání pro Šance (matematické operace místo string)
        sance_mods = [10**k for k in range(1, 7)]  # [10, 100, 1000, 10000, 100000, 1000000]
        sance_vyhry = {2:40, 3:100, 4:500, 5:10000, 6:200000}
        
        pokusu = 0
        celkova_vyhra = 0
        nejlepsi_vyhra = 0
        nejlepsi_pokus = 0
        
        # Hlavní smyčka - optimalizovaná
        while not self.stop_auto_slosovani:
            pokusu += 1
            
            # Aktualizace UI méně často pro lepší výkon
            if pokusu % 1000 == 0:
                pocet_label.config(text=f"Pokusů: {pokusu:,}")
                progress_window.update()
            
            # Rychlejší slosování - použití random.choices místo sample pro rychlost
            tah1 = random.sample(cisla_1_49, 7)
            tah2 = random.sample(cisla_1_49, 7)
            hlavni1_set = set(tah1[:6])
            hlavni1_list = sorted(tah1[:6])
            dod1 = tah1[6]
            hlavni2_set = set(tah2[:6])
            hlavni2_list = sorted(tah2[:6])
            dod2 = tah2[6]
            sance_los = random.randint(0, 999999)
            
            vyhra_slos = 0
            jackpot = False
            
            # Optimalizovaná kontrola výher s předpočítanými sety
            for i, (komb_list, komb_sety) in enumerate(zip(kombinace_sloupcu, kombinace_sety)):
                for k_set in komb_sety:
                    # Kontrola prvního tahu
                    shoda = len(k_set & hlavni1_set)
                    if shoda == 6:
                        vyhra_slos += 10_000_000
                        jackpot = True
                        break
                    elif shoda == 5:
                        if dod1 in k_set:
                            vyhra_slos += 500_000
                        else:
                            vyhra_slos += 50_000
                    elif shoda == 4:
                        vyhra_slos += 2_000
                    elif shoda == 3:
                        vyhra_slos += 300
                    
                    # Kontrola druhého tahu (pokud ještě není jackpot)
                    if not jackpot:
                        shoda = len(k_set & hlavni2_set)
                        if shoda == 6:
                            vyhra_slos += 10_000_000
                            jackpot = True
                            break
                        elif shoda == 5:
                            if dod2 in k_set:
                                vyhra_slos += 500_000
                            else:
                                vyhra_slos += 50_000
                        elif shoda == 4:
                            vyhra_slos += 2_000
                        elif shoda == 3:
                            vyhra_slos += 300
                if jackpot:
                    break
            
            # Optimalizovaná Šance - matematické operace místo string
            vyhra_sance = 0
            if sance and sance_cislo is not None:
                for k in range(5, -1, -1):  # 5, 4, 3, 2, 1, 0
                    mod = sance_mods[k]
                    if (sance_cislo % mod) == (sance_los % mod):
                        shodnych = k + 1
                        if shodnych >= 2:
                            vyhra_sance = sance_vyhry.get(shodnych, 0)
                        break
            
            # Uložení hlavních hodnot pro zobrazení
            if jackpot:
                hlavni1 = hlavni1_list
                hlavni2 = hlavni2_list
            
            celkova_vyhra_slos = vyhra_slos + vyhra_sance
            celkova_vyhra += celkova_vyhra_slos
            
            if celkova_vyhra_slos > nejlepsi_vyhra:
                nejlepsi_vyhra = celkova_vyhra_slos
                nejlepsi_pokus = pokusu
            
            # Pokud je jackpot, ukončit
            if jackpot:
                progress_window.destroy()
                cena_celkem = cena_na_slos * pokusu
                
                # Zobrazení výsledků
                vysledek = f"🎉 JACKPOT VYHRÁN! 🎉\n\n"
                vysledek += f"Počet pokusů: {pokusu:,}\n"
                vysledek += f"Celkem vsazeno: {cena_celkem:,} Kč\n"
                vysledek += f"Celkem vyhráno: {celkova_vyhra:,} Kč\n"
                vysledek += f"Zisk: +{celkova_vyhra - cena_celkem:,} Kč\n\n"
                vysledek += f"1. tah: {hlavni1} + {dod1}\n"
                vysledek += f"2. tah: {hlavni2} + {dod2}\n"
                vysledek += f"Šance: {sance_los:06d}\n"
                
                messagebox.showinfo("🎉 JACKPOT!", vysledek)
                break
        
        if self.stop_auto_slosovani:
            progress_window.destroy()
            cena_celkem = cena_na_slos * pokusu
            vysledek = f"Slosování zastaveno po {pokusu:,} pokusech\n\n"
            vysledek += f"Celkem vsazeno: {cena_celkem:,} Kč\n"
            vysledek += f"Celkem vyhráno: {celkova_vyhra:,} Kč\n"
            if nejlepsi_vyhra > 0:
                vysledek += f"Nejlepší výhra: {nejlepsi_vyhra:,} Kč (v pokusu #{nejlepsi_pokus:,})\n"
            messagebox.showinfo("Zastaveno", vysledek)
        
        self.stop_auto_slosovani = False

    # ───── SLOSOVÁNÍ ─────
    def slosovani(self):
        if not os.path.exists(SOUBOR_TICKET):
            messagebox.showerror("Chyba", "Nejprve vyplň a ulož ticket!")
            return

        sloupce = []
        sance = False
        sance_cislo = None
        pocet_slos = 1

        with open(SOUBOR_TICKET, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("Sloupec"):
                    cisla = [int(x) for x in line.split(":")[1].split(",") if x.strip().isdigit()]
                    if len(cisla) >= 6:
                        sloupce.append(sorted(cisla))
                elif "Šance: Ano" in line:
                    sance = True
                elif line.startswith("Šance_číslo:"):
                    sance_cislo = int(line.split(":")[1].strip())
                elif line.startswith("Počet slosování:"):
                    pocet_slos = int(line.split(":")[1].strip())

        pocet_kombinaci = sum(comb(len(tip), 6) if len(tip) >= 6 else 0 for tip in sloupce)
        cena_na_slos = pocet_kombinaci * CENA_KOMBINACE + (CENA_SANCE if sance else 0)
        cena_celkem = cena_na_slos * pocet_slos

        # Pro velký počet slosování použijeme optimalizovaný režim
        optimalizovany_rezim = pocet_slos > 1000
        
        if optimalizovany_rezim:
            # Zobrazit progress okno
            progress_window = self.zobraz_progress(pocet_slos)
            self.root.update()

        # Optimalizace: ukládáme jen základní data, detaily jen pro top/bottom N
        TOP_N = 50  # Počet nejlepších a nejhorších pro detailní zobrazení
        vysledky_slosovani = []  # Pouze základní data: cislo, vyhra, vydel
        top_vysledky = []  # Top N s detaily
        bottom_vysledky = []  # Bottom N s detaily
        
        celkova_vyhra = 0
        statistika = {
            'jackpot': 0, '5plus': 0, '5': 0, '4': 0, '3': 0,
            'sance_6': 0, 'sance_5': 0, 'sance_4': 0, 'sance_3': 0, 'sance_2': 0
        }

        # Optimalizovaný výpočet kombinací - předpočítat jednou včetně setů
        kombinace_sloupcu = []
        kombinace_sety = []  # Předpočítané sety pro rychlejší operace
        for tip in sloupce:
            if len(tip) > 6:
                komb_list = list(combinations(tip, 6))
                kombinace_sloupcu.append(komb_list)
                kombinace_sety.append([set(k) for k in komb_list])
            else:
                komb_tuple = tuple(sorted(tip))
                kombinace_sloupcu.append([komb_tuple])
                kombinace_sety.append([set(komb_tuple)])
        
        # Předpočítání pro rychlejší random generování
        cisla_1_49 = list(range(1, 50))
        
        # Předpočítání pro Šance (matematické operace místo string)
        sance_mods = [10**k for k in range(1, 7)]  # [10, 100, 1000, 10000, 100000, 1000000]
        sance_vyhry = {2:40, 3:100, 4:500, 5:10000, 6:200000}

        # Provedení všech slosování
        for slos in range(pocet_slos):
            if optimalizovany_rezim and slos % max(1, pocet_slos // 100) == 0:
                progress_window.progress['value'] = (slos / pocet_slos) * 100
                progress_window.label.config(text=f"Slosování {slos:,} / {pocet_slos:,}...")
                self.root.update()

            # Rychlejší slosování s předpočítaným seznamem
            tah1 = random.sample(cisla_1_49, 7)
            tah2 = random.sample(cisla_1_49, 7)
            hlavni1_set = set(tah1[:6])
            hlavni1_list = sorted(tah1[:6])
            dod1 = tah1[6]
            hlavni2_set = set(tah2[:6])
            hlavni2_list = sorted(tah2[:6])
            dod2 = tah2[6]
            sance_los = random.randint(0, 999999)

            vyhra_slos = 0
            # Detaily vytváříme jen pokud nejsme v optimalizovaném režimu nebo pokud máme málo záznamů
            potrebujeme_detaily = not optimalizovany_rezim or len(top_vysledky) < TOP_N * 2 or len(bottom_vysledky) < TOP_N * 2
            detaily = [] if potrebujeme_detaily else None

            # Optimalizovaný výpočet výher s předpočítanými sety
            for i, (komb_list, komb_sety) in enumerate(zip(kombinace_sloupcu, kombinace_sety), 1):
                for k_set in komb_sety:
                    # Kontrola prvního tahu
                    shoda = len(k_set & hlavni1_set)
                    if shoda == 6:
                        vyhra = 10_000_000
                        statistika['jackpot'] += 1
                        vyhra_slos += vyhra
                        if potrebujeme_detaily:
                            detaily.append(f"SL {i}: 6 ČÍSEL → JACKPOT 10 000 000 Kč!!!")
                    elif shoda == 5:
                        if dod1 in k_set:
                            vyhra = 500_000
                            statistika['5plus'] += 1
                            vyhra_slos += vyhra
                            if potrebujeme_detaily:
                                detaily.append(f"SL {i}: 5 + dod. → 500 000 Kč")
                        else:
                            vyhra = 50_000
                            statistika['5'] += 1
                            vyhra_slos += vyhra
                            if potrebujeme_detaily:
                                detaily.append(f"SL {i}: 5 čísel → 50 000 Kč")
                    elif shoda == 4:
                        vyhra = 2_000
                        statistika['4'] += 1
                        vyhra_slos += vyhra
                        if potrebujeme_detaily:
                            detaily.append(f"SL {i}: 4 čísla → 2 000 Kč")
                    elif shoda == 3:
                        vyhra = 300
                        statistika['3'] += 1
                        vyhra_slos += vyhra
                        if potrebujeme_detaily:
                            detaily.append(f"SL {i}: 3 čísla → 300 Kč")
                    
                    # Kontrola druhého tahu
                    shoda = len(k_set & hlavni2_set)
                    if shoda == 6:
                        vyhra = 10_000_000
                        statistika['jackpot'] += 1
                        vyhra_slos += vyhra
                        if potrebujeme_detaily:
                            detaily.append(f"SL {i}: 6 ČÍSEL → JACKPOT 10 000 000 Kč!!!")
                    elif shoda == 5:
                        if dod2 in k_set:
                            vyhra = 500_000
                            statistika['5plus'] += 1
                            vyhra_slos += vyhra
                            if potrebujeme_detaily:
                                detaily.append(f"SL {i}: 5 + dod. → 500 000 Kč")
                        else:
                            vyhra = 50_000
                            statistika['5'] += 1
                            vyhra_slos += vyhra
                            if potrebujeme_detaily:
                                detaily.append(f"SL {i}: 5 čísel → 50 000 Kč")
                    elif shoda == 4:
                        vyhra = 2_000
                        statistika['4'] += 1
                        vyhra_slos += vyhra
                        if potrebujeme_detaily:
                            detaily.append(f"SL {i}: 4 čísla → 2 000 Kč")
                    elif shoda == 3:
                        vyhra = 300
                        statistika['3'] += 1
                        vyhra_slos += vyhra
                        if potrebujeme_detaily:
                            detaily.append(f"SL {i}: 3 čísla → 300 Kč")

            # Optimalizovaná Šance - matematické operace místo string
            vyhra_sance = 0
            if sance and sance_cislo is not None:
                for k in range(5, -1, -1):  # 5, 4, 3, 2, 1, 0
                    mod = sance_mods[k]
                    if (sance_cislo % mod) == (sance_los % mod):
                        shodnych = k + 1
                        if shodnych >= 2:
                            vyhra_sance = sance_vyhry.get(shodnych, 0)
                            if shodnych == 6:
                                statistika['sance_6'] += 1
                            elif shodnych == 5:
                                statistika['sance_5'] += 1
                            elif shodnych == 4:
                                statistika['sance_4'] += 1
                            elif shodnych == 3:
                                statistika['sance_3'] += 1
                            elif shodnych == 2:
                                statistika['sance_2'] += 1
                            if potrebujeme_detaily:
                                detaily.append(f"ŠANCE: {shodnych} koncovek → {vyhra_sance:,} Kč!")
                        break
            
            # Uložení hlavních hodnot pro zobrazení
            hlavni1 = hlavni1_list
            hlavni2 = hlavni2_list

            celkova_vyhra_slos = vyhra_slos + vyhra_sance
            vydel = celkova_vyhra_slos - cena_na_slos
            celkova_vyhra += celkova_vyhra_slos

            # Uložení základních dat (vždy)
            vysledky_slosovani.append({
                'cislo': slos + 1,
                'vyhra': celkova_vyhra_slos,
                'vydel': vydel
            })

            # Uložení detailních dat pouze pro potenciální top/bottom
            # V optimalizovaném režimu ukládáme detaily jen pokud je to potřeba
            if not optimalizovany_rezim:
                # Pro malý počet - ukládáme všechno
                top_vysledky.append({
                    'cislo': slos + 1,
                    'tah1': hlavni1,
                    'dod1': dod1,
                    'tah2': hlavni2,
                    'dod2': dod2,
                    'sance_los': sance_los,
                    'vyhra': celkova_vyhra_slos,
                    'vydel': vydel,
                    'detaily': detaily if detaily is not None else []
                })
                bottom_vysledky.append({
                    'cislo': slos + 1,
                    'tah1': hlavni1,
                    'dod1': dod1,
                    'tah2': hlavni2,
                    'dod2': dod2,
                    'sance_los': sance_los,
                    'vyhra': celkova_vyhra_slos,
                    'vydel': vydel,
                    'detaily': detaily if detaily is not None else []
                })
            else:
                # Optimalizovaný režim - ukládáme jen pokud je to potenciálně top/bottom
                # Top: ukládáme pokud je výdělek kladný nebo pokud máme málo záznamů
                if vydel >= 0 or len(top_vysledky) < TOP_N:
                    top_vysledky.append({
                        'cislo': slos + 1,
                        'tah1': hlavni1,
                        'dod1': dod1,
                        'tah2': hlavni2,
                        'dod2': dod2,
                        'sance_los': sance_los,
                        'vyhra': celkova_vyhra_slos,
                        'vydel': vydel,
                        'detaily': detaily if detaily is not None else []
                    })
                    # Udržet jen top N
                    if len(top_vysledky) > TOP_N * 2:
                        top_vysledky.sort(key=lambda x: x['vydel'], reverse=True)
                        top_vysledky = top_vysledky[:TOP_N]

                # Bottom: ukládáme pokud je výdělek záporný nebo pokud máme málo záznamů
                if vydel < 0 or len(bottom_vysledky) < TOP_N:
                    bottom_vysledky.append({
                        'cislo': slos + 1,
                        'tah1': hlavni1,
                        'dod1': dod1,
                        'tah2': hlavni2,
                        'dod2': dod2,
                        'sance_los': sance_los,
                        'vyhra': celkova_vyhra_slos,
                        'vydel': vydel,
                        'detaily': detaily if detaily is not None else []
                    })
                    # Udržet jen bottom N
                    if len(bottom_vysledky) > TOP_N * 2:
                        bottom_vysledky.sort(key=lambda x: x['vydel'])
                        bottom_vysledky = bottom_vysledky[:TOP_N]

        if optimalizovany_rezim:
            progress_window.progress['value'] = 100
            progress_window.label.config(text="Dokončuji...")
            self.root.update()

        # Seřazení podle výdělku (od nejlepšího k nejhoršímu)
        vysledky_slosovani.sort(key=lambda x: x['vydel'], reverse=True)
        
        # Seřazení top a bottom
        top_vysledky.sort(key=lambda x: x['vydel'], reverse=True)
        bottom_vysledky.sort(key=lambda x: x['vydel'])
        top_vysledky = top_vysledky[:TOP_N]
        bottom_vysledky = bottom_vysledky[:TOP_N]

        if optimalizovany_rezim:
            progress_window.window.destroy()

        # Sestavení textu výsledků
        vysledek = f"Vsazeno celkem: {cena_celkem:,} Kč\n"
        vysledek += f"Počet slosování: {pocet_slos:,}\n"
        vysledek += f"Cena na slosování: {cena_na_slos:,} Kč\n\n"
        
        if optimalizovany_rezim:
            vysledek += "=" * 70 + "\n"
            vysledek += "SOUHRNNÉ STATISTIKY\n"
            vysledek += "=" * 70 + "\n\n"
            vysledek += f"🎰 Jackpot (6 čísel): {statistika['jackpot']:,}x\n"
            vysledek += f"💰 5 + dodatečné: {statistika['5plus']:,}x\n"
            vysledek += f"💵 5 čísel: {statistika['5']:,}x\n"
            vysledek += f"💶 4 čísla: {statistika['4']:,}x\n"
            vysledek += f"💷 3 čísla: {statistika['3']:,}x\n"
            if sance:
                vysledek += f"\n🎯 Šance:\n"
                vysledek += f"  6 koncovek: {statistika['sance_6']:,}x\n"
                vysledek += f"  5 koncovek: {statistika['sance_5']:,}x\n"
                vysledek += f"  4 koncovek: {statistika['sance_4']:,}x\n"
                vysledek += f"  3 koncovek: {statistika['sance_3']:,}x\n"
                vysledek += f"  2 koncovek: {statistika['sance_2']:,}x\n"
            vysledek += "\n" + "=" * 70 + "\n"
            vysledek += f"TOP {TOP_N} NEJLEPŠÍCH SLOSOVÁNÍ\n"
            vysledek += "=" * 70 + "\n\n"
        else:
            vysledek += "=" * 70 + "\n"
            vysledek += "VÝSLEDKY SEŘAZENÉ PODLE VÝDĚLKU (nejlepší nahoře)\n"
            vysledek += "=" * 70 + "\n\n"

        # Zobrazení top výsledků
        for idx, slos_data in enumerate(top_vysledky, 1):
            puvodni_poradi = next((i for i, v in enumerate(vysledky_slosovani, 1) if v['cislo'] == slos_data['cislo']), idx)
            vysledek += f"═════ POŘADÍ #{puvodni_poradi} - SLOSOVÁNÍ #{slos_data['cislo']} ═════\n"
            vysledek += f"1. tah: {slos_data['tah1']} + {slos_data['dod1']}\n"
            vysledek += f"2. tah: {slos_data['tah2']} + {slos_data['dod2']}\n"
            vysledek += f"Šance: {slos_data['sance_los']:06d}\n"
            
            if slos_data['detaily']:
                vysledek += "\nVýhry:\n"
                for detail in slos_data['detaily']:
                    vysledek += f"  • {detail}\n"
            else:
                vysledek += "\nŽádné výhry\n"
            
            vysledek += f"\n💰 Vyhráno: {slos_data['vyhra']:,} Kč\n"
            if slos_data['vydel'] > 0:
                vysledek += f"🎉 ZISK: +{slos_data['vydel']:,} Kč\n"
            elif slos_data['vydel'] < 0:
                vysledek += f"😔 ZTRÁTA: {slos_data['vydel']:,} Kč\n"
            else:
                vysledek += f"➖ REMÍZA: 0 Kč\n"
            
            vysledek += "—" * 70 + "\n\n"

        if optimalizovany_rezim:
            vysledek += "\n" + "=" * 70 + "\n"
            vysledek += f"BOTTOM {TOP_N} NEJHORŠÍCH SLOSOVÁNÍ\n"
            vysledek += "=" * 70 + "\n\n"
            
            # Zobrazení bottom výsledků
            for idx, slos_data in enumerate(reversed(bottom_vysledky), 1):
                puvodni_poradi = next((i for i, v in enumerate(vysledky_slosovani, 1) if v['cislo'] == slos_data['cislo']), len(vysledky_slosovani) - idx + 1)
                vysledek += f"═════ POŘADÍ #{puvodni_poradi} - SLOSOVÁNÍ #{slos_data['cislo']} ═════\n"
                vysledek += f"1. tah: {slos_data['tah1']} + {slos_data['dod1']}\n"
                vysledek += f"2. tah: {slos_data['tah2']} + {slos_data['dod2']}\n"
                vysledek += f"Šance: {slos_data['sance_los']:06d}\n"
                
                if slos_data['detaily']:
                    vysledek += "\nVýhry:\n"
                    for detail in slos_data['detaily']:
                        vysledek += f"  • {detail}\n"
                else:
                    vysledek += "\nŽádné výhry\n"
                
                vysledek += f"\n💰 Vyhráno: {slos_data['vyhra']:,} Kč\n"
                vysledek += f"😔 ZTRÁTA: {slos_data['vydel']:,} Kč\n"
                vysledek += "—" * 70 + "\n\n"

        vysledek += f"\n{'='*70}\n"
        vysledek += f"CELKEM VSAZENO: {cena_celkem:,} Kč\n"
        vysledek += f"CELKEM VYHRÁNO: {celkova_vyhra:,} Kč\n"
        if celkova_vyhra > cena_celkem:
            vysledek += f"🎉 CELKOVÝ ZISK: +{celkova_vyhra - cena_celkem:,} Kč\n"
        elif celkova_vyhra < cena_celkem:
            vysledek += f"😔 CELKOVÁ ZTRÁTA: -{cena_celkem - celkova_vyhra:,} Kč\n"
        else:
            vysledek += "➖ REMÍZA – vrátil jsi vložené\n"

        # Kombinace top a bottom pro zobrazení
        kombinovane_vysledky = top_vysledky + list(reversed(bottom_vysledky))
        
        # Zobrazení v novém okně s lepším formátováním
        self.zobraz_vysledky(vysledek, cena_celkem, celkova_vyhra, kombinovane_vysledky, optimalizovany_rezim, vysledky_slosovani)
    
    def zobraz_vysledky(self, text, vsazeno, vyhrano, vysledky_slosovani=None, optimalizovany=False, vsechna_data=None):
        """Zobrazí výsledky v novém okně s lepším formátováním"""
        result_window = Toplevel(self.root)
        result_window.title("🎰 Výsledky slosování")
        result_window.geometry("900x750")
        result_window.config(bg="#f5f5f5")
        
        # Hlavička
        header = tk.Frame(result_window, bg=self.primary_color)
        header.pack(fill="x", pady=(0, 20))
        tk.Label(header, text="🎰 VÝSLEDKY SLOSOVÁNÍ", font=("Arial", 20, "bold"),
                bg=self.primary_color, fg="white").pack(pady=15)
        
        # Souhrn
        summary_frame = tk.Frame(result_window, bg="white", relief="flat", bd=0)
        summary_frame.pack(fill="x", padx=20, pady=(0, 20))
        shadow = tk.Frame(summary_frame, bg="#e0e0e0")
        shadow.place(x=3, y=3, relwidth=1, relheight=1)
        summary_frame.lift()
        
        inner_summary = tk.Frame(summary_frame, bg="white")
        inner_summary.pack(fill="both", expand=True, padx=15, pady=15)
        
        tk.Label(inner_summary, text=f"💰 VSAZENO: {vsazeno:,} Kč", 
                font=("Arial", 14, "bold"), bg="white", fg="#2d2d2d").pack(pady=5)
        tk.Label(inner_summary, text=f"🎁 VYHRÁNO: {vyhrano:,} Kč", 
                font=("Arial", 14, "bold"), bg="white", fg="#107C10").pack(pady=5)
        
        rozdil = vyhrano - vsazeno
        if rozdil > 0:
            tk.Label(inner_summary, text=f"🎉 CELKOVÝ ZISK: +{rozdil:,} Kč", 
                    font=("Arial", 16, "bold"), bg="white", fg="#107C10").pack(pady=10)
        elif rozdil < 0:
            tk.Label(inner_summary, text=f"😔 CELKOVÁ ZTRÁTA: {rozdil:,} Kč", 
                    font=("Arial", 16, "bold"), bg="white", fg="#D13438").pack(pady=10)
        else:
            tk.Label(inner_summary, text="➖ REMÍZA", 
                    font=("Arial", 16, "bold"), bg="white", fg="#666666").pack(pady=10)
        
        # Zobrazení top 3 a bottom 3 slosování
        if vysledky_slosovani and len(vysledky_slosovani) > 0:
            top_bottom_frame = tk.Frame(inner_summary, bg="white")
            top_bottom_frame.pack(pady=(15, 0))
            
            # Top 3
            if len(vysledky_slosovani) >= 3:
                top_frame = tk.Frame(top_bottom_frame, bg="#e8f5e9", relief="flat", bd=1)
                top_frame.pack(side="left", padx=5, fill="both", expand=True)
                tk.Label(top_frame, text="🏆 TOP 3", font=("Arial", 10, "bold"), 
                        bg="#e8f5e9", fg="#107C10").pack(pady=5)
                for i, slos in enumerate(vysledky_slosovani[:3], 1):
                    vydel_text = f"+{slos['vydel']:,} Kč" if slos['vydel'] > 0 else f"{slos['vydel']:,} Kč"
                    tk.Label(top_frame, text=f"#{i}: Slosování {slos['cislo']} → {vydel_text}", 
                            font=("Arial", 8), bg="#e8f5e9", fg="#2d2d2d").pack(pady=2)
            
            # Bottom 3
            if len(vysledky_slosovani) >= 3:
                bottom_frame = tk.Frame(top_bottom_frame, bg="#ffebee", relief="flat", bd=1)
                bottom_frame.pack(side="left", padx=5, fill="both", expand=True)
                tk.Label(bottom_frame, text="📉 BOTTOM 3", font=("Arial", 10, "bold"), 
                        bg="#ffebee", fg="#D13438").pack(pady=5)
                # Pro optimalizovaný režim použijeme vsechna_data pro správné pořadí
                if optimalizovany and vsechna_data:
                    bottom_sorted = sorted(vsechna_data, key=lambda x: x['vydel'])
                    for i, slos in enumerate(bottom_sorted[:3], len(vsechna_data)-2):
                        vydel_text = f"{slos['vydel']:,} Kč"
                        tk.Label(bottom_frame, text=f"#{i}: Slosování {slos['cislo']} → {vydel_text}", 
                                font=("Arial", 8), bg="#ffebee", fg="#2d2d2d").pack(pady=2)
                else:
                    for i, slos in enumerate(vysledky_slosovani[-3:], len(vysledky_slosovani)-2):
                        vydel_text = f"+{slos['vydel']:,} Kč" if slos['vydel'] > 0 else f"{slos['vydel']:,} Kč"
                        tk.Label(bottom_frame, text=f"#{i}: Slosování {slos['cislo']} → {vydel_text}", 
                                font=("Arial", 8), bg="#ffebee", fg="#2d2d2d").pack(pady=2)
        
        # Detailní výsledky
        text_frame = tk.Frame(result_window, bg="white", relief="flat", bd=0)
        text_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        shadow2 = tk.Frame(text_frame, bg="#e0e0e0")
        shadow2.place(x=3, y=3, relwidth=1, relheight=1)
        text_frame.lift()
        
        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        text_widget = Text(text_frame, wrap="word", font=("Consolas", 10),
                          bg="white", fg="#2d2d2d", yscrollcommand=scrollbar.set,
                          relief="flat", bd=10)
        text_widget.pack(fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")
        
        # Tlačítko pro uložení
        btn_frame = tk.Frame(result_window, bg="#f5f5f5")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        Button(btn_frame, text="💾 Uložit výsledky", font=("Arial", 10, "bold"),
              bg="#0078D4", fg="white", relief="flat", bd=0, cursor="hand2",
              command=lambda: self.uloz_vysledky(text, vsazeno, vyhrano),
              activebackground="#005a9e", activeforeground="white").pack(side="left", padx=5)
        Button(btn_frame, text="Zavřít", font=("Arial", 10, "bold"),
              bg="#666666", fg="white", relief="flat", bd=0, cursor="hand2",
              command=result_window.destroy,
              activebackground="#4d4d4d", activeforeground="white").pack(side="left", padx=5)
    
    def uloz_vysledky(self, text, vsazeno, vyhrano):
        """Uloží výsledky slosování do souboru"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vysledky_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Výsledky slosování - {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            f.write(text)
        messagebox.showinfo("✅ Uloženo", f"Výsledky uloženy do souboru:\n{filename}")

    # ───── OSTATNÍ ─────
    def tisk(self):
        if not os.path.exists(SOUBOR_TICKET):
            messagebox.showerror("Chyba", "Žádný ticket k tisku!")
            return
        with open("vytisteny_ticket.txt", "w", encoding="utf-8") as f:
            f.write("========== TVŮJ TIKET SPORTKA ==========\n\n")
            with open(SOUBOR_TICKET, "r", encoding="utf-8") as src:
                f.write(src.read())
        messagebox.showinfo("Tisk", "Ticket uložen jako vytisteny_ticket.txt")

    def reset(self):
        if os.path.exists(SOUBOR_TICKET):
            os.remove(SOUBOR_TICKET)
        messagebox.showinfo("Reset", "Vše vymazáno – začínáš znovu!")
        self.root.destroy()
        SportkaApp()

# ───── SPUŠTĚNÍ ─────
SportkaApp()