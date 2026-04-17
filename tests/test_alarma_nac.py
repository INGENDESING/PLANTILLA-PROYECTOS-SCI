"""
Validación alarma y notificación — NFPA 72 §10.6 / §18.4.
"""

import pytest
from src.pci import alarma_nac


class TestBateria:
    def test_caso_manual(self):
        """
        I_sb = 2 A, 24 h; I_alarma = 5 A, 5 min.
        Cruda = 2·24 + 5·(5/60) = 48 + 0.417 = 48.417 Ah.
        Con factor 1.20 → 58.10 Ah.
        """
        c = alarma_nac.capacidad_bateria_Ah(
            I_standby_A=2.0, t_standby_h=24.0,
            I_alarma_A=5.0, t_alarma_min=5.0,
            factor_envejecimiento=1.20,
        )
        assert pytest.approx(c, abs=0.1) == 58.10


class TestCaidaTension:
    def test_12awg_1A_500ft(self):
        """
        AWG 12 ≈ 1.6 ohm/kft (NEC Cap. 9 Tabla 8, ~75 °C).
        R = 2·500/1000 · 1.6 = 1.6 ohm.
        ΔV = 1·1.6 = 1.6 V.
        """
        dv = alarma_nac.caida_tension_circuito_V(
            I_A=1.0, L_ft=500.0, AWG_resistencia_ohm_kft=1.6
        )
        assert pytest.approx(dv, abs=0.1) == 1.6


class TestAudibilidad:
    def test_atenuacion_doblar_distancia(self):
        """Doble distancia → −6 dB."""
        db = alarma_nac.nivel_sonoro_dB_a_distancia(
            dB_ref=100.0, d_ref_m=10.0, d_m=20.0
        )
        assert pytest.approx(db, abs=0.1) == 94.0

    def test_distancia_negativa_error(self):
        with pytest.raises(ValueError):
            alarma_nac.nivel_sonoro_dB_a_distancia(100.0, 10.0, -5.0)
