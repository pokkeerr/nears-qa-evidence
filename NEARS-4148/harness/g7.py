import sys; sys.path.insert(0,'.')
from q import *
import subprocess
E=Ev('g7-regression-sweep.txt','G7 REGRESSION SWEEP (bounded) FIXED 8148')
def FORM(t): return all(('name="%s"' % f) in t for f in ('f_name','email','password','zone_id','module_id'))
def cc(): subprocess.run(['php','artisan','cache:clear'],cwd=W,env={**os.environ,'DB_DATABASE':DB},capture_output=True)
j=Jar('fixed','sweep'); r=j.apply_page()
E.line(f'GET /vendor/apply -> HTTP {r.status_code}; has registration form fields: {FORM(r.text)}; captcha input custome_recaptcha present: {"custome_recaptcha" in r.text}; logs={len(logs(r.rid))}')
E.line('        packages variable passed to view = purchasableBy(null): rendered package names in page: '+str(sorted(set(re.findall(r'nears4145-qa-[a-z-]+|QA Single-Store Fixture|QA NEARS-3285 Test Package[^<]*',r.text)))))
for mid,lab in (('1','grocery'),('2','food'),('7','grocery-2288')):
    r=j.req('GET',f'/vendor/get-module-type?id={mid}'); d=r.json(); names=sorted(set(re.findall(r'nears4145-qa-[a-z-]+|QA Single-Store Fixture|QA NEARS-3285 Test Package',d.get('view',''))))
    E.line(f'GET /vendor/get-module-type?id={mid} ({lab}) -> HTTP {r.status_code} module_type={d.get("module_type")} packages={names}; retired absent={"nears4145-qa-retired" not in d.get("view","")}; rental-type absent={"nears4145-qa-rental" not in d.get("view","")}')
r=j.req('GET','/vendor/get-module-type?id=999999'); E.line(f'GET get-module-type unknown module -> HTTP {r.status_code} {r.text[:80]}')
for mid,zid in (('2','1'),('1','2'),('5','1')):
    r=j.req('GET',f'/vendor/check-module-type?id={mid}&zone_id={zid}'); E.line(f'GET /vendor/check-module-type?id={mid}&zone_id={zid} -> HTTP {r.status_code} {r.text[:60]}')
r=j.req('GET','/vendor/get-all-modules?zone_id=1&q=Rest'); E.line(f'GET /vendor/get-all-modules?zone_id=1&q=Rest -> HTTP {r.status_code} {r.text[:100]}')
E.line('(no rental module exists on the clone: select modules where module_type=rental returned 0 rows; Rental add-on is absent by design)')
# vendor web login (approved, non-none)
for email in ('ahmed.khan@demo.com','countryfair@demo.com','john.smith@demo.com'):
    cc(); v=Jar('fixed','vlogin'); r=v.req('GET','/login/vendor'); v.token=tok(r.text)
    r=v.req('POST','/login_submit',data=[('email',email),('password','123456789'),('role','vendor'),('custome_recaptcha',v.captcha())])
    mdl=sql(f"select s.store_business_model from stores s join vendors vv on vv.id=s.vendor_id where vv.email='{email}' limit 1")
    d=v.req('GET','/vendor-panel') if r.status_code==302 else None
    E.line(f'vendor web login {email} (store_business_model={mdl}) -> {summarize(r)}; GET /vendor-panel -> {d.status_code if d is not None else None}')
    if r.status_code==302 and 'login' not in (r.headers.get('Location') or ''): break
cc(); a=Jar('fixed','alogin'); r=a.req('GET','/login/admin'); a.token=tok(r.text)
r=a.req('POST','/login_submit',data=[('email','admin@admin.com'),('password','123456789'),('role','admin'),('custome_recaptcha',a.captcha())]); d=a.req('GET','/admin')
E.line(f'admin web login -> {summarize(r)}; GET /admin -> {d.status_code}')
cc()
