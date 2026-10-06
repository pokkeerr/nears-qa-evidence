#!/usr/bin/env python3
# base-vs-tip comparison: (1) per-snapshot digest (header subtotals, rows, minimum caption, summary, Proceed) (2) request multiset per tag + endpoint totals
import os,re,sys,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from hdr import digest
S=os.path.dirname(os.path.abspath(__file__))
def snaps(var):
    d=f"{S}/evidence/walk-{var}"; out={}
    for f in sorted(os.listdir(d)):
        m=re.match(r'(\d+)-(.*)\.txt$',f)
        if m and not f.startswith('steps'): out[m.group(2)]=f"{d}/{f}"
    return out
def reqs(var):
    t=open(f"{S}/evidence/walk-{var}/requests.txt").read().split('\n## ')
    out={}
    for sec in t:
        head,_,body=sec.partition('\n'); head=head.lstrip('# ').strip()
        lines=[l.strip() for l in body.split('\n') if l.strip()]
        out.setdefault(head,[]).extend(lines)
    return out
EP=re.compile(r'^(GET|POST|PUT|PATCH|DELETE) (\S+?)(\?.*)? (\d+|ERR.*)$')
def norm(l):
    m=EP.match(l)
    if not m: return l
    p=re.sub(r'/\d+','/N',m.group(2)); return f"{m.group(1)} {p} {m.group(4)[:3]}"
b=snaps('base'); t=snaps('tip')
common=[k for k in t if k in b]
print(f"snapshots: base {len(b)} tip {len(t)} common {len(common)}; only-base {sorted(set(b)-set(t))[:6]} only-tip {sorted(set(t)-set(b))[:6]}")
diff=0; same=0; rows=[]
for k in common:
    db,dt=digest(b[k]),digest(t[k])
    if db==dt: same+=1
    else:
        diff+=1; rows.append((k,db,dt))
print(f"digest equal {same} / differing {diff}")
for k,db,dt in rows:
    print("DIFF",k)
    for key in ('heads','rows','min','sum','proceed'):
        if db[key]!=dt[key]: print("   ",key,"base",(db[key][:4] if isinstance(db[key],(list,)) else db[key]),"| tip",(dt[key][:4] if isinstance(dt[key],(list,)) else dt[key]))
rb,rt=reqs('base'),reqs('tip')
tags=[k for k in rt if k in rb]
tot_b=collections.Counter(); tot_t=collections.Counter(); rdiff=0
for k in tags:
    cb=collections.Counter(norm(l) for l in rb[k] if not l.startswith('##')); ct=collections.Counter(norm(l) for l in rt[k] if not l.startswith('##'))
    tot_b+=cb; tot_t+=ct
    if cb!=ct:
        rdiff+=1; print("REQDIFF",k,"base-only",dict(cb-ct),"tip-only",dict(ct-cb))
print(f"request sections common {len(tags)}; differing {rdiff}")
core=('cart/update','remove-item','cart/add','group/validate','cart/list','delivery-quote','get-Tax','distance-api','cart/remove','staples','order/details')
for c in core:
    kb=sum(v for k,v in tot_b.items() if c in k); kt=sum(v for k,v in tot_t.items() if c in k)
    print(f"  {c:16s} base {kb:4d} tip {kt:4d} {'EQUAL' if kb==kt else 'DIFF'}")
