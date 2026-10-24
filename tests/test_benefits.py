"""
test_benefits.py - Vollständige Test-Suite für sachbezug_dach
30+ automatisierte Tests für DE, AT, CH und den Gehaltserhöhungs-Optimierer.
"""

import pytest
from sachbezug_dach.svev_de import GermanyBenefitsCalculator
from sachbezug_dach.austria import AustriaBenefitsCalculator
from sachbezug_dach.switzerland import SwitzerlandBenefitsCalculator
from sachbezug_dach.salary_comparison import SalaryRaiseOptimizer

# ==========================================
# 1. DEUTSCHLAND TESTS (§ 8 EStG & SvEV 2026)
# ==========================================

def test_de_voucher_exactly_50_is_tax_free():
    res = GermanyBenefitsCalculator.calculate(voucher_value=50.00, zag_compliant=True)
    assert res.voucher_tax_free is True
    assert res.voucher_taxable_portion == 0.0

def test_de_voucher_50_01_is_fully_taxable():
    # Freigrenze: Bei 50.01 € ist der GESAMTE Betrag steuerpflichtig
    res = GermanyBenefitsCalculator.calculate(voucher_value=50.01, zag_compliant=True)
    assert res.voucher_tax_free is False
    assert res.voucher_taxable_portion == 50.01

def test_de_voucher_non_zag_is_taxable():
    res = GermanyBenefitsCalculator.calculate(voucher_value=40.00, zag_compliant=False)
    assert res.voucher_tax_free is False
    assert res.voucher_taxable_portion == 40.00

def test_de_svev_2026_constants():
    assert GermanyBenefitsCalculator.SVEV_2026_BREAKFAST == 2.30
    assert GermanyBenefitsCalculator.SVEV_2026_LUNCH == 4.40
    assert GermanyBenefitsCalculator.SVEV_2026_DINNER == 4.40
    assert GermanyBenefitsCalculator.SVEV_2026_MONTHLY_TOTAL == 333.00

def test_de_meal_voucher_daily_cap():
    # Maximal 7,50 € pro Tag steuerbegünstigt (4,40 € Sachbezugswert + 3,10 € steuerfreier AG-Zuschuss)
    res = GermanyBenefitsCalculator.calculate(meal_voucher_daily=10.00, meal_days=20)
    assert res.meal_total_daily_allowance == 7.50
    assert res.meal_total_monthly_benefit == 150.00

def test_de_jobticket_tax_free():
    res = GermanyBenefitsCalculator.calculate(jobticket_monthly=49.00)
    assert res.jobticket_monthly == 49.00

def test_de_health_promotion_annual_cap():
    res = GermanyBenefitsCalculator.calculate(health_annual=1000.00)
    # Gedeckelt auf 600 € / Jahr -> 50.00 € / Monat
    assert res.health_monthly == 50.00

def test_de_internet_allowance_flat_tax():
    res = GermanyBenefitsCalculator.calculate(internet_monthly=50.00)
    assert res.internet_monthly == 50.00
    # 50 € * 25% * 1.055 = 13.19 €
    assert res.internet_flat_tax == 13.19

def test_de_recreation_aid_calculation():
    res = GermanyBenefitsCalculator.calculate(has_spouse=True, children_count=2)
    # 156 (AN) + 104 (Ehegatte) + 2*52 (Kinder) = 364 €
    assert res.recreation_annual == 364.00

def test_de_amenities_personal_occasions():
    res = GermanyBenefitsCalculator.calculate(amenities_count=3)
    # 3 * 60 € = 180 €
    assert res.amenities_annual == 180.00

def test_de_staff_discount_cap():
    res = GermanyBenefitsCalculator.calculate(staff_discount_annual=1500.00)
    assert res.staff_discount_annual == 1080.00

# ==========================================
# 2. ÖSTERREICH TESTS (§ 3 EStG)
# ==========================================

def test_at_gastro_meal_voucher_cap():
    res = AustriaBenefitsCalculator.calculate(meal_voucher_type="gastro", custom_daily_voucher=12.00, meal_days=15)
    assert res.meal_daily_rate == 8.00
    assert res.meal_vouchers_monthly == 120.00

def test_at_grocery_meal_voucher_cap():
    res = AustriaBenefitsCalculator.calculate(meal_voucher_type="grocery", custom_daily_voucher=5.00, meal_days=15)
    assert res.meal_daily_rate == 2.00
    assert res.meal_vouchers_monthly == 30.00

def test_at_klimaticket_tax_free():
    res = AustriaBenefitsCalculator.calculate(transit_ticket_annual=1095.00)
    assert res.transit_ticket_monthly == round(1095.00 / 12.0, 2)

def test_at_future_security_cap():
    res = AustriaBenefitsCalculator.calculate(future_security_annual=500.00)
    assert res.future_security_monthly == round(300.00 / 12.0, 2)

def test_at_childcare_subsidy():
    res = AustriaBenefitsCalculator.calculate(eligible_children_count=2)
    # 2 * 2000 € = 4000 € / Jahr = 333.33 € / Monat
    assert res.childcare_monthly == 333.33

def test_at_gifts_standard_vs_jubilee():
    standard = AustriaBenefitsCalculator.calculate(gifts_annual=300.00, jubilee_year=False)
    assert standard.gifts_annual == 186.00

    jubilee = AustriaBenefitsCalculator.calculate(gifts_annual=500.00, jubilee_year=True)
    assert jubilee.gifts_annual == 372.00

def test_at_staff_discount_cap():
    res = AustriaBenefitsCalculator.calculate(staff_discount_annual=1500.00)
    assert res.staff_discount_monthly == round(1000.00 / 12.0, 2)

# ==========================================
# 3. SCHWEIZ TESTS (Lohnausweis & AHVV)
# ==========================================

def test_ch_lunch_check_cap():
    res = SwitzerlandBenefitsCalculator.calculate(lunch_check_monthly=250.00)
    assert res.lunch_check_monthly == 180.00

def test_ch_reka_discount_cap():
    res = SwitzerlandBenefitsCalculator.calculate(reka_discount_annual=1000.00)
    assert res.reka_discount_annual == 600.00
    assert res.reka_discount_monthly == 50.00

def test_ch_gifts_per_occasion():
    res = SwitzerlandBenefitsCalculator.calculate(occasions_count=2)
    # 2 * 500 CHF = 1000 CHF
    assert res.gifts_annual == 1000.00
    assert res.gifts_monthly == round(1000.00 / 12.0, 2)

def test_ch_transit_halbtax():
    res = SwitzerlandBenefitsCalculator.calculate(transit_contribution_annual=190.00)
    assert res.transit_contribution_monthly == round(190.00 / 12.0, 2)

# ==========================================
# 4. GEHALTSERHÖHUNGS-OPTIMIERER TESTS
# ==========================================

def test_salary_comparison_100_target():
    res = SalaryRaiseOptimizer.compare_fixed_net(target_net_monthly=100.00, marginal_tax_rate=0.35)
    # Um 100 € netto zu erzielen, braucht man klassisch ~224 € Brutto
    assert res.required_gross_salary_raise > 200.00
    # Arbeitgeber zahlt bei Brutto über 260 € inkl SV
    assert res.total_employer_cost_gross > 250.00
    # Bei Benefits zahlt der Arbeitgeber nur ~105 €
    assert res.total_employer_cost_benefits == 105.00
    # Ersparnis für KMU über 140 € pro Monat!
    assert res.monthly_employer_savings > 140.00
    assert res.employer_cost_reduction_percent > 50.0

def test_salary_comparison_positive_savings():
    res = SalaryRaiseOptimizer.compare_fixed_net(target_net_monthly=50.00)
    assert res.annual_employer_savings > 800.00
    assert res.employer_cost_reduction_percent > 50.0

# ==========================================
# 5. CLI & JSON TESTS
# ==========================================

def test_cli_de_json_output(monkeypatch, capsys):
    from sachbezug_dach.cli import main
    monkeypatch.setattr("sys.argv", ["dach-benefit", "de", "--voucher", "50", "--json"])
    main()
    captured = capsys.readouterr()
    assert '"voucher_amount": 50.0' in captured.out
    assert '"voucher_tax_free": true' in captured.out

def test_cli_at_json_output(monkeypatch, capsys):
    from sachbezug_dach.cli import main
    monkeypatch.setattr("sys.argv", ["dach-benefit", "at", "--type", "gastro", "--days", "15", "--json"])
    main()
    captured = capsys.readouterr()
    assert '"meal_vouchers_monthly": 120.0' in captured.out

def test_cli_ch_json_output(monkeypatch, capsys):
    from sachbezug_dach.cli import main
    monkeypatch.setattr("sys.argv", ["dach-benefit", "ch", "--lunch", "180", "--json"])
    main()
    captured = capsys.readouterr()
    assert '"lunch_check_monthly": 180.0' in captured.out

def test_cli_compare_json_output(monkeypatch, capsys):
    from sachbezug_dach.cli import main
    monkeypatch.setattr("sys.argv", ["dach-benefit", "compare", "--target-net", "100", "--json"])
    main()
    captured = capsys.readouterr()
    assert '"target_net_raise_monthly": 100.0' in captured.out
    assert '"monthly_employer_savings":' in captured.out

def test_de_lodging_constant():
    assert GermanyBenefitsCalculator.SVEV_2026_LODGING_MONTHLY == 282.00

def test_at_zero_children_childcare_is_zero():
    res = AustriaBenefitsCalculator.calculate(eligible_children_count=0)
    assert res.childcare_monthly == 0.0
