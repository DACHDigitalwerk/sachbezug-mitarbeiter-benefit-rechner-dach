"""
salary_comparison.py - Vergleichsrechner: Klassische Gehaltserhöhung vs. Steuerfreie Benefits
Rechnet den exakten Netto-Vorteil für den Arbeitnehmer und die Kosteneinsparung für den Arbeitgeber aus.
"""

from dataclasses import dataclass

@dataclass
class ComparisonResult:
    target_net_raise_monthly: float
    
    # Variante A: Klassische Bruttolohn-Erhöhung
    required_gross_salary_raise: float
    employer_social_security_raise: float
    total_employer_cost_gross: float
    employee_tax_deduction: float
    employee_social_deduction: float
    effective_employee_net_gross: float

    # Variante B: Steuerfreie / pauschalversteuerte Benefits
    benefit_net_value: float
    benefit_employer_flat_taxes: float
    total_employer_cost_benefits: float

    # Ersparnis & Hebel
    monthly_employer_savings: float
    annual_employer_savings: float
    employer_cost_reduction_percent: float


class SalaryRaiseOptimizer:
    # Standard-Kalkulationssätze KMU (DE Richtwerte 2026)
    DEFAULT_EMPLOYER_SV_RATE = 0.205   # ~20,5 % AG-Anteil SV (KV, PV, RV, AV, U-Umlagen)
    DEFAULT_EMPLOYEE_SV_RATE = 0.205   # ~20,5 % AN-Anteil SV
    DEFAULT_MARGINAL_TAX_RATE = 0.35   # ~35 % Grenzsteuersatz typischer Fachangestellter

    @classmethod
    def compare_fixed_net(
        cls,
        target_net_monthly: float = 100.00,
        marginal_tax_rate: float = 0.35,
        employer_sv_rate: float = 0.205,
        employee_sv_rate: float = 0.205,
        average_benefit_tax_drag: float = 0.05, # Durchschnittliche AG-Pauschalsteuer auf Benefits
    ) -> ComparisonResult:
        """
        Berechnet den Aufwand beider Varianten, um beim Mitarbeiter denselben
        Netto-Kaufkraftzuwachs (target_net_monthly) zu erzielen.
        """
        # Netto-Faktor im klassischen Brutto: Netto = Brutto * (1 - Grenzsteuer - AN-SV)
        net_retention = max(0.20, 1.0 - marginal_tax_rate - employee_sv_rate)
        
        # Erforderliches Brutto, um target_net_monthly netto rauszubekommen:
        req_gross = round(target_net_monthly / net_retention, 2)
        ag_sv_gross = round(req_gross * employer_sv_rate, 2)
        total_ag_gross = round(req_gross + ag_sv_gross, 2)

        tax_ded = round(req_gross * marginal_tax_rate, 2)
        an_sv_ded = round(req_gross * employee_sv_rate, 2)
        actual_net_gross = round(req_gross - tax_ded - an_sv_ded, 2)

        # Variante B: Steuerfreie Benefits
        benefit_net = target_net_monthly
        benefit_ag_taxes = round(benefit_net * average_benefit_tax_drag, 2)
        total_ag_benefit = round(benefit_net + benefit_ag_taxes, 2)

        savings_m = round(total_ag_gross - total_ag_benefit, 2)
        savings_y = round(savings_m * 12.0, 2)
        savings_pct = round((savings_m / total_ag_gross) * 100.0, 1) if total_ag_gross > 0 else 0.0

        return ComparisonResult(
            target_net_raise_monthly=target_net_monthly,
            required_gross_salary_raise=req_gross,
            employer_social_security_raise=ag_sv_gross,
            total_employer_cost_gross=total_ag_gross,
            employee_tax_deduction=tax_ded,
            employee_social_deduction=an_sv_ded,
            effective_employee_net_gross=actual_net_gross,
            benefit_net_value=benefit_net,
            benefit_employer_flat_taxes=benefit_ag_taxes,
            total_employer_cost_benefits=total_ag_benefit,
            monthly_employer_savings=savings_m,
            annual_employer_savings=savings_y,
            employer_cost_reduction_percent=savings_pct,
        )
