"""
switzerland.py - Steuerfreie Mitarbeiter-Benefits Schweiz 2026
Rechtsgrundlagen:
- Schweizer Wegleitung zum Ausfüllen des Lohnausweises (Ziff. 36 ff., Feld G Verpflegung)
- Art. 9 Abs. 2 lit. h AHVV (Naturalgeschenke bis CHF 500.- pro Anlass beitragsfrei)
- Reka-Geld Rabatte bis CHF 600.- pro Jahr abgabenfrei
- Beteiligung an Halbtax / Generalabonnement (GA) bei geschäftlicher Relevanz steuerfrei
"""

from dataclasses import dataclass

@dataclass
class SwitzerlandBenefitsResult:
    lunch_check_monthly: float
    reka_discount_annual: float
    reka_discount_monthly: float
    gifts_annual: float
    gifts_monthly: float
    transit_contribution_monthly: float
    total_tax_free_monthly: float
    annual_employee_net_benefit: float
    annual_employer_cost: float


class SwitzerlandBenefitsCalculator:
    MAX_LUNCH_CHECK_MONTHLY = 180.00   # Bis 180 CHF/Monat pauschal (Feld G)
    MAX_REKA_DISCOUNT_ANNUAL = 600.00  # Reka-Geld Rabattgrenze
    MAX_GIFT_PER_OCCASION = 500.00     # Art. 9 AHVV (z.B. Heirat, Jubiläum, Weihnachten)

    @classmethod
    def calculate(
        cls,
        lunch_check_monthly: float = 180.00,
        reka_discount_annual: float = 600.00,
        occasions_count: int = 1, # Anzahl persönliche Anlässe / Weihnachten
        transit_contribution_annual: float = 190.00, # z.B. Halbtax 190 CHF
    ) -> SwitzerlandBenefitsResult:
        
        # 1. Lunch-Check / Verpflegungsbeitrag
        lunch_capped = min(cls.MAX_LUNCH_CHECK_MONTHLY, max(0.0, lunch_check_monthly))

        # 2. Reka-Check Rabatt
        reka_capped = min(cls.MAX_REKA_DISCOUNT_ANNUAL, max(0.0, reka_discount_annual))
        reka_monthly = round(reka_capped / 12.0, 2)

        # 3. Naturalgeschenke (Art. 9 AHVV)
        gifts_total = occasions_count * cls.MAX_GIFT_PER_OCCASION
        gifts_monthly = round(gifts_total / 12.0, 2)

        # 4. ÖV-Beteiligung (Halbtax / GA)
        transit_monthly = round(max(0.0, transit_contribution_annual) / 12.0, 2)

        total_tax_free_m = lunch_capped + reka_monthly + gifts_monthly + transit_monthly
        annual_total = round(total_tax_free_m * 12.0, 2)

        return SwitzerlandBenefitsResult(
            lunch_check_monthly=lunch_capped,
            reka_discount_annual=reka_capped,
            reka_discount_monthly=reka_monthly,
            gifts_annual=gifts_total,
            gifts_monthly=gifts_monthly,
            transit_contribution_monthly=transit_monthly,
            total_tax_free_monthly=round(total_tax_free_m, 2),
            annual_employee_net_benefit=annual_total,
            annual_employer_cost=annual_total, # 100% frei von AHV/IV/EO/ALV und Quellensteuer!
        )
