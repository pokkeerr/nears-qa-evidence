#!/usr/bin/env python3
import sys,os,collections
S='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa'
def load(*files):
    d={}
    for f in files:
        p=S+'/'+f
        if not os.path.exists(p): continue
        for l in open(p):
            c=l.rstrip('\n').split('\t')
            if len(c)>=3: d[c[0]]=(c[1],c[2])
    return d
tip=load('tip_A.tsv','tip_B.tsv','tip_B2.tsv'); base=load('base_A.tsv','base_B.tsv','base_char.tsv')
def num(x): 
    try: return int(x.lstrip('+'))
    except: return None
rows=sorted(tip)
print('| file | tip rc | tip +N | base rc | base +N | equal |'); print('|---|---|---|---|---|---|')
tt=0;bt=0;eq=0;nb=0;bad=0
for f in rows:
    t=tip[f]; b=base.get(f)
    tt+= num(t[1]) or 0
    if t[0]!='0': bad+=1
    if b:
        nb+=1; bt+=num(b[1]) or 0; e = (b==t); eq+=e
        print(f'| {f.replace("test/","")} | {t[0]} | {t[1]} | {b[0]} | {b[1]} | {"yes" if e else "NO"} |')
    else:
        print(f'| {f.replace("test/","")} | {t[0]} | {t[1]} | - | - | (new file / not run on base) |')
print(f'\nfiles on tip: {len(rows)}, tip total tests {tt}, tip non-zero rc: {bad}; files compared with base: {nb}, equal: {eq}')
