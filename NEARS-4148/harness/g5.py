import sys; sys.path.insert(0,'.')
from q import *
import subprocess
which=sys.argv[1]   # fixed|base
E=Ev(f'g5-login-resume-limiter-{which}.txt',f'G5 LOGIN RESUME + LIMITER on {which} server ({SERV[which][0]})')
def sid_of(email): return sql(f"select s.id from stores s join vendors v on v.id=s.vendor_id where v.email='{email}'")
def cc(): subprocess.run(['php','artisan','cache:clear'],cwd=W,env={**os.environ,'DB_DATABASE':DB},capture_output=True)
def vst(S): return sql("select ifnull(v.status,'NULL') from vendors v join stores s on s.vendor_id=v.id where s.id=%s" % S)
def HASPKG(t): return 'name="package_id" value="1"' in t
def lim(): return sql("select `key`,value from cache where `key` like '%login-attempts%'") or 'no limiter key'
def errs(body):
    m=re.findall(r'<(?:li|span|strong|div)[^>]*>\s*(Password does not match\.|Email does not match\.|Too many login attempts[^<]*|[^<]*ReCAPTCHA[^<]*)\s*<',body)
    return sorted(set(m)) or ([x for x in ['Password does not match.','Email does not match.','Too many login attempts'] if x in body])
def is_payment_view(body,S): return ('name="payment"' in body or 'restaurant/payment' in body or '/vendor/payment' in body) and f'value="{S}"' in body
def registrant(tag):
    j=Jar(which,'reg-'+tag); j.apply_page(); r,email,pw=register(j,tag,captcha=j.captcha())
    return email,pw,sid_of(email)
def fresh_login_jar(name):
    j=Jar(which,name); r=j.req('GET','/login/vendor'); j.token=tok(r.text); return j
def login(j,email,pw,captcha=None):
    d=[('email',email),('role','vendor'),('custome_recaptcha',captcha if captcha is not None else j.captcha())]
    if isinstance(pw,list): d+= [('password[]',x) for x in pw]
    else: d.append(('password',pw))
    return j.req('POST','/login_submit',data=d)
def follow(j,r):
    loc=r.headers.get('Location'); return j.req('GET',loc[len(SERV[which][0]):]) if loc and loc.startswith(SERV[which][0]) else None
email,pw,S=registrant('g5'); 
E.line(f'pending registrant created through real POST /vendor/apply: store {S}; vendors.status={vst(S)} store_business_model={sql("select store_business_model from stores where id=%s" % S)} (email is a throwaway @example.test)')
if which=='base':
    cc(); j=fresh_login_jar('base-wrongpw'); r=login(j,email,'WrongPassw0rd!'); 
    E.line(f'BASE RED: login_submit with WRONG password for a none registrant -> {summarize(r)} body-is-payment-view={is_payment_view(r.text,S)} (store id {S} in page: {S in r.text})')
    sys.exit()
cc(); E.line('--- (a) WRONG password'); E.line('limiter before: '+lim())
ja=fresh_login_jar('wrongpw'); r=login(ja,email,'WrongPassw0rd!'); r2=follow(ja,r)
E.line(f'POST /login_submit role=vendor wrong password -> {summarize(r)}; follow -> {r2.status_code if r2 else None} errors={errs(r2.text) if r2 else None}; payment view in POST body: {is_payment_view(r.text,S)}; store id in follow page: {S in (r2.text if r2 else "")}')
E.line('limiter after: '+lim()+f'; registration_store_ids in this jar session: {ja.session_ids()}')
ja.token=tok(r2.text) if r2 else ja.token
b=counts([S]); r=ja.req('POST','/vendor/payment',data=dict(store_id=S,package_id='1',payment='free_trial')); a=counts([S]); L=logs(r.rid)
E.line(f'same jar POST /vendor/payment for the registrant store -> {summarize(r)} lines={[l[l.index("[FAIL]"):][:200] for l in L]} DB {delta(b,a)}  (expect store_not_owned refusal: jar NOT bound)')
cc(); E.line('--- (b) ARRAY password (6 elements, passes min:6)'); 
jb=fresh_login_jar('arraypw'); r=login(jb,email,['a','b','c','d','e','f']); r2=follow(jb,r)
E.line(f'POST password[]x6 -> {summarize(r)}; follow -> {r2.status_code if r2 else None} errors={errs(r2.text) if r2 else None}; payment view: {is_payment_view(r.text,S)}; NOT 500: {r.status_code!=500}; limiter: {lim()}')
cc(); E.line('--- (d) unknown email')
jd=fresh_login_jar('unknown'); r=login(jd,'nobody4148@example.test','WrongPassw0rd!'); r2=follow(jd,r)
E.line(f'POST unknown email -> {summarize(r)}; follow -> errors={errs(r2.text) if r2 else None}')
cc(); E.line('--- (c) RIGHT password: resume positive control'); E.line('limiter before: '+lim())
jc=fresh_login_jar('rightpw'); id0=os.path.basename(jc.session_file() or 'NONE'); t0=jc.token
r=login(jc,email,pw)
E.line(f'POST /login_submit right password -> {summarize(r)}; payment view with own store id {S}: {is_payment_view(r.text,S)}; package_id hidden field=1: {HASPKG(r.text)}; free_trial option: {"free_trial" in r.text}')
jc.token=tok(r.text); id1=os.path.basename(jc.session_file() or 'NONE')
E.line(f'session id rotated at login: {id0!=id1} (before {id0[:8]}.. after {id1[:8]}..); csrf token rotated: {t0!=jc.token}; registration_store_ids={jc.session_ids()} (only this registrant store)')
d=jc.req('GET','/vendor-panel'); E.line(f'GET /vendor-panel (vendor dashboard) same jar -> {summarize(d)} (not logged into the panel: redirect, no 200)')
b=counts([S]); r=jc.req('POST','/vendor/payment',data=dict(store_id=S,package_id='1',payment='free_trial')); a=counts([S]); L=logs(r.rid)
r2=follow(jc,r)
E.line(f'POST /vendor/payment package 1 free_trial from the login-resumed jar -> {summarize(r)} follow->{r2.status_code if r2 else None} {toasts(r2.text) if r2 else None} [FAIL] lines={len(L)}')
E.line(f'   DB before {b}'); E.line(f'   DB after  {a}'); E.line('   trial row: '+sql(f"select store_id,package_id,is_trial,payment_status from subscription_transactions where store_id={S}"))
cc(); E.line('--- (e) THROTTLE: 5 wrong passwords then the RIGHT one (second registrant)')
email2,pw2,S2=registrant('g5e'); cc()
je=fresh_login_jar('throttle'); outs=[]
for i in range(5):
    r=login(je,email2,'WrongPassw0rd!'); r2=follow(je,r); outs.append(errs(r2.text) if r2 else r.status_code)
E.line(f'5 wrong attempts -> {outs}; limiter: {lim()}')
r=login(je,email2,pw2); r2=follow(je,r)
E.line(f'6th attempt with the RIGHT password -> {summarize(r)}; follow errors={errs(r2.text) if r2 else None}; payment view: {is_payment_view(r.text,S2)} (expect refused by limiter)')
cc(); jf=fresh_login_jar('afterreset'); r=login(jf,email2,pw2); E.line(f'after cache:clear (limiter reset) right password -> {summarize(r)} payment view: {is_payment_view(r.text,S2)}')
cc(); E.line('--- (f) 12 right-password logins in ONE jar (third registrant), then pay')
email3,pw3,S3=registrant('g5f'); cc(); jg=Jar('fixed','repeat'); jg.token=tok(jg.req('GET','/login/vendor').text)
codes=[]
for i in range(12):
    r=login(jg,email3,pw3); codes.append((r.status_code,is_payment_view(r.text,S3)))
    jg.token=tok(jg.req('GET','/login/vendor').text) if True else jg.token
E.line(f'12 logins: {sorted(set(codes))}; registration_store_ids={jg.session_ids()} (deduped, no growth)')
b=counts([S3]); r=jg.req('POST','/vendor/payment',data=dict(store_id=S3,package_id='1',payment='paypal')); a=counts([S3]); L=logs(r.rid)
E.line(f'then POST /vendor/payment paypal -> {summarize(r)} [FAIL] lines={len(L)} DB {delta(b,a)}')
