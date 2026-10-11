#!/usr/bin/env python3
"""NEARS-4134 QA harness. Never prints token values: key paths, lengths, sha8 only."""
import hashlib, json, os, sys, urllib.request, urllib.parse, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
SECRET = os.path.join(HERE, "tokens.secret.json")
LRT = os.path.join(HERE, "lrt_values.secret")
KEY = "login_remember_token"


def sha8(s):
    return hashlib.sha256(s.encode()).hexdigest()[:8]


def http(base, method, path, headers=None, params=None, form=None):
    url = base + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = None
    h = {"Accept": "application/json"}
    h.update(headers or {})
    if form is not None:
        data = urllib.parse.urlencode(form).encode()
        h["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(), dict(e.headers)


def walk(node, path=""):
    """yield flattened key paths; list indices collapse to []"""
    if isinstance(node, dict):
        for k, v in node.items():
            p = f"{path}.{k}" if path else k
            yield p, k, v
            yield from walk(v, p)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v, path + "[]")


def analyse(body, secrets):
    try:
        j = json.loads(body)
    except Exception:
        return {"json": False, "len": len(body)}
    paths, lrt = set(), []
    for p, k, v in walk(j):
        paths.add(p)
        if k == KEY:
            lrt.append({"path": p, "type": type(v).__name__, "len": len(v) if isinstance(v, str) else None,
                        "sha8": sha8(v) if isinstance(v, str) else None})
    raw_hit = {name: (val in body) for name, val in secrets.items()}
    return {"json": True, "paths": sorted(paths), "lrt": lrt, "raw_contains_secret": raw_hit}


def login_all(base):
    out = {}
    s, b, _ = http(base, "POST", "/api/v1/auth/vendor/login",
                   form={"email": "ahmed.khan@demo.com", "password": "123456789", "vendor_type": "owner"})
    out["owner_status"] = s
    out["owner"] = json.loads(b).get("token")
    s, b, _ = http(base, "POST", "/api/v1/auth/vendor/login",
                   form={"email": "qa.n4134.store2.emp@nears.com", "password": "123456789", "vendor_type": "employee"})
    out["employee_status"] = s
    out["employee"] = json.loads(b).get("token")
    s, b, _ = http(base, "POST", "/api/v1/auth/login",
                   form={"login_type": "manual", "email_or_phone": "customer@nears.com", "password": "123456789", "field_type": "email"})
    out["customer_status"] = s
    out["customer"] = json.loads(b).get("token")
    s, b, _ = http(base, "POST", "/api/v1/auth/delivery-man/login",
                   form={"phone": "+971565656656", "password": "123456789"})
    out["dm_status"] = s
    out["dm"] = json.loads(b).get("token")
    json.dump(out, open(SECRET, "w"))
    os.chmod(SECRET, 0o600)
    print({k: (v if k.endswith("_status") else f"len={len(v) if v else None} sha8={sha8(v) if v else None}") for k, v in out.items()})


def auth_headers(tok, vtype=None):
    h = {"Authorization": f"Bearer {tok}"}
    if vtype:
        h["vendorType"] = vtype
    return h


def conv_ids():
    # conversation ids that involve vendor 91135's UserInfo, resolved via mysql CLI (SELECT only)
    import subprocess
    q = ("select c.id, c.sender_type, c.receiver_type from multi_food_db_qa4134.conversations c "
         "join multi_food_db_qa4134.user_infos u on (u.id=c.sender_id or u.id=c.receiver_id) where u.vendor_id=2 order by c.id")
    out = subprocess.check_output(["mysql", "-u", "root", "-N", "-e", q]).decode().split("\n")
    rows = [r.split("\t") for r in out if r]
    return rows


def probes(base, tk, cid_cust, cid_dm):
    secrets = {}
    vals = open(LRT).read().split()
    secrets["owner_lrt"], secrets["emp_lrt"] = vals[0], vals[1]
    P = {}

    def rec(name, resp):
        s, b, hd = resp
        a = analyse(b, secrets)
        a["status"] = s
        P[name] = a

    # profile
    rec("AC1_profile_owner", http(base, "GET", "/api/v1/vendor/profile", auth_headers(tk["owner"], "owner")))
    rec("AC2_profile_employee", http(base, "GET", "/api/v1/vendor/profile", auth_headers(tk["employee"], "employee")))
    # customer conversations
    ch = auth_headers(tk["customer"])
    rec("AC6_customer_list", http(base, "GET", "/api/v1/customer/message/list", ch, {"limit": 10, "offset": 1}))
    rec("AC6_customer_list_type_vendor", http(base, "GET", "/api/v1/customer/message/list", ch, {"limit": 10, "offset": 1, "type": "vendor"}))
    rec("AC6_customer_search", http(base, "GET", "/api/v1/customer/message/search-list", ch, {"name": "Fresh", "limit": 10, "offset": 1}))
    rec("AC6_customer_details", http(base, "GET", "/api/v1/customer/message/details", ch, {"conversation_id": cid_cust, "limit": 10, "offset": 1}))
    rec("AC6_customer_send", http(base, "POST", "/api/v1/customer/message/send", ch, None,
                                  {"conversation_id": cid_cust, "message": "qa4134 customer follow-up"}))
    # delivery man conversations (bearer + legacy ?token= which messages_store reads)
    dh = auth_headers(tk["dm"])
    dt = {"token": tk["dm"]}
    rec("AC6_dm_list", http(base, "GET", "/api/v1/delivery-man/message/list", dh, dict(dt, limit=10, offset=1)))
    rec("AC6_dm_search", http(base, "GET", "/api/v1/delivery-man/message/search-list", dh, dict(dt, name="Fresh", limit=10, offset=1)))
    rec("AC6_dm_details", http(base, "GET", "/api/v1/delivery-man/message/details", dh, dict(dt, conversation_id=cid_dm, limit=10, offset=1)))
    rec("AC6_dm_send", http(base, "POST", "/api/v1/delivery-man/message/send", dh, dt,
                            {"conversation_id": cid_dm, "message": "qa4134 dm follow-up"}))
    # vendor conversations (owner + employee)
    for who in ("owner", "employee"):
        vh = auth_headers(tk[who], who)
        rec(f"AC7_vendor_{who}_list", http(base, "GET", "/api/v1/vendor/message/list", vh, {"limit": 10, "offset": 1}))
        rec(f"AC7_vendor_{who}_search", http(base, "GET", "/api/v1/vendor/message/search-list", vh, {"name": "Customer", "limit": 10, "offset": 1}))
        rec(f"AC7_vendor_{who}_search_dm", http(base, "GET", "/api/v1/vendor/message/search-list", vh, {"name": "Ali", "limit": 10, "offset": 1}))
        rec(f"AC7_vendor_{who}_details_cust", http(base, "GET", "/api/v1/vendor/message/details", vh, {"conversation_id": cid_cust, "limit": 10, "offset": 1}))
        rec(f"AC7_vendor_{who}_details_dm", http(base, "GET", "/api/v1/vendor/message/details", vh, {"conversation_id": cid_dm, "limit": 10, "offset": 1}))
        rec(f"AC7_vendor_{who}_send", http(base, "POST", "/api/v1/vendor/message/send", vh, None,
                                           {"conversation_id": cid_cust, "message": f"qa4134 vendor {who} reply"}))
    return P


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "login":
        login_all(sys.argv[2])
    elif cmd == "run":
        label, base, cid_cust, cid_dm = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
        tk = json.load(open(SECRET))
        P = probes(base, tk, cid_cust, cid_dm)
        json.dump(P, open(os.path.join(HERE, f"result_{label}.json"), "w"), indent=1)
        for k, v in P.items():
            print(f"{label} {k}: status={v['status']} json={v.get('json')} lrt_hits={[(h['path'], h['len'], h['sha8']) for h in v.get('lrt', [])]} raw_secret={v.get('raw_contains_secret')} npaths={len(v.get('paths', []))}")
