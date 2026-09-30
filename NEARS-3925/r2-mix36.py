from h import *
import sys, itertools
setting('cross_module_basket','0')
def raws(lines):
    P=sum((dq(item(i)['price'])*q for i,q in lines),Dm(0))
    fR=sum((dq(item(i)['price'])*dq(item(i)['fpct'])/dq(100)*q for i,q in lines if item(i)['fpct'] is not None),Dm(0))
    nR=sum((dq(item(i)['price'])*dq(item(i)['idisc'])/dq(100)*q for i,q in lines if item(i)['fpct'] is None and item(i)['idt']=='percent'),Dm(0))
    return P,fR,nR
def run(lines,store=39,module=2):
    clear(); seed(lines,module)
    P,fR,nR=raws(lines)
    st,tr=call('POST','/customer/order/get-Tax',dict(COMMON,store_id=store,order_amount=float(P)),module=module)
    s,r=call('POST','/customer/order/place',dict(COMMON,store_id=store,distance=3),module=module)
    o=order_row(r['order_id']) if s==200 else {}
    dlv=dq(o.get('delivery_charge',0) or 0)
    app=q2((P-q2(fR+nR))*Dm('1.05')+dlv)            # W2 == app: whole store discount rounded once
    old=q2((P-q2(fR)-nR)*Dm('1.05')+dlv)            # old rule (flash once, non-flash raw) = previous QA fix build
    base=q2((P-fR-nR)*Dm('1.05')+dlv)               # base: everything raw
    # AC2
    whole=q2(fR+nR); nf=q2(nR)
    ac2a = abs(round((o.get('flash_admin_discount_amount') or 0)+(o.get('flash_store_discount_amount') or 0),4)-float(whole-nf))<1e-9
    ac2b = abs(round((o.get('store_discount_amount') or 0)+(o.get('flash_admin_discount_amount') or 0)+(o.get('flash_store_discount_amount') or 0),4)-float(whole))<1e-9
    gt=None
    if st==200: gt=float(q2(P-dq(tr['total_discount'])+dq(tr['tax_amount'])+dlv))
    return dict(lines=lines,P=float(P),fR=float(fR),nR=float(nR),place=s,oid=r.get('order_id'),chg=o.get('order_amount'),app=float(app),old=float(old),base=float(base),
      sd=o.get('store_discount_amount'),fa=o.get('flash_admin_discount_amount'),fv=o.get('flash_store_discount_amount'),dlv=float(dlv),gt=gt,gt_disc=tr.get('total_discount') if st==200 else None,gt_sd=tr.get('store_discount_amount') if st==200 else None,
      ac2a=ac2a,ac2b=ac2b, body=None if s==200 else r)
out=[]
for other in (389,392,394,395):
    for q1 in (1,2,3):
        for q2_ in (1,2,3):
            out.append(run([(390,q1),(other,q2_)]))
clear()
json.dump(out,open('mix36.json','w'),indent=1,default=str)
ok=0; ac2=0
print('basket | P | fRaw | nRaw | APP | OLD(fix@1c04b0f) | BASE | CHARGED | gettax | sd | fa+fv | ac2 | chg==app')
for r in out:
    e = r['chg'] is not None and abs(r['chg']-r['app'])<0.0049
    ok+=e; ac2+= (r['ac2a'] and r['ac2b'])
    print(r['lines'],r['P'],round(r['fR'],4),round(r['nR'],4),r['app'],r['old'],r['base'],r['chg'],r['gt'],r['sd'],round((r['fa'] or 0)+(r['fv'] or 0),2),r['ac2a'] and r['ac2b'],e,r['place'])
print('charged==app',ok,'/',len(out),' ac2 ok',ac2,'/',len(out))
