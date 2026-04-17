"""
Validación detección — NFPA 72 §17.6–17.8.
"""

import math

import pytest
from src.pci import deteccion


class TestDetectoresCalor:
    def test_area_2500ft2_espaciamiento_15ft(self):
        """2500 ft² / (15²) = 11.11 → 12 detectores."""
        assert deteccion.n_detectores_calor(2500.0, 15.0) == 12


class TestDetectoresHumo:
    def test_default_30ft(self):
        """10000 ft² / (30²) = 11.11 → 12 detectores."""
        assert deteccion.n_detectores_humo(10000.0) == 12


class TestCoberturaLlama:
    def test_angulo_90_distancia_10m(self):
        """
        r = 10·cos(45°) = 7.071 m.
        Área = π·r² ≈ 157.1 m².
        """
        a = deteccion.cobertura_detector_llama_m2(10.0, 90.0)
        assert pytest.approx(a, abs=0.5) == 157.1
