#!/usr/bin/env python3
"""crosscheck.py <tag...> : per window, search/place-details/get-zone-id counts from (a) the app [NET] GET lines (logcat) and (b) the logging proxy in front of the backend (marker-delimited). Prints a table row per window and OK/MISMATCH."""
import sys,re,json,collections
S='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa'
KEYS=('place-api-autocomplete','place-api-details','get-zone-id')
prox=[json.loads(l) for l in open(S+'/proxy_access.jsonl') if l.strip()]
def pwin(tag):
    d=collections.OrderedDict();cur=None
    for r in prox:
        if 'marker' in r:
            m=re.match(re.escape(tag)+r'__(.+)__(start|end)$',r['marker'])
            if m:
                if m.group(2)=='start': cur=m.group(1); d.setdefault(cur,collections.Counter())
                else: cur=None
            continue
        if cur and r['path'].split('/')[-1] in KEYS: d[cur][(r['path'].split('/')[-1],r['status'],bool(r.get('cached')))]+=1
    return d
def awin(tag):
    L=open('%s/walk/%s_logcat.txt'%(S,tag),errors='replace').read().splitlines()
    d=collections.OrderedDict();cur=None
    for ln in L:
        m=re.search(r'I QAWALK\s*: '+re.escape(tag)+r'__(\S+?)__(start|end)',ln)
        if m:
            if m.group(2)=='start': cur=m.group(1); d.setdefault(cur,collections.Counter())
            else: cur=None
            continue
        if cur:
            m=re.search(r'\[NET\] GET endpoint=\S*/(place-api-autocomplete|place-api-details|get-zone-id)\b',ln)
            if m: d[cur][m.group(1)]+=1
    return d
bad=0
for tag in sys.argv[1:]:
    a,p=awin(tag),pwin(tag)
    for w in a:
        ap={k:a[w][k] for k in KEYS if a[w][k]}
        pp=collections.Counter()
        for (k,st,c),n in p.get(w,{}).items(): pp[k]+=n
        pp={k:pp[k] for k in KEYS if pp[k]}
        # window-edge tolerance: proxy sees a request when it arrives, app logs when it sends; compare exactly and flag
        ok=ap==pp; bad+= (not ok)
        st=collections.Counter()
        for (k,s,c),n in p.get(w,{}).items(): st['%s:%s'%(k.split('-')[-1] if k!='get-zone-id' else 'zone',s)]+=n
        print('%-8s %-30s app-[NET] %-62s proxy(backend-side) %-62s %s'%(tag,w,ap,pp,'OK' if ok else 'MISMATCH'))
print('mismatching windows:',bad)
