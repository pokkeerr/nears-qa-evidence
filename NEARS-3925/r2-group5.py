from h import *
import sys
def model_store(lines):
    P=sum(dq(item(i)['price'])*q for i,q in lines)
    rawD=sum((dq(item(i)['price'])*dq(item(i)['fpct'])/dq(100)*q for i,q in lines if item(i)['fpct'] is not None),Dm(0))
    D=q2(rawD)
    return P,rawD,D
def run(name,baskets,flag,stores_dlv=None):
    setting('cross_module_basket',flag)
    clear()
    mods={}
    for store,module,lines in baskets:
        mods.setdefault(module,[]).extend(lines)
    for module,lines in mods.items(): seed(lines,module)
    stores=[{'store_id':s,'distance':(3.0042 if s==12 else 3),'dm_tips':0} for s,_,_ in baskets]
    body=dict(COMMON,stores=stores)
    hdr=baskets[0][1]
    sv,v=call('POST','/customer/order/group/validate',body,module=hdr)
    sp,p=call('POST','/customer/order/group/place',body,module=hdr)
    res=dict(name=name,flag=flag,validate_status=sv,valid=v.get('valid') if isinstance(v,dict) else None,place_status=sp)
    if sv==200 and v.get('valid') and 'amounts' in v:
        res['validate_total']=v['amounts']['order_amount']; res['validate_disc']=v['amounts']['discount_amount']
        res['validate_children']={c['store_id']:(c['amounts']['order_amount'],c['amounts']['discount_amount']) for c in v['stores']}
    else: res['validate_body']=v if not v.get('valid') else 'valid, no amounts key (single-module group)'
    if sp==200 and p.get('group_placed'):
        gid=p['group_id']; res['place_total']=p['total_amount']
        ch=sql("select id,store_id,order_amount,delivery_charge,total_tax_amount,flash_admin_discount_amount,flash_store_discount_amount from orders where order_group_id='%s' order by id"%gid,True)
        res['children']=[dict(id=int(c[0]),store=int(c[1]),amt=float(c[2]),dlv=float(c[3]),tax=float(c[4]),fa=float(c[5]),fv=float(c[6])) for c in ch]
        res['sum_children']=round(sum(c['amt'] for c in res['children']),2)
        # independent client model per store
        mt=Dm(0); per={}
        for store,module,lines in baskets:
            P,rawD,D=model_store(lines)
            dl=[c['dlv'] for c in res['children'] if c['store']==store][0]
            sh=q2(P-D+(P-D)*Dm('0.05')+dq(dl)); base=q2(P-rawD+(P-rawD)*Dm('0.05')+dq(dl))
            per[store]=dict(shown=float(sh),base=float(base),D=float(D),rawD=float(rawD))
            mt+=sh
        res['model']=per; res['shown_group_total']=float(mt)
        res['base_group_total']=float(sum(dq(x['base']) for x in per.values()))
    else: res['place_body']=p
    return res
CASES={
 'G5 ticket shape 388+390 @39 + 196+198+199 @12 (child 69.13)':[(39,2,[(388,1),(390,1)]),(12,1,[(196,1),(198,1),(199,1)])],
}
out=[]
for flag in sys.argv[1:]:
    for n,b in CASES.items():
        r=run(n,b,flag); out.append(r)
        print(json.dumps({k:v for k,v in r.items() if k not in('validate_body',)},default=str)[:1500]); print()
json.dump(out,open('group5_%s.json'%'_'.join(sys.argv[1:]),'w'),indent=1,default=str)
