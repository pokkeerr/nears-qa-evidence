import sys; sys.path.insert(0,'.')
from api import *
R=[]
def chk(name, ok, detail=''):
    R.append((name, ok)); print(('PASS ' if ok else 'FAIL ')+name+(' | '+str(detail) if detail else ''))
def dg(nm,ep,**p):
    p.setdefault('limit',200); p.setdefault('offset',1); p['token']=TOK[nm]
    return get(nm,ep,p)
for nm in ('D1','D2','D5','D6'):
    for typ,ep in (('current','delivery-man/current-orders'),('history','delivery-man/all-orders')):
        s,j,h=dg(nm,ep,with_filters=1)
        s2,cnt,_=dg(nm,'delivery-man/orders-count',type=typ)
        cm={c['key']:c['count'] for c in cnt}
        fb=j.get('filters'); 
        os_=dict((v,c) for v,c,_ in opts(fb,'status'))
        exp={k:v for k,v in cm.items() if k!='all' and v>0}
        print(nm,typ,s,'total',j['total_size'],'opts',os_,'count',exp)
        chk(f'{nm} {typ} option counts == orders-count (nonzero)', os_==exp, (os_,exp))
        chk(f'{nm} {typ} sum options == total_size == all', sum(os_.values())==j['total_size']==cm.get('all',j['total_size']), (sum(os_.values()),j['total_size'],cm.get('all')))
        chk(f'{nm} {typ} zero-count status not offered', all(c>0 for c in os_.values()))
        # per status selection
        for st,c in os_.items():
            s3,j3,h=dg(nm,ep,with_filters=1,order_status=st)
            ok = j3['total_size']==c and all(o['order_status']==st for o in j3['orders'])
            chk(f'{nm} {typ} order_status={st} -> {c}', ok, j3['total_size'])
            # counts ignore own selection
            os3=dict((v,cc) for v,cc,_ in opts(j3['filters'],'status'))
            if os3!=os_: chk(f'{nm} {typ} counts ignore own selection ({st})', False, (os3,os_))
        # unflagged keyset
        s4,ju,h=dg(nm,ep)
        chk(f'{nm} {typ} unflagged keyset', set(ju.keys())=={'total_size','limit','offset','orders'}, sorted(ju.keys()))
        if typ=='current': print(' item keys', [i['key'] for i in fb['items']], 'applied', fb['applied'], 'sort', fb.get('sort'))
# pools per principal
for nm in ('D1','D5','D2','D6'):
    s,j,h=dg(nm,'delivery-man/latest-orders',with_filters=1)
    fb=j.get('filters'); 
    print(nm,'latest',s,j['total_size'], 'pm',opts(fb,'payment_method') if fb else None,'ot',opts(fb,'order_type') if fb else None,'items',[i['key'] for i in fb['items']] if fb else None)
    s2,ju,h=dg(nm,'delivery-man/latest-orders'); chk(f'{nm} latest unflagged keyset', set(ju.keys())=={'total_size','limit','offset','orders'}, sorted(ju.keys()))
    chk(f'{nm} latest flagged total == unflagged total', ju['total_size']==j['total_size'], (ju['total_size'],j['total_size']))
    if fb:
      for k in ('payment_method','order_type'):
        chk(f'{nm} latest sum({k})==total', sum(c for _,c,_ in opts(fb,k))==j['total_size'], opts(fb,k))
        for v,c,_ in opts(fb,k):
            s3,j3,h=dg(nm,'delivery-man/latest-orders',with_filters=1,**{k:v})
            chk(f'{nm} latest {k}={v} -> {c}', j3['total_size']==c, j3['total_size'])
print('FAILS:',[n for n,o in R if not o])
