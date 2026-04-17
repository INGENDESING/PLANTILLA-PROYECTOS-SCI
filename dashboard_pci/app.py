"""
Dashboard PCI — calculadoras interactivas sobre los módulos de src/pci/.

Endpoints:
    GET  /                       Página principal con las tres calculadoras.
    POST /api/hidraulica/hw      Hazen-Williams (NFPA 13).
    POST /api/agentes/masa       Masa de agente limpio (NFPA 2001).
    POST /api/fuego/pluma        Temperatura centerline pluma Heskestad (SFPE).
"""

from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request

# Permite importar src/pci sin instalar el paquete
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.pci import agentes_limpios, fuego, hidraulica  # noqa: E402

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/hidraulica/hw")
def api_hw():
    d = request.get_json(force=True)
    p_loss = hidraulica.perdida_hazen_williams_psi(
        Q_gpm=float(d["Q_gpm"]),
        C=float(d["C"]),
        d_in=float(d["d_in"]),
        L_ft=float(d["L_ft"]),
    )
    return jsonify({"perdida_psi": round(p_loss, 3), "norma": "NFPA 13 Ec. 23.4.4.7"})


@app.post("/api/agentes/masa")
def api_agente():
    d = request.get_json(force=True)
    agentes = {
        "FM200": agentes_limpios.FM200,
        "Novec1230": agentes_limpios.NOVEC1230,
        "IG541": agentes_limpios.IG541,
    }
    ag = agentes[d["agente"]]
    C_pct = float(d["C_pct"])
    m = agentes_limpios.masa_agente_kg(ag, V_m3=float(d["V_m3"]), C_pct=C_pct, T_C=float(d["T_C"]))
    chk = agentes_limpios.verifica_ocupacion_normal(ag, C_pct)
    return jsonify({"masa_kg": round(m, 2), "norma": "NFPA 2001 Ec. 5.5.1.1", **chk})


@app.post("/api/fuego/pluma")
def api_pluma():
    d = request.get_json(force=True)
    T = fuego.heskestad_temperatura_centerline_K(
        Q_kw=float(d["Q_kw"]),
        D_m=float(d["D_m"]),
        z_m=float(d["z_m"]),
    )
    return jsonify({"T_K": round(T, 2), "T_C": round(T - 273.15, 2), "norma": "SFPE Handbook — Heskestad"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
