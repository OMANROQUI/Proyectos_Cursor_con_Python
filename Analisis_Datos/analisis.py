#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Lee un CSV y calcula media/mediana/desviación estándar por columna numérica "
            "y genera una gráfica de dispersión (x vs y)."
        )
    )
    p.add_argument(
        "--csv",
        default="Music_Evolution_2026_Pulse.csv",
        help="Ruta al archivo CSV (por defecto: Music_Evolution_2026_Pulse.csv)",
    )
    p.add_argument("--x", default=None, help="Columna para eje X (opcional)")
    p.add_argument("--y", default=None, help="Columna para eje Y (opcional)")
    p.add_argument(
        "--out",
        default=None,
        help="Ruta de salida para la imagen (opcional). Si no, se autogenera.",
    )
    return p.parse_args()


def _try_float(value: str) -> Optional[float]:
    v = value.strip()
    if v == "" or v.lower() in {"na", "nan", "null", "none"}:
        return None
    try:
        f = float(v)
    except Exception:
        return None
    if not math.isfinite(f):
        return None
    return f


def _read_numeric_columns(csv_path: Path) -> Tuple[List[str], Dict[str, List[float]]]:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV sin encabezados.")
        cols = list(reader.fieldnames)
        data: Dict[str, List[float]] = {c: [] for c in cols}

        for row in reader:
            for c in cols:
                val = _try_float(row.get(c, ""))
                if val is not None:
                    data[c].append(val)

    numeric_data = {c: xs for c, xs in data.items() if len(xs) > 0}
    if not numeric_data:
        raise ValueError("No se encontraron columnas numéricas.")
    numeric_cols = [c for c in cols if c in numeric_data]
    return numeric_cols, numeric_data


def _print_stats(numeric_cols: List[str], numeric_data: Dict[str, List[float]]) -> None:
    name_w = max(len(c) for c in numeric_cols)
    header = f"{'columna'.ljust(name_w)}  {'n':>8}  {'media':>14}  {'mediana':>14}  {'desv_std':>14}"
    print("\nEstadísticas por columna (solo numéricas):")
    print(header)
    print("-" * len(header))

    for c in numeric_cols:
        xs = numeric_data[c]
        n = len(xs)
        mean = statistics.fmean(xs) if n else float("nan")
        med = statistics.median(xs) if n else float("nan")
        stdev = statistics.stdev(xs) if n >= 2 else 0.0
        print(
            f"{c.ljust(name_w)}  {n:>8}  {mean:>14.6f}  {med:>14.6f}  {stdev:>14.6f}"
        )


def _scatter_with_matplotlib(x: List[float], y: List[float], x_col: str, y_col: str, out_path: Path) -> None:
    # Import opcional; si no existe, el caller hará fallback a SVG.
    import matplotlib.pyplot as plt  # type: ignore[import-not-found]

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, s=10, alpha=0.35)
    plt.title(f"Dispersión: {y_col} vs {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)


def _scatter_to_svg(x: List[float], y: List[float], x_col: str, y_col: str, out_path: Path) -> None:
    # Scatter básico en SVG (sin dependencias).
    w, h = 1000, 600
    pad = 60
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)

    def sx(v: float) -> float:
        if xmax == xmin:
            return pad + (w - 2 * pad) / 2
        return pad + (v - xmin) * (w - 2 * pad) / (xmax - xmin)

    def sy(v: float) -> float:
        if ymax == ymin:
            return pad + (h - 2 * pad) / 2
        # invertir eje Y para SVG
        return h - pad - (v - ymin) * (h - 2 * pad) / (ymax - ymin)

    title = f"Dispersión: {y_col} vs {x_col}"
    circles = "\n".join(
        f'<circle cx="{sx(xi):.2f}" cy="{sy(yi):.2f}" r="2" fill="#2563eb" fill-opacity="0.35" />'
        for xi, yi in zip(x, y)
    )

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="white"/>
  <text x="{pad}" y="{pad-20}" font-family="sans-serif" font-size="20" fill="#111827">{title}</text>
  <line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="#9ca3af" />
  <line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h-pad}" stroke="#9ca3af" />
  <text x="{w/2:.0f}" y="{h-15}" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#111827">{x_col}</text>
  <text x="18" y="{h/2:.0f}" transform="rotate(-90 18 {h/2:.0f})" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#111827">{y_col}</text>
  {circles}
</svg>
"""
    out_path.write_text(svg, encoding="utf-8")


def main() -> int:
    args = _parse_args()
    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"Error: no existe el archivo CSV: {csv_path}", file=sys.stderr)
        return 2

    # Ruta óptima: pandas + matplotlib (más rápido y correcto con NaNs por fila).
    try:
        import pandas as pd  # type: ignore[import-not-found]

        df = pd.read_csv(csv_path)
        numeric_df = df.select_dtypes(include="number")
        if numeric_df.shape[1] == 0:
            raise ValueError("No se encontraron columnas numéricas.")

        stats = pd.DataFrame(
            {
                "n": numeric_df.count(),
                "media": numeric_df.mean(numeric_only=True),
                "mediana": numeric_df.median(numeric_only=True),
                "desv_std": numeric_df.std(numeric_only=True, ddof=1),
            }
        )

        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 140)
        print("\nEstadísticas por columna (solo numéricas):")
        print(stats.to_string(float_format=lambda v: f"{v:,.6f}"))

        numeric_cols = list(numeric_df.columns)
        x_col = args.x or numeric_cols[0]
        y_col = args.y or (numeric_cols[1] if len(numeric_cols) > 1 else None)
        if y_col is None:
            print("Error: solo hay una columna numérica; no puedo hacer dispersión sin dos.", file=sys.stderr)
            return 4
        if x_col not in numeric_df.columns:
            print(f"Error: columna X no encontrada o no numérica: {x_col}", file=sys.stderr)
            return 5
        if y_col not in numeric_df.columns:
            print(f"Error: columna Y no encontrada o no numérica: {y_col}", file=sys.stderr)
            return 6

        out_path = Path(args.out) if args.out else Path(f"scatter_{x_col}_vs_{y_col}.png")
        plot_df = numeric_df[[x_col, y_col]].dropna()
        if plot_df.shape[0] == 0:
            print("Error: no hay datos para graficar tras eliminar NaNs.", file=sys.stderr)
            return 7

        # Si matplotlib no está, caemos al flujo sin dependencias (SVG).
        try:
            import matplotlib.pyplot as plt  # type: ignore[import-not-found]

            plt.figure(figsize=(10, 6))
            plt.scatter(plot_df[x_col], plot_df[y_col], s=10, alpha=0.35)
            plt.title(f"Dispersión: {y_col} vs {x_col}")
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.grid(True, alpha=0.25)
            plt.tight_layout()
            plt.savefig(out_path, dpi=160)
            print(f"\nGráfica guardada en: {out_path}")
            return 0
        except Exception:
            # Fallback a SVG con listas (mantiene el análisis con pandas, solo cambia la salida de la gráfica).
            x = plot_df[x_col].astype(float).tolist()
            y = plot_df[y_col].astype(float).tolist()
            if out_path.suffix.lower() != ".svg":
                out_path = out_path.with_suffix(".svg")
            _scatter_to_svg(x, y, x_col, y_col, out_path)
            print(
                "\nNota: no encontré matplotlib; generé la dispersión en SVG.\n"
                f"Gráfica guardada en: {out_path}"
            )
            return 0

    except Exception:
        # Ruta sin dependencias.
        pass

    try:
        numeric_cols, numeric_data = _read_numeric_columns(csv_path)
    except Exception as e:
        print(f"Error leyendo el CSV: {e}", file=sys.stderr)
        return 3

    _print_stats(numeric_cols, numeric_data)

    x_col = args.x or numeric_cols[0]
    y_col = args.y or (numeric_cols[1] if len(numeric_cols) > 1 else None)
    if y_col is None:
        print("Error: solo hay una columna numérica; no puedo hacer dispersión sin dos.", file=sys.stderr)
        return 4
    if x_col not in numeric_data:
        print(f"Error: columna X no encontrada o no numérica: {x_col}", file=sys.stderr)
        return 5
    if y_col not in numeric_data:
        print(f"Error: columna Y no encontrada o no numérica: {y_col}", file=sys.stderr)
        return 6

    # Alinea puntos por índice (hasta el mínimo disponible entre columnas).
    npts = min(len(numeric_data[x_col]), len(numeric_data[y_col]))
    x = numeric_data[x_col][:npts]
    y = numeric_data[y_col][:npts]
    if npts == 0:
        print("Error: no hay datos para graficar.", file=sys.stderr)
        return 7

    # Preferimos PNG si matplotlib está disponible; si no, generamos SVG.
    if args.out:
        out_path = Path(args.out)
    else:
        out_path = Path(f"scatter_{x_col}_vs_{y_col}.png")

    try:
        _scatter_with_matplotlib(x, y, x_col, y_col, out_path)
        print(f"\nGráfica guardada en: {out_path}")
        return 0
    except Exception:
        # fallback a SVG
        if out_path.suffix.lower() != ".svg":
            out_path = out_path.with_suffix(".svg")
        _scatter_to_svg(x, y, x_col, y_col, out_path)
        print(
            "\nNota: no encontré matplotlib; generé la dispersión en SVG.\n"
            f"Gráfica guardada en: {out_path}"
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

