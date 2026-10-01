#!/usr/bin/env python3
"""Resolve a control INSIDE a basket row live from the a11y tree, then tap it.
Rows = nodes whose label starts with ROWPREFIX, sorted top-to-bottom.
Usage: rowtap.py <row#(1-based)> <label> [--print] [--rowprefix P]
       rowtap.py --pair <row#> <label> <row#> <label>   (two taps in ONE adb shell)
Prints the row's full label so the row identity ("N gm" = row's own qty) is logged."""
import os, re, subprocess, sys, time
SERIAL = 'emulator-5600'
ROWPREFIX = 'Tones Mild Chili Powder |'
args = sys.argv[1:]
if '--rowprefix' in args:
    i = args.index('--rowprefix'); ROWPREFIX = args[i + 1]; del args[i:i + 2]

def dump():
    for _ in range(6):
        subprocess.run(['adb', '-s', SERIAL, 'shell', 'uiautomator', 'dump', '/sdcard/qa3977r.xml'], capture_output=True)
        x = subprocess.run(['adb', '-s', SERIAL, 'exec-out', 'cat', '/sdcard/qa3977r.xml'], capture_output=True, text=True).stdout
        if x.startswith('<?xml'):
            return x
        time.sleep(1.5)
    sys.exit('DUMP FAILED')

def nodes(x):
    out = []
    for n in re.findall(r'<node [^>]*>', x):
        lab = re.search(r'content-desc="([^"]*)"', n).group(1).replace('&#10;', ' | ')
        b = tuple(map(int, re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', n).groups()))
        if lab:
            out.append((lab, b))
    return out

def resolve(ns, row, label):
    rows = sorted([n for n in ns if n[0].startswith(ROWPREFIX)], key=lambda n: n[1][1])
    if len(rows) < row:
        sys.exit(f'only {len(rows)} rows: {[r[0] for r in rows]}')
    rl, rb = rows[row - 1]
    hits = [n for n in ns if n[0] == label and n[1][0] >= rb[0] and n[1][2] <= rb[2] and n[1][1] >= rb[1] and n[1][3] <= rb[3]]
    if len(hits) != 1:
        sys.exit(f'row {row} "{label}": {len(hits)} hits')
    b = hits[0][1]
    return rl, ((b[0] + b[2]) // 2, (b[1] + b[3]) // 2)

ns = nodes(dump())
if args[0] == '--pair':
    r1, c1 = resolve(ns, int(args[1]), args[2]); r2, c2 = resolve(ns, int(args[3]), args[4])
    print(f'A: row{args[1]} [{r1}] {args[2]} @ {c1}\nB: row{args[3]} [{r2}] {args[4]} @ {c2}')
    gap = os.environ.get('PAIR_GAP', '0')
    cmd = f'date +%s.%N; input tap {c1[0]} {c1[1]}; sleep {gap}; date +%s.%N; input tap {c2[0]} {c2[1]}; date +%s.%N'
    out = subprocess.run(['adb', '-s', SERIAL, 'shell', cmd], capture_output=True, text=True).stdout.split()
    t = [float(v) for v in out]
    print(f'tapA_start={t[0]:.3f} tapB_start={t[1]:.3f} end={t[2]:.3f} gap_ms={(t[1]-t[0])*1000:.0f}')
else:
    rl, c = resolve(ns, int(args[0]), args[1])
    print(f'row{args[0]} [{rl}] {args[1]} @ {c}')
    if '--print' not in args:
        subprocess.run(['adb', '-s', SERIAL, 'shell', 'input', 'tap', str(c[0]), str(c[1])])
        print('tapped at', time.strftime('%H:%M:%S', time.gmtime()) + 'Z')
