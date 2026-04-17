async function post(url, body) {
  const r = await fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body),
  });
  return r.json();
}

async function calcHW() {
  const out = await post("/api/hidraulica/hw", {
    Q_gpm: +hw_Q.value, C: +hw_C.value, d_in: +hw_d.value, L_ft: +hw_L.value,
  });
  hw_out.textContent = JSON.stringify(out, null, 2);
}

async function calcAgente() {
  const out = await post("/api/agentes/masa", {
    agente: ag_tipo.value, V_m3: +ag_V.value, C_pct: +ag_C.value, T_C: +ag_T.value,
  });
  ag_out.textContent = JSON.stringify(out, null, 2);
}

async function calcPluma() {
  const out = await post("/api/fuego/pluma", {
    Q_kw: +pl_Q.value, D_m: +pl_D.value, z_m: +pl_z.value,
  });
  pl_out.textContent = JSON.stringify(out, null, 2);
}
