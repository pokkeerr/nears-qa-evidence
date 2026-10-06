#!/usr/bin/env python3
# pixel equivalence of the walk-P screenshots, base vs tip (no image is read into the model; counts only). Status bar (top 130 px) excluded: it carries the clock.
import os,sys
from PIL import Image, ImageChops
S=os.path.dirname(os.path.abspath(__file__)); P=S+"/px"
names=sorted({f[len('tip-'):-4] for f in os.listdir(P) if f.startswith('tip-') and f.endswith('.png') and 'scratch' not in f})
tot=0
for n in names:
    a=P+f"/tip-{n}.png"; b=P+f"/base-{n}.png"
    if not os.path.exists(b): print(n,"base missing"); continue
    ia=Image.open(a).convert('RGB'); ib=Image.open(b).convert('RGB')
    if ia.size!=ib.size: print(n,"size differs",ia.size,ib.size); continue
    w,h=ia.size
    box=(0,130,w,h)
    d=ImageChops.difference(ia.crop(box),ib.crop(box))
    bbox=d.getbbox()
    cnt=sum(1 for px in d.getdata() if px!=(0,0,0)) if bbox else 0
    tot+=cnt
    print(f"{n:16s} size {w}x{h} differing pixels (below status bar): {cnt} of {w*(h-130)} bbox={bbox}")
print("total differing pixels",tot)
