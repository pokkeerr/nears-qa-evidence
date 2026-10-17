#!/usr/bin/env python3
"""NEARS-4243 post-fix timing instrument (QA artifact, not product code).

usage: frame_capture.py SER OUT DB ORDER CONFIRM_X CONFIRM_Y YES_X YES_Y STATUS_BOX(l,t,r,b) [--double-ms 800,6000] [--no-sync]
Opens nothing: the order details screen must already be showing the PENDING order.
Flow: wait for a poll tick (GET /vendor/order in logcat) -> +250ms -> tap Confirm -> 900ms -> tap Yes (T0) -> screencap loop for 14s.
Every frame is classified by pixel distance of the status-label crop vs a PENDING reference taken before Confirm and a CONFIRMED reference (last frame).
Device->host clock skew is measured and applied so logcat lines can be placed on the host timeline.
"""
import subprocess, sys, time, os, io, re, threading
from PIL import Image, ImageChops, ImageStat

SER, OUT, DB, ORDER = sys.argv[1:5]
CX, CY, YX, YY = sys.argv[5:9]
BOX = tuple(int(v) for v in sys.argv[9].split(","))
DOUBLE = []
if "--double-ms" in sys.argv:
    DOUBLE = [int(v) for v in sys.argv[sys.argv.index("--double-ms") + 1].split(",")]
SYNC = "--no-sync" not in sys.argv
os.makedirs(OUT, exist_ok=True)
adb = ["adb", "-s", SER]


def shot():
    t0 = time.time()
    p = subprocess.run(adb + ["exec-out", "screencap", "-p"], capture_output=True)
    return t0, time.time(), p.stdout


def crop(png):
    return Image.open(io.BytesIO(png)).convert("RGB").crop(BOX)


def dist(a, b):
    return sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / 3.0


def db(label):
    r = subprocess.run(["mysql", "-u", "root", "-N", DB, "-e", f"select order_status,confirmed from orders where id={ORDER}"], capture_output=True, text=True)
    return f"{label}: {r.stdout.strip()} (host {time.strftime('%H:%M:%S')})"


# clock skew (host - device)
h0 = time.time(); dv = float(subprocess.run(adb + ["shell", "date", "+%s.%N"], capture_output=True, text=True).stdout.strip()); h1 = time.time()
skew = (h0 + h1) / 2 - dv

# pending reference
_, _, ref_p_png = shot()
ref_p = crop(ref_p_png)
open(f"{OUT}/ref_pending.png", "wb").write(ref_p_png)
notes = [db("db-pre")]

subprocess.run(adb + ["logcat", "-c"])
lg = open(f"{OUT}/logcat.txt", "w")
lp = subprocess.Popen(adb + ["logcat", "-v", "epoch", "flutter:V", "FA:V", "FA-SVC:V", "*:S"], stdout=lg)
time.sleep(0.3)


def count_polls():
    lg.flush()
    return open(f"{OUT}/logcat.txt").read().count("GET endpoint=/api/v1/vendor/order\n")


if SYNC:
    last = count_polls()
    while count_polls() <= last:
        time.sleep(0.05)
    t_tick = time.time()
    time.sleep(0.25)
tc = time.time()
subprocess.run(adb + ["shell", "input", "tap", CX, CY])
if os.environ.get("PRE_SQL"):
    time.sleep(0.4)
    subprocess.run(["mysql", "-u", "root", DB, "-e", os.environ["PRE_SQL"]])
    notes.append(db("db-after-PRE_SQL"))
    time.sleep(0.5)
else:
    time.sleep(0.9)
frames = []
stop = False


def loop():
    while not stop:
        a, b, png = shot()
        frames.append((a, b, png))


th = threading.Thread(target=loop); th.start()
time.sleep(0.5)
t_yes0 = time.time()
subprocess.run(adb + ["shell", "input", "tap", YX, YY])
t_yes = time.time()
extra = []
for ms in DOUBLE:
    d = t_yes + ms / 1000.0 - time.time()
    if d > 0:
        time.sleep(d)
    t = time.time()
    subprocess.run(adb + ["shell", "input", "tap", CX, CY])
    extra.append(("confirm-retap", t, time.time()))
d = t_yes + 14 - time.time()
if d > 0:
    time.sleep(d)
stop = True; th.join()
notes.append(db("db-end"))
lp.terminate(); lg.close()

ref_c_png = frames[-1][2]
ref_c = crop(ref_c_png)
open(f"{OUT}/ref_confirmed.png", "wb").write(ref_c_png)
rows = []
first_conf = None
for a, b, png in frames:
    c = crop(png)
    dp, dc = dist(c, ref_p), dist(c, ref_c)
    st = "CONFIRMED" if dc < 3 and dc < dp else ("PENDING" if dp < 3 else "other")
    rows.append((a - t_yes, b - t_yes, st, dp, dc))
    if st == "CONFIRMED" and first_conf is None:
        first_conf = (a, b, png)
for off in (1.5, 3.0):
    cand = [f for f in frames if f[0] >= t_yes + off]
    if cand:
        open(f"{OUT}/frame_plus{off}.png", "wb").write(cand[0][2])
if first_conf:
    open(f"{OUT}/first_confirmed_frame.png", "wb").write(first_conf[2])
# last PENDING frame after yes
last_p = None
for a, b, png in frames:
    if a > t_yes and dist(crop(png), ref_p) < 3:
        last_p = (a, b, png)
if last_p:
    open(f"{OUT}/last_pending_frame.png", "wb").write(last_p[2])

with open(f"{OUT}/timeline.txt", "w") as f:
    f.write(f"clock skew host-device = {skew:+.3f}s ; YesTap host={t_yes0:.2f}..{t_yes:.2f}; order {ORDER}\n")
    for n in notes: f.write(n + "\n")
    for e in extra: f.write(f"{e[0]} at +{e[1]-t_yes:.2f}s..+{e[2]-t_yes:.2f}s\n")
    f.write("-- frame states (relative to Yes tap, seconds; dp=dist to pending ref, dc=dist to confirmed ref)\n")
    prev = None
    for s, e, st, dp, dc in rows:
        if st != prev:
            f.write(f"+{s:6.2f}s..+{e:6.2f}s  {st}  dp={dp:.1f} dc={dc:.1f}\n")
            prev = st
    f.write(f"frames={len(rows)}\n")
    f.write("-- logcat lines on host timeline (relative to Yes tap)\n")
    for ln in open(f"{OUT}/logcat.txt"):
        m = re.match(r"\s*(\d+\.\d+)\s+\d+\s+\d+\s+\S\s+(\S+)\s*:\s*(.*)", ln)
        if m and ("[NET]" in m.group(3) or "[FAIL]" in m.group(3) or "[ERR]" in m.group(3) or "order_accept" in ln or "Logging event" in ln):
            f.write(f"+{float(m.group(1)) + skew - t_yes:7.2f}s  {m.group(3)[:150]}\n")
print(open(f"{OUT}/timeline.txt").read())
