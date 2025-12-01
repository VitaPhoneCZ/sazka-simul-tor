# Sportka Simulator 2025

**Nejlepší český simulátor Sportky v Pythonu** – moderní design, optimalizovaný výkon, automatické slosování do jackpotu, benchmark rychlosti a všechno funguje na první dobrou!

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Tkinter](https://img.shields.io/badge/Tkinter-built--in-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Co to umí

### 🎫 Ticket
- **10 sloupců** uspořádaných do přehledného layoutu 5 × 2  
- **Moderní design** s bílými kartami a stíny
- **Velké čitelné čísla** (2× scaling – ideální na tablet nebo pro starší uživatele)  
- **Náhodný tip** pro každý sloupec + tlačítko **„NÁHODNÝ CELÝ TICKET"**  
- **Automatická validace** – max. 12 čísel na sloupec
- **Cena v reálném čase** – zobrazuje celkovou cenu při každé změně
- **Výběr slosování** – Středa, Pátek, Neděle
- **Počet slosování** – 1 až 52
- **Šance** – volitelná s náhodným číslem
- Scrollování kolečkem myši (Windows + Linux)  
- Plně responzivní ticketové okno (lze měnit velikost)

### 🎰 Slosování
- **Přesné slosování** se dvěma tahy + Šance  
- **Výsledky seřazené podle výdělku** – nejlepší nahoře, nejhorší dole
- **Souhrnné statistiky** – počet jackpotů, 5+1, 5, 4, 3 čísel
- **Top 50 a Bottom 50** slosování s detaily (pro velký počet slosování)
- **Optimalizace pro velký počet** – podporuje i 100 000+ slosování
- **Progress bar** pro dlouhé slosování
- **Uložení výsledků** do souboru s časovou značkou

### 🎯 Auto slosování do Jackpotu
- **Automatické slosování** dokud nevyhraje jackpot
- **Zobrazení průběhu** s počtem pokusů
- **Možnost zastavit** kdykoliv
- **Zobrazení výsledků** po vyhraní jackpotu

### ⚡ Benchmark rychlosti
- **Měření rychlosti** slosování (slosování za sekundu)
- **3 sekundy měření** pro přesné výsledky
- **Zobrazení statistik** – aktuálně ~113 000 slosování/sekundu

### 🖨️ Ostatní funkce
- **Tisk ticketu** do souboru `vytisteny_ticket.txt`  
- **Reset** – smaže ticket a začne znovu

## Jak spustit

1. Měj nainstalovaný **Python 3.9 nebo vyšší**
2. Stáhni nebo naklonuj repozitář:
   ```bash
   git clone https://github.com/VitaPhoneCZ/sazka-simul-tor.git
   ```
3. Přejdi do složky a spusť:
   ```bash
   python sazka.py
   ```

Hotovo! Hraj, tipuj, slosuj a vyhrávej (aspoň v simulaci)

## Ovládání

### Hlavní okno
| Akce                        | Tlačítko                     |
|-----------------------------|------------------------------|
| Otevřít ticket              | 🎫 **Ticket**                |
| Slosovat                    | 🎰 **Slosovat**              |
| Auto slosování do jackpotu  | 🎯 (vedle Slosovat)          |
| Benchmark rychlosti         | ⚡ (vedle Slosovat)          |
| Tisk ticketu                | 🖨️ **Tisk**                  |
| Smazat vše                  | 🔄 **Reset**                 |

### V ticketu
| Akce                        | Tlačítko / Možnost           |
|-----------------------------|------------------------------|
| Náhodný tip (jeden sloupec) | 🎲 **Náhodný** v každém sloupci |
| Smazat sloupec              | 🗑️ **Smazat** v každém sloupci |
| Náhodný celý ticket         | 🎲 **NÁHODNÝ CELÝ TICKET**   |
| Výběr slosování             | Checkboxy: Středa, Pátek, Neděle |
| Počet slosování             | Spinbox (1-52)               |
| Šance                       | Radio button: Ano/Ne         |
| Uložit sázku                | 💾 **ULOŽIT SÁZKU**          |


## Proč je to nejlepší Sportka simulátor?

### 🎨 Design
- **Moderní UI** s tmavým pozadím a barevnými kartami
- **Hover efekty** na tlačítkách
- **Přehledné zobrazení výsledků** s barevným zvýrazněním
- **Progress bary** pro dlouhé operace
- Vypadá jako moderní aplikace, ne jako školní projekt z roku 2005

### ⚡ Výkon
- **Optimalizované slosování** – ~113 000 slosování/sekundu
- **Předpočítané sety** pro rychlejší výpočty
- **Matematické operace** místo string operací
- **Optimalizace pro velký počet** – podporuje 100 000+ slosování bez crashnutí
- **Batch processing** pro efektivní zpracování

### 🎯 Funkce
- **Automatické slosování do jackpotu** – slosuje dokud nevyhraje
- **Benchmark rychlosti** – měření výkonu
- **Výsledky seřazené podle výdělku** – nejlepší nahoře
- **Souhrnné statistiky** pro velký počet slosování
- **Uložení výsledků** s časovou značkou
- **Cena v reálném čase** – vidíš cenu při každé změně

### 💻 Technické
- Žádné otravné messageboxy při náhodném vyplnění  
- Přesná cena podle počtu kombinací
- Super čistý kód s komentáři  
- Vše funguje na Windows, macOS i Linux  
- Bez externích závislostí (kromě standardní knihovny Pythonu)

## Autor

**Vita Phone**  
Full-stack vývojář | Python | Tkinter | Design  

[![GitHub](https://img.shields.io/badge/GitHub-000000?style=flat&logo=github&logoColor=white)](https://github.com/VitaPhoneCZ)  

> „Když už hrát Sportku, tak aspoň s pořádným simulátorem.“

---

**Líbí se ti projekt? Dej hvězdičku – moc to pomůže!**

Made with passion & coffee in Plzeň, Czech Republic  
**VitaPhoneCZ © 2025**
