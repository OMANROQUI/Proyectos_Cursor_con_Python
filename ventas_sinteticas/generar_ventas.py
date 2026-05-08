#!/usr/bin/env python3
"""Genera un CSV sintético de ventas: fecha, producto, cantidad, precio."""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

PRODUCTOS = (
    "Laptop Pro 14",
    "Monitor 27\" 4K",
    "Teclado mecánico",
    "Ratón inalámbrico",
    "Auriculares BT",
    "Webcam HD",
    "Disco SSD 1TB",
    "Memoria RAM 32GB",
    "Hub USB-C",
    "Cable HDMI 2m",
    "Tablet 11\"",
    "Smartphone mid-range",
    "Impresora láser",
    "Tinta cartucho pack",
    "Mochila portátil",
)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--filas",
        type=int,
        default=500,
        help="Número de filas a generar (por defecto: 500)",
    )
    p.add_argument(
        "--desde",
        type=str,
        default=None,
        help="Fecha inicio YYYY-MM-DD (por defecto: hace ~1 año)",
    )
    p.add_argument(
        "--hasta",
        type=str,
        default=None,
        help="Fecha fin YYYY-MM-DD (por defecto: hoy)",
    )
    p.add_argument(
        "--semilla",
        type=int,
        default=42,
        help="Semilla del generador aleatorio (por defecto: 42)",
    )
    p.add_argument(
        "--salida",
        type=Path,
        default=Path(__file__).resolve().parent / "ventas_sinteticas.csv",
        help="Ruta del CSV de salida",
    )
    return p.parse_args()


def _parse_date(s: str) -> date:
    y, m, d = (int(x) for x in s.split("-"))
    return date(y, m, d)


def main() -> None:
    args = _parse_args()
    random.seed(args.semilla)

    hoy = date.today()
    if args.hasta:
        fin = _parse_date(args.hasta)
    else:
        fin = hoy
    if args.desde:
        inicio = _parse_date(args.desde)
    else:
        inicio = fin - timedelta(days=365)

    if inicio > fin:
        raise SystemExit("La fecha --desde debe ser anterior o igual a --hasta.")

    dias = (fin - inicio).days + 1
    args.salida.parent.mkdir(parents=True, exist_ok=True)

    with args.salida.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["fecha", "producto", "cantidad", "precio"])
        for _ in range(args.filas):
            offset = random.randrange(dias)
            d = inicio + timedelta(days=offset)
            producto = random.choice(PRODUCTOS)
            cantidad = random.randint(1, 25)
            precio = round(random.uniform(4.99, 1299.99), 2)
            w.writerow([d.isoformat(), producto, cantidad, precio])

    print(f"Escrito: {args.salida} ({args.filas} filas)")


if __name__ == "__main__":
    main()
