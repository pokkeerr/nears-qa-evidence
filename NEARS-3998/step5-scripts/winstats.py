#!/usr/bin/env python3
"""winstats.py <logcat> <tag> : per marker window -> app [NET] request counts (path -> status multiset), [FAIL] lines (reason set), [INFO] blocked taps, FA events + param keys, ERR/Get.find not found counts. No place ids/coordinates are printed."""
import sys,re,collections
f,tag=sys.argv[1],sys.argv[2]
L=open(f,errors='replace').read().splitlines()
mk=re.compile(r'I QAWALK\s*: '+re.escape(tag)+r'__(\S+?)__(start|end)')
wins=collections.OrderedDict(); cur=None
for ln in L:
    m=mk.search(ln)
    if m:
        name,k=m.groups()
        if k=='start': cur=name; wins.setdefault(name,[])
        else: cur=None
        continue
    if cur and ' flutter ' in ln.replace('  ',' ') or (cur and 'flutter :' in ln) or (cur and 'FA-SVC' in ln):
        wins[cur].append(ln)
def norm(ln): return re.sub(r'^\d\d-\d\d \d\d:\d\d:\d\d\.\d+\s+\d+\s+\d+\s+\w\s+','',ln)
for name,lines in wins.items():
    net=collections.Counter(); fails=[]; infos=[]; events=[]; errs=0; notfound=0
    pend={}
    for ln in lines:
        n=norm(ln)
        m=re.search(r'\[NET\] GET endpoint=(\S+)',n)
        if m: net[('req',m.group(1).split('/')[-1])]+=1
        m=re.search(r'\[NET\] endpoint=(\S+) http_status=(\d+)',n)
        if m: net[('resp',m.group(1).split('/')[-1],m.group(2))]+=1
        if '[FAIL]' in n: fails.append(re.sub(r'correlationId=\S+\s*','',n[n.find('[FAIL]'):])[:170])
        if '[ERR]' in n or 'Unhandled Exception' in n: errs+=1
        if re.search(r'Get\.find.*not found|not found.*Get\.find|"LocationController" not found',n,re.I): notfound+=1
        if 'pick-map suggestion tap blocked' in n: infos.append(n[n.find('pick-map'):][:90])
        m=re.search(r'analytics: (location_search_suggestion\w*) \{(.*)\}',n)
        if m: events.append((m.group(1),m.group(2)))
    reqs={k[1]:v for k,v in net.items() if k[0]=='req'}
    resp={'%s:%s'%(k[1],k[2]):v for k,v in sorted(net.items()) if k[0]=='resp'}
    print('## %s'%name); print('   requests',dict(sorted(reqs.items())),'responses',resp)
    print('   FAIL x%d'%len(fails),' | '.join(sorted(set(fails))) if fails else '')
    for i in infos: print('   INFO',i)
    for e in events: print('   EVENT',e[0],'{'+e[1]+'}')
    print('   ERR',errs,'GetFindNotFound',notfound)
