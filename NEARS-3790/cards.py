#!/usr/bin/env python3
"""cards.py <png> <nodes.txt> [min_h_dp] — compact per-card gap summary."""
import re, subprocess, sys
png, nodes = sys.argv[1], sys.argv[2]
minh = float(sys.argv[3]) if len(sys.argv) > 3 else 150
txt = open(nodes).read()
for m in re.finditer(r'bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label="(.*?)"\n(?=class=|\Z)', txt, re.S):
    x1,y1,x2,y2 = map(int, m.groups()[:4]); lab = m.group(5)
    if ('AED' not in lab and 'د.إ' not in lab) or (y2-y1)/3 < minh or (x2-x1)/3 < 100: continue
    if y2 > 2700: continue  # under bottom nav / clipped
    out = subprocess.run(['python3', sys.argv[0].replace('cards.py','measure.py'), png, str(x1),str(y1),str(x2),str(y2)], capture_output=True, text=True).stdout.splitlines()
    box = out[0].split('= ')[-1]
    runs = []
    for l in out[1:]:
        mm = re.match(r'(INK|blank)\s+y=\s*([\d.]+)\.\.\s*([\d.]+)dp\s+h=\s*([\d.]+)dp(?:\s+x=\[([\d.]+),([\d.]+)\])?', l)
        if mm: runs.append((mm.group(1), float(mm.group(2)), float(mm.group(3)), float(mm.group(4)), mm.group(5), mm.group(6)))
    # image = tallest INK run
    img = max((r for r in runs if r[0]=='INK'), key=lambda r: r[3])
    after = [r for r in runs if r[1] >= img[2]]
    inks = [r for r in after if r[0]=='INK' and r[3] >= 3]
    if not inks: print(f"{box} NO-INFO {lab[:60]!r}"); continue
    last = inks[-1]
    interior = [r for r in after if r[0]=='blank' and r[1] >= inks[0][2] and r[2] <= last[1]]
    lead = inks[0][1] - img[2]
    trail = [r for r in after if r[0]=='blank' and r[1] >= last[2]]
    tr = sum(r[3] for r in trail)
    rows = ' '.join(f"{r[3]:.0f}@x{float(r[4]):.0f}-{float(r[5]):.0f}" for r in inks)
    mx = max([r[3] for r in interior], default=0)
    print(f"{box} lead={lead:.1f} maxInteriorGap={mx:.1f} trail={tr:.1f} rows[{rows}] :: {lab.replace(chr(10),' | ')[:90]}")
