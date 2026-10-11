import json, sys, os, re, urllib.request, urllib.error, urllib.parse

port, arm, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = f"http://127.0.0.1:{port}"
KEYS = ["temp_token", "cm_firebase_token", "social_id"]
VALS = ["n4135-qa-temp-token", "n4135-qa-fcm-token", "n4135-qa-google-sub-0001"]
os.makedirs(outdir, exist_ok=True)

def call(method, path, headers=None, data=None, label=None, save=True):
    h = {"Accept": "application/json", "X-localization": "en"}
    h.update(headers or {})
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=body, headers=h, method=method)
    try:
        r = urllib.request.urlopen(req, timeout=60); code = r.status; raw = r.read()
    except urllib.error.HTTPError as e:
        code = e.code; raw = e.read()
    text = raw.decode("utf-8", "replace")
    if save and label:
        open(os.path.join(outdir, label + ".json"), "w").write(text)
    return code, text

def login(path, data):
    code, text = call("POST", path, data=data, save=False)
    assert code == 200, (path, code, text[:200])
    return json.loads(text)["token"]

cust = login("/api/v1/auth/login", {"login_type": "manual", "email_or_phone": "+971500041351", "password": "123456789", "field_type": "phone"})
own = login("/api/v1/auth/vendor/login", {"email": "qa.n4135.vendor@nears.com", "password": "123456789", "vendor_type": "owner"})
emp = login("/api/v1/auth/vendor/login", {"email": "qa.n4135.vendor.emp@nears.com", "password": "123456789", "vendor_type": "employee"})
dm = login("/api/v1/auth/delivery-man/login", {"phone": "+971500041355", "password": "123456789"})

H = {
    "customer": {"Authorization": "Bearer " + cust},
    "owner": {"Authorization": "Bearer " + own, "vendorType": "owner"},
    "employee": {"Authorization": "Bearer " + emp, "vendorType": "employee"},
    "dm": {"Authorization": "Bearer " + dm},
}
PFX = {"customer": "/api/v1/customer/message/", "owner": "/api/v1/vendor/message/", "employee": "/api/v1/vendor/message/", "dm": "/api/v1/delivery-man/message/"}
CONVS = {"customer": [221, 222, 223, 224], "owner": [221, 222], "employee": [221, 222], "dm": [223, 224]}
SEND_CONV = {"customer": 221, "owner": 221, "employee": 222, "dm": 223}

results = []  # (label, group, code)
def rec(label, group, code, text):
    results.append({"label": label, "group": group, "code": code, "bytes": len(text)})

for who in ["customer", "owner", "employee", "dm"]:
    c, t = call("GET", PFX[who] + "list?limit=100&offset=1", H[who], label=f"{who}.message.list"); rec(f"{who}.message.list", "conv", c, t)
    c, t = call("GET", PFX[who] + "search-list?name=N4135&limit=100&offset=1", H[who], label=f"{who}.message.search-list"); rec(f"{who}.message.search-list", "conv", c, t)
    for cid in CONVS[who]:
        c, t = call("GET", PFX[who] + f"details?conversation_id={cid}&limit=100&offset=1", H[who], label=f"{who}.message.details.{cid}"); rec(f"{who}.message.details.{cid}", "conv", c, t)

# customer/info (needs X-localization, already default)
c, t = call("GET", "/api/v1/customer/info", H["customer"], label="customer.info"); rec("customer.info", "info", c, t)

# order blocks
for who, pre in [("owner", "/api/v1/vendor/"), ("employee", "/api/v1/vendor/"), ("dm", "/api/v1/delivery-man/")]:
    for oid in (91804, 91805):
        for ep in ("order", "order-details"):
            lab = f"{who}.{ep}.{oid}"
            c, t = call("GET", f"{pre}{ep}?order_id={oid}", H[who], label=lab); rec(lab, "order", c, t)
    for ep, q in [("current-orders", "?limit=100&offset=1"), ("all-orders", "?limit=100&offset=1")]:
        lab = f"{who}.{ep}"
        c, t = call("GET", pre + ep + q, H[who], label=lab); rec(lab, "order", c, t)
c, t = call("GET", "/api/v1/delivery-man/latest-orders?limit=100&offset=1", H["dm"], label="dm.latest-orders"); rec("dm.latest-orders", "order", c, t)
c, t = call("GET", "/api/v1/delivery-man/profile", H["dm"], label="dm.profile"); rec("dm.profile", "order", c, t)

# POST sends last (they add rows to the clone)
for who in ["owner", "employee", "dm", "customer"]:
    lab = f"{who}.message.send"
    c, t = call("POST", PFX[who] + "send", H[who], data={"conversation_id": SEND_CONV[who], "message": f"n4135-qa send {arm} {who}"}, label=lab); rec(lab, "send", c, t)

# --- walker ---
def walk(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            p = f"{path}.{k}" if path else k
            out.append((p, k, v)); walk(v, p, out)
    elif isinstance(node, list):
        for v in node:
            walk(v, path + "[]", out)

summary = {"arm": arm, "port": port, "bodies": 0, "json_bodies": 0, "key_hits": [], "value_hits": [], "rawkeyname_hits": [], "files": {}}
for r in results:
    text = open(os.path.join(outdir, r["label"] + ".json")).read()
    summary["bodies"] += 1
    try:
        j = json.loads(text); summary["json_bodies"] += 1
    except Exception:
        j = None
    paths = []
    if j is not None:
        walk(j, "", paths)
    flat = sorted({p for p, _, _ in paths})
    keyhits = sorted({p for p, k, _ in paths if k in KEYS})
    valhits = [v for v in VALS if v in text]
    rawkeys = [k for k in KEYS if k in text]
    summary["files"][r["label"]] = {"code": r["code"], "bytes": r["bytes"], "paths": flat, "key_paths": keyhits, "value_hits": valhits, "raw_keyname_hits": rawkeys}
    for p in keyhits: summary["key_hits"].append((r["label"], p))
    for v in valhits: summary["value_hits"].append((r["label"], v))
    for k in rawkeys: summary["rawkeyname_hits"].append((r["label"], k))
json.dump(summary, open(os.path.join(outdir, "_summary.json"), "w"), indent=1)
print(arm, "bodies", summary["bodies"], "json", summary["json_bodies"], "keypath hits", len(summary["key_hits"]), "value hits", len(summary["value_hits"]), "rawkey hits", len(summary["rawkeyname_hits"]))
print("codes:", sorted({(r["label"], r["code"]) for r in results if r["code"] != 200}))
