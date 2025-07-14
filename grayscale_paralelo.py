#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Conversión paralela RGB → escala de grises con ThreadPoolExecutor.

Uso:
    python grayscale_paralelo.py <imagen_entrada> <imagen_salida> [num_hilos]
Si no se indica num_hilos, se usa os.cpu_count().
"""
import sys
import time
import os
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# --- Validar argumentos ---
if len(sys.argv) < 3:
    print(f"Uso: {sys.argv[0]} <imagen_entrada> <imagen_salida> [num_hilos]")
    sys.exit(1)

entrada = sys.argv[1]
salida  = sys.argv[2]
num_threads = int(sys.argv[3]) if len(sys.argv) > 3 else os.cpu_count()

# --- Cargar imagen ---
img = Image.open(entrada).convert("RGB")
img_array = np.asarray(img)
height, width = img_array.shape[:2]

gray_array = np.empty((height, width), dtype=np.uint8)
chunk_size = height // num_threads

def procesar_chunk(start_row, end_row):
    """Convierte las filas [start_row:end_row) a gris."""
    chunk = img_array[start_row:end_row]
    gray_chunk = np.dot(chunk, [0.299, 0.587, 0.114])
    gray_array[start_row:end_row] = gray_chunk.astype(np.uint8)

# --- Paralelizar ---
t0 = time.time()
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    for i in range(num_threads):
        s = i * chunk_size
        e = height if i == num_threads - 1 else (i + 1) * chunk_size
        executor.submit(procesar_chunk, s, e)
# (Al salir del with, espera a que todos los hilos terminen)

t_ms = (time.time() - t0) * 1000

# --- Guardar y mostrar métricas ---
Image.fromarray(gray_array, mode='L').save(salida)
print(f"Conversión paralela completada → {salida}")
print(f"Tiempo: {t_ms:.2f} ms  |  Hilos: {num_threads}")
