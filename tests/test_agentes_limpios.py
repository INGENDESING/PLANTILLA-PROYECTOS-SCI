"""
Validación agentes limpios PCI — NFPA 2001.

Casos:
    1. Masa FM-200 verificable manualmente.
    2. Verificación ocupación normal (NOAEL).
    3. Concentración de diseño con factor de seguridad.
"""

import pytest
from src.pci import agentes_limpios


class TestMasaAgente:
    """NFPA 2001 Ec. 5.5.1.1."""

    def test_fm200_manual(self):
        """
        FM-200 (HFC-227ea):
            k1 = 0.1269, k2 = 0.000513
            T = 20 °C → s = 0.1269 + 0.000513·20 = 0.13716 m³/kg
            V = 100 m³, C = 5.8 %
            m = (100 / 0.13716) · (5.8 / 94.2)
              ≈ 729.08 · 0.06157
              ≈ 44.89 kg
        """
        m = agentes_limpios.masa_agente_kg(
            agente=agentes_limpios.FM200,
            V_m3=100.0,
            C_pct=5.8,
            T_C=20.0,
        )
        assert pytest.approx(m, abs=0.1) == 44.89

    def test_novec1230_manual(self):
        """
        Novec 1230:
            k1 = 0.0664, k2 = 0.000274
            T = 20 °C → s = 0.0664 + 0.000274·20 = 0.07188 m³/kg
            V = 200 m³, C = 4.2 %
            m = (200 / 0.07188) · (4.2 / 95.8)
              ≈ 2782.4 · 0.04384
              ≈ 122.0 kg
        """
        m = agentes_limpios.masa_agente_kg(
            agente=agentes_limpios.NOVEC1230,
            V_m3=200.0,
            C_pct=4.2,
            T_C=20.0,
        )
        assert pytest.approx(m, abs=0.5) == 122.0

    def test_concentracion_100_error(self):
        with pytest.raises(ValueError, match="< 100%"):
            agentes_limpios.masa_agente_kg(
                agente=agentes_limpios.FM200,
                V_m3=100.0, C_pct=100.0, T_C=20.0
            )


class TestVerificacionOcupacion:
    """NFPA 2001 §1.5.1.2 — C_diseño ≤ NOAEL."""

    def test_fm200_cumple(self):
        r = agentes_limpios.verifica_ocupacion_normal(
            agente=agentes_limpios.FM200, C_pct=9.0
        )
        assert r["apto_ocupacion_normal"] is True
        assert r["margen_pct"] == 0.0

    def test_fm200_no_cumple(self):
        r = agentes_limpios.verifica_ocupacion_normal(
            agente=agentes_limpios.FM200, C_pct=10.0
        )
        assert r["apto_ocupacion_normal"] is False
        assert r["margen_pct"] == pytest.approx(-1.0, abs=0.01)


class TestConcentracionDiseno:
    """NFPA 2001 §5.4 — factor de seguridad."""

    def test_fm200_sf_default(self):
        """FM-200 extinción 5.8 % × 1.20 = 6.96 %."""
        cd = agentes_limpios.concentracion_diseno_pct(agentes_limpios.FM200)
        assert pytest.approx(cd, abs=0.01) == 6.96

    def test_ig541_sf_clase_a(self):
        """IG-541 extinción 34.2 % × 1.30 = 44.46 %."""
        cd = agentes_limpios.concentracion_diseno_pct(
            agentes_limpios.IG541, safety_factor=1.30
        )
        assert pytest.approx(cd, abs=0.01) == 44.46
