#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

# ---------- 1. Cargar resultados ----------
df = pd.read_csv("resultados.csv")          # columnas: variant,size,run,time_ms

# ---------- 2. Calcular medias y σ ----------
stats = (df.groupby(["size", "variant"])["time_ms"]
           .agg(mean="mean", std="std")
           .reset_index())

# ---------- 3. Calcular speed-up ----------
for size in stats["size"].unique():
    base = stats[(stats["size"] == size) & (stats["variant"] == "C_SEC")]["mean"].iloc[0]
    stats.loc[stats["size"] == size, "speedup"] = base / stats["mean"]

# ---------- 4. Figura 1: tiempo medio ± σ ----------
for size in stats["size"].unique():
    subset = stats[stats["size"] == size]
    plt.figure()
    plt.bar(subset["variant"], subset["mean"], yerr=subset["std"], capsize=5)
    plt.ylabel("Tiempo promedio (ms)")
    plt.title(f"Figura 1 – Tiempo medio ± σ   |   Imagen: {size}")
    plt.tight_layout()
    plt.savefig(f"tiempos_{size}.png", dpi=150)

# ---------- 5. Figura 2: speed-up ----------
for size in stats["size"].unique():
    subset = stats[stats["size"] == size]
    plt.figure()
    plt.bar(subset["variant"], subset["speedup"])
    plt.ylabel("Speed-up (×)")
    plt.title(f"Figura 2 – Speed-up vs C_SEC   |   Imagen: {size}")
    plt.tight_layout()
    plt.savefig(f"speedup_{size}.png", dpi=150)

print("Gráficas guardadas: tiempos_*.png  y  speedup_*.png")
