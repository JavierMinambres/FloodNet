import sys, numpy as np, pandas as pd, cv2
from pathlib import Path
root = Path(sys.argv[1]); out = Path(sys.argv[2])
NAMES = ["Background","Building-flooded","Building-non-flooded","Road-flooded","Road-non-flooded","Water","Tree","Vehicle","Pool","Grass"]
idx = pd.read_csv(root/"data/cache512_full/index.csv", dtype={"stem":str})
rep = idx[idx.mascara=="reparada"]
lab = root/"data/FloodNet/FloodNet-Supervised_v1.0/train/train-label-img"
filas=[]
for s in rep.stem:
    r = cv2.imread(str(root/f"data/cache512_full/mask/{s}.png"), cv2.IMREAD_GRAYSCALE).astype(np.int64)
    o = cv2.imread(str(lab/f"{s}_lab.png"), cv2.IMREAD_GRAYSCALE)
    o = cv2.resize(o, (r.shape[1], r.shape[0]), interpolation=cv2.INTER_NEAREST).astype(np.int64)
    d = o != r
    c = np.bincount(o[d]*10 + r[d], minlength=100)
    top = np.argsort(c)[::-1][:3]
    cambios = "; ".join(f"{NAMES[k//10]}->{NAMES[k%10]} {100*c[k]/d.size:.1f}%" for k in top if c[k] > 0)
    filas.append(dict(stem=s, pct_distinto=round(100*d.mean(),2),
                      clases_oficial=len(np.unique(o)), clases_reparada=len(np.unique(r)), cambios_principales=cambios))
a = pd.DataFrame(filas).sort_values("pct_distinto", ascending=False)
a.to_csv(out/"reparadas_vs_oficiales.csv", index=False, encoding="utf-8-sig")
print(len(a), "comparadas")
for u in (0,1,5,10,20,50): print(f">{u}%:", (a.pct_distinto>u).sum())
print("idénticas:", (a.pct_distinto==0).sum())
print(a.head(12).to_string(index=False))
