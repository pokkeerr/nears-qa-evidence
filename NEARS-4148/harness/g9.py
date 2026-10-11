import sys; sys.path.insert(0,'.')
from q import *
import base64
E=Ev('g9-delta-rb1-final-step-fixed.txt','G9 DELTA RE-QA cycle 1: RB-1 final_step (production hunk b19102c7f) on FIXED :8148, base :8149 for byte comparison')
def sid_of(email): return sql(f"select s.id from stores s join vendors v on v.id=s.vendor_id where v.email='{email}'")
SUCC='Thank you for your subscription purchase'
def kind(b): 
    s=SUCC in b; f=('Try_again' in b or 'Try again' in b)
    return 'SUCCESS' if s and not f else ('FAIL' if f and not s else f'ambiguous(s={s},f={f})')
def href(b):
    m=re.search(r'href="([^"]*vendor/back[^"]*)"',b); return m.group(1).replace('http://127.0.0.1:8148','') if m else None
def norm(b): 
    b=re.sub(r'(name="csrf-token"\s+content=")[^"]+','\\1X',b); b=re.sub(r'(name="_token"\s+value=")[^"]+','\\1X',b); b=re.sub(r'127\.0\.0\.1:81(48|49)','H',b); return b
rows=[]
def row(n,label,ok,detail):
    rows.append((n,ok)); E.line(f'{"PASS" if ok else "FAIL"} | RB-1.{n} | {label} | {detail}')
tokb=base64.b64encode(b'payment_method=paypal&&attribute_id=1&&transaction_reference=TXN4148').decode()
E.line('real-shape string built exactly as Processor::payment_response (Processor.php:93): external_redirect_link(?store_id=<id>) . "&" . "flag=<flag>&&token=" . base64(token_string)')
o=Jar('fixed','owner-g9'); o.apply_page(); r,email,pw=register(o,'g9',captcha=o.captcha()); S=sid_of(email)
FOREIGN=sql("select s.id from vendors v join stores s on s.vendor_id=v.id where v.status is null order by s.id limit 1")
E.line(f'owner store {S} via real POST /vendor/apply (session set={o.session_ids()}); foreign pending store {FOREIGN}; store {S} exists in clone: {sql(f"select count(*) from stores where id={S}")}, in shared DB: '+__import__("subprocess").run(['mysql','-u','root','multi_food_db','-N','-e',f'select count(*) from stores where id={S}'],capture_output=True,text=True).stdout.strip()+' (served-DB write proof)')
def get(jar,p): 
    r=jar.req('GET',p); L=logs(r.rid); return r,L
def chk(n,label,jar,who,path,want,hrefwant='any',lines=0):
    r,L=get(jar,path); k=kind(r.text) if r.status_code==200 else 'ERR'
    h=href(r.text); ok=r.status_code==200 and k==want and len(L)==lines
    if hrefwant=='owned': ok=ok and h==f'/vendor/back?store_id={S}'
    elif hrefwant=='noid': ok=ok and h=='/vendor/back'
    elif hrefwant=='none': ok=ok and h is None
    row(n,f'{who} {label}',ok,f'GET {path.split("&&token")[0]} | HTTP {r.status_code} {k} | try-again href={h} | log lines={len(L)}{" "+L[0][:140] if L else ""}')
    return r
nj=lambda: Jar('fixed','nojar')
shapes=[
 ('1','real return success', f'/vendor/final-step?store_id={S}&flag=success&&token={tokb}','SUCCESS','none'),
 ('1b','real return fail', f'/vendor/final-step?store_id={S}&flag=fail&&token={tokb}','FAIL',None),
 ('1c','real return CANCEL (Stripe/SSL/PayPal callbacks)', f'/vendor/final-step?store_id={S}&flag=cancel&&token={tokb}','FAIL',None),
 ('2','bare ?store_id=ID', f'/vendor/final-step?store_id={S}','FAIL',None),
 ('3','legacy %3Fflag%3Dsuccess', f'/vendor/final-step?store_id={S}%3Fflag%3Dsuccess','SUCCESS','none'),
 ('3b','legacy %3Fflag%3Dfail', f'/vendor/final-step?store_id={S}%3Fflag%3Dfail','FAIL',None),
 ('6a','flag=ok', f'/vendor/final-step?store_id={S}&flag=ok&&token={tokb}','FAIL',None),
 ('6b','flag= (empty)', f'/vendor/final-step?store_id={S}&flag=&&token={tokb}','FAIL',None),
 ('6c','flag[]=x', f'/vendor/final-step?store_id={S}&flag[]=x','FAIL',None),
 ('6d','flag=SUCCESS (case)', f'/vendor/final-step?store_id={S}&flag=SUCCESS','FAIL',None),
 ('10','precedence: legacy suffix fail + flag=success (query param wins)', f'/vendor/final-step?store_id={S}%3Fflag%3Dfail&flag=success','SUCCESS','none'),
]
for n,label,p,want,hw in shapes:
    for who,jar in (('owner jar',o),('no jar',None)):
        j=jar or nj()
        hwant = ('owned' if who=='owner jar' else 'noid') if want=='FAIL' else hw
        chk(n,label,j,who,p,want,hrefwant=hwant)
# foreign id never in href
for who,jar in (('owner jar',o),('no jar',None)):
    j=jar or nj(); r,L=get(j,f'/vendor/final-step?store_id={FOREIGN}&flag=fail&&token={tokb}'); h=href(r.text)
    row('1d',f'{who} real-shape FAIL with a FOREIGN id',r.status_code==200 and kind(r.text)=='FAIL' and h=='/vendor/back' and str(FOREIGN) not in r.text.replace(FOREIGN+'0',''),f'HTTP {r.status_code} href={h} (foreign id {FOREIGN} never echoed) log lines={len(L)}')
# byte comparison vs base for (4) and (5)
for n,label,p in (('4','no store_id','/vendor/final-step'),('5','?flag=success only','/vendor/final-step?flag=success')):
    for who in ('owner jar','no jar'):
        jf=o if who=='owner jar' else nj(); jb=Jar('base','b-'+who)
        rf=jf.req('GET',p); rb=jb.req('GET',p)
        same=norm(rf.text)==norm(rb.text); 
        row(n,f'{who} {label} vs BASE',rf.status_code==200==rb.status_code and kind(rf.text)=='SUCCESS' and same,f'fixed HTTP {rf.status_code} {kind(rf.text)} len={len(rf.text)}; base HTTP {rb.status_code} {kind(rb.text)} len={len(rb.text)}; normalized body identical={same}')
# base RED recheck of the real shape (still 500 at base)
jb=Jar('base','b-red'); rb=jb.req('GET',f'/vendor/final-step?store_id=1&flag=success&&token={tokb}'); E.line(f'(control) BASE real-shape success = HTTP {rb.status_code} (expect 500: RB-1 RED still reproduces at base)')
# 7 free_trial end to end
b=counts([S]); r=o.req('POST','/vendor/payment',data=dict(store_id=S,package_id='1',payment='free_trial')); a=counts([S]); L=logs(r.rid)
loc=r.headers.get('Location'); r2=o.req('GET',loc[len('http://127.0.0.1:8148'):]) if loc else None
row('7','owner free_trial flow end to end',r.status_code==302 and loc=='http://127.0.0.1:8148/vendor/final-step' and r2.status_code==200 and kind(r2.text)=='SUCCESS' and len(L)==0 and b!=a,f'POST /vendor/payment pkg1 free_trial -> {summarize(r)} follow GET /vendor/final-step (no params) -> {r2.status_code} {kind(r2.text)} toasts={toasts(r2.text)}; trial rows: {delta(b,a)}; [FAIL] lines={len(L)}')
# 8 G1 smoke non-owner
att=Jar('fixed','attacker'); att.apply_page(); V=FOREIGN
b=counts([V]); r=att.req('POST','/vendor/payment',data=dict(store_id=V,package_id='1',payment='free_trial')); a=counts([V]); L=logs(r.rid); loc=r.headers.get('Location'); r2=att.req('GET','/vendor/apply')
c=json.loads(re.search(r'(\{.*\})\s*$',L[0]).group(1)) if len(L)==1 else None
row('8','G1 smoke: non-owner POST /vendor/payment',r.status_code==302 and loc.endswith('/vendor/apply') and len(L)==1 and c and c['reason']=='store_not_owned' and c['correlation_id']==r.rid and set(c)=={'correlation_id','store_id','reason'} and b==a,f'{summarize(r)} line ctx={c} DB {delta(b,a)} (earlier behaviour unchanged at b19102c7f)')
E.line(f'SUMMARY: {sum(1 for _,ok in rows if ok)}/{len(rows)} rows PASS')
