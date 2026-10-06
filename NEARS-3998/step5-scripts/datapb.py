#!/usr/bin/env python3
"""Pre-flight data probe (read-only HTTP GETs via the backend): query -> top-5 autocomplete candidates -> place-api-details -> get-zone-id status. Prints per-candidate index+status only (no place ids, no coordinates)."""
import sys,json,urllib.request,urllib.parse,urllib.error
B='http://127.0.0.1:8334/api/v1/config/'
def get(path,params):
    u=B+path+'?'+urllib.parse.urlencode(params)
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={'Accept':'application/json'}),timeout=40); return r.status,json.loads(r.read() or b'null')
    except urllib.error.HTTPError as e:
        try: return e.code,json.loads(e.read() or b'null')
        except Exception: return e.code,None
def probe(q):
    st,d=get('place-api-autocomplete',{'search_text':q})
    sug=(d or {}).get('suggestions') or []
    ids=[s['placePrediction']['placeId'] for s in sug if 'placePrediction' in s]
    out=[]
    for i,pid in enumerate(ids[:5]):
        s2,d2=get('place-api-details',{'placeid':pid})
        loc=((d2 or {}).get('location') or {})
        lat,lng=loc.get('latitude'),loc.get('longitude')
        if lat is None: out.append((i+1,'details',s2)); continue
        s3,_=get('get-zone-id',{'lat':lat,'lng':lng})
        out.append((i+1,'zone',s3))
    return st,len(ids),out
for q in sys.argv[1:]:
    st,n,out=probe(q)
    inz=sum(1 for x in out if x[1]=='zone' and x[2]==200); outz=sum(1 for x in out if x[1]=='zone' and x[2] in(403,404))
    print('%-28r ac_status=%s preds=%d top5=%s  => in=%d out=%d other=%d'%(q,st,n,' '.join('%d:%s%s'%(i,k[0],c) for i,k,c in out),inz,outz,len(out)-inz-outz))
