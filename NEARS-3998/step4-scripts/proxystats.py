#!/usr/bin/env python3
import json,sys,re,collections
S='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa'
def load():
    rows=[json.loads(l) for l in open(S+'/proxy_access.jsonl')]
    return rows
def windows(rows):
    res=collections.OrderedDict(); cur=None
    for r in rows:
        if 'marker' in r:
            m=re.match(r'(\w+?)__(\w+?)__(start|end)$',r['marker'])
            if not m: continue
            tag,step,kind=m.groups()
            if kind=='start': cur=(tag,step); res[cur]=[]
            else: cur=None
            continue
        if cur: res[cur].append(r)
    return res
def zone_counts(reqs):
    z=[r for r in reqs if '/config/get-zone-id' in r['path']]
    c=collections.Counter(r['status'] for r in z)
    return len(z), dict(c)
if __name__=='__main__':
    w=windows(load())
    tags=sys.argv[1:] or sorted({k[0] for k in w})
    steps=list(dict.fromkeys(k[1] for k in w))
    print('%-34s'%'step',*['%-14s'%t for t in tags])
    for s in steps:
        row=[]
        for t in tags:
            reqs=w.get((t,s))
            if reqs is None: row.append('%-14s'%'-'); continue
            n,c=zone_counts(reqs)
            row.append('%-14s'%(f'{n} '+','.join(f'{k}x{v}' for k,v in sorted(c.items()))))
        print('%-34s'%s,*row)
