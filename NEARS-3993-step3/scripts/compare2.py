#!/usr/bin/env python3
# scroll-aware compare: a label diff is REAL only if the two snapshots share the same scroll offset (anchor = common non-nav label)
import os,re,sys
S=os.path.dirname(os.path.abspath(__file__))
def load(var):
    d=f"{S}/evidence/walk-{var}"; out={}
    for f in sorted(os.listdir(d)):
        m=re.match(r'(\d+)-(.*)\.txt$',f)
        if m: out[m.group(2)]=(int(m.group(1)),open(f"{d}/{f}").read().splitlines())
    return out
P=re.compile(r'clickable=(\w+) bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label="(.*)"')
def nodes(L):
    r=[]
    for l in L:
        m=P.search(l)
        if m and m.group(6): r.append((m.group(6),m.group(1),int(m.group(3)),int(m.group(5))))
    return r
NAV={'Home','Categories','Search','Basket','Profile','Proceed to Checkout'}
b=load('base'); t=load('tip'); real=[]; noise=[]; same=0
for tag in sorted(set(b)&set(t), key=lambda k:t[k][0]):
    nb,nt=nodes(b[tag][1]),nodes(t[tag][1])
    if [(a,c) for a,c,_,_ in nb]==[(a,c) for a,c,_,_ in nt]: same+=1; continue
    # anchor offset: first label (excluding nav) with unique occurrence in both
    cb={}; ct={}
    for a,c,y0,y1 in nb: cb.setdefault(a,[]).append(y0)
    for a,c,y0,y1 in nt: ct.setdefault(a,[]).append(y0)
    off=None
    for a,ys in cb.items():
        if a in NAV or a not in ct or len(ys)!=1 or len(ct[a])!=1: continue
        if ys[0]>360 and ct[a][0]>360: off=ys[0]-ct[a][0]; break
    sb=set((a,c) for a,c,_,_ in nb); st=set((a,c) for a,c,_,_ in nt)
    # visible-window-aware: drop labels that sit within 12px of the viewport top/bottom edge in either snapshot (partially clipped rows)
    def inner(N): return set((a,c) for a,c,y0,y1 in N if y0>=360 and y1<=2380) | set((a,c) for a,c,y0,y1 in N if a in NAV)
    ib,it=inner(nb),inner(nt)
    d_only_b=ib-st; d_only_t=it-sb   # labels fully inside one view that are absent from the other view altogether
    if off is not None and abs(off)<=6:
        (real if (d_only_b or d_only_t) else noise).append((tag,off,sorted(d_only_b),sorted(d_only_t)))
    else:
        noise.append((tag,off,sorted(d_only_b),sorted(d_only_t)))
print(f"identical label+flag lists: {same}; differing: {len(real)+len(noise)} (scroll-offset-or-edge noise: {len(noise)}; REAL same-offset diffs: {len(real)})")
for tag,off,x,y in real: print("REAL",tag,"off",off,"base-only",x[:6],"tip-only",y[:6])
if '-v' in sys.argv:
    for tag,off,x,y in noise: print("noise",tag,"off",off,"base-only",[l[:30] for l in x][:3],"tip-only",[l[:30] for l in y][:3])
