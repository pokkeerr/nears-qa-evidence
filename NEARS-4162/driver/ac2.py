import sys
from q import *
assert PORT==8163
DB='multi_food_db_qa4162a'
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
def reads():
    return {'wallet(total_earning,withdrawn,pending)': sql(DB,"select total_earning,total_withdrawn,pending_withdraw from store_wallets where vendor_id=4"),
            'refund_hist_rows_store4': sql(DB,"select count(*) from subscription_billing_and_refund_histories where store_id=4"),
            'store(model,package,status)': sql(DB,"select store_business_model,package_id,status from stores where id=4"),
            'store_subscriptions(status,is_canceled)': sql(DB,"select status,is_canceled from store_subscriptions where store_id=4")}
SUB='/vendor-panel/subscription/subscriber-detail'
def run(b, mode, ap_ctx_page):
    P('=================== MODE', mode)
    P('set mode:', set_notification_mode(b, mode), 'db value:', sql(DB,"select value from business_settings where `key`='order_notification_type'"))
    before=reads(); P('BEFORE', before)
    o=b.ctx(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor','john.smith@demo.com','123456789')
    resp=[]
    op.on('response', lambda r: resp.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if '/vendor-panel/' in r.url else None)
    cons=[]
    op.on('console', lambda m: cons.append(m.text[:160]) if m.type=='error' else None)
    op.goto(BASE+SUB, wait_until='domcontentloaded'); op.locator('button[data-target="#plan-modal"]').first.click(); op.wait_for_selector('.shift_to_commission', state='visible', timeout=20000)
    P('tab A on', op.url, ' shift button present; poll responses so far:', len(resp))
    resp.clear()
    P('admin suspend', admin_post(ap_ctx_page,'/admin/store/status/4/0')); P('admin reactivate', admin_post(ap_ctx_page,'/admin/store/status/4/1'))
    t0=time.time()
    if mode=='firebase':
        time.sleep(11)   # tab idle > one poll interval; firebase mode has no poll
        P('after 11s idle: vendor-panel responses on tab A:', resp, '| modal:', modal_state(op)['popup'])
        op.locator('.shift_to_commission').click(position={'x': 140, 'y': 18})
        op.wait_for_selector('.swal2-confirm', timeout=10000)
        P('confirm Swal text:', modal_state(op)['popup'])
        op.locator('.swal2-confirm').click()
        wait_modal_text = lambda: op.wait_for_function("() => { const p=document.querySelector('.swal2-popup'); return p && /session|suspend|inactive/i.test(p.innerText); }", timeout=20000)
        wait_modal_text()
    else:
        op.wait_for_function("() => { const p=document.querySelector('.swal2-popup'); return p && /session|suspend|inactive/i.test(p.innerText); }", timeout=30000)
    P('modal appeared after %.1fs' % (time.time()-t0))
    ms=modal_state(op); P('MODAL', ms)
    P('vendor-panel responses on tab A (status, method, path, X-Panel-Session):', resp)
    P('console errors:', cons)
    op.screenshot(path='%s/ac2_%s_modal.png' % (EVD, mode))
    # Esc + outside click inert
    op.keyboard.press('Escape'); time.sleep(0.4); P('after Esc modal still:', modal_state(op)['popup'] is not None)
    op.mouse.click(5,5); time.sleep(0.4); P('after outside click modal still:', modal_state(op)['popup'] is not None)
    P('success toast ever shown?', [t for t in modal_state(op)['toasts'] if 'Switched' in t], 'all toasts:', modal_state(op)['toasts'])
    op.locator('.swal2-confirm').click()
    op.wait_for_url(lambda u: '/login/' in u, timeout=15000)
    P('post-OK url:', op.url)
    P('AFTER ', reads(), 'UNCHANGED' if reads()==before else 'CHANGED!')
    P('wallet/model identical to before:', reads()==before)
    # 4155 suspended-door arm
    P('--- 4155 door arm (suspend while tab open, click)')
    o2=b.ctx(); o2.add_init_script(INIT_TOASTS); p2=login(o2,'vendor','john.smith@demo.com','123456789')
    p2.goto(BASE+SUB, wait_until='domcontentloaded'); p2.locator('button[data-target="#plan-modal"]').first.click(); p2.wait_for_selector('.shift_to_commission', state='visible')
    resp2=[]; p2.on('response', lambda r: resp2.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if '/vendor-panel/' in r.url else None)
    P('admin suspend', admin_post(ap_ctx_page,'/admin/store/status/4/0'))
    if mode=='firebase':
        p2.locator('.shift_to_commission').click(position={'x': 140, 'y': 18}); p2.wait_for_selector('.swal2-confirm'); p2.locator('.swal2-confirm').click()
    p2.wait_for_function("() => { const p=document.querySelector('.swal2-popup'); return p && /suspend/i.test(p.innerText); }", timeout=30000)
    P('DOOR MODAL', modal_state(p2)); P('responses', resp2)
    p2.screenshot(path='%s/ac2_%s_door_modal.png' % (EVD, mode))
    p2.locator('.swal2-confirm').click(); p2.wait_for_url(lambda u: '/login/' in u, timeout=15000); P('post-OK url:', p2.url)
    P('admin reactivate', admin_post(ap_ctx_page,'/admin/store/status/4/1'))
    P('AFTER door arm', reads(), 'UNCHANGED' if reads()==before else 'CHANGED!')
with Browser() as b:
    a=b.ctx(); ap=login(a,'admin','admin@admin.com','123456789')
    for mode in sys.argv[1:]:
        run(b, mode, ap)
    set_notification_mode(b,'firebase')
save('ac2_%s.txt' % '_'.join(sys.argv[1:]),'\n'.join(out))
