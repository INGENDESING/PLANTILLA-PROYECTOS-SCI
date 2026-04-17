"""
Clasificación de áreas peligrosas — NEC (NFPA 70) Art. 500–505, API RP 500/505, NFPA 499.

Modelo simplificado por Clase/División (sistema tradicional US) y Zona (IEC/Art. 505).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Clase = Literal["I", "II", "III"]      # I=gases, II=polvos, III=fibras
Division = Literal["1", "2"]
Zona_gases = Literal["0", "1", "2"]
Zona_polvos = Literal["20", "21", "22"]


@dataclass
class AreaClasificada:
    id: str
    descripcion: str
    clase: Clase
    division: Division | None = None
    zona: Zona_gases | Zona_polvos | None = None
    grupo: str | None = None           # A-D (Clase I), E-G (Clase II) — NEC
    temperatura_codigo: str | None = None  # T1..T6 — NEC Art. 500.8
    fuente_ignicion: str | None = None


def equivalencia_division_zona(division: Division, clase: Clase) -> str:
    """
    Mapeo indicativo División ↔ Zona (NEC Art. 505.9 / IEC 60079).
    Clase I Div 1 ≈ Zona 0 + Zona 1; Div 2 ≈ Zona 2.
    Clase II Div 1 ≈ Zona 20 + Zona 21; Div 2 ≈ Zona 22.
    """
    if clase == "I":
        return "Zona 0/1" if division == "1" else "Zona 2"
    if clase == "II":
        return "Zona 20/21" if division == "1" else "Zona 22"
    return "N/A"
