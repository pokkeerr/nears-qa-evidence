import json, urllib.request, urllib.error, sys
B="http://127.0.0.1:8196"
def _get(qs, zone="[2]", module="1", lon="54.3526", lat="24.4752", extra=None, path="/api/v1/search/unified", auth=None, loc="en"):
    h={"Accept":"application/json","X-localization":loc}
    if zone is not None: h["zoneId"]=zone
    if module is not None: h["moduleId"]=module
    if lon is not None: h["longitude"]=lon
    if lat is not None: h["latitude"]=lat
    if extra: h.update(extra)
    if auth: h["Authorization"]="Bearer "+auth
    req=urllib.request.Request(B+path+"?"+qs, headers=h)
    try:
        r=urllib.request.urlopen(req, timeout=60)
        return r.status, json.loads(r.read()), dict(r.headers)
    except urllib.error.HTTPError as e:
        b=e.read()
        try: j=json.loads(b)
        except Exception: j=b[:200]
        return e.code, j, dict(e.headers)
def ids(j,k): return [x["id"] for x in j.get(k,[])]
def blk(j,ns,key):
    f=j.get("filters",{}).get(ns)
    if not f: return None
    for it in f["items"]:
        if it["key"]==key: return it
    return None
def keys(j,ns):
    f=j.get("filters",{}).get(ns); return [i["key"] for i in f["items"]] if f else None
def opts(j,ns,key):
    b=blk(j,ns,key); return {o["value"]:o["count"] for o in b["options"]} if b else None

import time
def get(qs, *a, retry429=True, **kw):
    while True:
        r=_get(qs,*a,**kw)
        if r[0]==429 and retry429:
            time.sleep(15); continue
        return r
