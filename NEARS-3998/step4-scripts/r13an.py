import sys,re
sys.path.insert(0,'.')
import proxystats as ps
S='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa'
win=ps.windows(ps.load())
def analyse(tag,steps):
    txt=open(f'{S}/walk/{tag}_logcat.txt',errors='replace').read().split('\n')
    res={}
    for s in steps:
        st=None;lines=[]
        for l in txt:
            if re.search(r'QAWALK\s*:\s*'+tag+'__'+s+'__start',l): st=True; lines=[]; continue
            if re.search(r'QAWALK\s*:\s*'+tag+'__'+s+'__end',l): break
            if st and ' flutter : ' in l: lines.append(l.split(' flutter : ',1)[1])
        loads=sum(1 for l in lines if 'home load started' in l); skips=sum(1 for l in lines if 'home load skipped' in l)
        ttl=sum(1 for l in lines if 'short-TTL' in l); fails=sum(1 for l in lines if '[FAIL]' in l)
        zid=ps.zone_counts(win.get((tag,s),[]))[0]
        try: stt=open(f'{S}/walk/{tag}_{s}_state.txt').read()
        except: stt=''
        skel=('Days' in stt and 'Hours' in stt)
        res[s]=(loads,skips,ttl,zid,fails,skel)
    return res
if __name__=='__main__':
    print('step: (home-load-started, skipped, ttl-reuse, get-zone-id req, [FAIL], flash-sale-countdown-placeholder-at-40s)')
    for tag in sys.argv[1:]:
        r=analyse(tag,['d1','m1','d2','m2','d3','m3'])
        print('==',tag,' '.join(f'{s}={v}' for s,v in r.items()))
