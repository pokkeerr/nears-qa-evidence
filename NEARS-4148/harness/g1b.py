import sys; sys.path.insert(0,'.')
from q import *
E=Ev('g1b-extra-id-shapes-and-payment-param-robustness.txt','G1b EXTRA exploratory: odd store_id shapes (non-owner and owner) and owner-side odd payment param, FIXED 8148')
def ctx(line):
    m=re.search(r'(\{.*\})\s*$',line); return json.loads(m.group(1)) if m else None
def sid_of(email): return sql(f"select s.id from stores s join vendors v on v.id=s.vendor_id where v.email='{email}'")
VICT=sql("select s.id from vendors v join stores s on s.vendor_id=v.id where v.status is null order by s.id").split()[0]
j=Jar('fixed','exploratory'); j.apply_page()
for raw in (f'0{VICT}', f'{VICT}+', f'%20{VICT}', f'{VICT}%20', f'%2B{VICT}', f'-{VICT}', '99999999999999999999', '0', '', '%D9%A9%D9%A1%D9%A1%D9%A0%D9%A8', f'{VICT}.0', f'{VICT}e0', f'0x{int(VICT):x}'):
    b=counts([VICT]); r=j.req('POST','/vendor/payment',data=f'store_id={raw}&package_id=1&payment=free_trial&_token={j.token}',token=False,hdr={'Content-Type':'application/x-www-form-urlencoded'})
    a=counts([VICT]); L=logs(r.rid); c=ctx(L[0]) if len(L)==1 else None
    E.line(f'non-owner store_id={raw!r:34} -> {summarize(r)} lines={len(L)} ctx={ {k:v for k,v in (c or {}).items() if k!="correlation_id"} } DB {delta(b,a)}')
# owner jar odd payment param (own store)
o=Jar('fixed','owner-g1b'); o.apply_page(); r,email,pw=register(o,'g1b',captcha=o.captcha()); S=sid_of(email)
for lab,items in (('payment[]=free_trial (array)',[('payment[]','free_trial')]),('payment=bogus_gateway',[('payment','bogus_gateway')]),('payment=free_trial&payment_platform=app',[('payment','free_trial'),('payment_platform','app')])):
    b=counts([S]); r=o.req('POST','/vendor/payment',data=[('store_id',S),('package_id','1')]+items); a=counts([S]); L=logs(r.rid)
    E.line(f'OWNER {lab} -> {summarize(r)} log-lines={[l[l.index("] ")+2:][:130] for l in L]} DB {delta(b,a)}')
# whole-log sanity: refusal lines by reason, PII leak scan since QA start
import subprocess
out=subprocess.run(['grep','-F','web_registration_purchase_refused',W+'/storage/logs/laravel.log'],capture_output=True,text=True).stdout.splitlines()
from collections import Counter
cnt=Counter(); keys=Counter()
for l in out:
    if not l.startswith('[2026-10-11 21:3') and not l.startswith('[2026-10-11 21:4') and not l.startswith('[2026-10-11 22:'): continue
    c=ctx(l); cnt[c['reason']]+=1; keys[tuple(sorted(c))]+=1
E.line(f'refusal lines in laravel.log during this QA window by reason: {dict(cnt)}; context key-sets seen: {dict(keys)}')
leak=subprocess.run('grep -c -E "Regr3ss|qa4148\\.|@example\\.test|password" '+W+'/storage/logs/laravel.log',shell=True,capture_output=True,text=True).stdout.strip()
win=subprocess.run("awk '/^\\[2026-10-11 21:3|^\\[2026-10-11 21:4|^\\[2026-10-11 22:/' "+W+"/storage/logs/laravel.log | grep -F 'web_registration_purchase_refused' | grep -c -i -E 'Regr3ss|qa4148\\.|@example|password|email'",shell=True,capture_output=True,text=True).stdout.strip()
E.line(f'PII scan: refusal lines containing a registrant email/password/the word email|password: {win} (expect 0)')
