"""
austria.py - Steuerfreie Mitarbeiter-Benefits Österreich 2026
Rechtsgrundlagen:
- § 3 Abs. 1 Z 17 EStG (Essensgutscheine bis 8,00 € Gastronomie / 2,00 € Lebensmittel)
- § 26 Z 5 lit. b EStG (Klimaticket / Öffi-Ticket steuer- und beitragsfrei)
- § 3 Abs. 1 Z 15 lit. a EStG (Zukunftssicherung bis 300 €/Jahr)
- § 3 Abs. 1 Z 14 EStG (Sachzuwendungen bis 186 €/Jahr + 186 € Jubiläumsgaben)
- § 3 Abs. 1 Z 21 EStG (Mitarbeiter-Rabatte bis 20% generell, darüber 1.000 € Freibetrag/Jahr)
- § 3 Abs. 1 Z 13 lit. b EStG (Kinderbetreuungszuschuss bis 2.000 €/Kind/Jahr bis zum 14. Lebensjahr)
"""

from dataclasses import dataclass

@dataclass
class AustriaBenefitsResult:
    meal_vouchers_monthly: float
    meal_daily_rate: float
    meal_days: int
    transit_ticket_monthly: float
    future_security_monthly: float
    childcare_monthly: float
    gifts_annual: float
    gifts_monthly: float
    staff_discount_monthly: float
    total_tax_free_monthly: float
    annual_employee_net_benefit: float
    annual_employer_cost: float


class AustriaBenefitsCalculator:
    MAX_MEAL_GASTRO_DAILY = 8.00     # Gastronomie / fertige Mahlzeiten
    MAX_MEAL_GROCERY_DAILY = 2.00    # Lebensmittel
    MAX_FUTURE_SECURITY_ANNUAL = 300.00
    MAX_GIFTS_ANNUAL = 186.00
    MAX_JUBILEE_GIFTS_ANNUAL = 186.00
    MAX_CHILDCARE_PER_CHILD_ANNUAL = 2000.00
    MAX_STAFF_DISCOUNT_ANNUAL = 1000.00

    @classmethod
    def calculate(
        cls,
        meal_voucher_type: str = "gastro", # 'gastro' or 'grocery'
        meal_days: int = 18,
        custom_daily_voucher: float = 8.00,
        transit_ticket_annual: float = 1095.00, # z.B. Klimaticket Österreich 1.095 €
        future_security_annual: float = 300.00,
        eligible_children_count: int = 0,
        gifts_annual: float = 186.00,
        jubilee_year: bool = False,
        staff_discount_annual: float = 0.00,
    ) -> AustriaBenefitsResult:
        
        # 1. Essensgutscheine (§ 3 Abs. 1 Z 17 EStG)
        max_rate = cls.MAX_MEAL_GASTRO_DAILY if meal_voucher_type == "gastro" else cls.MAX_MEAL_GROCERY_DAILY
        effective_rate = min(max_rate, max(0.0, custom_daily_voucher))
        meal_monthly = round(effective_rate * meal_days, 2)

        # 2. Öffi-Ticket / Klimaticket (§ 26 Z 5 lit. b EStG)
        transit_monthly = round(max(0.0, transit_ticket_annual) / 12.0, 2)

        # 3. Zukunftssicherung (§ 3 Abs. 1 Z 15 lit. a EStG)
        future_sec_capped = min(cls.MAX_FUTURE_SECURITY_ANNUAL, max(0.0, future_security_annual))
        future_sec_monthly = round(future_sec_capped / 12.0, 2)

        # 4. Kinderbetreuungszuschuss (§ 3 Abs. 1 Z 13 lit. b EStG)
        childcare_annual = eligible_children_count * cls.MAX_CHILDCARE_PER_CHILD_ANNUAL
        childcare_monthly = round(childcare_annual / 12.0, 2)

        # 5. Sachzuwendungen & Geschenke (§ 3 Abs. 1 Z 14 EStG)
        allowed_gifts = cls.MAX_GIFTS_ANNUAL + (cls.MAX_JUBILEE_GIFTS_ANNUAL if jubilee_year else 0.0)
        gifts_capped = min(allowed_gifts, max(0.0, gifts_annual))
        gifts_monthly = round(gifts_capped / 12.0, 2)

        # 6. Mitarbeiter-Rabatt (§ 3 Abs. 1 Z 21 EStG)
        discount_capped = min(cls.MAX_STAFF_DISCOUNT_ANNUAL, max(0.0, staff_discount_annual))
        discount_monthly = round(discount_capped / 12.0, 2)

        total_tax_free_m = (
            meal_monthly +
            transit_monthly +
            future_sec_monthly +
            childcare_monthly +
            gifts_monthly +
            discount_monthly
        )

        annual_total = round(total_tax_free_m * 12.0, 2)

        return AustriaBenefitsResult(
            meal_vouchers_monthly=meal_monthly,
            meal_daily_rate=effective_rate,
            meal_days=meal_days,
            transit_ticket_monthly=transit_monthly,
            future_security_monthly=future_sec_monthly,
            childcare_monthly=childcare_monthly,
            gifts_annual=gifts_capped,
            gifts_monthly=gifts_monthly,
            staff_discount_monthly=discount_monthly,
            total_tax_free_monthly=round(total_tax_free_m, 2),
            annual_employee_net_benefit=annual_total,
            annual_employer_cost=annual_total, # 100% abgaben- und nebenkostenfrei!
        )
