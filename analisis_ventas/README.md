# Análisis de ventas — mini laboratorio de datos

> Donde cada fila del CSV cuenta una historia breve (fecha, producto, cantidad, precio) y el script la convierte en **tendencias**, **rankings** y **gráficas listas para enseñar**.

Este directorio es un taller autocontenido: cargas ventas, miras la salud del dataset en consola, calculas ingresos y sales con dos instantáneas visuales — evolución mensual y quién manda en el top por dinero. Ideal para practicar pandas con un flujo realista sin montar un backend ni una base de datos.

---

## Tabla de contenidos

1. [Qué hace el proyecto](#qué-hace-el-proyecto)
2. [Requisitos](#requisitos)
3. [Instalación rápida](#instalación-rápida)
4. [Cómo ejecutarlo](#cómo-ejecutarlo)
5. [Formato del CSV de entrada](#formato-del-csv-de-entrada)
6. [Qué genera (salidas)](#qué-genera-salidas)
7. [Renovar o crear datos sintéticos](#renovar-o-crear-datos-sintéticos)
8. [Estructura de esta carpeta](#estructura-de-esta-carpeta)
9. [Autor](#autor)

---

## Qué hace el proyecto

El script principal `[analisis_ventas.py](analisis_ventas.py)` ejecuta un pipeline lineal:


| Etapa             | Idea en una frase                                                                     |
| ----------------- | ------------------------------------------------------------------------------------- |
| Carga             | Lee `ventas_sinteticas.csv` y parsea la columna `fecha` como calendario.              |
| Chequeo           | Imprime dimensiones, tipos, nulos y rango temporal — antes de fiarte de los gráficos. |
| Ingeniería mínima | Añade `ingreso = cantidad × precio` y `año_mes` para agrupar por mes.                 |
| Agregaciones      | Suma ingresos por mes; por producto suma unidades e ingresos y saca líderes y top 5.  |
| Visualización     | Guarda dos PNG en alta resolución y muestra ventanas si tu entorno lo permite.        |


No hay menús ni argumentos por línea de comandos: está pensado para abrir el archivo, entender el flujo de arriba abajo y ejecutarlo tal cual.

---

## Requisitos

- **Python** 3.10 o superior recomendado (cualquier 3.x reciente suele valer).
- Librerías:
  - `pandas` — tablas y agrupaciones.
  - `matplotlib` — figuras y exportación PNG.
  - `seaborn` — estilo y paletas (por ejemplo `viridis` en el top 5).

Si algo falla al importar, la solución casi siempre es instalar o actualizar esos tres paquetes en el mismo entorno donde lanzas el script.

---

## Instalación rápida

Desde la raíz del repositorio (o desde esta carpeta), usando un entorno virtual es buena costumbre:

```bash
cd analisis_ventas
python3 -m venv .venv
source .venv/bin/activate   
pip install pandas matplotlib seaborn
```

---

## Cómo ejecutarlo

El script busca `**ventas_sinteticas.csv` en el directorio de trabajo actual**, no junto al archivo `.py` por ruta absoluta. Por tanto:

```bash
cd analisis_ventas
python3 analisis_ventas.py
```

Si ejecutas `python3 analisis_ventas/analisis_ventas.py` desde la carpeta padre sin copiar el CSV, aparecerá un error de archivo no encontrado. La regla práctica: **siempre `cd` a `analisis_ventas` antes de correr**.

---

## Formato del CSV de entrada

Archivo esperado: `**ventas_sinteticas.csv`** (nombre fijo en el código).


| Columna    | Tipo esperado              | Descripción                                                                                      |
| ---------- | -------------------------- | ------------------------------------------------------------------------------------------------ |
| `fecha`    | Fecha parseable por pandas | Día de la operación (por ejemplo `YYYY-MM-DD`).                                                  |
| `producto` | Texto                      | Identificador o nombre del artículo.                                                             |
| `cantidad` | Numérico entero razonable  | Unidades vendidas en esa línea.                                                                  |
| `precio`   | Numérico                   | Precio unitario (la moneda es solo convención en los textos del script; usa € en las etiquetas). |


El código crea automáticamente:

- `ingreso` — producto de `cantidad` y `precio`.
- `año_mes` — periodo mensual derivado de `fecha`.

---

## Qué genera (salidas)

### Consola

- Resumen de filas cargadas, vista previa (`head`), tipos y conteo de nulos.
- Rango mínimo y máximo de fechas.
- Lista de **ventas totales por mes** (suma de `ingreso`).
- Bloque de **análisis por producto**: el más vendido en unidades, el de mayores ingresos y tabla del **top 5 por ingreso**.

### Archivos en disco (misma carpeta de trabajo)


| Archivo                | Contenido                                                            |
| ---------------------- | -------------------------------------------------------------------- |
| `ventas_mensuales.png` | Barras verticales de ingresos por mes; valores encima de cada barra. |
| `top5_productos.png`   | Barras horizontales del top 5 productos por ingreso.                 |


Ambos se guardan con `dpi=300` para que se vean nítidos en documentos o presentaciones.

Además, `plt.show()` intenta abrir ventanas interactivas. En servidores sin display puede dar error: en ese caso puedes comentar las líneas `plt.show()` o definir un backend no interactivo (por ejemplo `matplotlib.use("Agg")` antes de importar `pyplot`).

---

## Renovar o crear datos sintéticos

Este repo incluye un generador en `**ventas_sinteticas/generar_ventas.py`** (un nivel por encima en el árbol del proyecto). Para producir un CSV nuevo y luego analizarlo:

```bash
cd ../ventas_sinteticas
python3 generar_ventas.py --filas 500 --salida ../analisis_ventas/ventas_sinteticas.csv
cd ../analisis_ventas
python3 analisis_ventas.py
```

Así mantienes copias frescas sin editar el script de análisis.

---

## Estructura de esta carpeta

```
analisis_ventas/
├── README.md              ← este archivo
├── analisis_ventas.py     ← pipeline de carga, métricas y gráficas
├── ventas_sinteticas.csv  ← datos de ejemplo (puedes sobrescribirlos)
├── ventas_mensuales.png   ← salida generada al ejecutar el script
└── top5_productos.png     ← salida generada al ejecutar el script
```

Los PNG y el CSV de ejemplo pueden cambiar cada vez que ejecutes el generador o el análisis.

---

## Autor

| | |
| --- | --- |
| **Usuario de Git** | `OMANROQUI` |
| **Correo** | [omanroqui@gmail.com](mailto:omanroqui@gmail.com) |

Proyecto y documentación mantenidos por **OMANROQUI**. Para colaboraciones o consultas sobre este módulo de análisis, puedes usar el correo indicado o abrir un issue en el repositorio si está publicado en GitHub.

---

## Licencia y uso

Código de ejemplo para aprendizaje y experimentación dentro del repositorio del autor. Adapta, rompe y reconstruye sin ceremonia.