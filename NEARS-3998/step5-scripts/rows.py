#!/usr/bin/env python3
"""rows.py [tap-edit|tap-label <substr> [n]|state]: one uiautomator dump; labels from the dump only, taps computed from node bounds (no stored coordinates).
state -> one line per labelled node (label | enabled | clickable) + SUMMARY line (suggestion-row badge counts, hint, snackbar-ish)."""
import subprocess,sys,re,xml.etree.ElementTree as ET
ser='emulator-5556'
def dump():
    for _ in range(5):
        subprocess.run(['adb','-s',ser,'shell','uiautomator','dump','/sdcard/uis5.xml'],capture_output=True)
        x=subprocess.run(['adb','-s',ser,'exec-out','cat','/sdcard/uis5.xml'],capture_output=True,text=True).stdout
        if '<node' in x: return x
    return ''
def nodes():
    x=dump(); r=ET.fromstring(x) if x else None
    out=[]
    if r is None: return out
    for n in r.iter('node'):
        b=re.findall(r'\d+',n.get('bounds',''))
        lab=(n.get('content-desc') or n.get('text') or '').replace('\n',' / ')
        out.append(dict(lab=lab,cls=n.get('class',''),en=n.get('enabled'),clk=n.get('clickable'),b=tuple(map(int,b)) if len(b)==4 else None))
    return out
def tap(b): subprocess.run(['adb','-s',ser,'shell','input','tap',str((b[0]+b[2])//2),str((b[1]+b[3])//2)])
BAD=('Checking availability','Available','Not available yet')
CHROME={'Confirm Location','Confirm your location','Google Map','Move the map to place the pin','Use my current location','Zoom in','Zoom out','Search Location'}
def state(ns):
    lines=[];sm=dict(pending=0,available=0,not_available=0,plain=0,hint=0,edit_texts=0)
    for n in ns:
        lab=n['lab']
        if not lab: continue
        if n['cls'].endswith('EditText'):
            sm['edit_texts']+=1; lab='<SEARCH-FIELD>'
        elif lab.endswith('Checking availability…') or lab.endswith('Checking availability...'): sm['pending']+=1
        elif lab.endswith(', Available'): sm['available']+=1
        elif lab.endswith(', Not available yet'): sm['not_available']+=1
        elif 'no service in these' in lab.lower(): sm['hint']+=1
        elif lab not in CHROME: sm['plain']+=1
        lines.append('%s | enabled=%s | clickable=%s'%(lab,n['en'],n['clk']))
    return lines,sm
if __name__=='__main__':
    cmd=sys.argv[1] if len(sys.argv)>1 else 'state'
    ns=nodes()
    if cmd=='tap-edit':
        e=[n for n in ns if n['cls'].endswith('EditText') and n['b']]
        if not e: print('NOEDIT'); sys.exit(1)
        k=int(sys.argv[2]) if len(sys.argv)>2 else 1
        if len(e)<k: print('NOEDIT',k,len(e)); sys.exit(1)
        tap(e[k-1]['b']); print('tapped edit',k,'of',len(e)); sys.exit(0)
    if cmd=='tap-label':
        sub=sys.argv[2]; k=int(sys.argv[3]) if len(sys.argv)>3 else 1
        m=[n for n in ns if sub in n['lab'] and n['b'] and not n['cls'].endswith('EditText')]
        if len(m)<k: print('NOTFOUND',sub,len(m)); sys.exit(1)
        tap(m[k-1]['b']); print('tapped',sub,k,'of',len(m)); sys.exit(0)
    lines,sm=state(ns)
    print('\n'.join(lines))
    print('SUMMARY '+' '.join('%s=%s'%kv for kv in sm.items()))
