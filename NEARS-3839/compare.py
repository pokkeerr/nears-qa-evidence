import json,sys,subprocess
from decimal import Decimal as D, ROUND_HALF_UP
v=json.load(open(sys.argv[1])); pl=json.load(open(sys.argv[2])); p=int(sys.argv[3]) if len(sys.argv)>3 else 2
q=D(1).scaleb(-p)
gid=pl['group_id']
cols="store_id,order_amount,delivery_charge,dm_tips,total_tax_amount,extra_packaging_amount,additional_charge,store_discount_amount,flash_admin_discount_amount,flash_store_discount_amount,coupon_discount_amount,ref_bonus_amount,coupon_code"
out=subprocess.run(['mysql','-u','root','-N','-r','nears3839_qa','-e',f"SELECT {cols} FROM orders WHERE order_group_id='{gid}' ORDER BY id"],capture_output=True,text=True).stdout
names=cols.split(',')
rows={}
print('persisted children (group',gid+'):')
for line in out.strip().split('\n'):
    r=dict(zip(names,line.split('\t'))); rows[int(r['store_id'])]=r; print('  ',r)
ok=True
def dec(x): return D(repr(x)) if isinstance(x,float) else D(str(x))
def rd(x): return dec(x).quantize(q,rounding=ROUND_HALF_UP)
for s in v['stores']:
    sid=s['store_id']; a=s['amounts']; r=rows.get(sid)
    if r is None: print('store',sid,'NOT PLACED'); ok=False; continue
    disc=sum(rd(r[k]) for k in ['store_discount_amount','flash_admin_discount_amount','flash_store_discount_amount','coupon_discount_amount','ref_bonus_amount'])
    exp={'order_amount':dec(r['order_amount']),'delivery_charge':rd(r['delivery_charge']),'dm_tips':rd(r['dm_tips']),'total_tax_amount':rd(r['total_tax_amount']),
         'extra_packaging_amount':rd(r['extra_packaging_amount']),'additional_charge':rd(r['additional_charge']),'discount_amount':disc}
    for k,e in exp.items():
        got=dec(a[k])
        flag='==' if got==e else '!='
        if got!=e: ok=False
        if k=='order_amount' or got!=e: print(f'  store {sid} {k}: validate {a[k]} {flag} persisted {e}')
tot=dec(pl['total_amount'])
print('  TOP validate amounts.order_amount',v['amounts']['order_amount'],'==' if dec(v['amounts']['order_amount'])==tot else '!=','place total_amount',pl['total_amount'])
if dec(v['amounts']['order_amount'])!=tot: ok=False
print('RESULT','OK' if ok else 'FAIL')
