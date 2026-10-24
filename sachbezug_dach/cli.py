"""
cli.py - Command Line Interface für DACH Sachbezug- & Benefit-Optimierer 2026
"""

import argparse
import sys
import os
import json

if __package__ is None or __package__ == "":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from sachbezug_dach.svev_de import GermanyBenefitsCalculator
    from sachbezug_dach.austria import AustriaBenefitsCalculator
    from sachbezug_dach.switzerland import SwitzerlandBenefitsCalculator
    from sachbezug_dach.salary_comparison import SalaryRaiseOptimizer
else:
    from .svev_de import GermanyBenefitsCalculator
    from .austria import AustriaBenefitsCalculator
    from .switzerland import SwitzerlandBenefitsCalculator
    from .salary_comparison import SalaryRaiseOptimizer

def main():
    parser = argparse.ArgumentParser(
        prog="dach-benefit",
        description="DACH Sachbezug-, Essensgutschein- & Benefit-Optimierer 2026 (DE, AT, CH)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Ländermodus oder Vergleich wählen")

    # Command: DE
    de_parser = subparsers.add_parser("de", help="Deutschland (SvEV 2026 & § 8 EStG)")
    de_parser.add_argument("--voucher", type=float, default=50.00, help="Gutschein-Wert (max 50 € Freigrenze)")
    de_parser.add_argument("--non-zag", action="store_true", help="Gutschein erfüllt ZAG-Kriterien nicht")
    de_parser.add_argument("--meals", type=int, default=15, help="Arbeitstage mit Essenszuschuss")
    de_parser.add_argument("--meal-rate", type=float, default=7.50, help="Täglicher Zuschuss (max 7,50 €)")
    de_parser.add_argument("--jobticket", type=float, default=49.00, help="Jobticket / Deutschlandticket monatlich")
    de_parser.add_argument("--health", type=float, default=600.00, help="Gesundheitsförderung jährlich (§ 3 Nr. 34)")
    de_parser.add_argument("--internet", type=float, default=50.00, help="Internetpauschale monatlich (§ 40 Abs. 2)")
    de_parser.add_argument("--json", action="store_true", help="JSON-Ausgabe")

    # Command: AT
    at_parser = subparsers.add_parser("at", help="Österreich (§ 3 Abs. 1 Z 17 EStG)")
    at_parser.add_argument("--type", choices=["gastro", "grocery"], default="gastro", help="Essensgutschein-Art (8€ oder 2€)")
    at_parser.add_argument("--days", type=int, default=18, help="Arbeitstage mit Essensgutschein")
    at_parser.add_argument("--klimaticket", type=float, default=1095.00, help="Klimaticket / Öffi-Ticket jährlich")
    at_parser.add_argument("--future", type=float, default=300.00, help="Zukunftssicherung jährlich (max 300 €)")
    at_parser.add_argument("--children", type=int, default=0, help="Kinder für Betreuungszuschuss (bis 2.000 €)")
    at_parser.add_argument("--json", action="store_true", help="JSON-Ausgabe")

    # Command: CH
    ch_parser = subparsers.add_parser("ch", help="Schweiz (Lohnausweis Feld G & Art. 9 AHVV)")
    ch_parser.add_argument("--lunch", type=float, default=180.00, help="Lunch-Check monatlich (max 180 CHF)")
    ch_parser.add_argument("--reka", type=float, default=600.00, help="Reka-Rabatt jährlich (max 600 CHF)")
    ch_parser.add_argument("--occasions", type=int, default=1, help="Anlässe für Naturalgeschenke (500 CHF)")
    ch_parser.add_argument("--halbtax", type=float, default=190.00, help="ÖV-Beteiligung Halbtax jährlich")
    ch_parser.add_argument("--json", action="store_true", help="JSON-Ausgabe")

    # Command: COMPARE
    comp_parser = subparsers.add_parser("compare", help="Gehaltserhöhungs-Vergleich (Brutto vs. Benefits)")
    comp_parser.add_argument("--target-net", type=float, default=100.00, help="Gewünschtes Netto-Plus beim AN")
    comp_parser.add_argument("--tax-rate", type=float, default=0.35, help="Grenzsteuersatz (Standard 0.35)")
    comp_parser.add_argument("--json", action="store_true", help="JSON-Ausgabe")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "de":
        res = GermanyBenefitsCalculator.calculate(
            voucher_value=args.voucher,
            zag_compliant=not args.non_zag,
            meal_days=args.meals,
            meal_voucher_daily=args.meal_rate,
            jobticket_monthly=args.jobticket,
            health_annual=args.health,
            internet_monthly=args.internet,
        )
        if args.json:
            print(json.dumps(res.__dict__, indent=2))
        else:
            print("==========================================================")
            print("  DACH Digitalwerk — Sachbezug & Benefits Deutschland 2026")
            print("==========================================================")
            print(f"50-€-Sachbezug:        {res.voucher_amount:.2f} € | Steuerfrei: {res.voucher_tax_free} (ZAG: {res.voucher_zag_compliant})")
            print(f"Essenszuschuss:        {res.meal_total_monthly_benefit:.2f} €/Monat ({res.meal_days} Tage à {res.meal_total_daily_allowance:.2f} €)")
            print(f"Jobticket:             {res.jobticket_monthly:.2f} €/Monat (100% steuer- & SV-frei)")
            print(f"Gesundheitsförderung:  {res.health_monthly:.2f} €/Monat (max 600 €/Jahr)")
            print(f"Internetpauschale:     {res.internet_monthly:.2f} €/Monat (AG-Pauschalsteuer: {res.internet_flat_tax:.2f} €)")
            print("----------------------------------------------------------")
            print(f"Effektiver Netto-Vorteil AN: {res.total_effective_employee_net_monthly:.2f} €/Monat ({res.annual_employee_net_benefit:.2f} €/Jahr)")
            print(f"Gesamtaufwand Arbeitgeber:   {res.total_employer_cost_monthly:.2f} €/Monat ({res.annual_employer_cost:.2f} €/Jahr)")
            print("==========================================================")

    elif args.command == "at":
        res = AustriaBenefitsCalculator.calculate(
            meal_voucher_type=args.type,
            meal_days=args.days,
            transit_ticket_annual=args.klimaticket,
            future_security_annual=args.future,
            eligible_children_count=args.children,
        )
        if args.json:
            print(json.dumps(res.__dict__, indent=2))
        else:
            print("==========================================================")
            print("  DACH Digitalwerk — Steuerfreie Benefits Österreich 2026")
            print("==========================================================")
            print(f"Essensgutscheine ({args.type}): {res.meal_vouchers_monthly:.2f} €/Monat ({res.meal_days} Tage)")
            print(f"Klimaticket / Öffi:     {res.transit_ticket_monthly:.2f} €/Monat (100% steuer- & beitragsfrei)")
            print(f"Zukunftssicherung:      {res.future_security_monthly:.2f} €/Monat")
            print(f"Kinderbetreuung:        {res.childcare_monthly:.2f} €/Monat")
            print("----------------------------------------------------------")
            print(f"Effektives Netto-Plus:  {res.total_tax_free_monthly:.2f} €/Monat ({res.annual_employee_net_benefit:.2f} €/Jahr)")
            print(f"Gesamtaufwand AG:       {res.annual_employer_cost:.2f} €/Jahr (0 € Lohnnebenkosten!)")
            print("==========================================================")

    elif args.command == "ch":
        res = SwitzerlandBenefitsCalculator.calculate(
            lunch_check_monthly=args.lunch,
            reka_discount_annual=args.reka,
            occasions_count=args.occasions,
            transit_contribution_annual=args.halbtax,
        )
        if args.json:
            print(json.dumps(res.__dict__, indent=2))
        else:
            print("==========================================================")
            print("  DACH Digitalwerk — Steuerfreie Benefits Schweiz 2026")
            print("==========================================================")
            print(f"Lunch-Check (Feld G):   {res.lunch_check_monthly:.2f} CHF/Monat")
            print(f"Reka-Geld Rabatt:       {res.reka_discount_monthly:.2f} CHF/Monat ({res.reka_discount_annual:.2f} CHF/Jahr)")
            print(f"Geschenke (Art. 9 AHVV):{res.gifts_monthly:.2f} CHF/Monat ({res.gifts_annual:.2f} CHF/Jahr)")
            print(f"ÖV-Beteiligung Halbtax: {res.transit_contribution_monthly:.2f} CHF/Monat")
            print("----------------------------------------------------------")
            print(f"Netto-Kaufkraftzuwachs: {res.total_tax_free_monthly:.2f} CHF/Monat ({res.annual_employee_net_benefit:.2f} CHF/Jahr)")
            print(f"AG-Aufwand:             {res.annual_employer_cost:.2f} CHF/Jahr (0 CHF Sozialabgaben!)")
            print("==========================================================")

    elif args.command == "compare":
        res = SalaryRaiseOptimizer.compare_fixed_net(
            target_net_monthly=args.target_net,
            marginal_tax_rate=args.tax_rate,
        )
        if args.json:
            print(json.dumps(res.__dict__, indent=2))
        else:
            print("==========================================================")
            print("  DACH Digitalwerk — Gehaltserhöhungs-Optimierer 2026")
            print("==========================================================")
            print(f"Ziel: +{res.target_net_raise_monthly:.2f} € Netto auf dem Mitarbeiterkonto")
            print("----------------------------------------------------------")
            print(f"VARIANTE A (Klassisches Brutto):")
            print(f"  Erforderliches Brutto:      +{res.required_gross_salary_raise:.2f} €")
            print(f"  + AG-Sozialabgaben (~20.5%): +{res.employer_social_security_raise:.2f} €")
            print(f"  -> Gesamtaufwand AG:          {res.total_employer_cost_gross:.2f} €/Monat")
            print(f"VARIANTE B (Steuerfreie Sachbezüge):")
            print(f"  Netto-Gutscheine / Benefits: +{res.benefit_net_value:.2f} €")
            print(f"  + AG-Pauschalsteuer (~5%):   +{res.benefit_employer_flat_taxes:.2f} €")
            print(f"  -> Gesamtaufwand AG:          {res.total_employer_cost_benefits:.2f} €/Monat")
            print("----------------------------------------------------------")
            print(f"🔥 ERSPARNIS FÜR DAS KMU:      {res.monthly_employer_savings:.2f} € / Monat ({res.annual_employer_savings:.2f} € / Jahr)")
            print(f"   Kostenreduktion:            -{res.employer_cost_reduction_percent:.1f} %")
            print("==========================================================")

if __name__ == "__main__":
    main()
