# status.md — Contexto del Proyecto

> Archivo mantenido por la IA entre sesiones para preservar contexto y ahorrar tokens.
> Leer como primera acción al iniciar una sesión; actualizar al cerrar.

**Última actualización:** 2026-04-17
**Fase:** plantilla base publicable (sin proyecto específico cargado)
**Avance estimado:** —

---

## 1. Identificación del proyecto

- Código del documento: *(pendiente: solicitar al usuario formato `P{YYMM}-{AREA}-{TIPO}-{NNN} REV{N}`)*
- Ocupación: *(ej. Planta de cogeneración de energía a partir de bagazo)*
- Clase de riesgo NFPA 13: *(LH / OH1 / OH2 / EH1 / EH2)*
- Normas aplicables (código + edición + año): *(llenar según alcance)*
- AHJ (Authority Having Jurisdiction): *(pendiente)*
- Áreas clasificadas NEC: *(resumen; detalle en `data/clasificacion_areas.csv`)*

---

## 2. Archivos tocados en esta sesión

| Ruta | Propósito |
|---|---|
| `CLAUDE.md` | Reescritura completa hacia rol PCI senior, NFPA/NEC, guías técnicas |
| `status.md` | Creación de plantilla de contexto persistente |
| `README.md`, `LICENSE`, `.gitignore` | Preparación para publicación GitHub |
| `.github/workflows/latex.yml` | CI de compilación de PDF |
| `src/pci/` | Stubs de librería PCI (hidráulica, fuego, agentes, riesgos, etc.) |
| `dashboard_pci/` | Reemplazo de `ejemplo_web/` |
| `plantillalatex/config/datos_proyecto.tex` | Variables PCI (ocupación, riesgo, AHJ, normas) |
| `plantillalatex/references/bibliografia.bib` | Entradas NFPA / SFPE / NEC |
| `plantillalatex/sections/07–09, 13` | Adaptación a contenido PCI |

---

## 3. Cálculos completados

*(vacío — plantilla sin proyecto cargado)*

| Módulo | Norma + edición | Entrada clave | Resultado | Archivo |
|---|---|---|---|---|

---

## 4. Cálculos pendientes

*(a poblar con el alcance del proyecto)*

- [ ] Análisis de riesgos HAZOP + What-If
- [ ] Selección de sistemas por escenario
- [ ] Diseño hidráulico NFPA 13 (densidad/área, nodal)
- [ ] Bomba NFPA 20 (curva y suministro)
- [ ] Detección NFPA 72 (espaciamiento, batería, NAC)
- [ ] Agentes limpios NFPA 2001 (si aplica)
- [ ] Clasificación áreas NEC Art. 500–505

---

## 5. Decisiones de diseño

*(vacío — registrar a medida que se avanza)*

- Sistemas seleccionados: …
- Agente(s): …
- Densidad de diseño: …
- Tiempo de operación: …
- Bomba: capacidad y CDT …

---

## 6. Supuestos abiertos

- Edición exacta de cada NFPA y NEC vigente al inicio del proyecto debe confirmarse con el AHJ.
- Unidades en memoria: **SI + US customary** (política dual definida en `CLAUDE.md`).

---

## 7. Próximos pasos

1. Cargar proyecto específico: actualizar `config/datos_proyecto.tex`.
2. Ejecutar HAZOP + What-If sobre P&ID.
3. Dimensionar sistemas seleccionados en `src/pci/`.
4. Compilar PDF y verificar con `pdflatex` (dos pasadas).
5. Actualizar este `status.md` antes de cerrar la sesión.
