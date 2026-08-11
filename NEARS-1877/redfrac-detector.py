#!/usr/bin/env python3
"""Red-fraction detector for the Flutter debug ErrorWidget (full-screen red).

Instrument for NEARS-1877 QA. Log silence is not evidence on this surface
(NEARS-1860 open), so the red screen is detected in pixels.

A pixel counts as "error red" when R is dominant and both G and B are low:
    R > 140 and G < 110 and B < 110 and R - max(G,B) > 50
Reports the fraction of such pixels over the whole frame.
"""
import sys
from PIL import Image


def red_fraction(path: str) -> float:
    im = Image.open(path).convert("RGB")
    im = im.resize((im.width // 4, im.height // 4))
    px = im.load()
    w, h = im.size
    red = 0
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r > 140 and g < 110 and b < 110 and r - max(g, b) > 50:
                red += 1
    return red / float(w * h)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(f"{red_fraction(p):.3f}\t{p}")
