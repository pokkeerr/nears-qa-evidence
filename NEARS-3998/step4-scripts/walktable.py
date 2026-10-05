#!/usr/bin/env python3
import sys,re,collections,json
sys.path.insert(0,'/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa')
import walkstats as ws, proxystats as ps
S=ws.S
runs=[('base1','tip1'),('base2','tip2'),('base3','tip3')]
rows=ps.load(); win=ps.windows(rows)
steps=list(ws.load('base1').keys())
def fails(lines): 
    return sorted(collections.Counter(re.sub(r'correlation_id=\S+','',l) for l in lines if '[FAIL]' in l).items())
out=[]
for s in steps:
    b=[];t=[];sb_eq=0;fail_eq=0;ok=0
    for rb,rt in runs:
        A=ws.load(rb); B=ws.load(rt)
        if s not in A or s not in B: continue
        ok+=1
        b.append(ps.zone_counts(win.get((rb,s),[]))[0]); t.append(ps.zone_counts(win.get((rt,s),[]))[0])
        try: sb_eq+= open(f'{S}/walk/{rb}_{s}_state.txt').read()==open(f'{S}/walk/{rt}_{s}_state.txt').read()
        except: pass
        fail_eq+= fails(A[s])==fails(B[s])
    out.append((s,b,t,sb_eq,fail_eq,ok))
print('| step | get-zone-id req base [r1,r2,r3] | tip [r1,r2,r3] | ui state equal | [FAIL] set equal |')
print('|---|---|---|---|---|')
for s,b,t,e,f,ok in out:
    print(f'| {s} | {b} | {t} | {e}/{ok} | {f}/{ok} |')
