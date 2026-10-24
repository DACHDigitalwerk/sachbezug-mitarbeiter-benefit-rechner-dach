# 🎁 DACH Sachbezug-, Essensgutschein- & Mitarbeiter-Benefit-Optimierer 2026 (DE, AT, CH)

[![CI Tests](https://github.com/DACHDigitalwerk/sachbezug-mitarbeiter-benefit-rechner-dach/actions/workflows/ci.yml/badge.svg)](https://github.com/DACHDigitalwerk/sachbezug-mitarbeiter-benefit-rechner-dach/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![BGH Smartlaw Compliant](https://img.shields.io/badge/Compliance-BGH%20Smartlaw%20(I%20ZR%20226%2F20)-green.svg)](https://dachdigitalwerk.github.io/haftungsausschluss/)

Reine kaufmännische, steuerliche und sozialversicherungsrechtliche Tarif- und Freibetrags-Mathematik für Arbeitgeber, HR-Abteilungen, Steuerkanzleien und Arbeitnehmer im DACH-Raum (Deutschland, Österreich, Schweiz).

🔗 **Interaktiver Web-Rechner (100% Client-Side & kostenlos im Browser):**  
👉 **[https://dachdigitalwerk.github.io/sachbezug-benefit-rechner/](https://dachdigitalwerk.github.io/sachbezug-benefit-rechner/)**

---

## 📌 Rechtliche Grundlagen & Gesetzliche Werte 2026

### 🇩🇪 Deutschland
- **50-€-Sachbezugsfreigrenze (§ 8 Abs. 2 Satz 11 EStG):**  
  Monatliche Freigrenze für Sachbezugskarten und Gutscheine. Strikte Freigrenze (kein Freibetrag): Bei Überschreitung um 1 Cent (50,01 €) wird der **gesamte Betrag steuer- und sozialversicherungspflichtig**. Automatische Validierung der ZAG-Kriterien (§ 2 Abs. 1 Nr. 10 ZAG).
- **Amtliche Sachbezugswerte 2026 (SvEV):**
  - Frühstück: **2,30 €**
  - Mittagessen: **4,40 €**
  - Abendessen: **4,40 €**
  - Gesamter Monatswert Verpflegung: **333,00 €**
  - Monatswert freie Unterkunft: **282,00 €**
- **Digitaler Essenszuschuss:**  
  4,40 € amtlicher Sachbezugswert (pauschalversteuerbar mit 25 %) + 3,10 € steuerfreier Arbeitgeberzuschuss = **max. 7,50 € pro Arbeitstag** steuerbegünstigt (bis zu **150,00 € Netto-Plus** pro Monat).
- **Weitere steuerfreie Extras:**
  - **Jobticket / Deutschlandticket (§ 3 Nr. 15 EStG):** 100 % steuer- und abgabenfrei.
  - **Betriebliche Gesundheitsförderung (§ 3 Nr. 34 EStG):** Bis zu **600 € jährlich** steuerfrei.
  - **Internetpauschale (§ 40 Abs. 2 Satz 1 Nr. 5 EStG):** Bis zu **50 € monatlich** pauschal mit 25 % Lohnsteuer.
  - **Erholungsbeihilfe (§ 40 Abs. 2 Satz 2 EStG):** 156 € (AN) + 104 € (Ehegatte) + 52 € (Kind) pauschal 25 %.
  - **Aufmerksamkeiten (R 19.6 LStR):** Bis zu **60 € brutto** je persönlichem Anlass (Geburtstag, Hochzeit).
  - **Rabattfreibetrag (§ 8 Abs. 3 EStG):** Bis zu **1.080 € jährlich** für Waren/Dienstleistungen des AG.

### 🇦🇹 Österreich
- **Essensgutscheine (§ 3 Abs. 1 Z 17 EStG):**  
  Bis zu **8,00 € pro Arbeitstag** für Mahlzeiten im Gastgewerbe bzw. bis zu **2,00 €** für Lebensmittel.
- **Klimaticket / Öffi-Ticket (§ 26 Z 5 lit. b EStG):**  
  100 % steuer- und sozialversicherungsfrei vom Arbeitgeber bezahlt.
- **Zukunftssicherung (§ 3 Abs. 1 Z 15 lit. a EStG):**  
  Bis zu **300 € jährlich** für Vorsorge und Lebensversicherungen steuerfrei.
- **Kinderbetreuungszuschuss (§ 3 Abs. 1 Z 13 lit. b EStG):**  
  Bis zu **2.000 € pro Kind/Jahr** bis zum 14. Lebensjahr steuerfrei.
- **Sachzuwendungen (§ 3 Abs. 1 Z 14 EStG):**  
  Bis zu **186 € jährlich** abgabenfrei + 186 € für Firmen- und Dienstjubiläen.

### 🇨🇭 Schweiz
- **Verpflegungsbeiträge / Lunch-Check:**  
  Bis zu **180 CHF monatlich** steuerfrei (Feld G im Lohnausweis).
- **Reka-Geld Rabatte:**  
  Verbilligte Abgabe mit bis zu **600 CHF Ersparnis pro Jahr** steuer- und abgabenfrei.
- **Geschenke & Naturalleistungen (Art. 9 AHVV):**  
  Bis zu **500 CHF pro Anlass / Jahr** frei von AHV/IV/EO/ALV-Beiträgen.
- **ÖV-Beteiligung (Halbtax / GA):**  
  Steuer- und beitragsfrei bei geschäftlicher Relevanz.

---

## ⚡ Schnellstart & Installation

```bash
git clone https://github.com/DACHDigitalwerk/sachbezug-mitarbeiter-benefit-rechner-dach.git
cd sachbezug-mitarbeiter-benefit-rechner-dach
pip install -e .
```

### CLI Verwendung

```bash
# Deutschland: 50 € Sachbezug + 15 Tage Essenszuschuss + 49 € Jobticket
dach-benefit de --voucher 50 --meals 15 --jobticket 49

# Österreich: Gastronomie-Essensgutscheine 18 Tage + Klimaticket
dach-benefit at --type gastro --days 18 --klimaticket 1095

# Schweiz: Lunch-Check 180 CHF + Reka 600 CHF + 1 persönliches Geschenk
dach-benefit ch --lunch 180 --reka 600 --occasions 1

# Gehaltserhöhungs-Optimierer (Klassisches Brutto vs. Steuerfreie Benefits)
dach-benefit compare --target-net 100
```

---

## 🧪 Tests ausführen

```bash
pytest tests/ -v
# 30 Tests bestanden (100% Pass Rate)
```

---

## 🛡️ Rechtlicher Hinweis & Compliance

Dieses Tool ist ein rein mathematisches Berechnungs- und Simulationstool. Es erfolgt keine individuelle Rechts- oder Steuerberatung im Sinne des deutschen Rechtsdienstleistungsgesetzes (§ 2 RDG) oder Steuerberatungsgesetzes (§ 5 StBerG). Konform mit dem BGH-Smartlaw-Urteil (Az. I ZR 226/20).

Offizielle Plattform & Nutzungsbedingungen:  
- Web-App: [https://dachdigitalwerk.github.io/sachbezug-benefit-rechner/](https://dachdigitalwerk.github.io/sachbezug-benefit-rechner/)  
- AGB: [https://dachdigitalwerk.github.io/agb/](https://dachdigitalwerk.github.io/agb/)  
- Haftungsausschluss: [https://dachdigitalwerk.github.io/haftungsausschluss/](https://dachdigitalwerk.github.io/haftungsausschluss/)

---

## 📄 Lizenz

MIT License — Copyright (c) 2026 DACH Digitalwerk.
