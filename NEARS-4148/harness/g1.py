import sys; sys.path.insert(0,'.')
from q import *
E=Ev('g1-non-owner-fixed.txt','G1 NON-OWNER on FIXED server 8148 (AC1, AC4): every step handler, many jar/id shapes')
def ctx(line):
    m=re.search(r'(\{.*\})\s*$',line); return json.loads(m.group(1)) if m else None
VICT=sql("select s.id from vendors v join stores s on s.vendor_id=v.id where v.status is null order by s.id").split()[0]
E.line(f'target victim (pending, untouched by G0 fixed arms): store {VICT}')
# jar F owns a DIFFERENT store
F=Jar('fixed','foreignowner'); F.apply_page(); r,email,pw=register(F,'g1f')
SF=sql(f"select s.id from stores s join vendors v on v.id=s.vendor_id where v.email='{email}'")
E.line(f'jar F created its OWN store {SF} via POST /vendor/apply ({summarize(r)}); session registration_store_ids={F.session_ids()}')
Eem=Jar('fixed','emptyset'); Eem.apply_page()
Ecookieless=Jar('fixed','cookieless')
n_ok=0; n_tot=0
def go(label, jar, method, path, params, expect, qs=None):
    """expect = ('refuse', store_id_or_None) | ('render200',)"""
    global n_ok,n_tot
    b=counts([VICT,SF]); 
    if method=='GET':
        items=params; url=path+('?'+'&'.join(f'{k}={v}' for k,v in items) if items else '')
        r=jar.req('GET',url)
    else:
        r=jar.req('POST',path,data=params)
    a=counts([VICT,SF])
    L=logs(r.rid); 
    toast=''
    loc=r.headers.get('Location')
    if loc and loc.startswith('http://127.0.0.1:8148'):
        r2=jar.req('GET',loc[len('http://127.0.0.1:8148'):]); toast=f'follow->{r2.status_code} {toasts(r2.text)}'
    ok=False; note=''
    if expect[0]=='refuse':
        c=ctx(L[0]) if len(L)==1 else None
        ok = (r.status_code==302 and loc.endswith('/vendor/apply') and len(L)==1 and '[FAIL] subscription.web_registration_purchase_refused' in L[0]
              and c and set(c.keys())=={'correlation_id','store_id','reason'} and c['reason']=='store_not_owned' and c['store_id']==expect[1] and c['correlation_id']==r.rid
              and ('error','Please follow the steps properly.') in [tuple(t) for t in toasts(r2.text)] and b==a and r.echo==r.rid)
        note=f'line={len(L)} ctx={c}'
    else:
        ok = r.status_code==200 and len(L)==0 and b==a
        note=f'lines={len(L)}'
    n_tot+=1; n_ok+=ok
    E.line(f'{"PASS" if ok else "FAIL"} | {label} | {method} {path} {params if not isinstance(params,list) else dict(params) if len({k for k,_ in params})==len(params) else params} | {summarize(r)} | {toast} | {note} | DB {delta(b,a)}')
P1=lambda s: dict(store_id=s,business_plan='subscription-base',package_id='1')
PAY=lambda s: dict(store_id=s,package_id='1',payment='free_trial')
for jn,jar in (('emptyset',Eem),('foreign-owner',F)):
    E.line(f'--- jar {jn}')
    go(f'{jn} business_plan POST digits id',jar,'POST','/vendor/business-plan',P1(VICT),('refuse',int(VICT)))
    go(f'{jn} business_plan POST commission-base',jar,'POST','/vendor/business-plan',dict(store_id=VICT,business_plan='commission-base'),('refuse',int(VICT)))
    go(f'{jn} secondStep GET',jar,'GET','/vendor/business-plan',[('store_id',VICT),('business_plan','subscription-base')],('refuse',int(VICT)))
    go(f'{jn} back GET',jar,'GET','/vendor/back',[('store_id',VICT)],('refuse',int(VICT)))
    go(f'{jn} back GET no store_id',jar,'GET','/vendor/back',[],('refuse',None))
    go(f'{jn} payment POST valid params',jar,'POST','/vendor/payment',PAY(VICT),('refuse',int(VICT)))
    go(f'{jn} payment POST package_id+payment MISSING',jar,'POST','/vendor/payment',dict(store_id=VICT),('refuse',int(VICT)))
    go(f'{jn} payment POST array store_id[]',jar,'POST','/vendor/payment',[('store_id[]',VICT),('package_id','1'),('payment','free_trial')],('refuse',None))
    go(f'{jn} payment POST garbage abc',jar,'POST','/vendor/payment',PAY('abc'),('refuse',None))
    go(f'{jn} payment POST garbage 1abc',jar,'POST','/vendor/payment',PAY('1abc'),('refuse',None))
    go(f'{jn} business_plan POST array store_id[]',jar,'POST','/vendor/business-plan',[('store_id[]',VICT),('business_plan','commission-base')],('refuse',None))
    go(f'{jn} back GET array store_id[]',jar,'GET','/vendor/back',[('store_id[]',VICT)],('refuse',None))
    go(f'{jn} secondStep GET garbage',jar,'GET','/vendor/business-plan',[('store_id','abc'),('business_plan','commission-base')],('refuse',None))
    go(f'{jn} payment POST id of a store owned by ANOTHER jar',jar,'POST','/vendor/payment',PAY(SF if jn=='emptyset' else VICT),('refuse',int(SF if jn=='emptyset' else VICT)))
    go(f'{jn} final_step foreign id, legacy shape store_id=<id>%3Fflag%3Dsuccess',jar,'GET','/vendor/final-step',[('store_id',VICT+'%3Fflag%3Dsuccess')],('render200',))
    go(f'{jn} final_step bare ?store_id=<id> (G6 shape, see g6 file)',jar,'GET','/vendor/final-step',[('store_id',VICT)],('render200',))
# cookieless GETs (no session at all)
E.line('--- jar cookieless (no cookie sent; GET handlers have no CSRF)')
go('cookieless back GET',Ecookieless,'GET','/vendor/back',[('store_id',VICT)],('refuse',int(VICT)))
go('cookieless secondStep GET',Ecookieless,'GET','/vendor/business-plan',[('store_id',VICT),('business_plan','commission-base')],('refuse',int(VICT)))
E.line(f'G1 SUMMARY: {n_ok}/{n_tot} requests behaved as specified (redirect to /vendor/apply, Toastr, exactly ONE store_not_owned line with keys {{correlation_id,store_id,reason}}, correlation_id == sent+echoed X-Request-Id, zero DB delta); final_step 200 no line')
