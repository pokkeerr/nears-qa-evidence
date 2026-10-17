import sys; sys.path.insert(0,'.')
from api import *
from collections import defaultdict
R=[]
def chk(name, ok, detail=''):
    R.append((name, ok)); print(('PASS ' if ok else 'FAIL ')+name+(' | '+str(detail) if detail else ''))
def dg(nm,ep,**p):
    p.setdefault('limit',200); p.setdefault('offset',1); p['token']=TOK[nm]
    return get(nm,ep,p)
for lab,qs in (('unknown','order_status=bogus'),('array','order_status[]=pending&order_status[]=accepted'),('negdays','placed_days_min=-1'),('empty','order_status='),('long','order_status='+'x'*500),('wild','order_status=%25'),('search','search=abc'),('sort','sort=zzz'),('pm on running','payment_method=wallet')):
    for ep in ('delivery-man/current-orders','delivery-man/all-orders','delivery-man/latest-orders'):
        s,j,h=get('D1',ep,raw_qs='with_filters=1&limit=200&offset=1&token='+TOK['D1']+'&'+qs)
        chk(f'garbage {lab} {ep.split("/")[1]} 200', s==200, (s,j.get('total_size') if isinstance(j,dict) else j, j.get('filters',{}).get('applied') if isinstance(j,dict) else ''))
# isolation
a={nm:set(ids(dg(nm,'delivery-man/current-orders',with_filters=1)[1])) for nm in ('D1','D2','D5','D6')}
b={nm:set(ids(dg(nm,'delivery-man/all-orders',with_filters=1)[1])) for nm in ('D1','D2','D5','D6')}
for x in a:
    for y in a:
        if x<y: chk(f'disjoint running {x}/{y}', not(a[x]&a[y]))
        if x<y: chk(f'disjoint history {x}/{y}', not(b[x]&b[y]))
# tie paging
def page_all(nm,ep,lim,**q):
    out=[]; off=1
    while True:
        s,j,h=get(nm,ep,{'limit':lim,'offset':off,'with_filters':1,'token':TOK[nm],**q})
        if not j['orders']: break
        out+=[(o['id'],o.get('schedule_at'),o.get('accepted')) for o in j['orders']]; off+=1
        if off>100: break
    return out
for nm,ep in (('D1','delivery-man/current-orders'),('D1','delivery-man/all-orders'),('D2','delivery-man/current-orders'),('D2','delivery-man/all-orders'),('D6','delivery-man/all-orders')):
    s,j,h=dg(nm,ep,with_filters=1); full=[(o['id'],o.get('schedule_at'),o.get('accepted')) for o in j['orders']]
    for lim in (1,2):
        pg=page_all(nm,ep,lim); chk(f'paging {nm} {ep.split("/")[1]} lim={lim}', pg==full and len(set(pg))==len(pg), len(full))
    g=defaultdict(list)
    for i,sa,ac in full: g[(sa,ac)].append(i)
    print('  ties', {k:v for k,v in g.items() if len(v)>1 and k[0] is not None} if True else '')
# status order_status=pending on history -> unknown dropped
s,j,h=dg('D1','delivery-man/all-orders',with_filters=1,order_status='pending'); chk('history order_status=pending (not a history status) dropped -> all 8', j['total_size']==8, j['total_size'])
s,j,h=dg('D1','delivery-man/current-orders',with_filters=1,order_status='delivered'); chk('running order_status=delivered dropped -> all 9', j['total_size']==9, j['total_size'])
# rows within offset 2 have no block
s,j,h=dg('D1','delivery-man/all-orders',with_filters=1,limit=2,offset=2); chk('no block at offset 2', 'filters' not in j)
print('FAILS:',[n for n,o in R if not o])
