"""
Agentes limpios — NFPA 2001 (halocarbonados e inertes), NFPA 12/12A.

Calcula masa de agente, concentración y verifica límites NOAEL para ocupación normal.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AgenteLimpio:
    nombre: str
    k1: float              # volumen específico a 0 °C [m³/kg]
    k2: float              # pendiente [m³/(kg·°C)]
    NOAEL_pct: float       # NFPA 2001 Tabla 1.5.1.2
    LOAEL_pct: float
    conc_extincion_pct: float

    def s_m3_kg(self, T_C: float) -> float:
        """Volumen específico superheated: s = k1 + k2·T."""
        return self.k1 + self.k2 * T_C


# Datos representativos (NFPA 2001, ed. vigente — confirmar edición por proyecto)
FM200 = AgenteLimpio("HFC-227ea (FM-200)", 0.1269, 0.000513, NOAEL_pct=9.0, LOAEL_pct=10.5, conc_extincion_pct=5.8)
NOVEC1230 = AgenteLimpio("FK-5-1-12 (Novec 1230)", 0.0664, 0.000274, NOAEL_pct=10.0, LOAEL_pct=10.0, conc_extincion_pct=4.2)
IG541 = AgenteLimpio("IG-541 (Inergen)", 0.65799, 0.00239, NOAEL_pct=43.0, LOAEL_pct=52.0, conc_extincion_pct=34.2)


def concentracion_diseno_pct(agente: AgenteLimpio, safety_factor: float = 1.20) -> float:
    """
    Concentración de diseño = concentración de extinción × factor de seguridad.
    NFPA 2001 §5.4: S.F. mínimo 1.20 para Clase B, 1.30 Clase A.
    """
    return agente.conc_extincion_pct * safety_factor


def masa_agente_kg(
    agente: AgenteLimpio, V_m3: float, C_pct: float, T_C: float
) -> float:
    """
    Masa de agente a descargar (NFPA 2001 Ec. 5.5.1.1):
        m = (V / s) · (C / (100 - C))

    Parámetros
    ----------
    V_m3 : volumen neto del recinto protegido [m³]
    C_pct: concentración de diseño [%]
    T_C  : temperatura mínima esperada en el recinto [°C]
    """
    if C_pct >= 100:
        raise ValueError("Concentración debe ser < 100%.")
    s = agente.s_m3_kg(T_C)
    return (V_m3 / s) * (C_pct / (100.0 - C_pct))


def verifica_ocupacion_normal(agente: AgenteLimpio, C_pct: float) -> dict:
    """NFPA 2001 §1.5.1.2: C_diseño ≤ NOAEL para ocupación normal."""
    return {
        "apto_ocupacion_normal": C_pct <= agente.NOAEL_pct,
        "NOAEL_pct": agente.NOAEL_pct,
        "LOAEL_pct": agente.LOAEL_pct,
        "margen_pct": agente.NOAEL_pct - C_pct,
    }
