#!/usr/bin/env python3
"""Swipe basket row N (label-resolved live) left, then tap the single revealed
clickable Button inside that row's bounds. Usage: swipe_delete.py <row#> [rowprefix]"""
import re, subprocess, sys, time
SER = 'emulator-5600'
row = int(sys.argv[1]); pref = sys.argv[2] if len(sys.argv) > 2 else 'Tones Mild Chili Powder'
def dump():
    for _ in range(6):
        subprocess.run(['adb', '-s', SER, 'shell', 'uiautomator', 'dump', '/sdcard/qa3977s.xml'], capture_output=True)
        x = subprocess.run(['adb', '-s', SER, 'exec-out', 'cat', '/sdcard/qa3977s.xml'], capture_output=True, text=True).stdout
        if x.startswith('<?xml'): return x
        time.sleep(1.5)
    sys.exit('DUMP FAILED')
def nodes(x):
    for n in re.findall(r'<node [^>]*>', x):
        yield (re.search(r'content-desc="([^"]*)"', n).group(1).replace('&#10;', ' | '),
               tuple(map(int, re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', n).groups())),
               re.search(r'class="([^"]*)"', n).group(1), re.search(r'clickable="([^"]*)"', n).group(1))
rows = sorted([n for n in nodes(dump()) if n[0].startswith(pref + ' |')], key=lambda n: n[1][1])
lab, (x1, y1, x2, y2), _, _ = rows[row - 1]
print('swipe row%d [%s]' % (row, lab[:60]))
y = y1 + int(0.2 * (y2 - y1)); sx = x1 + int(0.55 * (x2 - x1)); ex = x1 + int(0.1 * (x2 - x1))
subprocess.run(['adb', '-s', SER, 'shell', 'input', 'swipe', str(sx), str(y), str(ex), str(y), '300'])
time.sleep(1.5)
btn = [n for n in nodes(dump()) if n[2] == 'android.widget.Button' and n[3] == 'true' and not n[0]
       and n[1][1] >= y1 - 5 and n[1][3] <= y2 + 5 and n[1][0] > (x1 + x2) // 2]
if len(btn) != 1:
    sys.exit('revealed button hits=%d %s' % (len(btn), btn))
b = btn[0][1]; c = ((b[0] + b[2]) // 2, (b[1] + b[3]) // 2)
subprocess.run(['adb', '-s', SER, 'shell', 'input', 'tap', str(c[0]), str(c[1])])
print('tapped revealed delete Button %s @ %s at %sZ' % (b, c, time.strftime('%H:%M:%S', time.gmtime())))
