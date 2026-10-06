import re,glob,collections
def stats(var):
    plus=[];minus=[];ups=[]
    n=0
    for f in sorted(glob.glob(f"evidence/walk-{var}/burst2-run*.txt")):
        for l in open(f):
            m=re.match(r'r(\d+) start=(\w+) after\+5=(\w+) updates=(\d+) after-5=(\w+) updates=(\d+) removes=(\d+)',l)
            if not m: continue
            s,p,mm=m.group(2),m.group(3),m.group(5)
            n+=1
            if s.isdigit() and p.isdigit(): plus.append(int(p)-int(s))
            if p.isdigit() and mm.isdigit(): minus.append(int(p)-int(mm))
            elif p.isdigit() and mm=='NOROW': minus.append(int(p))  # removed: all decrements landed (qty -> 0)
            ups.append((int(m.group(4)),int(m.group(6)),int(m.group(7))))
    return n,collections.Counter(plus),collections.Counter(minus),collections.Counter(ups)
for v in ('base','tip'):
    n,pl,mi,up=stats(v)
    print(v,"bursts(rounds)",n,"| +5 burst deltas",dict(sorted(pl.items())),"| -5 burst deltas",dict(sorted(mi.items())))
    print("   updates/removes per round (plus-updates, minus-updates, removes):",dict(up))
