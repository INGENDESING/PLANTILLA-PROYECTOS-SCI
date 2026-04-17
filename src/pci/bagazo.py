"""
Aplicación a plantas de cogeneración a partir de bagazo.

Referencias normativas clave:
    NFPA 850 — Fire Protection for Electric Generating Plants (calderas, turbinas,
               transformadores, cables, hidrógeno).
    NFPA 654 — Prevention of Fires and Dust Explosions from Combustible
               Particulate Solids (silos, transportadores, ciclones, filtros).
    NFPA 664 — Prevention of Fires and Explosions in Wood Processing (aplicable
               por analogía al bagazo como biomasa lignocelulósica).
    NFPA 499 — Classification of Combustible Dusts (áreas Clase II).
    NFPA 61  — Fires and Dust Explosions in Agricultural and Food Processing.

Este módulo concentra reglas de selección y criterios específicos del escenario
bagazo-cogeneración. No duplica las funciones generales de `hidraulica.py`,
`agentes_limpios.py`, etc.
"""

from __future__ import annotations

from dataclasses import dataclass


# Propiedades representativas del bagazo (referenciar fuente al usarlas)
PCI_BAGAZO_kJkg = 7700.0          # PCI típico 50% humedad (Hugot, Handbook of Cane Sugar Engineering)
KST_BAGAZO_bar_m_s = 120.0        # clase St1 (orientativo; medir por proyecto)
MIE_BAGAZO_mJ = 30.0              # mínima energía de ignición (orientativa)


@dataclass
class EscenarioFuegoBagazo:
    id: str
    ubicacion: str                 # patio, silo, transportador, caldera, turbina, TX, cable
    combustible: str
    modo_ignicion: str
    consecuencia_esperada: str


def sistema_recomendado(ubicacion: str) -> str:
    """
    Criterio orientativo de selección (NFPA 850 y buenas prácticas industria bagaceña).
    Debe validarse por proyecto contra HAZOP y AHJ.
    """
    mapa = {
        "patio_bagazo": "Monitores + rociadores perimetrales (agua)",
        "silo": "Supresión de explosión + inertización N₂/CO₂ + venteo (NFPA 68/69)",
        "transportador_banda": "Rociadores lineales + detección chispas IR/UV",
        "caldera": "Espuma AFFF para zona aceite lubricación; CO₂ en ducts",
        "turbina_vapor": "CO₂/agua pulverizada en cojinetes y aceite (NFPA 850)",
        "transformador": "Diluvio de agua pulverizada NFPA 15; o agente limpio en sala",
        "sala_control": "Agente limpio NFPA 2001 + detección muy temprana (VESDA)",
        "cable_tray": "Rociadores + sellos cortafuego; recubrimiento intumescente",
    }
    return mapa.get(ubicacion, "Pendiente de análisis específico")
