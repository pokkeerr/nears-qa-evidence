#!/usr/bin/env python3
"""hseg.py <png> <nodes> <label-substr> — for the card, print horizontal ink segments
(gap>=6dp splits) for each info row, plus navy-badge pill extent (dark navy pixels)."""
import re, sys, subprocess
from PIL import Image
png, nodes, sub = sys.argv[1:4]
txt = open(nodes).read()
im = Image.open(png).convert('RGB'); px = im.load()
for m in re.finditer(r'bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label="(.*?)"\n(?=class=|\Z)', txt, re.S):
    x1,y1,x2,y2 = map(int, m.groups()[:4]); lab = m.group(5)
    if sub not in lab or ('AED' not in lab and 'د.إ' not in lab) or (y2-y1) < 450 or y2 > 2700: continue
    # navy pill: pixels with b>90, r<40, g<40
    navy = [(x,y) for y in range(y1,y2) for x in range(x1,x2) if (lambda p: p[2]>90 and p[0]<40 and p[1]<40)(px[x,y])]
    # exclude price text (navy too) — keep the tallest contiguous rectangle-ish: take rows with >60 navy px
    from collections import defaultdict
    rows = defaultdict(list)
    for x,y in navy: rows[y].append(x)
    def longest(xs):
        xs=sorted(xs); best=(0,0,0); a=xs[0]; prev=xs[0]
        for x in xs[1:]+[10**9]:
            if x!=prev+1:
                if prev-a>best[0]: best=(prev-a,a,prev)
                a=x
            prev=x
        return best
    pill = {y: longest(xs) for y,xs in rows.items()}
    pill = {y:v for y,v in pill.items() if v[0] >= 45}
    if pill:
        ys = list(pill); xs = [v[1] for v in pill.values()] + [v[2] for v in pill.values()]
        print(f"{lab[:40]!r}: badge pill x=[{(min(xs)-x1)/3:.1f},{(max(xs)-x1)/3:.1f}]dp y=[{(min(ys)-y1)/3:.1f},{(max(ys)-y1)/3:.1f}]dp card_w={(x2-x1)/3:.0f}dp")
    else:
        print(f"{lab[:40]!r}: no badge pill found")
