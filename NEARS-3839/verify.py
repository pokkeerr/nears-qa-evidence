import json,sys
from decimal import Decimal as D
p=int(sys.argv[2]) if len(sys.argv)>2 else 2
d=json.load(open(sys.argv[1]))
q=D(1).scaleb(-p)
SK=['order_amount','items_total','delivery_charge','dm_tips','discount_amount','total_tax_amount','extra_packaging_amount','additional_charge']
TK=['order_amount','items_total','delivery_charge','dm_tips','discount_amount']
ok=True
def dec(x): return D(repr(x)) if isinstance(x,float) else D(x)
def chk(a,keys,label):
    global ok
    if list(a.keys())!=keys: print(label,'KEYS MISMATCH',list(a.keys())); ok=False
    for k in keys:
        v=dec(a[k])
        if v!=v.quantize(q): print(label,k,a[k],'NOT at precision',p); ok=False
    lhs=dec(a['items_total'])+dec(a['delivery_charge'])+dec(a['dm_tips'])-dec(a['discount_amount'])
    if lhs!=dec(a['order_amount']): print(label,'IDENTITY FAIL',lhs,a['order_amount']); ok=False
    else: print(label,'identity ok',lhs,'==',a['order_amount'])
for r in d['stores']:
    if r['pass']:
        chk(r['amounts'],SK,'store %s'%r['store_id'])
    else:
        print('store',r['store_id'],'pass false amounts=',r.get('amounts','<absent>'))
        if r.get('amounts','X') is not None: ok=False
if d['valid']:
    chk(d['amounts'],TK,'TOP')
    for k in TK:
        s=sum(dec(r['amounts'][k]) for r in d['stores'])
        if s.quantize(q)!=dec(d['amounts'][k]): print('TOP sum mismatch',k,s,d['amounts'][k]); ok=False
    print('TOP sums == round(sum per store)')
else:
    print('valid false; top amounts=',d.get('amounts','<absent>'))
    if d.get('amounts','X') is not None: ok=False
print('RESULT', 'OK' if ok else 'FAIL')
