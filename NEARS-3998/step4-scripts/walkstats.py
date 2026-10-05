#!/usr/bin/env python3
import re,sys,json,collections
S='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa'
PAT={'FAIL':r'\[FAIL\]','ERR':r'\[ERR\]','inZone':r'location: inZone=','ttl':r'short-TTL coord cache','getfind':r'Get\.find|GetX.*not found|"[A-Za-z]+" not found','unhandled':r'Unhandled Exception|EXCEPTION CAUGHT|Another exception'}
def norm(msg):
    msg=re.sub(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b','<uuid>',msg)
    msg=re.sub(r'\b\d{4}-\d\d-\d\d[T ][\d:.]+Z?','<ts>',msg)
    msg=re.sub(r'\b\d+ ?ms\b','<n>ms',msg)
    return msg.strip()
def load(build):
    steps=collections.OrderedDict(); cur=None
    for line in open(f'{S}/walk/{build}_logcat.txt',errors='replace'):
        m=re.search(r'QAWALK\s*:\s*'+build+r'__(\w+?)__(start|end)',line)
        if m:
            if m.group(2)=='start': cur=m.group(1); steps.setdefault(cur,[])
            else: cur=None
            continue
        if cur is None: continue
        m=re.search(r' [VDIWEF] flutter\s*:\s*(.*)$',line)
        if not m: continue
        msg=m.group(1)
        if re.match(r'^#\d+ |^\s+#\d+|^<asynchronous|^\(package:|^package:',msg): continue
        steps[cur].append(norm(msg))
    return steps
def stats(lines):
    c={k:sum(1 for l in lines if re.search(p,l)) for k,p in PAT.items()}
    return c
if __name__=='__main__':
    out={}
    for b in sys.argv[1:]:
        st=load(b); out[b]={k:{'counts':stats(v),'lines':v} for k,v in st.items()}
    json.dump(out,open(S+'/walk/walkstats.json','w'),indent=1)
    steps=list(dict.fromkeys(k for b in out for k in out[b]))
    print('%-34s'%'step', *['%-34s'%b for b in out])
    for k in steps:
        row=[]
        for b in out:
            c=out[b].get(k,{}).get('counts')
            row.append('%-34s'%(' '.join(f'{n}={v}' for n,v in c.items() if v) or ('clean' if c is not None else '-')) if c is not None else '%-34s'%'-')
        print('%-34s'%k,*row)
