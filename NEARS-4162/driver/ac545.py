from q import *
assert PORT==8163
DB='multi_food_db_qa4162a'
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
def reads():
    return {'wallet': sql(DB,"select total_earning,total_withdrawn,pending_withdraw from store_wallets where vendor_id=4"),
            'refund_hist_rows': sql(DB,"select count(*) from subscription_billing_and_refund_histories where store_id=4"),
            'store(model,package)': sql(DB,"select store_business_model,package_id from stores where id=4"),
            'store_subscriptions(status,is_canceled)': sql(DB,"select status,is_canceled from store_subscriptions where store_id=4")}
def wait_end_modal(op, timeout=25000):
    op.wait_for_function("() => { const p=document.querySelector('.swal2-popup'); return p && getComputedStyle(p).display !== 'none' && /session|suspend|inactive/i.test(p.innerText); }", timeout=timeout); time.sleep(0.4)
with Browser() as b:
    a=b.ctx(); ap=login(a,'admin','admin@admin.com','123456789')
    before=reads(); P('BEFORE', before)
    o=b.ctx(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor','john.smith@demo.com','123456789')
    resp=[]; op.on('response', lambda r: resp.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if ('cancel-subscription' in r.url) else None)
    op.goto(BASE+'/vendor-panel/subscription/subscriber-detail', wait_until='domcontentloaded'); time.sleep(2)
    P('cancel button visible:', op.locator('.status_change_alert').first.is_visible())
    admin_post(ap,'/admin/store/status/4/0'); admin_post(ap,'/admin/store/status/4/1')
    op.locator('.status_change_alert').first.click(); op.wait_for_selector('.swal2-confirm', state='visible'); op.locator('.swal2-confirm').click()
    wait_end_modal(op); ms=modal_state(op)
    P('vendor-subscription:545 cancel-subscription under session-ended owner: responses', resp, '| MODAL', ms['popup'], '| toasts', ms['toasts'], '| #loading', ms['loading_display'])
    P('  no "Successfully canceled" toast:', not any('cancel' in t.lower() for t in ms['toasts']), '| url still', ms['url'])
    op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P('  post-OK', op.url)
    P('AFTER', reads(), 'UNCHANGED' if reads()==before else 'CHANGED')
save('ac545_vendor_subscription_cancel.txt','\n'.join(out))
