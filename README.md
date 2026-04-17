# Plantilla Proyectos IA — Detección y Extinción de Incendios (NFPA / NEC)

Plantilla maestra reutilizable para proyectos de **ingeniería de protección contra incendios (PCI)** a nivel maestría: análisis de riesgos, detección, alarma, extinción (agua, espumas, agentes limpios), hidráulica, termodinámica del fuego y clasificación de áreas.

Diseñada para ingenieros químicos computacionales senior que asisten su trabajo con IA (Claude Code), con foco inicial en **plantas de cogeneración de energía a partir de bagazo** pero aplicable a cualquier planta industrial bajo **NFPA** y **NEC (NFPA 70)**.

## Características

- 📐 **Plantilla LaTeX** (`elsarticle`) con membrete corporativo, hoja de firmas y control de revisiones.
- 🐍 **Librería Python** `src/pci/` con módulos para los cálculos principales (hidráulica, agentes, fuego, riesgos).
- 🔁 **Unidades duales** SI + US customary (NFPA trabaja nativamente en US).
- 🧪 **Validación contra SFPE Handbook / NFPA Annex** en `tests/`.
- 📊 **Dashboard PCI** (Flask) con calculadoras interactivas.
- 🤖 **Instrucciones IA** (`CLAUDE.md`) optimizadas para Claude Code.
- 💾 **Contexto persistente** (`status.md`) entre sesiones de IA.
- ⚙️ **CI GitHub Actions** que compila el PDF en cada push.

## Normas cubiertas

NFPA 13, 14, 15, 17/17A, 20, 22, 24, 25, 70 (NEC), 70E, 72, 11, 16, 12, 12A, 2001, 101, 170, 291, 499, 550, 654, 664, 850, 921 · NEC Art. 500–505 · API RP 500/505/752 · ISA 5.1 · SFPE Handbook of Fire Protection Engineering.

## Uso rápido

1. Clonar el repositorio.
2. Leer [`CLAUDE.md`](CLAUDE.md) — define rol, stack, guías y política de unidades.
3. Solicitar al usuario el **código del documento** (formato `P{YYMM}-{AREA}-{TIPO}-{NNN} REV{N}`) y renombrar el `.tex` maestro.
4. Editar `plantillalatex/config/datos_proyecto.tex` (ocupación, clase de riesgo, normas, AHJ, firmas).
5. Reemplazar `plantillalatex/logos/logo1.png` y `logo2.png`.
6. Llenar `plantillalatex/sections/` y compilar con `pdflatex` (dos pasadas).
7. Actualizar `status.md` al cerrar cada sesión.

## Estructura

Ver `CLAUDE.md` sección *Estructura de Proyecto Recomendada*.

## Requisitos

- **Python ≥ 3.11** con `numpy scipy sympy pandas matplotlib plotly pint CoolProp thermo chemicals flask`.
- **MiKTeX** (Windows) o **TeX Live** con `pdflatex`, paquetes `elsarticle`, `siunitx`, `mhchem`, `fancyhdr`, `circuitikz`.
- **VS Code** con extensiones *Python*, *Jupyter*, *LaTeX Workshop*.

## Licencia

[MIT](LICENSE).

## Aviso

Esta plantilla facilita el trabajo de diseño PCI, pero no sustituye el juicio profesional. Todo cálculo debe ser validado por un ingeniero colegiado y aprobado por la Autoridad Competente (AHJ).
