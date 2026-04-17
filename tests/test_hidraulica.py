"""
Validación hidráulica PCI contra referencias NFPA/SFPE.

Casos:
    1. Hazen-Williams manual verificable.
    2. Descarga rociador K-factor (NFPA 13 §3.6).
    3. Curva bomba NFPA 20.
"""

import pytest
from src.pci import hidraulica


class TestHazenWilliams:
    """NFPA 13 Ec. 23.4.4.7 — pérdida de fricción Hazen-Williams."""

    def test_caso_manual_100gpm_acero(self):
        """
        Caso verificable manualmente:
            Q = 100 gpm, C = 120 (acero ennegrecido húmedo),
            d = 4.000 in, L = 100 ft.
        p_f/ft = 4.52 · 100^1.85 / (120^1.85 · 4.000^4.87)
               ≈ 0.00378 psi/ft
        Total  ≈ 0.378 psi
        """
        p = hidraulica.perdida_hazen_williams_psi(
            Q_gpm=100.0, C=120.0, d_in=4.0, L_ft=100.0
        )
        assert pytest.approx(p, abs=0.01) == 0.378

    def test_caso_sfpe_handbook_cap40_ejemplo(self):
        """
        Referencia: SFPE Handbook, 5th ed., Cap. 40, Ejemplo 40.3 (orientativo).
        Valores típicos de tubería 6-in Sch 40, C=120, Q=500 gpm, L=200 ft.
        Resultado esperado ~ 1.95 psi (verificado con calculadora HW).
        """
        p = hidraulica.perdida_hazen_williams_psi(
            Q_gpm=500.0, C=120.0, d_in=6.065, L_ft=200.0
        )
        assert pytest.approx(p, abs=0.05) == 1.95


class TestRociador:
    """NFPA 13 §3.6 — Q = K·√P."""

    def test_k56_7psi(self):
        """K=5.6, P=7 psi → Q = 5.6·√7 ≈ 14.81 gpm."""
        assert pytest.approx(
            hidraulica.caudal_rociador_gpm(K=5.6, P_psi=7.0), abs=0.01
        ) == 14.81

    def test_presion_minima_7psi(self):
        with pytest.raises(ValueError, match="P ≥ 7 psi"):
            hidraulica.caudal_rociador_gpm(K=5.6, P_psi=6.9)


class TestCurvaBomba:
    """NFPA 20 — validación de límites de curva característica."""

    def test_valida_cumple(self):
        bomba = hidraulica.CurvaBomba(
            P_churn_psi=140.0, Q_diseno_gpm=500.0,
            P_diseno_psi=100.0, P_150_psi=70.0
        )
        r = bomba.valida_nfpa20()
        assert r["churn_ok"] is True   # 140 ≤ 140
        assert r["150pct_ok"] is True  # 70 ≥ 65

    def test_valida_falla_churn(self):
        bomba = hidraulica.CurvaBomba(
            P_churn_psi=150.0, Q_diseno_gpm=500.0,
            P_diseno_psi=100.0, P_150_psi=70.0
        )
        assert bomba.valida_nfpa20()["churn_ok"] is False

    def test_valida_falla_150pct(self):
        bomba = hidraulica.CurvaBomba(
            P_churn_psi=130.0, Q_diseno_gpm=500.0,
            P_diseno_psi=100.0, P_150_psi=60.0
        )
        assert bomba.valida_nfpa20()["150pct_ok"] is False
