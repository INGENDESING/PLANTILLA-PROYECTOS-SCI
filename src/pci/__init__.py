"""
src.pci — Librería de cálculos para Protección Contra Incendios (PCI).

Módulos:
    unidades            Conversión SI <-> US customary (pint).
    hidraulica          NFPA 13/14/20/24 — Hazen-Williams, nodal, bombas.
    espumas             NFPA 11/16 — tasas, proporcionadores, cámaras.
    agentes_limpios     NFPA 2001/12/12A — concentración, masa, descarga.
    deteccion           NFPA 72 — espaciamiento detectores.
    alarma_nac          NFPA 72 — SLC/NAC, batería, audibilidad.
    fuego               SFPE/NFPA 921 — HRR, plumas, radiación, flashover.
    riesgos             HAZOP, What-If, matriz de riesgo.
    clasificacion_areas NEC Art. 500–505 — Clase/División/Zona.
    bagazo              NFPA 850/654/664 — aplicación cogeneración.

Política de unidades: SI + US customary dual. Ver unidades.py.
"""

__version__ = "0.1.0"
