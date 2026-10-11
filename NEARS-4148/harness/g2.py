import sys; sys.path.insert(0,'.')
from q import *
E=Ev('g2-owner-positive-controls-fixed.txt','G2 OWNER positive controls on FIXED 8148 (AC3): own session completes its own store')
def sid_of(email): return sql(f"select s.id from stores s join vendors v on v.id=s.vendor_id where v.email='{email}'")
def newowner(tag, plan='subscription-base', pkg='1'):
    j=Jar('fixed','owner-'+tag); j.apply_page(); cap=j.captcha()
    r,email,pw=register(j,tag,plan=plan,package_id=pkg,captcha=cap)
    sid=sid_of(email)
    return j,r,email,pw,sid
# (vi) rotation + same-session retry after validation failure
V=Jar('fixed','validation'); V.apply_page(); c0,t0=V.sess_id_cookie(),V.token
r,email,pw=register(V,'v1',extra={'f_name':''},refresh=False)   # missing required field
E.line(f'(vi-a) POST /vendor/apply with f_name empty (right captcha): {summarize(r)} body={r.text[:140]}')
E.line(f'      session cookie unchanged after validation failure: {V.sess_id_cookie()==c0}; csrf token unchanged (same _token still accepted below)')
V.pre_cookie=V.sess_id_cookie()
r,email,pw=register(V,'v2',refresh=False)       # same session, same token, fixed payload: must NOT 419
E.line(f'(vi-b) SAME session+token retry with valid payload: {summarize(r)} body={r.text[:150]}  -> not 419: {r.status_code!=419}')
E.line(f'      store created: {sid_of(email)}; session cookie rotated after success: {V.pre_cookie!=V.sess_id_cookie()}')
r=V.req('GET','/vendor/apply'); newtok=tok(r.text)
E.line(f'      CSRF token rotated after store(): old={t0[:8]}.. new={newtok[:8]}.. rotated={newtok!=t0}; set after store: registration_store_ids={None}')
V.token=newtok
E.line(f'      session file registration_store_ids={V.session_ids()}')
# also wrong captcha early return keeps session
W1=Jar('fixed','wrongcaptcha'); W1.apply_page(); c1=W1.sess_id_cookie()
r,email,pw=register(W1,'wc',captcha='WRONG',refresh=False)
E.line(f'(vi-c) wrong captcha early return: {summarize(r)} body={r.text[:100]} cookie unchanged={W1.sess_id_cookie()==c1}')
# (i)+(ii)
E.line('--- (i)/(ii) owner O1: store(), business_plan subscription-base, payment free_trial')
j,r,email,pw,sid=newowner('o1')
E.line(f'POST /vendor/apply -> {summarize(r)} {r.text[:170]}; cookie rotated: {j.pre_cookie!=j.post_cookie}; token rotated: {j.pre_token!=j.token}; store {sid}; session set={j.session_ids()}')
b=counts([sid]); r=j.req('POST','/vendor/business-plan',data=dict(store_id=sid,business_plan='subscription-base',package_id='1')); a=counts([sid])
hs = (sid in r.text); hf = ('free_trial' in r.text); pm = sorted(set(re.findall(r'name="payment"[^>]*value="([a-z_]+)"', r.text)) | set(re.findall(r'value="([a-z_]+)"[^>]*name="payment"', r.text)))
E.line(f'(i) POST /vendor/business-plan subscription-base pkg 1 -> {summarize(r)} view-has-store-id={hs} view-has-free-trial={hf} payment-options-in-view={pm} logs={len(logs(r.rid))}')
r=j.req('GET',f'/vendor/business-plan?store_id={sid}&business_plan=subscription-base'); E.line(f'    GET secondStep (the store() redirect_url) -> {summarize(r)} logs={len(logs(r.rid))}')
b=counts([sid]); r=j.req('POST','/vendor/payment',data=dict(store_id=sid,package_id='1',payment='free_trial')); a=counts([sid])
L=logs(r.rid); loc=r.headers.get('Location'); r2=j.req('GET',loc[len(SERV['fixed'][0]):]) if loc else None
E.line(f'(ii) POST /vendor/payment pkg 1 free_trial -> {summarize(r)} follow->{r2.status_code if r2 else None} {toasts(r2.text) if r2 else ""} log lines={len(L)}')
E.line(f'     DB before {b}'); E.line(f'     DB after  {a}')
E.line('     trial rows: '+sql(f"select id,store_id,package_id,is_trial,payment_method,payment_status,reference from subscription_transactions where store_id={sid}")+' | store_subscriptions: '+sql(f"select id,store_id,package_id,status from store_subscriptions where store_id={sid}"))
# (iii) gateway
E.line('--- (iii) owner O2: payment with eligible package 1 + active gateway paypal')
j,r,email,pw,sid=newowner('o2')
b=counts([sid]); pre=sql(f"select count(*) from payment_requests where payer_id={sid}")
r=j.req('POST','/vendor/payment',data=dict(store_id=sid,package_id='1',payment='paypal')); a=counts([sid]); L=logs(r.rid)
E.line(f'(iii) POST /vendor/payment pkg 1 paypal store {sid} -> {summarize(r)} log lines={len(L)}')
E.line(f'     DB before {b}'); E.line(f'     DB after  {a}')
E.line('     payment_requests row: '+sql(f"select id,payer_id,payment_method,attribute,attribute_id,is_paid,payment_platform,external_redirect_link is not null from payment_requests where payer_id={sid}"))
E.line(f'     trial rows written? {sql(f"select count(*) from subscription_transactions where store_id={sid}")} (expect 0: gateway not paid)')
# (iv) commission-base
E.line('--- (iv) owner O3: commission-base flips store_business_model')
j,r,email,pw,sid=newowner('o3')
b=counts([sid]); r=j.req('POST','/vendor/business-plan',data=dict(store_id=sid,business_plan='commission-base')); a=counts([sid])
E.line(f'(iv) POST business-plan commission-base store {sid} -> {summarize(r)} complete-page={"register" in r.text.lower() or r.status_code==200} logs={len(logs(r.rid))}')
E.line(f'     before {b[f"store{sid}"]}  after {a[f"store{sid}"]}')
# (v) two stores one jar
E.line('--- (v) two stores created in ONE jar both stay steppable')
j=Jar('fixed','owner-two'); j.apply_page(); r1,e1,_=register(j,'t1',captcha=j.captcha())
j.apply_page(); r2,e2,_=register(j,'t2',captcha=j.captcha())
s1,s2=sid_of(e1),sid_of(e2)
E.line(f'stores {s1} {s2}; both created: {r1.status_code},{r2.status_code}; session set={j.session_ids()}')
for s in (s1,s2):
    r=j.req('POST','/vendor/business-plan',data=dict(store_id=s,business_plan='subscription-base',package_id='1')); E.line(f'   store {s} business_plan -> {summarize(r)} logs={len(logs(r.rid))}')
