#!/usr/bin/env python3
"""Swipe basket row N (label-resolved) left; VERIFY the reveal (row's own 'Remove <name>' moved left
of its closed x) before tapping the single unlabeled clickable Button inside the row's right half.
Usage: swipe2.py <row#> [prefix]"""
import re, subprocess, sys, time
SER='emulator-5600'
row=int(sys.argv[1]); pref=sys.argv[2] if len(sys.argv)>2 else 'Tones Mild Chili Powder'
def dump():
    for _ in range(6):
        subprocess.run(['adb','-s',SER,'shell','uiautomator','dump','/sdcard/qa3977s2.xml'],capture_output=True)
        x=subprocess.run(['adb','-s',SER,'exec-out','cat','/sdcard/qa3977s2.xml'],capture_output=True,text=True).stdout
        if x.startswith('<?xml'): return x
        time.sleep(1.5)
    sys.exit('DUMP FAILED')
def nodes(x):
    for n in re.findall(r'<node [^>]*>',x):
        yield (re.search(r'content-desc="([^"]*)"',n).group(1).replace('&#10;',' | '),
               tuple(map(int,re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',n).groups())),
               re.search(r'class="([^"]*)"',n).group(1), re.search(r'clickable="([^"]*)"',n).group(1))
def state():
    ns=list(nodes(dump()))
    rows=sorted([n for n in ns if n[0].startswith(pref+' |')],key=lambda n:n[1][1])
    lab,rb,_,_=rows[row-1]
    rem=[n for n in ns if n[0]=='Remove '+pref and n[1][1]>=rb[1]-5 and n[1][3]<=rb[3]+5]
    return ns,lab,rb,rem
ns,lab,rb,rem=state(); closed_x=rem[0][1][0] if rem else None
print('row%d [%s] closed Remove x=%s'%(row,lab[:60],closed_x))
for attempt in range(3):
    x1,y1,x2,y2=rb; y=y1+int(0.2*(y2-y1))
    subprocess.run(['adb','-s',SER,'shell','input','swipe',str(x1+int(0.55*(x2-x1))),str(y),str(x1+int(0.1*(x2-x1))),str(y),'300'])
    time.sleep(2)
    ns,lab,rb2,rem=state()
    if rem and closed_x and rem[0][1][0] < closed_x-100: break
    print('reveal not observed (attempt %d), Remove x=%s'%(attempt+1, rem[0][1][0] if rem else None))
else:
    sys.exit('REVEAL FAILED')
btn=[n for n in ns if n[2]=='android.widget.Button' and n[3]=='true' and not n[0] and n[1][1]>=rb[1]-5 and n[1][3]<=rb[3]+5 and n[1][0]>(rb[0]+rb[2])//2]
if len(btn)!=1: sys.exit('revealed button hits=%d'%len(btn))
b=btn[0][1]; c=((b[0]+b[2])//2,(b[1]+b[3])//2)
print('reveal verified: Remove x %s -> %s; tapping revealed delete Button %s @ %s'%(closed_x,rem[0][1][0],b,c))
subprocess.run(['adb','-s',SER,'shell','input','tap',str(c[0]),str(c[1])])
print('tapped at %sZ'%time.strftime('%H:%M:%S',time.gmtime()))
