import subprocess, threading, time, sys, re, os
SER, OUT, DB = sys.argv[1], sys.argv[2], sys.argv[3]
TAPX, TAPY = sys.argv[4], sys.argv[5]
ORDER = sys.argv[6]
os.makedirs(OUT, exist_ok=True)
adb = ["adb", "-s", SER]
rows = []
stop = False
def dump_loop():
    while not stop:
        t = time.time()
        r = subprocess.run(adb + ["exec-out", "uiautomator", "dump", "/dev/tty"], capture_output=True, text=True)
        x = r.stdout
        t2 = time.time()
        rows.append(("dump", t, t2, 'Order is  Pending' in x, 'Order is  Confirmed' in x, bool(re.search(r'text="Confirm"|content-desc="Confirm"', x)), 'Swipe to Process' in x, bool(re.search(r'content-desc="Yes"|text="Yes"', x))))
def db(label):
    r = subprocess.run(["mysql","-u","root","-N",DB,"-e",f"select order_status,confirmed from orders where id={ORDER}"],capture_output=True,text=True)
    rows.append(("db", time.time(), label, r.stdout.strip()))
subprocess.run(adb + ["logcat", "-c"])
lg = open(f"{OUT}/logcat.txt", "w")
lp = subprocess.Popen(adb + ["logcat", "-v", "time", "flutter:V", "*:S"], stdout=lg)
db("pre")
if os.environ.get("SYNC_POLL"):
    lg.flush(); t_start=time.time(); last=None
    while True:
        lg.flush()
        txt=open(f"{OUT}/logcat.txt").read()
        n=txt.count("GET endpoint=/api/v1/vendor/order\n")
        if last is None: last=n
        if n>last: break
        time.sleep(0.05)
    time.sleep(0.25)
    subprocess.run(adb+["shell","input","tap","797","2248"]); time.sleep(0.9)
th = threading.Thread(target=dump_loop); th.start()
time.sleep(0.5)
T0 = time.time()
subprocess.run(adb + ["shell", "input", "tap", TAPX, TAPY])
Ttap = time.time()
rows.append(("tap", T0, Ttap))
def shot(name):
    t = time.time()
    with open(f"{OUT}/{name}.png", "wb") as f:
        subprocess.run(adb + ["exec-out", "screencap", "-p"], stdout=f)
    rows.append(("shot", name, t, time.time()))
for name, off in [("p0",0.0),("p1",1.0),("p2",2.0),("p4",4.0),("p6",6.0),("p7",7.0),("p9",9.0),("p12",12.0),("p15",15.0)]:
    d = Ttap + off - time.time()
    if d > 0: time.sleep(d)
    shot(name)
    if name in ("p2","p7"): db(name)
    if name == os.environ.get("DOUBLE_AT","p2") and os.environ.get("DOUBLE"):
        t=time.time(); subprocess.run(adb+["shell","input","tap","797","2248"]); rows.append(("tap2c", t, time.time()))
        time.sleep(0.4)
        shot("dlg_check")
        rr=subprocess.run(adb+["exec-out","uiautomator","dump","/dev/tty"],capture_output=True,text=True).stdout
        rows.append(("dlg", time.time(), 'Are you sure to confirm' in rr, bool(re.search(r'content-desc="Yes"|text="Yes"', rr))))
        t=time.time(); subprocess.run(adb+["shell","input","tap",TAPX,TAPY]); rows.append(("tap2y", t, time.time()))
stop = True; th.join()
db("end")
lp.terminate(); lg.close()
with open(f"{OUT}/timeline.txt","w") as f:
    f.write(f"T0(before tap)={T0:.2f} Ttap(after tap returns)={Ttap:.2f}\n")
    for r in rows:
        if r[0]=="dump": f.write(f"dump  start=+{r[1]-Ttap:6.2f}s end=+{r[2]-Ttap:6.2f}s  pending={r[3]} confirmed={r[4]} ConfirmBtn={r[5]} SwipeToProcess={r[6]} YesBtn={r[7]}\n")
        elif r[0]=="shot": f.write(f"shot  {r[1]} taken at +{r[2]-Ttap:6.2f}s..+{r[3]-Ttap:6.2f}s\n")
        elif r[0]=="db": f.write(f"db    {r[2]} at +{r[1]-Ttap:6.2f}s: {r[3]}\n")
        elif r[0]=="dlg": f.write(f"dlgdump at +{r[1]-Ttap:6.2f}s: confirm-dialog-text-present={r[2]} YesBtn={r[3]}\n")
        elif r[0] in ("tap2c","tap2y"): f.write(f"{r[0]} second-confirm tap at +{r[1]-Ttap:6.2f}s\n")
        else: f.write(f"tap   took {r[2]-r[1]:.2f}s\n")
print(open(f"{OUT}/timeline.txt").read())
