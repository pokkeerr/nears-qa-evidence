import json, urllib.request, urllib.parse, urllib.error, os
P=os.path.dirname(os.path.abspath(__file__))
B=os.environ.get('QA_BASE','http://127.0.0.1:8199/api/v1')
TOK={}
for l in open(P+'/tok.env'):
    k,_,v=l.strip().partition('='); TOK[k]=v
def get(nm, ep, params=None, raw_qs=None, tokenparam=True):
    qs = raw_qs if raw_qs is not None else urllib.parse.urlencode(params or {}, doseq=True)
    url = f"{B}/{ep}?{qs}"
    req = urllib.request.Request(url, headers={'Accept':'application/json','zoneId':'[1]','moduleId':'1','Authorization':'Bearer '+TOK[nm],'vendorType':('employee' if nm.startswith('E') else 'owner'),'X-Request-Id':'qa4199-'+str(abs(hash(url)))[:8]})
    try:
        r = urllib.request.urlopen(req, timeout=60)
        return r.status, json.loads(r.read().decode() or 'null'), dict(r.headers)
    except urllib.error.HTTPError as e:
        b=e.read().decode()
        try: j=json.loads(b)
        except Exception: j=b[:300]
        return e.code, j, dict(e.headers)
def items(fb):
    return {i['key']: i for i in (fb or {}).get('items',[])}
def opts(fb,key):
    it=items(fb).get(key); 
    return [(o['value'],o['count'],o.get('selected')) for o in (it or {}).get('options',[])]
def ids(j): return [o['id'] for o in j['orders']]
