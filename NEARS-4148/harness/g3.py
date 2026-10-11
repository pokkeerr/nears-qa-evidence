import sys; sys.path.insert(0,'.')
from q import *
E=Ev('g3-owner-refusals-fixed.txt','G3 OWNER refusals on FIXED 8148 (AC2, AC4): own session, bad package, never a 500, zero writes, one line')
def ctx(line):
    m=re.search(r'(\{.*\})\s*$',line); return json.loads(m.group(1)) if m else None
j=Jar('fixed','owner-g3'); j.apply_page(); r,email,pw=register(j,'g3',captcha=j.captcha())
S=sql(f"select s.id from stores s join vendors v on v.id=s.vendor_id where v.email='{email}'")
E.line(f'owner jar created store {S} (module 1 grocery); session set={j.session_ids()}')
RET,REN='3','4'
variants=[('nonexistent 999999',[('package_id','999999')],'package_missing'),
          ('flat array package_id[]=1',[('package_id[]','1')],'package_missing'),
          ('nested package_id[0][]=1&package_id[0][]=2',[('package_id[0][]','1'),('package_id[0][]','2')],'package_missing'),
          ('keyed array package_id[x]=1',[('package_id[x]','1')],'package_missing'),
          ('RETIRED nears4145-qa-retired (status 0)',[('package_id',RET)],'package_ineligible'),
          ('RENTAL-type nears4145-qa-rental',[('package_id',REN)],'package_ineligible')]
n_ok=n=0
for vname,items,reason in variants:
    for pay in ('free_trial','paypal'):
        b=counts([S]); pre_pr=sql(f"select count(*) from payment_requests where payer_id={S}")
        r=j.req('POST','/vendor/payment',data=[('store_id',S),('payment',pay)]+items)
        a=counts([S]); L=logs(r.rid); loc=r.headers.get('Location')
        r2=j.req('GET',loc[len(SERV['fixed'][0]):]) if loc and loc.startswith(SERV['fixed'][0]) else None
        c=ctx(L[0]) if len(L)==1 else None
        names=re.findall(r'nears4145-qa-[a-z-]+|QA Single-Store Fixture|QA NEARS-3285 Test Package[^<]*',r2.text) if r2 else []
        ok=(r.status_code==302 and loc.endswith(f'/vendor/back?store_id={S}') and r2 is not None and r2.status_code==200
            and ('error','Something went wrong!.') in [tuple(t) for t in toasts(r2.text)]
            and len(L)==1 and '[FAIL] subscription.web_registration_purchase_refused' in L[0] and c and set(c)=={'correlation_id','store_id','reason'}
            and c['reason']==reason and c['store_id']==int(S) and c['correlation_id']==r.rid and b==a and 'nears4145-qa-retired' not in r2.text and 'nears4145-qa-rental' not in r2.text)
        n+=1; n_ok+=ok
        E.line(f'{"PASS" if ok else "FAIL"} | {vname} x {pay} | {summarize(r)} | follow-> {r2.status_code if r2 else None} toasts={toasts(r2.text) if r2 else None} list-shows={sorted(set(names))} | line={len(L)} ctx={c} | DB {delta(b,a)}')
# validation-only arm (information): empty package_id
b=counts([S]); r=j.req('POST','/vendor/payment',data=dict(store_id=S,package_id='',payment='free_trial')); a=counts([S])
E.line(f'INFO empty package_id (validate() fails, not a package refusal): {summarize(r)} logs={len(logs(r.rid))} DB {delta(b,a)}')
# control: after all refusals the same owner can still complete a valid purchase
b=counts([S]); r=j.req('POST','/vendor/payment',data=dict(store_id=S,package_id='1',payment='free_trial')); a=counts([S]); L=logs(r.rid)
E.line(f'CONTROL after 12 refusals, same owner, package 1 free_trial: {summarize(r)} log lines={len(L)} DB {delta(b,a)}')
E.line(f'G3 SUMMARY: {n_ok}/{n} refusal arms exactly as specified (302 -> /vendor/back?store_id, back page 200 + Toastr, retired/rental absent in list, one line, right reason, zero writes, no 500)')
