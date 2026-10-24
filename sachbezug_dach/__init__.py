"""
sachbezug_dach - DACH Sachbezug-, Essensgutschein- & Mitarbeiter-Benefit-Optimierer 2026 (DE, AT, CH)
Reine kaufmännische, steuerliche und sozialversicherungsrechtliche Tarif- und Freibetragsmathematik.
Konform mit BGH Smartlaw (Az. I ZR 226/20) - 100% Client-Side / Offline-tauglich.
"""

__version__ = "1.0.0"
__author__ = "DACH Digitalwerk"

from .svev_de import GermanyBenefitsCalculator
from .austria import AustriaBenefitsCalculator
from .switzerland import SwitzerlandBenefitsCalculator
from .salary_comparison import SalaryRaiseOptimizer

__all__ = [
    "GermanyBenefitsCalculator",
    "AustriaBenefitsCalculator",
    "SwitzerlandBenefitsCalculator",
    "SalaryRaiseOptimizer",
]
