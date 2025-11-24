import tkinter as tk
from tkinter import messagebox, Toplevel, Button, Label, Checkbutton, Radiobutton, IntVar, BooleanVar, Spinbox
import random
from itertools import combinations
from math import comb
import os

SOUBOR_TICKET = "ticket.txt"
CENA_KOMB = 20
CENA_SANCE = 20

class SportkaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.tk.call("tk", "scaling", 2.0)          # VŠECHNO 2× větší – super řešení!
        self.root.title("Sportka od Sazky")
        self.root.geometry("900x750")                    # velikost zůstává, ale obsah je 2×
        self.root.resizable(True, True)                 # můžeš okno libovolně měnit
        self.root.config(bg="black")

        tk.Label(self.root, text="SPORTKA", font=("Arial", 19, "bold"), bg="black", fg="#FF8C00").pack(pady=(40, 5))
        tk.Label(self.root, text="SAZKA", font=("Arial", 13, "bold"), bg="black", fg="white").pack(pady=(0, 40))

        Button(self.root, text="Ticket", font=("Arial", 7, "bold"), width=36, height=6, bg="#FF8C00", fg="white", relief="flat", command=self.otevri_ticket).pack(pady=12)
        Button(self.root, text="Slosovat", font=("Arial", 7, "bold"), width=36, height=6, bg="#0078D4", fg="white", relief="flat", command=self.slosovani).pack(pady=12)
        Button(self.root, text="Tisk", font=("Arial", 7, "bold"), width=36, height=6, bg="#107C10", fg="white", relief="flat", command=self.tisk).pack(pady=12)
        Button(self.root, text="Reset", font=("Arial", 7, "bold"), width=36, height=6, bg="#D13438", fg="white", relief="flat", command=self.reset).pack(pady=12)

        self.root.mainloop()

    def otevri_ticket(self):
        if hasattr(self, 'ticket_window') and self.ticket_window.winfo_exists():
            self.ticket_window.lift()
            return

        self.ticket_window = Toplevel(self.root)
        self.ticket_window.title("Vyplň ticket Sportky")
        self.ticket_window.geometry("3200x1900")        # velké okno, vše se vejde i při 2× zvětšení
        self.ticket_window.resizable(True, True)
        self.ticket_window.config(bg="#FF8C00")

        # Nadpisy
        tk.Label(self.ticket_window, text="SPORTKA", font=("Arial", 26, "bold"), bg="#FF8C00", fg="white").pack(pady=(12, 4))
        tk.Label(self.ticket_window, text="SAZKA", font=("Arial", 16, "bold"), bg="#FF8C00", fg="black").pack(pady=(0, 16))

        # Scrollovatelný canvas pro 10 sloupců
        canvas = tk.Canvas(self.ticket_window, bg="#FF8C00", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.ticket_window, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="top", fill="both", expand=True)

        self.scroll_frame = tk.Frame(canvas, bg="#FF8C00")
        canvas.create_window((0,0), window=self.scroll_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.scroll_frame.bind("<Configure>", on_configure)

        self.vars = [{} for _ in range(10)]
        self.pocet_labels = []

        for sl in range(10):
            frame_sloupec = tk.Frame(self.scroll_frame, bg="#FF8C00")
            frame_sloupec.pack(side="left", padx=30, pady=40)

            tk.Label(frame_sloupec, text=f"{sl+1}.", font=("Arial", 10, "bold"), bg="#FF8C00", fg="black").pack()
            pocet_var = tk.StringVar(value="0 vybráno")
            self.pocet_labels.append(pocet_var)
            tk.Label(frame_sloupec, textvariable=pocet_var, font=("Arial", 6, "bold"), bg="#FF8C00", fg="black").pack(pady=4)

            btns_frame = tk.Frame(frame_sloupec, bg="#FF8C00")
            btns_frame.pack(pady=2)
            Button(btns_frame, text="Náhodný tip", font=("Arial", 4, "bold"), bg="white", fg="black", command=lambda s=sl: self.nahodny_tip(s)).pack(side="left", padx=4)
            Button(btns_frame, text="Smazat sloupec", font=("Arial", 4, "bold"), bg="#CC0000", fg="white", command=lambda s=sl: self.clear_sloupec(s)).pack(side="left")

            grid = tk.Frame(frame_sloupec, bg="#FF8C00")
            grid.pack(pady=6)

            for r in range(7):
                for c in range(7):
                    cislo = r * 7 + c + 1
                    if cislo > 49: continue
                    var = tk.IntVar(value=0)
                    self.vars[sl][cislo] = var
                    chk = tk.Checkbutton(grid,
                                         text=str(cislo).zfill(2),
                                         variable=var,
                                         indicatoron=False,
                                         bg="white", fg="black",
                                         selectcolor="#00CC00",
                                         font=("Arial", 6, "bold"),
                                         width=5, height=2,
                                         bd=2, relief="raised",
                                         command=lambda s=sl: self.update_count(s))
                    chk.grid(row=r, column=c, padx=4, pady=4)

        # Dolní část (Slosování + Šance + tlačítko Uložit)
        dolni = tk.Frame(self.ticket_window, bg="#FF8C00")
        dolni.pack(fill="x", pady=12)

        slos_frame = tk.Frame(dolni, bg="#FF8C00")
        slos_frame.pack(side="left", padx=24)

        tk.Label(slos_frame, text="2. Slosování", font=("Arial", 6, "bold"), bg="#FF8C00").pack()
        self.streda_var = BooleanVar(value=True)
        self.patek_var = BooleanVar(value=True)
        self.nedele_var = BooleanVar(value=True)

        f1 = tk.Frame(slos_frame, bg="#FF8C00")
        f1.pack(pady=4)
        Checkbutton(f1, text="Středeční", variable=self.streda_var, bg="#FF8C00", font=("Arial", 6)).pack(side="left", padx=6)
        Checkbutton(f1, text="Páteční", variable=self.patek_var, bg="#FF8C00", font=("Arial", 6)).pack(side="left", padx=6)
        Checkbutton(f1, text="Nedělní", variable=self.nedele_var, bg="#FF8C00", font=("Arial", 6)).pack(side="left", padx=6)

        tk.Label(slos_frame, text="Počet slosování:", font=("Arial", 6), bg="#FF8C00").pack(pady=8)
        self.pocet_slos_var = IntVar(value=1)
        Spinbox(slos_frame, from_=1, to=52, width=6, font=("Arial", 6), textvariable=self.pocet_slos_var).pack(pady=2)

        sance_frame = tk.Frame(dolni, bg="#FF8C00")
        sance_frame.pack(side="right", padx=40)
        tk.Label(sance_frame, text="3. Šance", font=("Arial", 6, "bold"), bg="#FF8C00").pack()
        self.sance_var = IntVar(value=0)
        rframe = tk.Frame(sance_frame, bg="#FF8C00")
        rframe.pack(pady=4)
        Radiobutton(rframe, text="Ano", variable=self.sance_var, value=1, bg="#FF8C00", selectcolor="black", font=("Arial", 6, "bold")).pack(side="left", padx=12)
        Radiobutton(rframe, text="Ne", variable=self.sance_var, value=0, bg="#FF8C00", selectcolor="black", font=("Arial", 6, "bold")).pack(side="left", padx=12)

        Button(dolni, text="ULOŽIT SÁZKU", font=("Arial", 8, "bold"), bg="#006600", fg="white", width=44, height=4, command=self.uloz_ticket).pack(pady=12)

    def update_count(self, sloupec):
        count = sum(var.get() for var in self.vars[sloupec].values())
        if count > 12:
            messagebox.showwarning("Limit", "Maximálně 12 čísel na sloupec!")
        self.pocet_labels[sloupec].set(f"{count} vybráno")

    def nahodny_tip(self, sloupec):
        for var in self.vars[sloupec].values():
            var.set(0)
        cisla = random.sample(range(1, 50), 6)
        for c in cisla:
            self.vars[sloupec][c].set(1)
        self.update_count(sloupec)

    def clear_sloupec(self, sloupec):
        for var in self.vars[sloupec].values():
            var.set(0)
        self.update_count(sloupec)

    def uloz_ticket(self):
        vyplneno = any(len({c for c, v in self.vars[sl].items() if v.get() == 1}) >= 6 for sl in range(10))
        if not vyplneno:
            messagebox.showwarning("Chyba", "Vyplň alespoň jeden sloupec (min. 6 čísel)!")
            return
        with open(SOUBOR_TICKET, "w", encoding="utf-8") as f:
            for sl in range(10):
                sada = {c for c, v in self.vars[sl].items() if v.get() == 1}
                if len(sada) >= 6:
                    f.write(f"Sloupec {sl+1}: {','.join(map(str, sorted(sada)))}\n")
            f.write(f"Středeční: {'Ano' if self.streda_var.get() else 'Ne'}\n")
            f.write(f"Páteční: {'Ano' if self.patek_var.get() else 'Ne'}\n")
            f.write(f"Nedělní: {'Ano' if self.nedele_var.get() else 'Ne'}\n")
            f.write(f"Počet slosování: {self.pocet_slos_var.get()}\n")
            f.write(f"Šance: {'Ano' if self.sance_var.get() == 1 else 'Ne'}\n")
            if self.sance_var.get() == 1:
                sance_cislo = random.randint(0, 999999)
                f.write(f"Šance_číslo: {sance_cislo:06d}\n")
        messagebox.showinfo("Hotovo", "Ticket uložen!")
        self.ticket_window.destroy()

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
                        sloupce.append(cisla)
                elif "Šance: Ano" in line:
                    sance = True
                elif line.startswith("Šance_číslo:"):
                    sance_cislo = int(line.split(":")[1].strip())
                elif line.startswith("Počet slosování:"):
                    pocet_slos = int(line.split(":")[1].strip())
        # Počet kombinací a vsazeno
        celkem_kombinaci = sum(comb(len(t), 6) if len(t) > 6 else 1 for t in sloupce)
        vsazeno = celkem_kombinaci * CENA_KOMB * pocet_slos + (CENA_SANCE if sance else 0) * pocet_slos
        celkova_vyhra = 0
        vysledek = f"Vsazeno celkem: {vsazeno} Kč\n\n"
        for s in range(pocet_slos):
            tah1 = random.sample(range(1,50), 7)
            hlavni1 = sorted(tah1[:6])
            dod1 = tah1[6]
            tah2 = random.sample(range(1,50), 7)
            hlavni2 = sorted(tah2[:6])
            dod2 = tah2[6]
            sance_los = random.randint(0,999999)
            sance_str = f"{sance_los:06d}"
            vysledek += f"═════ SLOSOVÁNÍ {s+1}/{pocet_slos} ═════\n"
            vysledek += f"1. tah: {hlavni1} + {dod1}\n"
            vysledek += f"2. tah: {hlavni2} + {dod2}\n"
            vysledek += f"Šance: {sance_str}\n\n"
            vyhra_tento_tah = 0
            for i, tip in enumerate(sloupce, 1):
                komb = list(combinations(tip, 6)) if len(tip) > 6 else [tuple(sorted(tip))]
                for k in komb:
                    ks = set(k)
                    for hlavni, dod in [(hlavni1, dod1), (hlavni2, dod2)]:
                        shoda = len(ks & set(hlavni))
                        if shoda == 6:
                            vyhra = 10_000_000 # simulovaný jackpot
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
                        vyhra_tento_tah += vyhra
                        celkova_vyhra += vyhra
            if sance and sance_cislo is not None:
                sc = str(sance_cislo)
                shodnych = next((k for k in range(6,0,-1) if sc[-k:] == sance_str[-k:]), 0)
                if shodnych >= 2:
                    vyhry_sance = {2:40, 3:100, 4:500, 5:10000, 6:200000}
                    vyhra_s = vyhry_sance.get(shodnych, 0)
                    celkova_vyhra += vyhra_s
                    vysledek += f"ŠANCE: {shodnych} koncovek → {vyhra_s:,} Kč!\n"
            vysledek += "—" * 52 + "\n\n"
        # Celkový výsledek
        vysledek += f"\nCELKEM VSAZENO: {vsazeno} Kč\n"
        vysledek += f"CELKEM VYHRÁNO: {celkova_vyhra:,} Kč\n"
        if celkova_vyhra > vsazeno:
            vysledek += f"→ ZISK: +{celkova_vyhra - vsazeno:,} Kč 🎉\n"
        elif celkova_vyhra < vsazeno:
            vysledek += f"→ ZTRÁTA: -{vsazeno - celkova_vyhra:,} Kč 😭\n"
        else:
            vysledek += "→ REMÍZA – vrátil jsi vložené 😐\n"
        messagebox.showinfo("Výsledky slosování", vysledek)

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

# Spuštění aplikace
SportkaApp()