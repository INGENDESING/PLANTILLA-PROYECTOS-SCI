"""
Detección — NFPA 72.

Espaciamiento de detectores de calor, humo y llama.
"""

from __future__ import annotations

import math


def n_detectores_calor(area_ft2: float, espaciamiento_ft: float) -> int:
    """
    Cantidad mínima de detectores puntuales de calor (NFPA 72 §17.6).
    Área cuadrada máxima por detector = espaciamiento².
    """
    area_unitaria = espaciamiento_ft ** 2
    return math.ceil(area_ft2 / area_unitaria)


def n_detectores_humo(area_ft2: float, espaciamiento_ft: float = 30.0) -> int:
    """NFPA 72 §17.7: espaciamiento nominal 30 ft (habitaciones lisas)."""
    area_unitaria = espaciamiento_ft ** 2
    return math.ceil(area_ft2 / area_unitaria)


def cobertura_detector_llama_m2(distancia_max_m: float, angulo_cono_deg: float) -> float:
    """
    Cobertura de detector de llama (UV/IR) aproximada como sector circular.
    NFPA 72 §17.8.
    """
    r = distancia_max_m * math.cos(math.radians(angulo_cono_deg / 2))
    return math.pi * r ** 2
