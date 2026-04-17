"""
Espumas de extinción — NFPA 11 (baja/media/alta expansión) y NFPA 16 (foam-water).

Stub base: tasa de aplicación y proporcionador.
"""

from __future__ import annotations


def tasa_aplicacion_gpm_ft2(clase_liquido: str, tipo_tanque: str) -> float:
    """
    Tasa de aplicación mínima según NFPA 11 Tabla 5.2.5.2.1 (ed. vigente).

    Ejemplos (confirmar edición):
        hidrocarburo / cono_fijo / tipo_II -> 0.10 gpm/ft²
        alcohol-soluble / cono_fijo         -> 0.16 gpm/ft² (ajustar por producto)

    Esta función es un stub; poblar tabla completa al inicio del proyecto.
    """
    raise NotImplementedError("Poblar tabla NFPA 11 §5.2.5 por proyecto.")


def caudal_solucion_espuma_gpm(area_ft2: float, tasa_gpm_ft2: float) -> float:
    """Caudal total de solución agua+concentrado espumante."""
    return area_ft2 * tasa_gpm_ft2


def caudal_concentrado_gpm(Q_solucion_gpm: float, pct_concentrado: float) -> float:
    """Caudal de concentrado: 1%, 3% o 6% según el proporcionador."""
    return Q_solucion_gpm * (pct_concentrado / 100.0)
