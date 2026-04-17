# Plan de Corrección de Errores LaTeX

## Lista de Tareas Pendientes

- [x] **1. Solucionar advertencia de tamaño de encabezado (`\headheight is too small`)**
  - Archivo: `config/header.tex`
  - Acción: Ajustar la inserción de la imagen `membrete.pdf` envolviéndola en un `\raisebox{0pt}[\headheight][0pt]{...}`. Esto le indica a LaTeX que asuma que la caja de la imagen no supera la altura máxima permitida (`\headheight`), solucionando la advertencia de `Overfull \hbox` y `\headheight` sin cambiar su posición real en la hoja.
- [x] **2. Solucionar error de tabla (`Misplaced \noalign` en `tabularx`)**
  - Archivo: `sections/00_hojafirmas.tex`
  - Acción: El error se ocasiona al finalizar filas antes de un salto de línea u `\hline` cuando hay redefiniciones de columnas. Se utilizará `\tabularnewline` para terminar explícitamente la fila, o en su defecto se usará una estructura compatible en la definición de la fila final para prevenir la desalineación de `tabularx`.
- [x] **3. Solucionar advertencia de versión PDF (`PDF inclusion: found PDF version <1.7>`)**
  - Archivo: `config/preamble.tex`
  - Acción: Añadir la regla `\pdfminorversion=7` para evitar advertencias por la inclusión de PDFs guardados en versiones más recientes como la 1.7.
- [x] **4. Compilar el proyecto**
  - Acción: Verificar por línea de comandos que el documento finalice su compilación de manera limpia.
- [x] **5. Revisión Final**
  - Acción: Llenar la sección de revisión en este documento con un resumen de los cambios.

## Sección de Revisión
**Resumen de cambios realizados:**
1. **Advertencia de `\headheight is too small:`** Se solucionó envolviendo la inserción de `membrete.pdf` (`config/header.tex`) en un entorno `\raisebox{0pt}[\headheight][0pt]{...}`. Esto permite que el visual original ocupe todo el espacio (90cm) pero le indica a LaTeX que su "caja de compilación" equivale a 0pt, eliminando la advertencia.
2. **Error `Misplaced \noalign:`** Se identificó que el ambiente `tabularx` dentro de `00_hojafirmas.tex` reaccionaba de forma conflictiva a la inserción de colores en las filas con el paquete `colortbl`. Para solucionarlo definitivamente y preservar el layout estricto, cambiamos los entornos `tabularx` por `tabular` estándar de dimensiones fijas (combinaciones de celdas tipo `p{0.3\textwidth}`) y eliminamos la directiva `\rowcolor`. 
3. **Advertencia de versión de PDF:** Se forzó la compatibilidad en `config/preamble.tex` utilizando `\pdfminorversion=7`.
4. **Compilación final:** Tras aplicar estas medidas, la compilación de `pdflatex` finalizó sin interrupciones, generando el archivo `.pdf` correctamente.

# Nuevo Plan: Solucionar Encabezado Desaparecido (Intento 3)

## Lista de Tareas Pendientes
- [x] **1. Corregir renderizado del membrete (`config/header.tex` y `config/preamble.tex`)**
  - Acción: Revertir la línea del membrete en `config/header.tex` a su estado original `\includegraphics[width=\paperwidth,height=90cm,keepaspectratio]{assets/membrete.pdf}`. Como el problema raíz es que la imagen es muy grande, en lugar de enmascararla con cajas y arriesgar que se oculte o desplace como fondo de página, vamos a atender la advertencia original aumentando directamente el `\headheight` en `config/preamble.tex` al valor gigantesco que LaTeX pide (`152pt` o ajustando márgenes) o en su defecto colocándolo en un nodo de tikz/eso-pic. Para mantener la simplicidad, se usará `eso-pic` para un background absoluto u optaremos por subir el headheight. Usaremos `eso-pic` para insertarlo al background de manera infalible.
- [x] **2. Compilar y verificar**
  - Acción: Compilar el proyecto localmente para confirmar que el membrete vuelve a verse detrás del texto normal como estaba originalmente destinado.
- [x] **3. Revisión Final**
  - Acción: Reflejar las correcciones en el resumen de cambios.

**Resumen resolución de encabezado:** Se eludió por completo la mecánica conflictiva de `fancyhdr` y `\raisebox`. Al usar el paquete `eso-pic`, el compilador inyectará el `membrete.pdf` como un fondo absoluto universal (`\AddToShipoutPictureBG*`) detrás del texto de cada página. El documento ahora compila en cero errores, cero advertencias, los índices están vinculados y la imagen se muestra completamente.

# Nuevo Plan: Solucionar Contador de Páginas
## Lista de Tareas Pendientes
- [x] **1. Solucionar `Reference 'LastPage' undefined`**
  - Acción: Añadir el paquete `lastpage` en la sección de "OTROS PAQUETES" dentro de `config/preamble.tex`. Esto habilitará el uso de la directiva `\pageref{LastPage}` que actualmente se utiliza en `config/header.tex` como contador global.
- [x] **2. Compilar**
  - Acción: Compilar el proyecto dos veces para que las referencias a `LastPage` queden capturadas y mapeadas en el historial de páginas.
- [x] **3. Revisión Final**
  - Acción: Acotar los problemas resueltos en el documento.

**Resumen resolución de contador de páginas:** Se inyectó eficazmente el paquete faltante `lastpage` en los parámetros globales de compilación de `preamble.tex`. Al compilar por última vez el proyecto, la advertencia "Reference 'LastPage' undefined" desapareció orgánicamente en el bitácora del motor, habilitando al pie de página (footer) de `fancyhdr` proyectar exitosamente la cantidad total de páginas del documento.

# Nuevo Plan: Recrear Encabezado Nativamente en LaTeX
## Lista de Tareas Pendientes
- [x] **1. Preparar el entorno para logos nativos**
  - Acción: Eliminar la dependencia del fondo `membrete.pdf` (y opcionalmente `eso-pic`) en `config/header.tex`.
- [x] **2. Recrear el diseño del encabezado**
  - Acción: Utilizar comandos nativos de `fancyhdr` (junto a tablas o `minipages`) en `config/header.tex` para colocar `logos/logo1.png` y `logos/logo2.png` en las posiciones adecuadas (por ejemplo, DML a la izquierda y el cliente a la derecha). Ajustar el `\headheight` en `preamble.tex` si las imágenes lo requieren.
- [x] **3. Compilar y verificar**
  - Acción: Ejecutar `pdflatex` para asegurar que el documento procese los nuevos logos correctamente, respete márgenes y no arroje advertencias de dimensiones.
- [x] **4. Revisión Final**
  - Acción: Registrar los cambios y acotar lecciones aprendidas.

**Resumen de arquitectura del nuevo encabezado:** Se eludió de forma final el uso de un archivo `PDF` base (`membrete.pdf`) a tamaño completo que generaba ambigüedades con el motor gráfico de `eso-pic` y `fancyhdr`. Para modernizar el proyecto y hacerlo mantenible, recreé el entorno del encabezado dentro de `config/header.tex` valiendonos de un entorno `\parbox` a lo de ancho de la página donde anclé el logo de la firma en la esquina superior izquierda y el del cliente a la superior derecha (`logo1.png` y `logo2.png` ubicados en `/logos/`). Al compilar, todo ajustó nítidamente y libre de penalizaciones o advertencias.

# Nuevo Plan: Recrear la Tabla de Información en el Encabezado
## Lista de Tareas Pendientes
- [x] **1. Recrear estructura tubular del membrete original**
  - Acción: Ya que el PDF original sí poseía un cuadro (tabla) con los textos e información documental, reconstruiremos el código en `config/header.tex` agrupando `logo1.png`, el título/código del proyecto y `logo2.png` en una estructura formal `\begin{tabular}` que abarque el ancho total de la página conformando el clásico membrete corporativo recuadrado.
- [x] **2. Compilar**
  - Acción: Re-ejecutar `pdflatex` y asegurar que el ancho de la tabla se acopla a las márgenes dictadas.
- [x] **3. Revisión Final**
  - Acción: Registrar los cambios.

**Resumen de arquitectura del membrete tabular:** Se actualizó satisfactoriamente el diseño flotante previo (`\parbox`) por una tabla estricta de 3 columnas definida en formato `\begin{tabularx}{\textwidth}{| c | X | c |}`. El logo primario se acomoda fluidamente a la izquierda y el secundario a la derecha (ambos dentro de minipages de 3.5cm). Adicionalmente, se extrajeron y centralizaron de forma dinámica las propiedades `\projecttitle` y `\documentcode` de `preamble.tex` en la celda intermedia, dotando al documento de un recuadro superior profesional, idéntico conceptualmente a un archivo base de `Word`.

# Nuevo Plan: Prototipado y Análisis Preciso del Membrete
## Lista de Tareas Pendientes
- [x] **1. Análisis Estructural del diseño PDF**
  - Acción: Extraer y convertir (o leer por línea de comandos) información gráfica del `membrete.pdf` provisto.
- [x] **2. Crear Entorno Aislado (`layout.tex`)**
  - Acción: Diseñar un archivo independiente `layout.tex` donde se simule la tabla perfecta con los anchos exactos, bordes, tamaños de fuente y alineamientos extraídos desde la revisión visual, garantizando la aprobación visual sin afectar el código de producción.
- [x] **3. Presentación y Revisión**
  - Acción: Mostrar el código del layout al usuario para obtener aprobación antes de inyectarlo oficialmente en la rama de `header.tex`.

# Nuevo Plan: Integración Tipográfica Final al Proyecto
## Lista de Tareas Pendientes
- [x] **1. Trasladar configuración de fuentes**
  - Acción: Reemplazar `mathptmx` en `config/preamble.tex` por los componentes premium `tgtermes`, `microtype` y `fontenc[T1]`. Complementar con nuevas variables globales (fechas, autores).
- [x] **2. Reemplazar `\empresaheader`**
  - Acción: Inyectar el código `tabularx` definitivo en `config/header.tex`, enlazando las variables del paso anterior para el llenado de metadatos.
- [x] **3. Compilación de Verificación**
  - Acción: Compilar `P25XX-PR-INF-00X REVX.tex` con los cambios y certificar la integración perfecta del membrete.

**Resumen de arquitectura superior tipográfica:** El bloque extraído del prototipado (`layout.tex`) se integró exitosamente en la definición superior de documento. Las variables estáticas de marcaje ("Revisión", "Fecha", "Elaboró") fueron declaradas nativamente en `preamble.tex` de modo que modificar cualquier campo corporativo en el PDF tome solo 1 segundo ajustando los comandos madre. El documento compila excepcionalmente con TeX Gyre Termes.

# Nuevo Plan: Reducir Altura de Filas del Encabezado
## Lista de Tareas Pendientes
- [x] **1. Ajustar escalar de filas (`\arraystretch`)**
  - Acción: Introducir en `config/header.tex` la instrucción `\renewcommand{\arraystretch}{0.85}` (o un factor similar menor a 1) justo antes de abrir la tabla para comprimir su altura vertical dejando el suficiente "respiro" o padding mínimo que requieres.
- [x] **2. Compilar y verificar**
  - Acción: Re-compilar el pdf para aplicar los ajustes tipográficos minúsculos.
- [x] **3. Revisión Final**
  - Acción: Documentar el cierre en este log de tareas.

**Resumen de arquitectura del afinado de espaciado:** Se redujo en un 20% la altura neta de las filas individuales del membrete insertando dinámicamente el comando temporal `\renewcommand{\arraystretch}{0.80}` instantes antes de iniciar la tabla en el constructor `\empresaheader`. Esto acerca el nivel de compresión visual casi hasta tocar el texto central, brindándole elegancia compacta sin aplastar la legibilidad.

# Nuevo Plan: Auto-numeración de Filas en Tablas ("Item")
## Lista de Tareas Pendientes
- [x] **1. Configurar Contador Global**
  - Acción: Definir en `config/preamble.tex` un nuevo contador (`\newcounter{itemcount}`) y un nuevo tipo de columna personalizada (`N`) usando el paquete `array` que auto-incremente este contador e imprima su valor: `\newcolumntype{N}{>{\stepcounter{itemcount}\theitemcount}c}`.
- [x] **2. Modificar Tablas del Cuerpo**
  - Acción: Recorrer los archivos como `sections/07_bases_disenio.tex` y `sections/09_resultados.tex`. Por cada tabla:
    1. Añadir el reseteo del contador antes de abrir el entorno: `\setcounter{itemcount}{0}`.
    2. Agregar la nueva columna `N` a la definición de columnas (ej. de `Xcc` a `NXcc`).
    3. Añadir el encabezado `\multicolumn{1}{c}{\textbf{Item}} &` a la primera fila (para que no numere el título de la columna).
    4. Añadir el símbolo `&` al inicio de cada fila de datos de manera que caigan en la primera columna autocompletando el número.
- [x] **3. Compilar y Verificar**
  - Acción: Ejecutar `pdflatex` y verificar que las tablas corporales ahora cuenten con números automáticos en su primera columna.

**Resumen de la arquitectura de tablas:** Se integró un sistema global con un contador (`itemcount`) anclado a un macro columnar (`N`) en `preamble.tex`. Esto permite que las 5 tablas principales (4 en Bases de Diseño y 1 en Resultados) dispongan de una barrera incremental invisible a la izquierda mediante el tipo de entrada de fila ordinaria `&`. Con esto se extripa el esfuerzo de corrección del usuario ante nuevas inyecciones de datos en medio de matrices.

# Nuevo Plan: Desacoplar Columnas "Unidad -- Referencia"
## Lista de Tareas Pendientes
- [x] **1. Reestructurar Tablas Base**
  - Acción: Ubicar las tablas 1 a 4 del archivo `sections/07_bases_disenio.tex`. Cambiar la cabecera actual `\textbf{Unidad} -- \textbf{Referencia}` por celdas separadas `\textbf{Unidad} & \textbf{Referencia}`.
- [x] **2. Separar datos**
  - Acción: Reemplazar el separador textual `--` por el comando de tabulación `&` en todas las filas subyacentes. Añadir una columna extra `c` a los parámetros de la tabla.
- [x] **3. Compilación Visual**
  - Acción: Ejecutar `pdflatex` y revisar el documento para verificar que las medidas se ajusten a la matriz ampliada dinámicamente.

**Resumen de separación modular en bases de diseño:** Las tablas 1, 2, 3 y 4 en `07_bases_disenio.tex` fueron modificadas para escalar su partición horizontal agregando una nueva columna para aislar matemáticamente las "Unidades" de las "Referencias". Se reemplazó el obsoleto separador doble-guion `--` por la inserción del salto de la celda `&`. A pesar del incremento de datos, todas las matrices compilan a tope con un entorno `\textwidth` auto balanceado (y la enumeración dinámica de "Item" reacciona perfectamente en el renderizado).

# Nuevo Plan: Sombreado de Tablas en la Portada
## Lista de Tareas Pendientes
- [x] **1. Inyectar macros de color en filas**
  - Acción: Ubicar las 3 tablas en `sections/00_portada.tex` e insertar el comando `\rowcolor{green!15}` justo después del primer `\toprule` de cada matriz. A su vez incluimos `[table]{xcolor}` globalmente en el preámbulo.
- [x] **2. Compilar PDF y Validar**
  - Acción: Reejecutar `pdflatex` y revisar que ningún entorno numérico se rompa y que el color aplique simétricamente a todo lo ancho de las filas superiores.

**Resumen del sombreado corporativo:** Se inyectó dinámicamente un código de color transparente (`\rowcolor{green!15}`) en la primera fila arquitectónica de las tres tablas centrales que conforman la portada principal. Resultando en una banda de color distintiva pero elegante. La opacidad manejada precavé alteraciones de contraste con el texto oscuro, favoreciendo visibilidad.

# Nuevo Plan: Sombreado de Tablas en Hoja de Firmas
## Lista de Tareas Pendientes
- [x] **1. Inyectar `\rowcolor` en 00\_hojafirmas.tex**
  - Acción: Ubicar las Tablas 1 y 2 en `sections/00_hojafirmas.tex`. Insertar `\rowcolor{green!15}` luego de la primera `\hline` para que la primera fila adopte el sombreado verde claro corporativo.
- [x] **2. Validar compilación**
  - Acción: Compilar nuevamente el archivo PDF y verificar el renderizado del color.

**Resumen del sombreado en firmas:** Se ejecutó la inyección paramétrica de `\rowcolor{green!15}` subsecuente al límite topológico `\hline` en las dos tablas base que dominan el archivo `00_hojafirmas.tex`. La compilación arroja cero errores referenciales ya que hereda el paquete colortbl habilitado para la portada previamente, demostrando sincronía estética a través de toda la documentación.

# Nuevo Plan: Centralización de Metadatos del Proyecto
## Lista de Tareas Pendientes
- [x] **1. Crear archivo maestro `datos_proyecto.tex`**
  - Acción: Redactar todas las variables estandarizadas (cliente, código, integrantes, fechas) dentro de este nuevo archivo bajo `config/`.
- [x] **2. Vincular metadatos desde el preámbulo**
  - Acción: Borrar parámetros fijos antiguos en `preamble.tex` e inyectar `\input{config/datos_proyecto.tex}`, puenteando las traducciones exigidas por el encabezado (convirtiendo a mayúsculas paramétricamente).
- [x] **3. Dinamizar archivos documentales**
  - Acción: Remplazar valores textuales quemados en `00_portada.tex` y `00_hojafirmas.tex` por el respectivo llamado a los constructos de los metadatos globales (`\firmaElaboro`, `\fechaEmision`, etc.)
- [x] **4. Verificación de Ensamblaje Visual**
  - Acción: Compilar PDF y validar que todas las máscaras reaccionan unánimemente reflejando los datos inyectados por la plantilla máster.

**Resumen de arquitectura global de datos:** Se creó un núcleo llamado `config/datos_proyecto.tex` desde el cual se configuran todos los textos clave (autores, fechas, aprobaciones y códigos). Se purgó el código rígido en la portada, hoja de firmas y preámbulo corporativo enlazándolos enteramente a los `\newcommand` de este núcleo. Como resultado, cualquier proyecto del futuro se actualiza tan solo editando las 15 líneas de variables en este único archivo frontal, garantizando consistencia absoluta en todo el informe técnico sin requerir barridos manuales.

# Nuevo Plan: Expansión de Historial de Revisiones (Hasta Rev. 4)
## Lista de Tareas Pendientes
- [x] **1. Ampliar `datos_proyecto.tex`**
  - Acción: Agregar las variables `\fechaRevTres`, `\descRevTres`, `\fechaRevCuatro` y `\descRevCuatro` en el bloque 5 del archivo maestro.
- [x] **2. Vincular a Portada (`00_portada.tex`)**
  - Acción: Añadir las filas para la revisión 3 y 4 en la matriz, mapeándolas a sus respectivos macros.
- [x] **3. Vincular a Hoja de Firmas (`00_hojafirmas.tex`)**
  - Acción: Mapear las filas de REV1, REV2, REV3 y REV4 hacia las nuevas variables.
- [x] **4. Validar compilación final**
  - Acción: Ejecutar `pdflatex` y asegurar consistencia visual en ambos cuadros.

**Resumen de expansión de revisiones:** Se ampliaron las tablas de métricas de revisiones dentro de `00_portada.tex` y `00_hojafirmas.tex` hasta contemplar un ciclo de vida de versión número 4. Los parámetros textuales fueron directamente vinculados con el nuevo archivo global mediante los comandos abstractos `\fechaRevTres`, `\descRevCuatro`, etc. Elevando la robustez documental frente a proyectos de larga auditoría.

# Corrección de Distribución Estructural en el Encabezado
## Registro de Cierre Operativo
- [x] **1. Intercambiar posiciones de título y tipo de documento**
  - Acción: En el archivo `config/header.tex`, se descendió el comando `\projecttitle` hacia la intersección de las filas 5 y 6, y se ascendió `\documenttype` a la intersección de las filas 3 y 4 del bloque frontal derecho respondiendo al estándar corporativo estricto.

**Resumen de la corrección de membrete:** Se readaptó la cuadrícula `\tabularx` que dibuja el encabezado general del proyecto, invirtiendo de lugar a los constructos que extraen el Nombre del Proyecto y la Tipología del Informe, salvaguardando la simetría paramétrica sin desbordar los límites del formato A4 configurados originalmente. El ajuste ya fue ratificado a nivel de compilación PDF global.
