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
        self.root.tk.call("tk", "scaling", 2.0)
        self.root.title("Sportka od Sazky")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
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
        self.ticket_window.geometry("2200x2000")
        self.ticket_window.resizable(True, True)
        self.ticket_window.config(bg="#FF8C00")

        # === HLAVNÍ KONTEJNER S SCROLLOVÁNÍM (vše uvnitř) ===
        canvas = tk.Canvas(self.ticket_window, bg="#FF8C00", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.ticket_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame, který bude scrollovatelný – sem dáme úplně všechno
        self.main_container = tk.Frame(canvas, bg="#FF8C00")
        canvas.create_window((0, 0), window=self.main_container, anchor="nw")

        # Aby se správně nastavil scrollregion
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.main_container.bind("<Configure>", on_frame_configure)

        # === KOLEČKO MYŠI FUNGUJE NA WINDOWS I LINUX ===
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        def _on_mousewheel_linux(event):
            canvas.yview_scroll(event.num == 4 and -1 or 1, "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)          # Windows
        canvas.bind_all("<Button-4>", _on_mousewheel_linux)     # Linux scroll nahoru
        canvas.bind_all("<Button-5>", _on_mousewheel_linux)     # Linux scroll dolů

        # === OBSAH TICKETU ===
        # Nadpisy
        tk.Label(self.main_container, text="SPORTKA", font=("Arial", 26, "bold"), bg="#FF8C00", fg="white").pack(pady=(20, 5))
        tk.Label(self.main_container, text="SAZKA", font=("Arial", 16, "bold"), bg="#FF8C00", fg="black").pack(pady=(0, 30))

        self.vars = [{} for _ in range(10)]
        self.pocet_labels = []

        # 5 řádků × 2 sloupce
        for radek in range(5):
            row_frame = tk.Frame(self.main_container, bg="#FF8C00")
            row_frame.pack(pady=25)

            for pozice in range(2):
                idx = radek * 2 + pozice
                frame_sloupec = tk.Frame(row_frame, bg="#FF8C00", relief="solid", bd=2)
                frame_sloupec.pack(side="left", padx=80)

                tk.Label(frame_sloupec, text=f"{idx+1}.", font=("Arial", 10, "bold"), bg="#FF8C00", fg="black").pack()
                pocet_var = tk.StringVar(value="0 vybráno")
                self.pocet_labels.append(pocet_var)
                tk.Label(frame_sloupec, textvariable=pocet_var, font=("Arial", 6, "bold"), bg="#FF8C00", fg="black").pack(pady=4)

                btns_frame = tk.Frame(frame_sloupec, bg="#FF8C00")
                btns_frame.pack(pady=3)
                Button(btns_frame, text="Náhodný tip", font=("Arial", 4, "bold"), bg="white", fg="black",
                       command=lambda s=idx: self.nahodny_tip(s)).pack(side="left", padx=4)
                Button(btns_frame, text="Smazat sloupec", font=("Arial", 4, "bold"), bg="#CC0000", fg="white",
                       command=lambda s=idx: self.clear_sloupec(s)).pack(side="left")

                grid = tk.Frame(frame_sloupec, bg="#FF8C00")
                grid.pack(pady=8)

                for r in range(7):
                    for c in range(7):
                        cislo = r * 7 + c + 1
                        if cislo > 49: continue
                        var = tk.IntVar(value=0)
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

        # === DOLNÍ LIŠTA (Slosování + Šance + Uložit) ===
        dolni = tk.Frame(self.main_container, bg="#FF8C00")
        dolni.pack(fill="x", pady=(40, 20), padx=40)

        # Levá část – slosování
        slos_frame = tk.Frame(dolni, bg="#FF8C00")
        slos_frame.pack(side="left")

        tk.Label(slos_frame, text="2. Slosování", font=("Arial", 6, "bold"), bg="#FF8C00").pack()
        self.streda_var = BooleanVar(value=True)
        self.patek_var = BooleanVar(value=True)
        self.nedele_var = BooleanVar(value=True)

        f1 = tk.Frame(slos_frame, bg="#FF8C00")
        f1.pack(pady=4)
        Checkbutton(f1, text="Středeční", variable=self.streda_var, bg="#FF8C00", font=("Arial", 6)).pack(side="left", padx=6)
        Checkbutton(f1, text="Páteční", variable=self.patek_var, bg="#FF8C00", font=("Arial", 6)).pack(side="left", padx=6)
        Checkbutton(f1, text="Nedělní", variable=self.nedele_var, bg="#FF8C00", font=("Arial", 6)).pack(side="left", padx=6)

        tk.Label(slos_frame, text="Počet slosování:", font=("Arial", 6), bg="#FF8C00").pack(pady=(10, 2))
        self.pocet_slos_var = IntVar(value=1)
        Spinbox(slos_frame, from_=1, to=52, width=6, font=("Arial", 6), textvariable=self.pocet_slos_var).pack(pady=2)

        # Pravá část – šance
        sance_frame = tk.Frame(dolni, bg="#FF8C00")
        sance_frame.pack(side="right")

        tk.Label(sance_frame, text="3. Šance", font=("Arial", 6, "bold"), bg="#FF8C00").pack()
        self.sance_var = IntVar(value=0)
        rframe = tk.Frame(sance_frame, bg="#FF8C00")
        rframe.pack(pady=4)
        Radiobutton(rframe, text="Ano", variable=self.sance_var, value=1, bg="#FF8C00", selectcolor="black", font=("Arial", 6, "bold")).pack(side="left", padx=12)
        Radiobutton(rframe, text="Ne", variable=self.sance_var, value=0, bg="#FF8C00", selectcolor="black", font=("Arial", 6, "bold")).pack(side="left", padx=12)

        # Tlačítko uložit uprostřed
        Button(dolni, text="ULOŽIT SÁZKU", font=("Arial", 8, "bold"), bg="#006600", fg="white",
               width=44, height=4, command=self.uloz_ticket).pack(pady=20)

    # -------------------------------------------------
    # Zbytek metod beze změny (update_count, nahodny_tip, clear_sloupec, uloz_ticket, slosovani, tisk, reset)
    # -------------------------------------------------
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

    # (metody slosovani, tisk, reset zůstávají stejné jako v předchozím kódu – fungují perfektně)

    def slosovani(self):
        if not os.path.exists(SOUBOR_TICKET):
            messagebox.showerror("Chyba", "Nejprve vyplň a ulož ticket!")
            return
        # ... (zbytek stejný jako dříve) ...

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

SportkaApp()