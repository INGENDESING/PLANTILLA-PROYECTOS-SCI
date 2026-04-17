"""
Análisis de riesgos — HAZOP + What-If base, matriz de riesgo.

Módulo base: estructuras de datos para registro HAZOP y matriz severidad×probabilidad.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

PalabraGuia = Literal["NO", "MAS", "MENOS", "INVERSO", "TAMBIEN", "PARTE_DE", "OTRO"]


@dataclass
class NodoHAZOP:
    id: str
    descripcion: str
    intencion_diseno: str


@dataclass
class RegistroHAZOP:
    nodo: str
    palabra_guia: PalabraGuia
    desviacion: str
    causas: list[str] = field(default_factory=list)
    consecuencias: list[str] = field(default_factory=list)
    salvaguardas_existentes: list[str] = field(default_factory=list)
    severidad: int = 0       # 1–5
    probabilidad: int = 0    # 1–5
    recomendaciones: list[str] = field(default_factory=list)

    @property
    def riesgo(self) -> int:
        return self.severidad * self.probabilidad


def categoria_riesgo(riesgo: int) -> str:
    """Categorización estándar para matriz 5×5."""
    if riesgo >= 20:
        return "INACEPTABLE"
    if riesgo >= 12:
        return "ALTO"
    if riesgo >= 6:
        return "MODERADO"
    return "BAJO"
