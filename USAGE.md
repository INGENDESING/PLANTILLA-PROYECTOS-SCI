# USAGE.md — Guía de Uso de la Plantilla PCI

> Cómo usar esta plantilla para iniciar un **proyecto específico** de Protección Contra Incendios (PCI).

---

## Paso 0: Clonar la plantilla (no trabajar sobre el repo original)

```bash
# 1. Clonar
gh repo clone INGENDESING/PLANTILLA-PROYECTOS-SCI nuevo-proyecto-pci

# 2. Entrar al directorio
cd nuevo-proyecto-pci

# 3. Eliminar el remote original (para no sobreescribir la plantilla)
git remote remove origin

# 4. Crear tu propio repo en GitHub y vincularlo
git remote add origin https://github.com/TU_USUARIO/nuevo-proyecto-pci.git
git branch -M main
git push -u origin main
```

> **Regla de oro:** nunca hagas `git push` directo sobre `PLANTILLA-PROYECTOS-SCI`. Siempre clona en una carpeta nueva con el nombre del proyecto real.

---

## Paso 1: Solicitar al usuario los datos del proyecto

Antes de tocar código, recopilar del usuario (o del alcance contractual):

| Dato | Formato esperado | Ejemplo |
|---|---|---|
| **Código del documento** | `P{YYMM}-{AREA}-{TIPO}-{NNN} REV{N}` | `P2604-PR-INF-001 REV0` |
| **Ocupación / proceso** | Texto descriptivo | "Planta de cogeneración a partir de bagazo, 35 MW" |
| **Clase de riesgo NFPA 13** | `LH` / `OH1` / `OH2` / `EH1` / `EH2` | `OH2` |
| **Normas aplicables (con edición y año)** | Lista separada por comas | "NFPA 13 (2025), NFPA 20 (2025), NFPA 72 (2023), NEC (2023)" |
| **AHJ** | Nombre de la autoridad | "Cuerpo de Bomberos de Palmira / DAGRD" |
| **Áreas clasificadas NEC** | Resumen por área | "Clase II Div 2 Grupo G (silos y patio bagazo)" |
| **Combustibles presentes** | Lista con estado físico | "Bagazo (sólido), diesel (líquido), H₂ (gas)" |
| **Altitud del sitio** | msnm | 960 |
| **Temperatura ambiente min/max** | °C | 15 / 38 |

---

## Paso 2: Configurar el documento LaTeX

### 2.1 Renombrar el archivo maestro

```bash
cd plantillalatex
mv "P25XX-PR-INF-00X REVX.tex" "P2604-PR-INF-001 REV0.tex"
```

> Actualiza la referencia en `.github/workflows/latex.yml` si el CI sigue buscando `P*.tex` (ya lo hace automáticamente con `ls`).

### 2.2 Editar `config/datos_proyecto.tex`

Rellenar **todas** las variables, especialmente las de la sección PCI:

```latex
\newcommand{\projecttitle}{DISEÑO DEL SISTEMA DE PROTECCIÓN CONTRA INCENDIOS}
\newcommand{\documentcode}{P2604-PR-INF-001 REV0}
\newcommand{\documenttype}{MEMORIA DE CÁLCULO PCI}
\newcommand{\targetcompany}{Ingeniería del Cliente S.A.S.}

\newcommand{\occupancy}{Planta de cogeneración de energía a partir de bagazo, 35 MW}
\newcommand{\hazardclass}{OH2}
\newcommand{\ahj}{Cuerpo de Bomberos de Palmira}
\newcommand{\nfpacodes}{NFPA 13 (2025), NFPA 20 (2025), NFPA 72 (2023), NEC (2023), NFPA 850 (2021)}
\newcommand{\classifiedareas}{Clase II Div.\,2 Grupo G (patio bagazo, silos); Clase I Div.\,2 Grupo D (tanque diesel)}
```

### 2.3 Reemplazar logos

Sustituir `plantillalatex/logos/logo1.png` y `logo2.png` por los logos reales del cliente y de tu firma.

---

## Paso 3: Cargar datos del proyecto en los CSV

Editar los archivos en `data/` con la información específica (no los dejes con datos de ejemplo):

| Archivo | Qué llenar |
|---|---|
| `data/matriz_riesgo.csv` | Nodos HAZOP, escenarios, severidad, probabilidad, recomendaciones |
| `data/inventario_combustibles.csv` | Todos los combustibles del sitio con PCI, ΔHc, Kst, MIE, grupo NEC |
| `data/clasificacion_areas.csv` | Cada área clasificada con clase, división, zona, grupo, código temperatura |

---

## Paso 4: Ejecutar análisis de riesgos

1. **HAZOP + What-If:**
   - Dividir el P&ID en nodos (máx. 5–8 nodos para empezar).
   - Aplicar palabras guía: `NO`, `MAS`, `MENOS`, `TAMBIEN`, `INVERSO`, `OTRO`.
   - Registrar en `data/matriz_riesgo.csv` y en notebook Jupyter.

2. **Seleccionar sistemas** por escenario dominante usando `src/pci/riesgos.py` y `src/pci/bagazo.py`.

3. **Matriz de riesgo:** confirmar umbrales de aceptación con el cliente/AHJ.

---

## Paso 5: Dimensionar sistemas en `src/pci/`

Trabajar en Jupyter notebooks dentro de `notebooks/` importando los módulos:

```python
from src.pci import hidraulica, fuego, agentes_limpios, deteccion, alarma_nac
```

### Secuencia recomendada:

| Orden | Módulo | Norma | Entregable |
|---|---|---|---|
| 1 | `fuego.py` | SFPE / NFPA 921 | HRR, radiación térmica, flashover |
| 2 | `hidraulica.py` | NFPA 13/20 | Caudal, pérdidas, curva bomba |
| 3 | `deteccion.py` + `alarma_nac.py` | NFPA 72 | Cantidad detectores, batería, caída tensión |
| 4 | `agentes_limpios.py` | NFPA 2001 | Masa agente, concentración, venteo |
| 5 | `clasificacion_areas.py` | NEC Art. 500–505 | Tabla resumen áreas clasificadas |

> **Validación obligatoria:** cada resultado debe contrastarse contra un caso resuelto del SFPE Handbook o NFPA Annex. Agregar el test a `tests/` si es un caso nuevo.

---

## Paso 6: Documentar en LaTeX

Llenar las secciones de `plantillalatex/sections/`:

| Sección | Contenido |
|---|---|
| `07_bases_disenio.tex` | Ocupación, clase riesgo, normas, densidades, tiempos |
| `08_metodologia.tex` | Ecuaciones usadas, criterios de aceptación, software |
| `09_resultados.tex` | Tablas y figuras de cálculos (importar desde notebooks) |
| `13_anexos.tex` | Hoja HAZOP, planos, isométricos, memoria de cálculo |

### Compilar:

```bash
cd plantillalatex
pdflatex "P2604-PR-INF-001 REV0.tex"
pdflatex "P2604-PR-INF-001 REV0.tex"   # segunda pasada para refs
```

---

## Paso 7: Cerrar sesión (actualizar `status.md`)

Antes de terminar cualquier sesión de trabajo, actualizar `status.md` con:

- **Fecha de última actualización**
- **Fase actual** (análisis de riesgos | diseño | cálculo | documentación | cierre)
- **Avance estimado** (%)
- **Archivos tocados** en la sesión
- **Cálculos completados** (módulo, norma, resultado clave)
- **Cálculos pendientes**
- **Decisiones de diseño** tomadas
- **Supuestos abiertos**
- **Próximos pasos**

---

## Checklist de inicio de proyecto

- [ ] Clonado en carpeta nueva (no se tocó el repo plantilla)
- [ ] `git remote` apunta al repo del proyecto, no a la plantilla
- [ ] Código del documento definido y renombrado `.tex`
- [ ] `config/datos_proyecto.tex` completado
- [ ] Logos reales colocados
- [ ] `data/*.csv` poblados con datos reales
- [ ] `status.md` inicializado con datos del proyecto
- [ ] `tests/` corren: `pytest tests/ -v`
- [ ] CI de LaTeX compila sin errores

---

## Notas de mantenimiento

- **No subas datos confidenciales** del cliente a repos públicos. Usa repos privados o `.gitignore` para `data/*.csv` reales.
- **Mantén `CLAUDE.md` intacto** en cada proyecto clonado; la IA lo lee para saber su rol.
- **Versiona los PDFs finales** (`git tag v1.0.0` cuando el informe esté aprobado).
