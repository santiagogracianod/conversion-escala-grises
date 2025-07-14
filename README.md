# Conversión a Escala de Grises – Comparación Secuencial vs. Paralelo

Este repositorio contiene cuatro implementaciones que convierten imágenes RGB a escala de grises y un pequeño banco de pruebas para comparar su rendimiento.

| Variante | Lenguaje | Estrategia |
| -------- | -------- | ---------- |
| **C_SEC** | C | Bucle doble, secuencial |
| **C_OMP** | C | Paralelo por hilos usando OpenMP |
| **PY_SEQ** | Python | Secuencial con Pillow |
| **PY_TH** | Python | Paralelo con `ThreadPoolExecutor` + NumPy |

Hay scripts auxiliares que lanzan todas las corridas, guardan los resultados y generan las gráficas mostradas en el informe.

---

## 1 · Estructura rápida

```
├── benchmark.py         # lanza todas las pruebas y crea resultados.csv
├── graficas.ipynb       # Jupyter notebook con análisis + gráficas
├── graficas.py          # misma lógica del notebook en .py (opcional)
├── grayscale_secuencial.c / .py
├── grayscale_paralelo.c / .py
├── img_small.jpg        # imágenes de prueba (no se suben por defecto)
└── ...
```

---

## 2 · Requisitos

| Entorno | Versión mínima |
|---------|----------------|
| **GNU gcc** | 9.0 (soporte OpenMP 4) |
| **Python** | 3.8 |
| **NumPy**  | 1.22 |
| **Pillow** | 10.0 |
| **matplotlib** | 3.8 |

> Recomendado usar un *virtualenv*.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # <– crea este fichero si lo deseas
```

---

## 3 · Compilación

```bash
# Secuencial
gcc -O3 grayscale_secuencial.c  -o grayscale_secuelcial_opt

# Paralelo con OpenMP
gcc -O3 -fopenmp grayscale_paralelo.c -o grayscale_paralelo_opt
```

---

## 4 · Ejecución simple

```bash
# C
./c_sec     img_small.jpg out_c.png
./c_omp     img_small.jpg out_c_omp.png

# Python
python3 grayscale_secuencial.py img_small.jpg out_py.png
python3 grayscale_paralelo.py   img_small.jpg out_py_th.png
```

---

## 5 · Benchmark completo

```bash
python3 benchmark.py   # corre 7 veces cada variante × 3 tamaños
```
Generará:
* `resultados.csv` – tiempos brutos
* `stats.csv` – promedios y desviaciones
* `tiempos_*.png`, `speedup_*.png` – gráficas listas para el informe

---

## 6 · Cómo reproducir las gráficas


Script
```bash
python3 graficas.py      # lee resultados.csv y guarda PNGs
```

---

## 7 · Licencia

Este proyecto se distribuye bajo la licencia MIT. 

---

## 8 · Autor

Santiago Graciano David

Alexander Valencia 

Universidad de Antioquia  (2025)
