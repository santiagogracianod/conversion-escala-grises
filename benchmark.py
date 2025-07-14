import csv, os, subprocess, time, itertools

IMAGES   = [("small",  "img_small.jpg"),
            ("medium", "img_medium.jpg"),
            ("large",  "img_large.jpg")]

VARIANTS = [
    ("C_SEC", "./grayscale_secuelcial_opt {image} out.jpg"),
    ("C_OMP", "./grayscale_paralelo_opt {image} out.jpg"),
    ("PY_SEQ", "python3 grayscale_secuencial.py {image} out_seq.png"),
    ("PY_TH",  "python3 grayscale_paralelo.py  {image} out_th.png"),
]

N_RUNS = 7
rows   = [["variant","size","run","time_ms"]]

def run(cmd):
    t0 = time.perf_counter()
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
    return (time.perf_counter() - t0) * 1000

for (size_tag, img), (variant, tmpl) in itertools.product(IMAGES, VARIANTS):
    for r in range(1, N_RUNS + 1):
        t = run(tmpl.format(image=img))
        rows.append([variant, size_tag, r, round(t, 2)])
        print(f"{variant} | {size_tag} | run {r}: {t:.1f} ms")

with open("resultados.csv", "w", newline="") as f:
    csv.writer(f).writerows(rows)

print("\nDatos guardados en resultados.csv")
