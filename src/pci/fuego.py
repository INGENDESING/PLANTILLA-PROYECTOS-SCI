"""
Termodinámica del fuego — SFPE Handbook / NFPA 921.

Incluye HRR, pluma de Heskestad, radiación a blanco y criterio de flashover.
Unidades SI.
"""

from __future__ import annotations

import math

G = 9.81          # m/s²
T_INF = 293.15    # K (ambiente por defecto)
CP_AIR = 1.005    # kJ/kg·K
RHO_INF = 1.204   # kg/m³


def hrr_kw(m_dot_f_kgs: float, delta_Hc_kJkg: float, chi: float = 0.85) -> float:
    """
    Heat Release Rate: Q̇ = ṁ_f · ΔH_c · χ.

    chi : eficiencia de combustión (0.7–0.95 típ.). SFPE Handbook Cap. 26.
    """
    return m_dot_f_kgs * delta_Hc_kJkg * chi


def heskestad_altura_virtual_m(Q_kw: float, D_m: float) -> float:
    """Altura virtual z₀ = 0.083·Q^(2/5) − 1.02·D (SFPE Heskestad)."""
    return 0.083 * (Q_kw ** 0.4) - 1.02 * D_m


def heskestad_temperatura_centerline_K(
    Q_kw: float, D_m: float, z_m: float, chi_c: float = 0.7, T_inf: float = T_INF
) -> float:
    """
    Temperatura en el eje de la pluma (Heskestad).

    T_cl - T_∞ = 9.1·[T_∞/(g·cp²·ρ_∞²)]^(1/3) · Q_c^(2/3) · (z - z₀)^(-5/3)
    """
    Q_c = chi_c * Q_kw
    z0 = heskestad_altura_virtual_m(Q_kw, D_m)
    if z_m - z0 <= 0:
        raise ValueError("z debe ser mayor que z₀ para aplicar Heskestad.")
    coef = 9.1 * (T_inf / (G * (CP_AIR ** 2) * (RHO_INF ** 2))) ** (1 / 3)
    return T_inf + coef * (Q_c ** (2 / 3)) * ((z_m - z0) ** (-5 / 3))


def radiacion_a_blanco_kw_m2(
    Q_kw: float, r_m: float, chi_r: float = 0.3, F: float = 1.0
) -> float:
    """
    Flujo radiativo a blanco puntual: q̇'' = F · χ_r · Q̇ / (4π·r²).

    χ_r : fracción radiativa (0.15–0.4 según combustible).
    F   : factor de configuración (1 si blanco enfrentado al incendio).
    """
    return F * chi_r * Q_kw / (4 * math.pi * r_m ** 2)


def hrr_flashover_thomas_kw(A_T_m2: float, A_v_m2: float, H_v_m: float) -> float:
    """
    Criterio de Thomas para flashover en recinto (SFPE Handbook):
    Q̇_fo ≈ 7.8·A_T + 378·A_v·√H_v   [kW]
    """
    return 7.8 * A_T_m2 + 378 * A_v_m2 * math.sqrt(H_v_m)
