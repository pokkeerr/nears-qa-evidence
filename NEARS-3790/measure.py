#!/usr/bin/env python3
"""measure.py <png> x1 y1 x2 y2 [density=3] [start_y]
Prints vertical ink/blank runs inside a card box (px bounds from uiautomator),
in dp. Ink = pixel differing from the card background by > THR (sum abs RGB).
Also prints per-run horizontal ink extent (for badge/name start-edge checks)."""
import sys
from collections import Counter
from PIL import Image

png = sys.argv[1]
x1, y1, x2, y2 = map(int, sys.argv[2:6])
dens = float(sys.argv[6]) if len(sys.argv) > 6 else 3.0
start = int(sys.argv[7]) if len(sys.argv) > 7 else y1
THR = 60
MX = 9  # skip border/shadow columns
im = Image.open(png).convert("RGB")
W, H = im.size
x2 = min(x2, W); y2 = min(y2, H)
px = im.load()
# background = most common colour in the lowest 6 interior rows
bg = (255, 255, 255)
# shrink box to the white card surface (node bounds can include section bg)
def isw(x, y):
    p = px[x, y]; return p[0] > 250 and p[1] > 250 and p[2] > 250
colw = [sum(isw(x, y) for y in range((y1+y2)//2, y2, 3)) for x in range(x1, x2)]
cm = max(colw) if colw else 0
cols = [x1 + i for i, v in enumerate(colw) if v > 0.5 * cm]
if cols: x1, x2 = cols[0], cols[-1] + 1
roww = [sum(isw(x, y) for x in range(x1, x2, 3)) for y in range(y1, y2)]
rm = max(roww) if roww else 0
rws = [y1 + i for i, v in enumerate(roww) if v > 0.5 * rm]
if rws: y2 = rws[-1] + 1
if start < y1: start = y1

def ink(x, y):
    p = px[x, y]
    return abs(p[0]-bg[0]) + abs(p[1]-bg[1]) + abs(p[2]-bg[2]) > THR

rows = []
for y in range(start, y2 - 4):
    xs = [x for x in range(x1 + MX, x2 - MX) if ink(x, y)]
    rows.append((y, len(xs), (min(xs), max(xs)) if xs else None))
runs = []
cur = None
for y, n, ext in rows:
    kind = 'INK' if n > 0 else 'blank'
    if cur and cur[0] == kind:
        cur[2] = y
        if ext:
            cur[3] = (min(cur[3][0], ext[0]), max(cur[3][1], ext[1])) if cur[3] else ext
    else:
        if cur: runs.append(cur)
        cur = [kind, y, y, ext]
runs.append(cur)
print(f"bg={bg} box=[{x1},{y1}][{x2},{y2}] = {(x2-x1)/dens:.0f}x{(y2-y1)/dens:.0f}dp")
for kind, a, b, ext in runs:
    h = (b - a + 1) / dens
    e = f" x=[{(ext[0]-x1)/dens:.1f},{(ext[1]-x1)/dens:.1f}]dp" if ext else ""
    print(f"{kind:5s} y={(a-y1)/dens:6.1f}..{(b-y1+1)/dens:6.1f}dp  h={h:5.1f}dp{e}")
