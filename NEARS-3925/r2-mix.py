from h import *
import sys
setting('cross_module_basket','0')
def go(name,lines,module,store,coupon=None):
    clear(); seed(lines,module)
    P=sum(dq(item(i)['price'])*q for i,q in lines)
    fR=sum((dq(item(i)['price'])*dq(item(i)['fpct'])/dq(100)*q for i,q in lines if item(i)['fpct'] is not None),Dm(0))
    nR=sum((dq(item(i)['price'])*dq(item(i)['idisc'])/dq(100)*q for i,q in lines if item(i)['fpct'] is None and item(i)['idt']=='percent'),Dm(0))
    extra={'coupon_code':coupon} if coupon else {}
    st,tr=call('POST','/customer/order/get-Tax',dict(COMMON,store_id=store,order_amount=float(P),**extra),module=module)
    s,r=call('POST','/customer/order/place',dict(COMMON,store_id=store,distance=3,**extra),module=module)
    o=order_row(r['order_id']) if s==200 else {}
    dets=details(r['order_id']) if s==200 else []
    res=dict(name=name,lines=lines,P=float(P),fRaw=float(fR),nRaw=float(nR),gettax=tr,place_status=s,order=o,details=dets, place_body=None if s==200 else r)
    dlv=dq(o.get('delivery_charge',0) or 0)
    # models (5% VAT on discounted total)
    cpn=Dm(0)
    if coupon:
        cpn=dq(o.get('coupon_discount_amount',0))
    app=q2((P-q2(fR+nR)-cpn)*Dm('1.05')+dlv)              # app: whole store discount rounded once
    srv_expected=q2((P-q2(fR)-nR-cpn)*Dm('1.05')+dlv)     # fix semantics: flash once + non-flash raw
    base=q2((P-fR-nR-cpn)*Dm('1.05')+dlv)                 # pre-fix: everything raw
    res.update(app_style=float(app),fix_expected=float(srv_expected),base_model=float(base))
    return res
out=[]
C=[('M1 mixed 390x1 + 395x1 (store 39)',[(390,1),(395,1)],2,39,None),
   ('M2 mixed 390x2 + 394x2 (store 39)',[(390,2),(394,2)],2,39,None),
   ('M3 mixed 390x2 + 392x2 (store 39)',[(390,2),(392,2)],2,39,None),
   ('N1 non-flash discount only 395x1',[(395,1)],2,39,None),
   ('N2 plain 388x1',[(388,1)],2,39,None),
   ('N3 plain 388x2 + 395x1 (no flash)',[(388,2),(395,1)],2,39,None),
   ('K1 coupon FOODIE15 + flash 388+390',[(388,1),(390,1)],2,39,'FOODIE15'),
   ('K2 coupon FOODIE15 + flash 390x1',[(390,1)],2,39,'FOODIE15'),
   ('K3 coupon FOODIE15 + flash 390x3',[(390,3)],2,39,'FOODIE15')]
for c in C:
    r=go(*c); out.append(r)
    o=r['order']
    print(r['name'],'| P',r['P'],'fRaw',r['fRaw'],'nRaw',r['nRaw'],'| app',r['app_style'],'fixexp',r['fix_expected'],'base',r['base_model'],'| CHARGED',o.get('order_amount'),'cpn',o.get('coupon_discount_amount'),'sd',o.get('store_discount_amount'),'fl',o.get('flash_admin_discount_amount'),o.get('flash_store_discount_amount'),'dlv',o.get('delivery_charge'),'| gettax disc',r['gettax'].get('total_discount') if isinstance(r['gettax'],dict) else r['gettax'],'tax',r['gettax'].get('tax_amount') if isinstance(r['gettax'],dict) else '', r['place_status'])
json.dump(out,open('mix.json','w'),indent=1,default=str)
