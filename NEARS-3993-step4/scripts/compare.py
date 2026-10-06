#!/usr/bin/env python3
import os,re,sys,difflib,collections
S=os.path.dirname(os.path.abspath(__file__))
def load(var):
    d=f"{S}/evidence/walk-{var}"; out={}
    for f in sorted(os.listdir(d)):
        m=re.match(r'(\d+)-(.*)\.txt$',f)
        if m: out[m.group(2)]=open(f"{d}/{f}").read().splitlines()
    return out
def norm(lines):
    # drop bounds-only noise? keep full: label + bounds + clickable
    return lines
b=load('base'); t=load('tip')
only_b=sorted(set(b)-set(t)); only_t=sorted(set(t)-set(b))
print(f"snaps base={len(b)} tip={len(t)} common={len(set(b)&set(t))} only-base={only_b} only-tip={only_t}")
ndiff=0; nlab=0
for tag in sorted(set(b)&set(t), key=lambda k:(int(re.match(r'(\d+)',[f for f in os.listdir(f'{S}/evidence/walk-tip') if f.endswith('-'+k+'.txt')][0]).group(1)))):
    if b[tag]==t[tag]: continue
    ndiff+=1
    lab=lambda L:[re.sub(r'^class=\S+ clickable=(\w+) bounds=\[[0-9,]+\]\[[0-9,]+\] ',r'\1 ',l) for l in L if 'label="' in l and 'label=""' not in l]
    lb,lt=lab(b[tag]),lab(t[tag])
    if lb!=lt:
        nlab+=1; print(f"\n### LABEL-DIFF {tag}")
        for l in difflib.unified_diff(lb,lt,'base','tip',lineterm='',n=0): 
            if not l.startswith(('---','+++','@@')): print('  ',l[:200])
    else:
        gd=[l for l in difflib.unified_diff(b[tag],t[tag],'base','tip',lineterm='',n=0) if not l.startswith(('---','+++','@@'))]
        print(f"\n### GEOMETRY-ONLY {tag}"); [print('  ',l[:230]) for l in gd[:8]]
print(f"\nSUMMARY: differing snaps={ndiff} (label-diff={nlab}, geometry/flag-only={ndiff-nlab}) of {len(set(b)&set(t))}")
# requests
def reqs(var):
    s=open(f"{S}/evidence/walk-{var}/requests.txt").read().split('## ')[1:]
    out=collections.OrderedDict()
    for blk in s:
        ls=blk.strip().split('\n'); out[ls[0]]=ls[1:]
    return out
rb,rt=reqs('base'),reqs('tip')
print("\nREQUESTS: blocks base=%d tip=%d"%(len(rb),len(rt)))
tot=0
for k in rt:
    if k not in rb: print("  only-tip block",k); continue
    nz=lambda L:[re.sub(r'(lat|lng|latitude|longitude)=-?[0-9.]+',r'\1=<c>',re.sub(r'(origin_lat|origin_lng|destination_lat|destination_lng)=-?[0-9.]+',r'\1=<c>',l)) for l in L]
    cb=collections.Counter(nz(rb[k])); ct=collections.Counter(nz(rt[k]))
    if cb!=ct:
        tot+=1; print("  DIFF",k,"| base-only:",dict(cb-ct),"| tip-only:",dict(ct-cb))
for k in rb:
    if k not in rt: print("  only-base block",k)
print("REQUEST-DIFF-BLOCKS",tot)
