import sys, numpy as np, pandas as pd, cv2
from pathlib import Path
root = Path(sys.argv[1]); out = Path(sys.argv[2]); umbral = float(sys.argv[3])
PAL = np.array([[0,0,0],[255,0,0],[180,120,120],[160,150,20],[140,140,140],[61,230,250],[0,82,255],[255,0,245],[255,235,0],[4,250,7]],np.uint8)  # RGB
NAMES = ["Background","Bld-flood","Bld-noflood","Road-flood","Road-noflood","Water","Tree","Vehicle","Pool","Grass"]
a = pd.read_csv(out/"reparadas_vs_oficiales.csv", dtype={"stem":str})
a = a[a.pct_distinto > umbral]
lab = root/"data/FloodNet/FloodNet-Supervised_v1.0/train/train-label-img"
S=256
def fila(s, pct):
    img = cv2.cvtColor(cv2.imread(str(root/f"data/cache512_full/image/{s}.png")), cv2.COLOR_BGR2RGB)
    r = cv2.imread(str(root/f"data/cache512_full/mask/{s}.png"), 0)
    o = cv2.resize(cv2.imread(str(lab/f"{s}_lab.png"),0), (r.shape[1], r.shape[0]), interpolation=cv2.INTER_NEAREST)
    d = np.where((o!=r)[...,None], np.array([255,0,0],np.uint8), (img*0.35).astype(np.uint8))
    tiles=[cv2.resize(x,(S,S),interpolation=cv2.INTER_NEAREST) for x in (img, PAL[o], PAL[r], d)]
    row=np.hstack(tiles); bar=np.full((22,row.shape[1],3),255,np.uint8)
    cv2.putText(bar,f"{s}  |  {pct:.1f}% distinto  |  foto - oficial - corregida - diferencia",(5,16),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)
    return np.vstack([bar,row])
ley=np.full((22,4*S,3),255,np.uint8)
for i,n in enumerate(NAMES):
    x=5+i*102; ley[4:18,x:x+14]=PAL[i]; cv2.putText(ley,n,(x+17,16),cv2.FONT_HERSHEY_SIMPLEX,0.36,(0,0,0),1)
filas=[fila(s,p) for s,p in zip(a.stem,a.pct_distinto)]
for k in range(0,len(filas),8):
    hoja=np.vstack([ley]+filas[k:k+8])
    cv2.imwrite(str(out/f"lamina_{k//8+1:02d}.png"), cv2.cvtColor(hoja,cv2.COLOR_RGB2BGR))
print(len(filas),"filas,",(len(filas)+7)//8,"láminas")
