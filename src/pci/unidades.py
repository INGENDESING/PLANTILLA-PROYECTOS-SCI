"""
Conversiones SI <-> US customary para PCI.

NFPA trabaja nativamente en US customary (gpm, psi, ft, ft², BTU/s).
Este módulo expone factores de conversión documentados y un registro `pint`.
"""

from __future__ import annotations

try:
    from pint import UnitRegistry
    ureg = UnitRegistry()
    Q_ = ureg.Quantity
except ImportError:  # pint opcional
    ureg = None
    Q_ = None

# Factores de conversión directos (si pint no está disponible)
GPM_A_M3S = 6.30901964e-5       # 1 gpm -> m³/s
M3S_A_GPM = 1 / GPM_A_M3S
PSI_A_PA = 6894.757
PA_A_PSI = 1 / PSI_A_PA
FT_A_M = 0.3048
M_A_FT = 1 / FT_A_M
BTU_A_J = 1055.056
KW_A_BTUS = 0.9478171            # 1 kW -> BTU/s
GAL_A_M3 = 3.785411784e-3
LB_A_KG = 0.45359237


def gpm_a_lpm(q_gpm: float) -> float:
    """gpm (US) -> L/min."""
    return q_gpm * 3.785411784


def gpm_ft2_a_mm_min(d_gpm_ft2: float) -> float:
    """Densidad NFPA 13: gpm/ft² -> mm/min (L/min·m²)."""
    return d_gpm_ft2 * 40.7458  # (3.7854 L/gal * 1 ft² / 0.09290 m²)


def psi_a_bar(p_psi: float) -> float:
    return p_psi * 0.0689476
