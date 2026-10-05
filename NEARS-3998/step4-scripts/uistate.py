#!/usr/bin/env python3
"""uistate.py -> prints one normalized line per labelled node: label | enabled | clickable. Used for state-by-state compare."""
import subprocess,sys,re,xml.etree.ElementTree as ET
ser='emulator-5554'
def dump():
    for _ in range(4):
        subprocess.run(['adb','-s',ser,'shell','uiautomator','dump','/sdcard/uis.xml'],capture_output=True)
        x=subprocess.run(['adb','-s',ser,'exec-out','cat','/sdcard/uis.xml'],capture_output=True,text=True).stdout
        if '<node' in x: return x
    return ''
x=dump()
root=ET.fromstring(x) if x else None
out=[]
if root is not None:
    for n in root.iter('node'):
        lab=(n.get('content-desc') or n.get('text') or '').replace('\n',' / ')
        if lab:
            if n.get('class','').endswith('EditText') and ('Emirates' in lab or 'Bangladesh' in lab or 'Dhaka' in lab): lab='<ADDRESS-FIELD>'
            elif ('United Arab Emirates' in lab or 'Bangladesh' in lab) and len(lab)>40 and ' / ' not in lab: lab='<ADDRESS>'
            out.append(f"{lab} | enabled={n.get('enabled')} | clickable={n.get('clickable')}")
print('\n'.join(out))
