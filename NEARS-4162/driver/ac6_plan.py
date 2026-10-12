from q import *
assert PORT==8163
DB='multi_food_db_qa4162a'
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
def reads():
    return {'wallet': sql(DB,"select total_earning,total_withdrawn,pending_withdraw from store_wallets where vendor_id=4"),
            'refund_hist_rows': sql(DB,"select count(*) from subscription_billing_and_refund_histories where store_id=4"),
            'store(model,package)': sql(DB,"select store_business_model,package_id from stores where id=4")}
with Browser() as b:
    P('set manual:', set_notification_mode(b,'manual'))
    o=b.ctx(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor','john.smith@demo.com','123456789')
    resp=[]
    op.on('response', lambda r: resp.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if ('get-store-data' in r.url) else None)
    op.goto(BASE+'/vendor-panel/subscription/subscriber-detail', wait_until='domcontentloaded'); resp.clear()
    time.sleep(24)
    ms=modal_state(op)
    P('REGRESSION: manual-mode 10s poll for a NOT-held owner over 24s: get-store-data responses', resp, '| modal', ms['popup'], '| latch', ms['latch'], '| toasts', ms['toasts'])
    o.close()
    P('set firebase:', set_notification_mode(b,'firebase'))
    before=reads(); P('BEFORE', before)
    o=b.ctx(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor','john.smith@demo.com','123456789')
    resp=[]; op.on('response', lambda r: resp.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if ('switch-to-commission' in r.url) else None)
    op.goto(BASE+'/vendor-panel/subscription/subscriber-detail', wait_until='domcontentloaded'); time.sleep(1.5)
    op.locator('button[data-target="#plan-modal"]').first.click(); op.wait_for_selector('.shift_to_commission', state='visible')
    op.locator('.shift_to_commission').click(position={'x':140,'y':18}); op.wait_for_selector('.swal2-confirm'); op.locator('.swal2-confirm').click()
    t0=time.time()
    time.sleep(1.2)
    op.wait_for_load_state('domcontentloaded'); time.sleep(3)
    ss=op.evaluate("() => JSON.parse(sessionStorage.getItem('__toasts_ss') || '[]')")
    ms=modal_state(op); P('AC6 CONTROL Shift In This Plan > Yes (approved, not-held): toasts seen (persisted across the reload)', ss, 'resp', resp, 'modal(session) after reload', ms['popup'])
    P('  after reload url', op.url, '| AFTER', reads())
    save('ac6_plan_poll_controls.txt','\n'.join(out))
