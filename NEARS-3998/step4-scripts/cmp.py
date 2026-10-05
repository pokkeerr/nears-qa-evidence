#!/usr/bin/env python3
import sys,re,collections,json
sys.path.insert(0,'/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa')
import walkstats as ws
S=ws.S
A,B=sys.argv[1],sys.argv[2]
sa,sb=ws.load(A),ws.load(B)
def key(l):  # drop volatile numbers that are not behaviour
    l=re.sub(r'cold_start_ms: \d+','cold_start_ms: N',l)
    l=re.sub(r'(duration|elapsed|latency)[_a-z]*[:=] ?\d+','\\1=N',l)
    return l
tot_diff=0
for step in sa:
    if step not in sb: print('STEP only in',A,step); continue
    ca=collections.Counter(map(key,sa[step])); cb=collections.Counter(map(key,sb[step]))
    d1=ca-cb; d2=cb-ca
    # state files
    try:
        fa=open(f'{S}/walk/{A}_{step}_state.txt').read(); fb=open(f'{S}/walk/{B}_{step}_state.txt').read()
        stdiff = fa!=fb
    except Exception as e: stdiff=None
    cnt_a=ws.stats(sa[step]); cnt_b=ws.stats(sb[step])
    flag='SAME' if (not d1 and not d2 and not stdiff) else 'DIFF'
    print(f'{step:34s} {flag}  state_equal={not stdiff}  counts {A}:{ {k:v for k,v in cnt_a.items() if v} } {B}:{ {k:v for k,v in cnt_b.items() if v} }')
    for l,n in d1.items(): print(f'     only/more in {A} x{n}: {l[:160]}')
    for l,n in d2.items(): print(f'     only/more in {B} x{n}: {l[:160]}')
