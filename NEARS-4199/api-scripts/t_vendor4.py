import sys; sys.path.insert(0,'.')
from api import *
from collections import defaultdict
def page_all(nm,ep,lim,**q):
    out=[]; off=1
    while True:
        s,j,h=get(nm,ep,{'limit':lim,'offset':off,'with_filters':1,**q})
        if not j['orders']: break
        out+=[(o['id'],o['created_at']) for o in j['orders']]; off+=1
        if off>200: break
    return out
for nm,ep in (('V1','vendor/current-orders'),('V1','vendor/completed-orders'),('V1','vendor/canceled-orders'),('V26','vendor/completed-orders'),('V26','vendor/canceled-orders')):
    s,j,h=get(nm,ep,{'limit':200,'offset':1,'with_filters':1}); full=[(o['id'],o['created_at']) for o in j['orders']]
    g=defaultdict(list)
    for i,c in full: g[c].append(i)
    ties={c:v for c,v in g.items() if len(v)>1}
    for lim in (1,3):
        pg=page_all(nm,ep,lim)
        ok = pg==full and len(set(pg))==len(pg)
        print(('PASS' if ok else 'FAIL'), nm, ep, 'lim',lim, 'n',len(full), 'tie-groups', {c[:19]:v for c,v in list(ties.items())[:3]})
    # tie rows id desc?
    print('  ties id-desc:', all(v==sorted(v,reverse=True) for v in ties.values()))
