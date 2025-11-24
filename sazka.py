import tkinter as tk
from tkinter import messagebox, Toplevel, Button, Label, Checkbutton, Radiobutton, IntVar, BooleanVar, Spinbox
import random
from itertools import combinations
from math import comb
import os

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
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        self.root.config(bg="black")

        tk.Label(self.root, text="SPORTKA", font=("Arial", 19, "bold"), bg="black", fg="#FF8C00").pack(pady=(40, 5))
        tk.Label(self.root, text="SAZKA",   font=("Arial", 13, "bold"), bg="black", fg="white").pack(pady=(0, 40))

        Button(self.root, text="Ticket",   font=("Arial", 7, "bold"), width=36, height=6, bg="#FF8C00", fg="white", relief="flat", command=self.otevri_ticket).pack(pady=12)
        Button(self.root, text="Slosovat", font=("Arial", 7, "bold"), width=36, height=6, bg="#0078D4", fg="white", relief="flat", command=self.slosovani).pack(pady=12)
        Button(self.root, text="Tisk",     font=("Arial", 7, "bold"), width=36, height=6, bg="#107C10", fg="white", relief="flat", command=self.tisk).pack(pady=12)
        Button(self.root, text="Reset",    font=("Arial", 7, "bold"), width=36, height=6, bg="#D13438", fg="white", relief="flat", command=self.reset).pack(pady=12)

        self.root.mainloop()

    # ─────────────────────── OTEVŘENÍ TICKETU ───────────────────────
    def otevri_ticket(self):
        if hasattr(self, 'ticket_window') and self.ticket_window.winfo_exists():
            self.ticket_window.lift()
            return

        self.ticket_window = Toplevel(self.root)
        self.ticket_window.title("Vyplň ticket Sportky")
        self.ticket_window.geometry("2200x2000")
        self.ticket_window.resizable(True, True)
        self.ticket_window.config(bg="#FF8C00")

        canvas = tk.Canvas(self.ticket_window, bg="#FF8C00", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.ticket_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.main_container = tk.Frame(canvas, bg="#FF8C00")
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
        tk.Label(self.main_container, text="SPORTKA", font=("Arial", 26, "bold"), bg="#FF8C00", fg="white").pack(pady=(20, 5))
        tk.Label(self.main_container, text="SAZKA",   font=("Arial", 16, "bold"), bg="#FF8C00", fg="black").pack(pady=(0, 30))

        self.vars = [{} for _ in range(10)]
        self.pocet_labels = []

        # 5 řádků × 2 sloupce
        for radek in range(5):
            row_frame = tk.Frame(self.main_container, bg="#FF8C00")
            row_frame.pack(pady=25)

            for pozice in range(2):
                idx = radek * 2 + pozice
                sloupec_frame = tk.Frame(row_frame, bg="#FF8C00", relief="solid", bd=2)
                sloupec_frame.pack(side="left", padx=80)

                tk.Label(sloupec_frame, text=f"{idx+1}.", font=("Arial", 10, "bold"), bg="#FF8C00", fg="black").pack()

                var_pocet = tk.StringVar(value="0 vybráno")
                self.pocet_labels.append(var_pocet)
                tk.Label(sloupec_frame, textvariable=var_pocet, font=("Arial", 6, "bold"), bg="#FF8C00", fg="black").pack(pady=4)

                btns = tk.Frame(sloupec_frame, bg="#FF8C00")
                btns.pack(pady=3)
                Button(btns, text="Náhodný tip", font=("Arial", 4, "bold"), bg="white", fg="black",
                       command=lambda s=idx: self.nahodny_tip(s)).pack(side="left", padx=4)
                Button(btns, text="Smazat sloupec", font=("Arial", 4, "bold"), bg="#CC0000", fg="white",
                       command=lambda s=idx: self.clear_sloupec(s)).pack(side="left")

                grid = tk.Frame(sloupec_frame, bg="#FF8C00")
                grid.pack(pady=8)
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
                                           bg="white", fg="black",
                                           selectcolor="#00CC00",
                                           font=("Arial", 6, "bold"),
                                           width=5, height=2,
                                           bd=2, relief="raised",
                                           command=lambda s=idx: self.update_count(s))
                        chk.grid(row=r, column=c, padx=4, pady=4)

        # Dolní lišta
        dolni = tk.Frame(self.main_container, bg="#FF8C00")
        dolni.pack(fill="x", pady=(40, 20), padx=40)

        # Slosování
        slos_frame = tk.Frame(dolni, bg="#FF8C00")
        slos_frame.pack(side="left")

        tk.Label(slos_frame, text="2. Slosování", font=("Arial", 6, "bold"), bg="#FF8C00").pack()
        self.streda_var = BooleanVar(value=True)
        self.patek_var = BooleanVar(value=True)
        self.nedele_var = BooleanVar(value=True)

        dni = tk.Frame(slos_frame, bg="#FF8C00")
        dni.pack(pady=4)
        Checkbutton(dni, text="Středeční", variable=self.streda_var, bg="#FF8C00", font=("Arial", 6)).pack(side="left", padx=6)
        Checkbutton(dni, text="Páteční",   variable=self.patek_var,   bg="#FF8C00", font=("Arial", 6)).pack(side="left", padx=6)
        Checkbutton(dni, text="Nedělní",   variable=self.nedele_var,   bg="#FF8C00", font=("Arial", 6)).pack(side="left", padx=6)

        pocet_frame = tk.Frame(slos_frame, bg="#FF8C00")
        pocet_frame.pack(pady=(10, 2))
        tk.Label(pocet_frame, text="Počet slosování:", font=("Arial", 6), bg="#FF8C00").pack(side="left")
        self.pocet_slos_var = IntVar(value=1)
        Spinbox(pocet_frame, from_=1, to=52, width=6, font=("Arial", 6), textvariable=self.pocet_slos_var).pack(side="left", padx=(5, 20))

        Button(pocet_frame, text="NÁHODNÝ CELÝ TICKET", font=("Arial", 5, "bold"),
               bg="#FFD700", fg="black", relief="raised",
               command=self.nahodny_cely_ticket).pack(side="left", padx=(30, 0))

        # Šance
        sance_frame = tk.Frame(dolni, bg="#FF8C00")
        sance_frame.pack(side="right")
        tk.Label(sance_frame, text="3. Šance", font=("Arial", 6, "bold"), bg="#FF8C00").pack()
        self.sance_var = IntVar(value=0)
        rb = tk.Frame(sance_frame, bg="#FF8C00")
        rb.pack(pady=4)
        Radiobutton(rb, text="Ano", variable=self.sance_var, value=1, bg="#FF8C00", selectcolor="black", font=("Arial", 6, "bold")).pack(side="left", padx=12)
        Radiobutton(rb, text="Ne",  variable=self.sance_var, value=0, bg="#FF8C00", selectcolor="black", font=("Arial", 6, "bold")).pack(side="left", padx=12)

        Button(dolni, text="ULOŽIT SÁZKU", font=("Arial", 8, "bold"), bg="#006600", fg="white",
               width=44, height=4, command=self.uloz_ticket).pack(pady=20)

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
        self.nedelele_var.set(True)
        self.pocet_slos_var.set(1)

        self.ticket_window.title("Vyplň ticket Sportky – HOTOVO!")
        self.ticket_window.after(800, lambda: self.ticket_window.title("Vyplň ticket Sportky"))
        self.ticket_window.lift()

    # ───── POMOCNÉ FUNKCE ─────
    def update_count(self, sloupec):
        pocet = sum(v.get() for v in self.vars[sloupec].values())
        if pocet > 12:
            messagebox.showwarning("Limit", "Maximálně 12 čísel na sloupec!")
        self.pocet_labels[sloupec].set(f"{pocet} vybráno")

    def nahodny_tip(self, sloupec):
        for var in self.vars[sloupec].values():
            var.set(0)
        for c in random.sample(range(1, 50), 6):
            self.vars[sloupec][c].set(1)
        self.update_count(sloupec)

    def clear_sloupec(self, sloupec):
        for var in self.vars[sloupec].values():
            var.set(0)
        self.update_count(sloupec)

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

        messagebox.showinfo("Hotovo", "Ticket uložen!")
        self.ticket_window.destroy()

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
        cena_celkem = pocet_kombinaci * CENA_KOMBINACE * pocet_slos + (CENA_SANCE if sance else 0) * pocet_slos

        vysledek = f"Vsazeno celkem: {cena_celkem} Kč\n\n"
        celkova_vyhra = 0

        for slos in range(pocet_slos):
            tah1 = random.sample(range(1,50), 7)
            tah2 = random.sample(range(1,50), 7)
            hlavni1, dod1 = sorted(tah1[:6]), tah1[6]
            hlavni2, dod2 = sorted(tah2[:6]), tah2[6]
            sance_los = random.randint(0, 999999)

            vysledek += f"═════ SLOSOVÁNÍ {slos+1}/{pocet_slos} ═════\n"
            vysledek += f"1. tah: {hlavni1} + {dod1}\n"
            vysledek += f"2. tah: {hlavni2} + {dod2}\n"
            vysledek += f"Šance: {sance_los:06d}\n\n"

            for i, tip in enumerate(sloupce, 1):
                komb = list(combinations(tip, 6)) if len(tip) > 6 else [tuple(sorted(tip))]
                for k in komb:
                    ks = set(k)
                    for hlavni, dod in [(hlavni1, dod1), (hlavni2, dod2)]:
                        shoda = len(ks & set(hlavni))
                        if shoda == 6:
                            vyhra = 10_000_000
                            vysledek += f"SL {i}: 6 ČÍSEL → JACKPOT 10 000 000 Kč!!!\n"
                        elif shoda == 5 and dod in ks:
                            vyhra = 500_000
                            vysledek += f"SL {i}: 5 + dod. → 500 000 Kč\n"
                        elif shoda == 5:
                            vyhra = 50_000
                            vysledek += f"SL {i}: 5 čísel → 50 000 Kč\n"
                        elif shoda == 4:
                            vyhra = 2_000
                            vysledek += f"SL {i}: 4 čísla → 2 000 Kč\n"
                        elif shoda == 3:
                            vyhra = 300
                            vysledek += f"SL {i}: 3 čísla → 300 Kč\n"
                        else:
                            vyhra = 0
                        celkova_vyhra += vyhra

            if sance and sance_cislo is not None:
                sc = str(sance_cislo)
                sl = str(sance_los)
                shodnych = 0
                for k in range(6, 0, -1):
                    if sc[-k:] == sl[-k:]:
                        shodnych = k
                        break
                if shodnych >= 2:
                    vyhry = {2:40, 3:100, 4:500, 5:10000, 6:200000}
                    vyhra_s = vyhry.get(shodnych, 0)
                    celkova_vyhra += vyhra_s
                    vysledek += f"ŠANCE: {shodnych} koncovek → {vyhra_s:,} Kč!\n"

            vysledek += "—" * 52 + "\n\n"

        vysledek += f"\nCELKEM VSAZENO: {cena_celkem} Kč\n"
        vysledek += f"CELKEM VYHRÁNO: {celkova_vyhra:,} Kč\n"
        if celkova_vyhra > cena_celkem:
            vysledek += f"→ ZISK: +{celkova_vyhra - cena_celkem:,} Kč\n"
        elif celkova_vyhra < cena_celkem:
            vysledek += f"→ ZTRÁTA: -{cena_celkem - celkova_vyhra:,} Kč\n"
        else:
            vysledek += "→ REMÍZA – vrátil jsi vložené\n"

        messagebox.showinfo("Výsledky slosování", vysledek)

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