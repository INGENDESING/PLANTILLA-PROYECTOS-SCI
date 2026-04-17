"""
Alarma y notificación — NFPA 72 + NEC (NFPA 70).

Cálculo de batería standby+alarma, caída de tensión en NAC/SLC y audibilidad.
"""

from __future__ import annotations

import math


def capacidad_bateria_Ah(
    I_standby_A: float, t_standby_h: float,
    I_alarma_A: float, t_alarma_min: float,
    factor_envejecimiento: float = 1.20,
) -> float:
    """
    NFPA 72 §10.6.10: capacidad mínima de batería con factor de envejecimiento.

        C = (I_sb · t_sb + I_alarma · t_alarma) · factor
    """
    Ah = I_standby_A * t_standby_h + I_alarma_A * (t_alarma_min / 60.0)
    return Ah * factor_envejecimiento


def caida_tension_circuito_V(
    I_A: float, L_ft: float, AWG_resistencia_ohm_kft: float,
) -> float:
    """
    Caída en circuito NAC/SLC (ida y vuelta): ΔV = 2·I·R.
    R se toma de tabla NEC Cap. 9 Tabla 8 (resistencia por kft).
    """
    R_ohm = (2 * L_ft / 1000.0) * AWG_resistencia_ohm_kft
    return I_A * R_ohm


def nivel_sonoro_dB_a_distancia(
    dB_ref: float, d_ref_m: float, d_m: float
) -> float:
    """
    Atenuación en campo libre: ΔdB = 20·log10(d/d_ref).
    NFPA 72 §18.4 requiere ≥ 15 dB por encima del ruido ambiente promedio.
    """
    if d_m <= 0 or d_ref_m <= 0:
        raise ValueError("Distancias deben ser positivas.")
    return dB_ref - 20 * math.log10(d_m / d_ref_m)
