# -*- coding: utf-8 -*-
"""
Quickstart Example: DACH Sachbezug- & Benefit-Optimierer 2026
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sachbezug_dach import (
    GermanyBenefitsCalculator,
    AustriaBenefitsCalculator,
    SwitzerlandBenefitsCalculator,
    SalaryRaiseOptimizer,
)


def main():
    print("=== DACH Sachbezug & Benefit Quickstart 2026 ===")

    # 1. Deutschland: 50 € Sachbezug + Essenszuschuss (15 Tage à 7,50 €) + Jobticket (49 €)
    de_res = GermanyBenefitsCalculator.calculate(
        voucher_value=50.00,
        zag_compliant=True,
        meal_days=15,
        meal_voucher_daily=7.50,
        jobticket_monthly=49.00,
        health_annual=600.00,
        internet_monthly=50.00,
    )
    print(f"\nDeutschland:")
    print(f"  • Effektiver Netto-Vorteil AN: {de_res.total_effective_employee_net_monthly:,.2f} € / Monat")
    print(f"  • Gesamtaufwand Arbeitgeber  : {de_res.total_employer_cost_monthly:,.2f} € / Monat")

    # 2. Gehaltserhöhungs-Vergleich (100 € Netto-Plus beim AN)
    comp = SalaryRaiseOptimizer.compare_fixed_net(target_net_monthly=100.0, marginal_tax_rate=0.35)
    print(f"\nGehaltsvergleich für +100 € Netto:")
    print(f"  • Klassisches Brutto (AG-Kosten): {comp.total_employer_cost_gross:,.2f} €")
    print(f"  • Steuerfreie Benefits (AG-Kosten): {comp.total_employer_cost_benefits:,.2f} €")
    print(f"  • AG-Ersparnis: {comp.monthly_employer_savings:,.2f} € / Monat ({comp.employer_cost_reduction_percent:.1f} %)")


if __name__ == "__main__":
    main()
