#!/usr/bin/env python3
"""compare.py <tipfile.jsonl> <basefile.jsonl>  -> per-marker request windows, base vs tip; plus text/pixel parity of snaps."""
import json,sys,re,os
from PIL import Image, ImageChops
Q=os.path.dirname(os.path.abspath(__file__))
def windows(path,prefix):
    wins={}; cur=None
    for l in open(path):
        r=json.loads(l)
        if 'marker' in r:
            m=r['marker']
            if m.startswith(prefix+'-'): cur=m[len(prefix)+1:]; wins[cur]=[]
            else: cur=None
            continue
        if cur is None: continue
        p=r.get('path','')
        if p.startswith('/storage') or p.startswith('/public'): continue
        wins[cur].append((r['m'],p.replace('/api/v1/',''),r['status']))
    return wins
tipw=windows(sys.argv[1],'tip'); basew=windows(sys.argv[2],'base')
def norm(rs): return [ (m,p,s) for m,p,s in rs ]
FAM=re.compile(r'^(items/latest|items/search|categories/items/|stores/details|items/recommended|categories/offers|categories/items|customer/cart|customer/wish|cashback|search/)')
out=[]; eq=0; tot=0; diffs=[]
tot_t=tot_b=0
for k in tipw:
    t=norm(tipw[k]); b=norm(basew.get(k,[]))
    # noise filter for equality verdict: distance-api + extra_charge are derived from the store location, kept but compared separately
    same = t==b
    tot+=1; eq+=same
    tot_t+=len(t); tot_b+=len(b)
    out.append((k,len(b),len(t),'EQUAL' if same else 'DIFF'))
    if not same: diffs.append((k,b,t))
print('markers tip=%d base=%d  EQUAL=%d/%d  total requests base=%d tip=%d'%(len(tipw),len(basew),eq,tot,tot_b,tot_t))
for k,nb,nt,v in out: print('%-44s base=%2d tip=%2d %s'%(k,nb,nt,v))
for k,b,t in diffs:
    print('\n--- DIFF',k); print(' base:'); [print('   ',x) for x in b]; print(' tip:'); [print('   ',x) for x in t]
# text + pixel parity
print('\n=== snap parity (label text, pixels)')
tdir=os.path.join(Q,'walk','tip'); bdir=os.path.join(Q,'walk','base')
rows=[]
for f in sorted(os.listdir(tdir)):
    if not f.endswith('.txt') or f.startswith('.'): continue
    n=f[:-4]
    tt=open(os.path.join(tdir,f)).read(); bf=os.path.join(bdir,f)
    bt=open(bf).read() if os.path.exists(bf) else None
    pix='-'
    tp=os.path.join(tdir,n+'.png'); bp=os.path.join(bdir,n+'.png')
    if os.path.exists(tp) and os.path.exists(bp):
        a=Image.open(tp).convert('RGB'); b=Image.open(bp).convert('RGB')
        if a.size==b.size:
            d=ImageChops.difference(a,b).getbbox()
            if d is None: pix='0px'
            else:
                diff=ImageChops.difference(a,b).convert('L').point(lambda v:255 if v>8 else 0)
                pix=str(sum(1 for v in diff.getdata() if v))+'px'
        else: pix='size-differs'
    rows.append((n,'TEXT-EQUAL' if tt==bt else ('TEXT-DIFF' if bt is not None else 'NO-BASE'),pix))
for n,t,p in rows: print('%-12s %-11s %s'%(n,t,p))
