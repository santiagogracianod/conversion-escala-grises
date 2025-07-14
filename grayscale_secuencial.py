#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Conversión secuencial RGB → escala de grises.

Uso:
    python grayscale_secuencial.py <imagen_entrada> <imagen_salida>
"""
import sys
import time
from PIL import Image

# --- Validar argumentos ---
if len(sys.argv) < 3:
    print(f"Uso: {sys.argv[0]} <imagen_entrada> <imagen_salida>")
    sys.exit(1)

entrada = sys.argv[1]
salida  = sys.argv[2]

# --- Cargar imagen ---
img = Image.open(entrada).convert("RGB")
width, height = img.size
pixels = img.load()

gray_img = Image.new("L", (width, height))

# --- Conversión píxel a píxel ---
t0 = time.time()
for y in range(height):
    for x in range(width):
        r, g, b = pixels[x, y]
        gray = (299 * r + 587 * g + 114 * b) // 1000   # entero rápido
        gray_img.putpixel((x, y), gray)
t_ms = (time.time() - t0) * 1000

# --- Guardar y mostrar métricas ---
gray_img.save(salida)
print(f"Conversión completada → {salida}")
print(f"Tiempo: {t_ms:.2f} ms")
