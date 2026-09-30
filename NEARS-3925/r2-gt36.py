from h import *
setting('cross_module_basket','0')
m=json.load(open('mix36.json')); bad=0
for r in m:
    lines=[tuple(x) for x in r['lines']]
    clear(); seed(lines,2)
    st,tr=call('POST','/customer/order/get-Tax',dict(COMMON,store_id=39,order_amount=r['P']),module=2)
    D=dq(round(tr['total_discount'],4)); tot=q2(dq(r['P'])-q2(D)+dq(str(tr['tax_amount']))+dq(r['dlv']))
    r['gt_full']=dict(tr,preview_total=float(tot)); ok=abs(float(tot)-r['chg'])<0.0049; bad+= (not ok)
    print(r['lines'],'disc',round(tr['total_discount'],4),'sd',tr.get('store_discount_amount'),'tax',tr['tax_amount'],'preview total',float(tot),'charged',r['chg'],ok)
clear(); json.dump(m,open('mix36.json','w'),indent=1,default=str); print('preview!=charged:',bad)
