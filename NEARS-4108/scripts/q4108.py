import json, time, subprocess, urllib.request, urllib.error, uuid, collections, os, sys

BASE = "http://127.0.0.1:8408/api/v1"
EVID = "/Users/Apple/Projects/nears-NEARS-4108-verify-token-enumeration/docs/qa-evidence/NEARS-4108"
ADMIN = "/Users/Apple/Projects/nears-NEARS-4108-verify-token-enumeration/Admin"
TRANSCRIPT = EVID + "/transcript.txt"

EP = {
    "cust_verify": ("POST", "/auth/verify-token"),
    "cust_reset": ("PUT", "/auth/reset-password"),
    "dm_verify": ("POST", "/auth/delivery-man/verify-token"),
    "dm_reset": ("PUT", "/auth/delivery-man/reset-password"),
    "cust_forgot": ("POST", "/auth/forgot-password"),
    "dm_forgot": ("POST", "/auth/delivery-man/forgot-password"),
    "vendor_verify": ("POST", "/auth/vendor/verify-token"),
    "cust_login": ("POST", "/auth/login"),
    "dm_login": ("POST", "/auth/delivery-man/login"),
}

_hist = collections.defaultdict(list)  # bucket -> timestamps
_glob = []


def _bucket_keys(body):
    ks = []
    for f in ("email", "phone", "email_or_phone"):
        v = body.get(f) if isinstance(body, dict) else None
        if isinstance(v, (str, int, float)) and not isinstance(v, bool):
            v = str(v).strip().lower()
            if v:
                ks.append(f + ":" + v)
    return ks or ["ip"]


def pace(body):
    while True:
        now = time.time()
        wait = 0
        _glob[:] = [t for t in _glob if now - t < 62]
        if len(_glob) >= 17:
            wait = max(wait, 62 - (now - _glob[0]))
        for k in _bucket_keys(body):
            _hist[k] = [t for t in _hist[k] if now - t < 62]
            if len(_hist[k]) >= 5:
                wait = max(wait, 62 - (now - _hist[k][0]))
        if wait <= 0:
            return
        time.sleep(wait + 0.2)


def reset_state():
    out = subprocess.run(["php", "artisan", "cache:clear"], cwd=ADMIN, capture_output=True, text=True)
    _hist.clear()
    _glob.clear()
    return out.stdout.strip() + out.stderr.strip()


def log(s):
    with open(TRANSCRIPT, "a") as f:
        f.write(s + "\n")


def req(label, ep, body, raw=None, pace_it=True):
    method, path = EP[ep]
    if pace_it:
        pace(body)
    data = raw if raw is not None else json.dumps(body)
    r = urllib.request.Request(BASE + path, data=data.encode(), method=method,
                               headers={"Content-Type": "application/json", "Accept": "application/json",
                                        "X-Request-Id": "q4108-" + uuid.uuid4().hex[:12]})
    rid = r.get_header("X-request-id")
    t0 = time.perf_counter()
    try:
        resp = urllib.request.urlopen(r, timeout=60)
        status, text, hdr = resp.status, resp.read().decode(), resp.headers
    except urllib.error.HTTPError as e:
        status, text, hdr = e.code, e.read().decode(), e.headers
    dt = time.perf_counter() - t0
    now = time.time()
    _glob.append(now)
    for k in _bucket_keys(body):
        _hist[k].append(now)
    try:
        j = json.loads(text)
    except Exception:
        j = None
    code = msg = None
    if isinstance(j, dict) and j.get("errors"):
        e0 = j["errors"][0] if isinstance(j["errors"], list) else j["errors"]
        code = e0.get("code") if isinstance(e0, dict) else None
        msg = e0.get("message") if isinstance(e0, dict) else None
    elif isinstance(j, dict):
        msg = j.get("message")
    log("[%s] %s %s%s\n   req-id=%s body=%s\n   -> HTTP %s (%.3fs) code=%r message=%r\n   raw=%s" % (
        time.strftime("%H:%M:%S"), method, path, "", rid, data if len(data) < 300 else data[:300], status, dt, code, msg, text[:400]))
    print("%-34s %s %-4s code=%-16s msg=%r  (%.2fs)" % (label, ep, status, code, msg, dt))
    return {"status": status, "code": code, "message": msg, "json": j, "t": dt, "rid": rid, "raw": text}


def sel(sql):
    out = subprocess.run(["mysql", "-u", "root", "multi_food_db_qa4108", "-N", "-e", sql], capture_output=True, text=True)
    return out.stdout.strip()


def sig(r):
    return (r["status"], r["code"], r["message"])


def section(t):
    log("\n==== %s ====" % t)
    print("\n==== %s ====" % t)
