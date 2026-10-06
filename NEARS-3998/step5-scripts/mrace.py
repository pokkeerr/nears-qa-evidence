import re,glob,os,collections
S='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa/walk/'
rows=[]
for f in sorted(glob.glob(S+'*M[01]i*_logcat.txt')):
    tag=os.path.basename(f)[:-len('_logcat.txt')]
    L=open(f,errors='replace').read().splitlines(); on=False; c=collections.Counter(); skipped=0; started=0
    for ln in L:
        if re.search(r'I QAWALK\s*: %s__CONFIRM_TO_HOME__start'%tag,ln): on=True; continue
        if re.search(r'I QAWALK\s*: %s__CONFIRM_TO_HOME__end'%tag,ln): on=False
        if on:
            if 'home load skipped: already loading' in ln: skipped+=1
            if 'msg="home load started"' in ln: started+=1
            m=re.search(r'\[NET\] GET endpoint=\S*/(module|home/all|banners|all|basic)\b',ln)
            if m: c[m.group(1)]+=1
    rows.append((tag,started,skipped,dict(c)))
for r in rows: print('%-14s home-load-started=%d skipped=%d  %s'%r)
