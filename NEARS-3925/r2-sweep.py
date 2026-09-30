from h import *
import itertools
setting('cross_module_basket','0')
FLASH=[(390,2),(590,2),(664,3),(615,3),(105,1),(97,1),(101,1)]
rows=[]
def run(lines,module,store,place=True):
    clear(); seed(lines,module)
    it=[item(i) for i,_ in lines]
    P=sum(item(i)['price']*q for i,q in lines)
    rawD,D=client_flash_discount(lines)
    # server previews
    sv,vr=call('POST','/customer/order/group/validate',dict(COMMON,stores=[{'store_id':store,'distance':3,'dm_tips':0}]),module=module)
    amt=vr['stores'][0]['amounts'] if sv==200 and vr.get('stores') else {}
    st,tr=call('POST','/customer/order/get-Tax',dict(COMMON,store_id=store,order_amount=P),module=module)
    deliv=amt.get('delivery_charge',0) or 0
    shown=rd(P-D+(P-D)*0.05+deliv)                # UserApp figure: rounded discount, 5% VAT on the discounted total
    base=rd(P-rawD+(P-rawD)*0.05+deliv)           # pre-fix semantics: raw discount charged
    prev_tax=None
    if st==200: prev_tax=rd(P-tr['total_discount']+tr['tax_amount']+deliv)
    res=dict(lines=lines,store=store,P=round(P,2),rawD=round(rawD,5),D=D,deliv=deliv,shown=shown,base_model=base,
      validate=amt.get('order_amount'),val_disc=amt.get('discount_amount'),gettax_total=prev_tax,gettax_disc=tr.get('total_discount') if st==200 else tr)
    if place:
        s,r=call('POST','/customer/order/place',dict(COMMON,store_id=store,distance=3),module=module)
        res['place_status']=s
        if s==200:
            o=order_row(r['order_id']); res['order_id']=r['order_id']; res['charged']=o['order_amount']
            res['flash_adm']=o['flash_admin_discount_amount']; res['flash_ven']=o['flash_store_discount_amount']
            res['flash_sum']=round(o['flash_admin_discount_amount']+o['flash_store_discount_amount'],3)
            res['line_disc_x_qty']=round(sum(float(d[3])*int(d[1]) for d in details(r['order_id']) if d[4]=='flash_sale'),3)
            res['tax']=o['total_tax_amount']; res['dlv']=o['delivery_charge']
            res['ok_shown_eq_charged']= abs(o['order_amount']-shown)<0.0049
            res['base_delta']=round(o['order_amount']-base,2)
        else: res['place_body']=r
    return res
out=[]
for (iid,mod) in FLASH:
    st=item(iid)['store']
    for q in (1,2,3):
        out.append(run([(iid,q)],mod,st))
json.dump(out,open('sweep.json','w'),indent=1)
for r in out:
    print(r['lines'],'P',r['P'],'rawD',r['rawD'],'D',r['D'],'shown',r['shown'],'base',r['base_model'],'val',r['validate'],'gt',r['gettax_total'],'CHG',r.get('charged'),'dlt',r.get('base_delta'),'ok',r.get('ok_shown_eq_charged'),'flash',r.get('flash_adm'),r.get('flash_ven'),'line',r.get('line_disc_x_qty'),r.get('place_status'))
