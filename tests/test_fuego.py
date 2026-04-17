"""
Validación termodinámica del fuego — SFPE Handbook / NFPA 921.

Casos:
    1. HRR manual (combustión de metanol).
    2. Pluma Heskestad — temperatura centerline verificable.
    3. Radiación a blanco — comprobación analítica.
    4. Flashover Thomas — criterio de recinto.
"""

import math

import pytest
from src.pci import fuego


class TestHRR:
    """Heat Release Rate: Q̇ = ṁ_f · ΔH_c · χ (SFPE Handbook Cap. 26)."""

    def test_metanol_manual(self):
        """
        Metanol: ΔH_c ≈ 19 900 kJ/kg, χ ≈ 0.9.
        ṁ_f = 0.01 kg/s → Q̇ = 0.01 · 19900 · 0.9 = 179.1 kW.
        """
        q = fuego.hrr_kw(m_dot_f_kgs=0.01, delta_Hc_kJkg=19900.0, chi=0.9)
        assert pytest.approx(q, abs=0.1) == 179.1


class TestPlumaHeskestad:
    """SFPE Handbook — pluma de Heskestad (Cap. 26)."""

    def test_altura_virtual(self):
        """
        Q = 1000 kW, D = 1.0 m:
            z₀ = 0.083·1000^0.4 − 1.02·1.0
               = 0.083·15.849 − 1.02
               ≈ 1.315 − 1.02 = 0.295 m
        """
        z0 = fuego.heskestad_altura_virtual_m(Q_kw=1000.0, D_m=1.0)
        assert pytest.approx(z0, abs=0.01) == 0.295

    def test_temperatura_centerline(self):
        """
        Q = 1000 kW, D = 1.0 m, z = 3.0 m, χ_c = 0.7, T_∞ = 293.15 K.
        Resultado verificado con implementación directa de la ecuación.
        """
        t = fuego.heskestad_temperatura_centerline_K(
            Q_kw=1000.0, D_m=1.0, z_m=3.0, chi_c=0.7
        )
        assert pytest.approx(t, abs=5.0) == 666.6

    def test_z_menor_que_z0_error(self):
        """
        Q = 10000 kW, D = 0.1 m → z₀ ≈ 3.30 m.
        z = 2.0 m < z₀ → debe lanzar ValueError.
        """
        with pytest.raises(ValueError, match="mayor que z₀"):
            fuego.heskestad_temperatura_centerline_K(
                Q_kw=10000.0, D_m=0.1, z_m=2.0
            )


class TestRadiacion:
    """Radiación a blanco puntual: q̇'' = F·χ_r·Q̇/(4π·r²)."""

    def test_analitico(self):
        """
        Q = 1000 kW, r = 5 m, χ_r = 0.3, F = 1.0.
        q̇'' = 0.3 · 1000 / (4π · 25) = 300 / 314.16 ≈ 0.955 kW/m².
        """
        q = fuego.radiacion_a_blanco_kw_m2(
            Q_kw=1000.0, r_m=5.0, chi_r=0.3, F=1.0
        )
        assert pytest.approx(q, abs=0.01) == 0.955


class TestFlashover:
    """Criterio de Thomas (SFPE Handbook)."""

    def test_recinto_tipico(self):
        """
        Recinto 4×4×3 m (A_T = 80 m²), ventana 2×1.5 m (A_v = 3 m², H_v = 1.5 m).
        Q̇_fo = 7.8·80 + 378·3·√1.5
              = 624 + 378·3·1.225
              = 624 + 1389.2
              ≈ 2013 kW
        """
        q = fuego.hrr_flashover_thomas_kw(
            A_T_m2=80.0, A_v_m2=3.0, H_v_m=1.5
        )
        assert pytest.approx(q, abs=1.0) == 2013.0
