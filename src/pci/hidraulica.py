"""
Hidráulica PCI — NFPA 13, 14, 20, 24.

Incluye Hazen-Williams, descarga de rociadores K-factor, y esqueleto
de análisis nodal. Cálculos expresados en US customary (NFPA nativo).
"""

from __future__ import annotations

import math
from dataclasses import dataclass


# Coeficientes C de Hazen-Williams según NFPA 13, Tabla 23.4.4.7.1 (ed. vigente)
C_HW = {
    "acero_ennegrecido_humedo": 120,
    "acero_ennegrecido_seco": 100,
    "acero_galvanizado": 120,
    "cpvc": 150,
    "cobre": 150,
    "hierro_fundido_nuevo": 130,
}


def perdida_hazen_williams_psi(
    Q_gpm: float, C: float, d_in: float, L_ft: float
) -> float:
    """
    Pérdida de fricción en tubería por Hazen-Williams (NFPA 13, Ec. 23.4.4.7).

    p_f = 4.52 · Q^1.85 / (C^1.85 · d^4.87)   [psi/ft]

    Parámetros
    ----------
    Q_gpm : caudal [gpm]
    C     : coeficiente de Hazen-Williams (ver C_HW)
    d_in  : diámetro interno real [in]
    L_ft  : longitud equivalente [ft]

    Retorna
    -------
    Pérdida total [psi].

    Validación
    ----------
    SFPE Handbook, 5th ed., Cap. 40; NFPA 13 Annex A.
    """
    p_f_por_ft = 4.52 * (Q_gpm ** 1.85) / ((C ** 1.85) * (d_in ** 4.87))
    return p_f_por_ft * L_ft


def caudal_rociador_gpm(K: float, P_psi: float) -> float:
    """
    Descarga de rociador: Q = K·√P  (NFPA 13 §3.6.*).

    K en unidades US (gpm/psi^0.5). Valores típicos: 5.6, 8.0, 11.2, 14.0, 16.8.
    """
    if P_psi < 7:
        raise ValueError("NFPA 13 exige P ≥ 7 psi en el rociador hidráulicamente más remoto.")
    return K * math.sqrt(P_psi)


@dataclass
class CurvaBomba:
    """Curva de bomba NFPA 20 — puntos churn, diseño, 150%."""
    P_churn_psi: float
    Q_diseno_gpm: float
    P_diseno_psi: float
    P_150_psi: float

    def valida_nfpa20(self) -> dict:
        """Valida límites NFPA 20: churn ≤ 140% P_diseño; P@150%Q ≥ 65% P_diseño."""
        return {
            "churn_ok": self.P_churn_psi <= 1.40 * self.P_diseno_psi,
            "150pct_ok": self.P_150_psi >= 0.65 * self.P_diseno_psi,
        }


def densidad_a_caudal_requerido_gpm(densidad_gpm_ft2: float, area_ft2: float) -> float:
    """Caudal mínimo requerido por densidad/área (NFPA 13 §19.2.3)."""
    return densidad_gpm_ft2 * area_ft2
