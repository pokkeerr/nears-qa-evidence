import sys; sys.path.insert(0,'.')
from q import *
import base64
E=Ev('g6-final-step-return-shapes.txt','G6 FINAL_STEP real gateway-return shapes, MEASURE ONLY, BASE (8149) vs FIXED (8148)')
E.line('Shape source: app/Traits/Processor.php:79-96 payment_response() redirects to external_redirect_link (= route restaurant.final_step with ?store_id=<id>, set in VendorController::payment) + (str_contains "?" ? "&":"?") + "flag=<success|fail>&&token=<base64>" => /vendor/final-step?store_id=<id>&flag=success&&token=<b64>. A real sandbox gateway round trip is NOT feasible on the clone (paypal is mode=live with no sandbox credentials, the callback needs the gateway to call back); the shapes below are replayed with the exact string payment_response builds.')
def sid_of(email): return sql(f"select s.id from stores s join vendors v on v.id=s.vendor_id where v.email='{email}'")
def kind(body): 
    return 'SUCCESS page' if 'Thank you for your subscription purchase' in body else ('FAIL page (Try again)' if 'Try_again' in body or 'Try again' in body else 'other')
for srv in ('base','fixed'):
    o=Jar(srv,'owner-g6'); o.apply_page(); r,email,pw=register(o,'g6'+srv[0],captcha=o.captcha()); S=sid_of(email)
    tokb=base64.b64encode(b'payment_method=paypal&&attribute_id=1&&transaction_reference=TXN4148').decode()
    foreign=sql("select s.id from vendors v join stores s on s.vendor_id=v.id where v.status is null order by s.id limit 1")
    shapes=[('(1) ?store_id=ID&flag=success&&token=<b64> [real return, success]',f'/vendor/final-step?store_id={S}&flag=success&&token={tokb}'),
            ('(1b) ?store_id=ID&flag=fail&&token=<b64> [real return, fail]',f'/vendor/final-step?store_id={S}&flag=fail&&token={tokb}'),
            ('(2) ?store_id=ID',f'/vendor/final-step?store_id={S}'),
            ('(3) ?store_id=ID%3Fflag%3Dsuccess [legacy single-param]',f'/vendor/final-step?store_id={S}%3Fflag%3Dsuccess'),
            ('(3b) ?store_id=ID%3Fflag%3Dfail [legacy fail]',f'/vendor/final-step?store_id={S}%3Fflag%3Dfail'),
            ('(4) no store_id','/vendor/final-step'),
            ('(5) ?flag=success only','/vendor/final-step?flag=success')]
    E.line(f'--- {srv.upper()} ({SERV[srv][0]}): owner jar owns store {S} (session set={o.session_ids()})')
    for who,jar in (('owner jar',o),('no jar',None)):
        for lab,p in shapes:
            j=jar or Jar(srv,'nojar')
            r=j.req('GET',p); body=r.text
            L=logs(r.rid,srv)
            fl=[l[l.index(']')+2:][:110] for l in L if '[FAIL]' in l or 'ERROR' in l]
            tryhref=re.search(r'href="[^"]*vendor/back[^"]*"',body)
            E.line(f'{srv} | {who:9} | {lab} | HTTP {r.status_code} | {kind(body) if r.status_code==200 else "(error page)"} | try-again href={tryhref.group(0)[:70] if tryhref else None} | log={fl}')
