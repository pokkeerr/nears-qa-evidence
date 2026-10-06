#!/usr/bin/env python3
"""cmpwalk.py <baseTag> <tipTag> : per window compare (a) uifind state dumps line by line (b) winstats summary (requests/responses/FAIL set/INFO/EVENT keys+values minus ids). Prints EQUAL/DIFF per window."""
import sys,re,os,subprocess,glob,collections,difflib
S='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa'
b,t=sys.argv[1],sys.argv[2]
def states(tag):
    d={}
    for f in sorted(glob.glob('%s/walk/%s_*_state.txt'%(S,tag))):
        w=os.path.basename(f)[len(tag)+1:-len('_state.txt')]
        d[w]=[l.rstrip() for l in open(f) if l.strip()]
    return d
def stats(tag):
    out=subprocess.run(['python3',S+'/winstats.py','%s/walk/%s_logcat.txt'%(S,tag),tag],capture_output=True,text=True).stdout
    d=collections.OrderedDict();cur=None
    for l in out.splitlines():
        if l.startswith('## '): cur=l[3:]; d[cur]=[]
        elif cur: d[cur].append(re.sub(r'place_id: [A-Za-z0-9_-]+,? ?','',re.sub(r'correlation_id=\S+','',l)))
    return d
bs,ts=states(b),states(t); bst,tst=stats(b),stats(t)
allw=list(dict.fromkeys(list(bst)+list(tst)))
neq=0
for w in allw:
    s1=bs.get(w);s2=ts.get(w)
    # state dumps: drop volatile address-chip / counters? keep strict, report diff count
    ui='n/a' if s1 is None or s2 is None else ('EQUAL' if s1==s2 else 'DIFF(%d lines)'%sum(1 for l in difflib.unified_diff(s1,s2,lineterm='',n=0) if l[:1] in '+-' and l[:3] not in ('+++','---')))
    nt='EQUAL' if bst.get(w)==tst.get(w) else 'DIFF'
    if nt=='DIFF' or ui.startswith('DIFF'): neq+=1
    print('%-34s uifind-dump: %-14s wire/log/event: %s'%(w,ui,nt))
    if nt=='DIFF':
        for l in difflib.unified_diff(bst.get(w,[]),tst.get(w,[]),lineterm='',n=0,fromfile=b,tofile=t): print('     ',l[:200])
    if ui.startswith('DIFF'):
        for l in difflib.unified_diff(s1,s2,lineterm='',n=0,fromfile=b,tofile=t): 
            if l[:1] in '+-' and l[:3] not in ('+++','---'): print('     ',l[:200])
print('windows with a difference:',neq)
