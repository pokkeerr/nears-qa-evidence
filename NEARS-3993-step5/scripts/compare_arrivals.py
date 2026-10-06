#!/usr/bin/env python3
# ordered (arrival-time) request comparison base vs tip from arrivals.log; markers '### VAR tag' close a block
import re,sys,collections,os
Q=os.path.dirname(os.path.abspath(__file__))
blocks={}; cur=[]; TS={}; BT={}
for l in open(Q+'/arrivals.log'):
    l=l.rstrip('\n')
    if l.startswith('### '):
        _,var,tag=l.split(' ',2); blocks[(var,tag)]=cur; BT[(var,tag)]=TS.get(id(cur),[]); cur=[]; continue
    p=l.split('\t',2)
    if len(p)<3: continue
    req=p[2]
    if re.search(r'/storage/|/public/assets|\.png|\.jpg',req): continue
    cur.append(req); TS.setdefault(id(cur),[]).append(float(p[1]))
def nz(r): return re.sub(r'(lat|lng|latitude|longitude|origin_lat|origin_lng|destination_lat|destination_lng)=-?[0-9.]+',r'\1=<c>',re.sub(r'cart_id=[0-9]+','cart_id=<ID>',r))
tags=sorted({t for v,t in blocks})
nd=0; ordd=0; cntd=0; rows=[]
for t in tags:
    b=blocks.get(('base',t)); p=blocks.get(('tip',t))
    if b is None or p is None: rows.append((t,'MISSING',b is None,p is None)); continue
    sd=lambda L:[re.search(r'stores/details/(\d+)',x).group(1) for x in L if re.search(r'GET /api/v1/stores/details/\d+',x)]
    db,dt=sd(b),sd(p)
    cb=collections.Counter(map(nz,b)); ct=collections.Counter(map(nz,p))
    fullorder=[nz(x) for x in b]==[nz(x) for x in p]
    if db!=dt: nd+=1
    if cb!=ct: cntd+=1
    if not fullorder: ordd+=1
    rows.append((t,db,dt,'EQUAL' if db==dt else 'DIFF', 'counts-equal' if cb==ct else 'COUNT-DIFF %s | %s'%(dict(cb-ct),dict(ct-cb)),'order-equal' if fullorder else 'order-differs'))
for r in rows: print(r)
print('SUMMARY blocks=%d store-details-sequence-diffs=%d request-count-diffs=%d full-order-diffs=%d'%(len(tags),nd,cntd,ordd))

def clusters(key,GAP=0.25):
    L=blocks.get(key); T=BT.get(key)
    if L is None: return None
    ev=[(t,re.search(r'stores/details/(\d+)',r).group(1)) for t,r in zip(T,L) if re.search(r'GET /api/v1/stores/details/\d+',r)]
    out=[]; last=None
    for t,i in ev:
        if last is None or t-last>GAP: out.append([])
        out[-1].append(i); last=t
    return [''.join(sorted(c,key=int)).__len__() and ','.join(sorted(c,key=int)) for c in out]
print('--- burst-clustered store-details (gap>0.25 s = new group, within-group order unordered)')
bad=0
for t in tags:
    cb,cp=clusters(('base',t)),clusters(('tip',t))
    if cb is None or cp is None: continue
    eq=cb==cp; bad+=0 if eq else 1
    print('%-45s %s base=%s tip=%s'%(t,'EQUAL' if eq else 'DIFF',cb,cp))
print('CLUSTERED-DIFFS',bad)

print('--- phase-clustered store-details (gap>2.0 s = new phase; sequential-fetch/delay scale)')
bad=0
for t in tags:
    cb,cp=clusters(('base',t),2.0),clusters(('tip',t),2.0)
    if cb is None or cp is None: continue
    eq=cb==cp; bad+=0 if eq else 1
    print('%-45s %s base=%s tip=%s'%(t,'EQUAL' if eq else 'DIFF',cb,cp))
print('PHASE-CLUSTERED-DIFFS',bad)
