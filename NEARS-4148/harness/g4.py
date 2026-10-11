import sys; sys.path.insert(0,'.')
from q import *
from admin_login import admin_jar
from forms import FormHarvest
import subprocess
E=Ev('g4-not-pending-and-toggle-off.txt','G4 store_not_pending (real admin approve) + toggle_store_registration OFF (real admin form POST), FIXED 8148')
def ctx(line):
    m=re.search(r'(\{.*\})\s*$',line); return json.loads(m.group(1)) if m else None
def sid_of(email): return sql(f"select s.id from stores s join vendors v on v.id=s.vendor_id where v.email='{email}'")
def vst(S): return sql("select ifnull(v.status,'NULL') from vendors v join stores s on s.vendor_id=v.id where s.id=%s" % S)
def sst(S): return sql("select concat(status,' ',store_business_model,' pkg=',ifnull(package_id,'NULL')) from stores where id=%s" % S)
def tog(): return sql("select ifnull(value,'NULL') from business_settings where `key`='toggle_store_registration'")
def cc(): subprocess.run(['php','artisan','cache:clear'],cwd=W,env={**os.environ,'DB_DATABASE':DB},capture_output=True)
which=sys.argv[1]
if which=='a':
    o=Jar('fixed','owner-g4a'); o.apply_page(); r,email,pw=register(o,'g4a',captcha=o.captcha()); S=sid_of(email)
    E.line(f'(a) owner created store {S}; steppable before approval: business_plan -> {summarize(o.req("POST","/vendor/business-plan",data=dict(store_id=S,business_plan="subscription-base",package_id="1")))}')
    E.line(f'    vendor status before approval: {vst(S)}')
    a,r=admin_jar(); E.line(f'    admin login: {summarize(r)}')
    r=a.req('GET','/admin/store/pending-requests'); a.token=tok(r.text); E.line(f'    GET admin pending-requests -> {r.status_code}; lists store {S}: {str(S) in r.text}')
    r=a.req('POST',f'/admin/store/update-application/{S}/1',data={}); E.line(f'    real admin approve action POST /admin/store/update-application/{S}/1 -> {summarize(r)}')
    E.line(f'    vendor status after approval: {vst(S)}  store status/model: {sst(S)}')
    n=0;ok=0
    steps=[('business_plan POST subscription-base','POST','/vendor/business-plan',dict(store_id=S,business_plan='subscription-base',package_id='1')),
           ('business_plan POST commission-base','POST','/vendor/business-plan',dict(store_id=S,business_plan='commission-base')),
           ('secondStep GET','GET',f'/vendor/business-plan?store_id={S}&business_plan=commission-base',None),
           ('back GET','GET',f'/vendor/back?store_id={S}',None),
           ('payment POST package 1 free_trial','POST','/vendor/payment',dict(store_id=S,package_id='1',payment='free_trial')),
           ('payment POST package 1 paypal','POST','/vendor/payment',dict(store_id=S,package_id='1',payment='paypal')),
           ('payment POST RETIRED package free_trial','POST','/vendor/payment',dict(store_id=S,package_id='3',payment='free_trial'))]
    for lab,m,p,d in steps:
        b=counts([S]); r=o.req(m,p,data=d) if m=='POST' else o.req('GET',p); a_=counts([S]); L=logs(r.rid); c=ctx(L[0]) if len(L)==1 else None
        good=(r.status_code==403 and len(L)==1 and c and c['reason']=='store_not_pending' and c['store_id']==int(S) and set(c)=={'correlation_id','store_id','reason'} and c['correlation_id']==r.rid and b==a_)
        n+=1; ok+=good
        E.line(f'{"PASS" if good else "FAIL"} | approved-owner {lab} | {summarize(r)} | lines={len(L)} ctx={c} | DB {delta(b,a_)}')
    E.line(f'G4a SUMMARY {ok}/{n}: owner of an APPROVED store gets HTTP 403 + ONE store_not_pending line, zero writes')
if which=='b':
    a,r=admin_jar(); E.line(f'admin login {summarize(r)}')
    snap=lambda: dict(l.split('\t') for l in sql("select `key`, left(sha2(ifnull(value,''),256),12) from business_settings").splitlines())
    def post_store(on):
        r=a.req('GET','/admin/business-settings/business-setup/store'); a.token=tok(r.text)
        h=FormHarvest('update-store'); h.feed(r.text)
        f=[x for x in h.fields if x[0]!='_token']
        if not on: f=[x for x in f if x[0]!='store_self_registration']
        elif not any(x[0]=='store_self_registration' for x in f): f.append(('store_self_registration','1'))
        r=a.req('POST','/admin/business-settings/update-store',data=f)
        cc(); return r
    before=snap()
    E.line(f'toggle_store_registration before: {tog()}')
    r=post_store(False); E.line(f'real admin POST update-store with store self registration UNCHECKED -> {summarize(r)}; toggle now: {tog()}; cache:clear (inline DB) done')
    mid=snap(); E.line('business_settings keys changed by that form round-trip: '+str([k for k in set(before)|set(mid) if before.get(k)!=mid.get(k)]))
    # non-owner arms with toggle OFF
    n=ok=0
    for lab,m,p,d in [('back GET','GET','/vendor/back?store_id=91108',None),('payment POST','POST','/vendor/payment',dict(store_id='91108',package_id='1',payment='free_trial')),('business_plan POST','POST','/vendor/business-plan',dict(store_id='91108',business_plan='commission-base')),('secondStep GET','GET','/vendor/business-plan?store_id=91108&business_plan=commission-base',None)]:
        j=Jar('fixed','nonowner-g4b'); (setattr(j,'token',tok(j.req('GET','/login/vendor').text)) if m=='POST' else None)
        b=counts(['91108']); r=j.req(m,p,data=d) if m=='POST' else j.req('GET',p); a_=counts(['91108']); L=logs(r.rid); loc=r.headers.get('Location')
        r2=j.req('GET',loc[len('http://127.0.0.1:8148'):]) if loc else None
        r3=None
        c=ctx(L[0]) if len(L)==1 else None
        good=(r.status_code==302 and loc=='http://127.0.0.1:8148' or (loc or '').rstrip('/')=='http://127.0.0.1:8148') and r2 is not None and r2.status_code==200 and len(L)==1 and c and c['reason']=='store_not_owned' and b==a_ and ('error','Please follow the steps properly.') in [tuple(t) for t in toasts(r2.text)]
        n+=1; ok+=bool(good)
        E.line(f'{"PASS" if good else "FAIL"} | toggle OFF non-owner {lab} | {summarize(r)} | follow(home)->{r2.status_code if r2 else None} toasts={toasts(r2.text) if r2 else None} (no further redirect: {r2.headers.get("Location") is None if r2 else None}) | line={len(L)} ctx={c} | DB {delta(b,a_)}')
    j=Jar('fixed','apply-off'); r=j.req('GET','/vendor/apply'); E.line(f'INFO toggle OFF GET /vendor/apply -> {summarize(r)} (create() back() + Toastr, pre-existing)')
    r=post_store(True); E.line(f'RESTORE: real admin POST update-store with self registration CHECKED -> {summarize(r)}; toggle now: {tog()}')
    after=snap(); E.line('business_settings keys differing from the ORIGINAL snapshot after restore: '+str([k for k in set(before)|set(after) if before.get(k)!=after.get(k)]))
    j=Jar('fixed','nonowner-restored'); r=j.req('GET','/vendor/back?store_id=91108'); E.line(f'toggle ON again: non-owner back GET -> {summarize(r)} (expect /vendor/apply)')
    E.line(f'G4b SUMMARY {ok}/{n}: toggle OFF non-owner -> HOME route (no loop), Toastr, one store_not_owned line, zero writes')
