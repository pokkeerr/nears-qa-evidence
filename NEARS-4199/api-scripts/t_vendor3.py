import sys; sys.path.insert(0,'.')
from api import *
import datetime
R=[]
def chk(name, ok, detail=''):
    R.append((name, ok)); print(('PASS ' if ok else 'FAIL ')+name+(' | '+str(detail) if detail else ''))
def full(nm, ep, **p):
    p.setdefault('limit',200); p.setdefault('offset',1); p.setdefault('with_filters',1)
    return get(nm, ep, p)
# isolation
r={}
for nm in ('V1','V26','V4','E1','E26'):
    for ep in ('vendor/current-orders','vendor/completed-orders','vendor/canceled-orders'):
        s,j,h=full(nm,ep); r[(nm,ep)]=(s,j)
        print(nm,ep,s,j.get('total_size'), (min(ids(j)),max(ids(j))) if j.get('orders') else None, [ (k,sum(c for _,c,_ in opts(j['filters'],k))) for k in ('status','payment_method')] if 'filters' in j else '')
for ep in ('vendor/current-orders','vendor/completed-orders','vendor/canceled-orders'):
    chk('employee1 == owner1 rows+counts '+ep, ids(r[('E1',ep)][1])==ids(r[('V1',ep)][1]) and r[('E1',ep)][1]['filters']['items']==r[('V1',ep)][1]['filters']['items'])
    chk('employee26 == owner26 '+ep, ids(r[('E26',ep)][1])==ids(r[('V26',ep)][1]) and r[('E26',ep)][1]['filters']['items']==r[('V26',ep)][1]['filters']['items'])
    a=set(ids(r[('V1',ep)][1])); b=set(ids(r[('V26',ep)][1])); c=set(ids(r[('V4',ep)][1]))
    chk('disjoint V1/V26/V4 '+ep, not(a&b) and not(a&c) and not(b&c), (len(a),len(b),len(c)))
# other vendor's order not leaked via search by id
s,j,h=full('V26','vendor/current-orders',search='91420'); chk('V26 search other vendor id -> 0', j['total_size']==0, j['total_size'])
# V4 food module fixtures
s,j,h=full('V4','vendor/current-orders'); print('V4 status', opts(j['filters'],'status'), [ (v['names']['en'] ) for v in items(j['filters'])['status']['options']], ids(j))
# V26
s,j,h=full('V26','vendor/current-orders'); print('V26 status', opts(j['filters'],'status'), 'camp', opts(j['filters'],'campaign_only'))
s,j,h=full('V26','vendor/current-orders',campaign_only='1'); print('V26 camp ids', sorted(ids(j)))
chk('V26 campaign ids', sorted(ids(j))==[91442,91445])
# history
s,jh,h=full('V1','vendor/completed-orders'); fbh=jh['filters']
print('V1 history', jh['total_size'], opts(fbh,'status'), [i for i in items(fbh)])
chk('history status sum==total', sum(c for _,c,_ in opts(fbh,'status'))==jh['total_size'])
chk('history includes canceled option', any(v=='canceled' for v,_,_ in opts(fbh,'status')))
for v,c,_ in opts(fbh,'status'):
    s,jj,h=full('V1','vendor/completed-orders',status=v)
    chk(f'history status={v} count==list', jj['total_size']==c==len(jj['orders']) and all(o['order_status']==v for o in jj['orders']), (c,jj['total_size']))
s,jc,h=full('V1','vendor/canceled-orders'); print('canceled', jc['total_size'], [i for i in items(jc['filters'])], 'status item?', 'status' in items(jc['filters']))
chk('canceled: only canceled rows', all(o['order_status']=='canceled' for o in jc['orders']))
chk('canceled: no status filter', 'status' not in items(jc['filters']))
chk('history canceled count == canceled view', dict((v,c) for v,c,_ in opts(fbh,'status')).get('canceled')==jc['total_size'])
# 403 behaviours
s,j,h=get('V1','vendor/completed-orders',{'limit':100,'offset':1,'status':'canceled'}); chk('unflagged completed status=canceled -> 403', s==403, (s,str(j)[:150]))
s,j,h=get('V1','vendor/completed-orders',{'limit':100,'offset':1,'status':'all'}); chk('unflagged status=all -> 200', s==200, (s,j.get('total_size')))
s,j2,h=get('V1','vendor/completed-orders',{'limit':100,'offset':1,'status':'delivered'}); print('unflagged delivered',s,j2.get('total_size'))
s,j3,h=get('V1','vendor/completed-orders',{'limit':100,'offset':1,'status':'refunded'}); print('unflagged refunded',s,j3.get('total_size'))
s,j4,h=get('V1','vendor/completed-orders',{'limit':100,'offset':1,'status':'bogus'}); print('unflagged bogus',s,str(j4)[:100])
s,j5,h=full('V1','vendor/completed-orders',status='all'); chk('flagged status=all History -> 200 all 7 terminal', s==200 and j5['total_size']==jh['total_size'], (s,j5.get('total_size')))
s,j6,h=full('V1','vendor/completed-orders',status='canceled'); chk('flagged status=canceled -> 200', s==200, (s,j6.get('total_size')))
# unflagged completed keys
chk('unflagged completed key set', set(j.keys())=={'total_size','limit','offset','orders'} if isinstance(j,dict) and s==200 else True)
s,jj,h=get('V1','vendor/completed-orders',{'limit':100,'offset':1,'status':'all'}); chk('unflagged status=all keyset', set(jj.keys())=={'total_size','limit','offset','orders'}, sorted(jj.keys()))
s,jj,h=get('V1','vendor/canceled-orders',{'limit':100,'offset':1}); chk('unflagged canceled keyset', set(jj.keys())=={'total_size','limit','offset','orders'}, sorted(jj.keys()))
# paging stability over equal timestamps
def page_all(nm,ep,lim,**q):
    out=[]; off=1
    while True:
        s,j,h=get(nm,ep,{'limit':lim,'offset':off,'with_filters':1,**q})
        if not j['orders']: break
        out+=ids(j); off+=1
        if len(out)>=j['total_size'] or off>50: break
    return out
for nm,ep,q,eq in (('V1','vendor/current-orders',{'status':'handover'},[91439,91440,91441]),('V26','vendor/completed-orders',{'status':'delivered'},[91450,91451,91452])):
    s,jfull,h=full(nm,ep,**q); fullids=ids(jfull)
    for lim in (1,2):
        pg=page_all(nm,ep,lim,**q)
        chk(f'paging {nm} {ep} lim={lim} stable no dup/miss', pg==fullids and len(set(pg))==len(pg), (pg,fullids))
    print(' tie rows order', [i for i in fullids if i in eq])
# V1 unflagged canceled paging
print('FAILS:',[n for n,o in R if not o])
