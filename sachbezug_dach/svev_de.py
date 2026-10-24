"""
svev_de.py - Amtliche Sachbezugswerte & Steuerbefreiungen Deutschland 2026
Rechtsgrundlagen:
- § 8 Abs. 2 Satz 11 EStG (50-EUR-Sachbezugsfreigrenze & ZAG-Kriterien)
- Sozialversicherungsentgeltverordnung (SvEV) 2026 (Frühstück 2,30 €, Mittag 4,40 €, Abend 4,40 €)
- § 3 Nr. 15 EStG (Jobticket / Deutschlandticket)
- § 3 Nr. 34 EStG (Betriebliche Gesundheitsförderung bis 600 €/Jahr)
- § 40 Abs. 2 Satz 1 Nr. 5 EStG (Internetpauschale bis 50 €/Monat)
- § 40 Abs. 2 Satz 2 EStG (Erholungsbeihilfe 156 €/104 €/52 €)
- R 19.6 LStR (Aufmerksamkeiten bis 60 € je persönlichem Anlass)
- § 8 Abs. 3 EStG (Rabattfreibetrag bis 1.080 €/Jahr)
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class GermanyBenefitsResult:
    # 50-EUR-Sachbezug
    voucher_amount: float
    voucher_tax_free: bool
    voucher_zag_compliant: bool
    voucher_taxable_portion: float

    # Verpflegung & Essenszuschuss
    meal_days: int
    meal_official_value_per_day: float
    meal_ag_taxfree_allowance_per_day: float
    meal_total_daily_allowance: float
    meal_total_monthly_benefit: float
    meal_tax_free_portion: float
    meal_pauschal_tax_portion: float

    # Weitere Benefits (monatlich berechnet)
    jobticket_monthly: float
    health_monthly: float
    internet_monthly: float
    internet_flat_tax: float
    recreation_annual: float
    amenities_annual: float
    staff_discount_annual: float

    # Gesamtsummen
    total_tax_free_monthly: float
    total_flat_taxed_monthly: float
    total_employer_flat_taxes_monthly: float
    total_effective_employee_net_monthly: float
    total_employer_cost_monthly: float
    annual_employee_net_benefit: float
    annual_employer_cost: float


class GermanyBenefitsCalculator:
    # Amtliche Werte 2026
    SVEV_2026_BREAKFAST = 2.30
    SVEV_2026_LUNCH = 4.40
    SVEV_2026_DINNER = 4.40
    SVEV_2026_MONTHLY_TOTAL = 333.00
    SVEV_2026_LODGING_MONTHLY = 282.00

    TAX_FREE_MEAL_ADDITION = 3.10  # Max steuerfreier AG-Zuschuss
    MAX_DAILY_MEAL_VOUCHER = 7.50   # 4.40 + 3.10

    VOUCHER_MONTHLY_LIMIT = 50.00   # § 8 Abs. 2 Satz 11 EStG (Freigrenze)
    HEALTH_ANNUAL_LIMIT = 600.00    # § 3 Nr. 34 EStG
    INTERNET_MONTHLY_LIMIT = 50.00  # § 40 Abs. 2 Nr. 5 EStG
    FLAT_TAX_RATE = 0.25            # 25% pauschale Lohnsteuer (+ Soli/KiSt)
    SOLI_ON_FLAT_TAX = 0.055        # 5.5% auf 25% = 1.375%

    RECREATION_EMPLOYEE = 156.00
    RECREATION_SPOUSE = 104.00
    RECREATION_CHILD = 52.00

    STAFF_DISCOUNT_ANNUAL = 1080.00 # § 8 Abs. 3 EStG

    @classmethod
    def calculate(
        cls,
        voucher_value: float = 50.00,
        zag_compliant: bool = True,
        meal_days: int = 15,
        meal_voucher_daily: float = 7.50,
        jobticket_monthly: float = 49.00,
        health_annual: float = 600.00,
        internet_monthly: float = 50.00,
        has_spouse: bool = False,
        children_count: int = 0,
        amenities_count: int = 2,  # z.B. Geburtstag, Jubiläum
        staff_discount_annual: float = 0.00,
    ) -> GermanyBenefitsResult:
        
        # 1. 50-Euro-Sachbezugsfreigrenze (§ 8 Abs. 2 Satz 11 EStG)
        # Strikte FREIGRENZE: Bei Überschreitung um 1 Cent ist der GESAMTE Betrag steuer- und SV-pflichtig!
        if voucher_value <= cls.VOUCHER_MONTHLY_LIMIT and zag_compliant:
            v_tax_free = True
            v_taxable = 0.0
            v_net = voucher_value
        else:
            v_tax_free = False
            v_taxable = voucher_value
            v_net = 0.0  # Nicht mehr steuerfrei

        # 2. Essenszuschuss (SvEV 2026)
        daily_cap = min(meal_voucher_daily, cls.MAX_DAILY_MEAL_VOUCHER)
        meal_monthly = round(daily_cap * meal_days, 2)
        
        # Aufteilung amtlicher Sachbezugswert vs. AG-Zuschuss
        # Bis 3.10 € ist steuerfrei, 4.40 € kann pauschal mit 25% versteuert werden
        daily_tax_free = min(daily_cap - cls.SVEV_2026_LUNCH, cls.TAX_FREE_MEAL_ADDITION) if daily_cap > cls.SVEV_2026_LUNCH else 0.0
        daily_pauschal = min(daily_cap, cls.SVEV_2026_LUNCH)
        
        meal_tax_free_monthly = round(daily_tax_free * meal_days, 2)
        meal_pauschal_monthly = round(daily_pauschal * meal_days, 2)
        meal_flat_tax = round(meal_pauschal_monthly * (cls.FLAT_TAX_RATE * (1 + cls.SOLI_ON_FLAT_TAX)), 2)

        # 3. Jobticket (§ 3 Nr. 15 EStG - 100% steuer- und SV-frei)
        jt_monthly = max(0.0, jobticket_monthly)

        # 4. Gesundheitsförderung (§ 3 Nr. 34 EStG - max 600 €/Jahr steuerfrei)
        health_capped_annual = min(cls.HEALTH_ANNUAL_LIMIT, max(0.0, health_annual))
        health_monthly_eq = round(health_capped_annual / 12.0, 2)

        # 5. Internetpauschale (§ 40 Abs. 2 Nr. 5 EStG - max 50 €/Monat pauschal 25%)
        internet_capped = min(cls.INTERNET_MONTHLY_LIMIT, max(0.0, internet_monthly))
        internet_tax = round(internet_capped * (cls.FLAT_TAX_RATE * (1 + cls.SOLI_ON_FLAT_TAX)), 2)

        # 6. Erholungsbeihilfe (jährlich)
        recreation_total = cls.RECREATION_EMPLOYEE
        if has_spouse:
            recreation_total += cls.RECREATION_SPOUSE
        recreation_total += (children_count * cls.RECREATION_CHILD)
        recreation_monthly_eq = round(recreation_total / 12.0, 2)
        recreation_tax_monthly = round(recreation_monthly_eq * (cls.FLAT_TAX_RATE * (1 + cls.SOLI_ON_FLAT_TAX)), 2)

        # 7. Aufmerksamkeiten (R 19.6 LStR - 60 € brutto je persönlichem Anlass)
        amenities_total = amenities_count * 60.00
        amenities_monthly_eq = round(amenities_total / 12.0, 2)

        # 8. Rabattfreibetrag (§ 8 Abs. 3 EStG - 1.080 €/Jahr)
        discount_capped = min(cls.STAFF_DISCOUNT_ANNUAL, max(0.0, staff_discount_annual))
        discount_monthly_eq = round(discount_capped / 12.0, 2)

        # Gesamtrechnung Monat
        tax_free_m = (
            (voucher_value if v_tax_free else 0.0) +
            meal_tax_free_monthly +
            jt_monthly +
            health_monthly_eq +
            amenities_monthly_eq +
            discount_monthly_eq
        )

        flat_taxed_m = meal_pauschal_monthly + internet_capped + recreation_monthly_eq
        employer_taxes_m = meal_flat_tax + internet_tax + recreation_tax_monthly

        total_net_m = tax_free_m + flat_taxed_m
        total_ag_cost_m = total_net_m + employer_taxes_m

        return GermanyBenefitsResult(
            voucher_amount=voucher_value,
            voucher_tax_free=v_tax_free,
            voucher_zag_compliant=zag_compliant,
            voucher_taxable_portion=v_taxable,
            meal_days=meal_days,
            meal_official_value_per_day=cls.SVEV_2026_LUNCH,
            meal_ag_taxfree_allowance_per_day=daily_tax_free,
            meal_total_daily_allowance=daily_cap,
            meal_total_monthly_benefit=meal_monthly,
            meal_tax_free_portion=meal_tax_free_monthly,
            meal_pauschal_tax_portion=meal_pauschal_monthly,
            jobticket_monthly=jt_monthly,
            health_monthly=health_monthly_eq,
            internet_monthly=internet_capped,
            internet_flat_tax=internet_tax,
            recreation_annual=recreation_total,
            amenities_annual=amenities_total,
            staff_discount_annual=discount_capped,
            total_tax_free_monthly=round(tax_free_m, 2),
            total_flat_taxed_monthly=round(flat_taxed_m, 2),
            total_employer_flat_taxes_monthly=round(employer_taxes_m, 2),
            total_effective_employee_net_monthly=round(total_net_m, 2),
            total_employer_cost_monthly=round(total_ag_cost_m, 2),
            annual_employee_net_benefit=round(total_net_m * 12.0, 2),
            annual_employer_cost=round(total_ag_cost_m * 12.0, 2),
        )
