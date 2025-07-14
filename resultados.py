import pandas as pd, matplotlib.pyplot as plt
df = pd.read_csv("resultados.csv")
stats = (df.groupby(["size","variant"])["time_ms"]
           .agg(["mean","std"]).reset_index())

# calc speed-up por tamaño tomando C_SEC como baseline
for sz in df["size"].unique():
    base = stats[(stats["size"]==sz)&(stats["variant"]=="C_SEC")]["mean"].iloc[0]
    stats.loc[stats["size"]==sz,"speedup"] = base / stats["mean"]

stats.to_csv("stats.csv", index=False)
