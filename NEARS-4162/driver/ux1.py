import sys
from q import *
DB='multi_food_db_qa4162'
OW4=('john.smith@demo.com','123456789')
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
SET='/vendor-panel/business-settings/store-setup'
def sched(): return sql(DB,"select group_concat(id order by id) from store_schedule where store_id=4")
def wait_end_modal(op, timeout=25000):
    op.wait_for_function("() => { const p=document.querySelector('.swal2-popup'); return p && getComputedStyle(p).display !== 'none' && /session|suspend|inactive/i.test(p.innerText); }", timeout=timeout); time.sleep(0.4)
def end(ap, mode):
    admin_post(ap,'/admin/store/status/4/0')
    if mode=='expired': admin_post(ap,'/admin/store/status/4/1')
def restore(ap, mode):
    if mode=='suspended': admin_post(ap,'/admin/store/status/4/1')
def owner(b, path, init=True):
    o=b.ctx(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor',*OW4)
    resp=[]
    op.on('response', lambda r: resp.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if ('/vendor-panel/' in r.url and r.request.resource_type in ('xhr','fetch')) else None)
    op.goto(BASE+path, wait_until='domcontentloaded'); time.sleep(2)
    return o,op,resp
def stuck_item_submit(op):
    fill_item(op,'QA4162 ux item'); 
    op.locator('#item_form button[type=submit]').click()
def x_visible(op):
    return op.evaluate("() => { const c=document.querySelector('.swal2-close'); return !!c && getComputedStyle(c).display!=='none' && c.offsetParent!==null; }")
with Browser() as b:
    a=b.ctx(); ap=login(a,'admin','admin@admin.com','123456789')
    # ---- U-key: Enter / Space press OK ; Esc/backdrop inert ; swal2-close visible?
    for key in ['Enter','Space']:
        o,op,resp=owner(b,'/vendor-panel/item/add-new'); fill_item(op,'QA4162 key'); end(ap,'expired')
        op.locator('#item_form button[type=submit]').click(); wait_end_modal(op)
        P('UX key=%s: confirm focused on first paint: %s | swal2-close (x) visible: %s' % (key, modal_state(op)['confirm_focused'], x_visible(op)))
        op.keyboard.press(key); 
        try:
            op.wait_for_url(lambda u:'/login/' in u, timeout=8000); P('  pressing %s activates OK -> %s' % (key, op.url))
        except Exception as e: P('  pressing %s did NOT navigate' % key, modal_state(op)['popup'])
        o.close()
    # ---- U-x: click the visible X (close) button if visible
    o,op,resp=owner(b,'/vendor-panel/item/add-new'); fill_item(op,'QA4162 x'); end(ap,'expired')
    op.locator('#item_form button[type=submit]').click(); wait_end_modal(op)
    xv=x_visible(op); P('UX close-X visible:', xv)
    if xv:
        op.locator('.swal2-close').click(); time.sleep(1.5)
        P('  click X ->', op.url, '| modal still:', modal_state(op)['popup'])
    o.close()
    # ---- Swal-absent fallback
    o,op,resp=owner(b,'/vendor-panel/item/add-new'); fill_item(op,'QA4162 fallback'); end(ap,'expired')
    op.evaluate("() => { window.Swal = undefined; window.__msg = '<b>x</b>'; }")
    t0=time.time(); op.locator('#item_form button[type=submit]').click()
    op.wait_for_selector('#toast-container .toast-error', timeout=15000)
    txt=op.evaluate("() => { const t=document.querySelector('#toast-container .toast-error .toast-message'); return {text:t.innerText, html:t.innerHTML}; }")
    P('UX Swal-absent fallback: persistent toast:', txt, '| #loading', modal_state(op)['loading_display'])
    op.screenshot(path='%s/ux_swal_absent_fallback.png' % EVD)
    op.wait_for_url(lambda u:'/login/' in u, timeout=10000); P('  navigated after %.1fs -> %s' % (time.time()-t0, op.url))
    o.close()
    # ---- Swal-collision (manual mode poll while a delete-confirm Swal is open)
    P('set manual:', set_notification_mode(b,'manual'))
    s0=sched()
    o,op,resp=owner(b,SET)
    op.locator('.delete-schedule').first.click(); op.wait_for_selector('.swal2-confirm', state='visible')
    P('UX collision: confirm Swal open:', modal_state(op)['popup'])
    end(ap,'expired'); resp.clear()
    wait_end_modal(op, 35000)
    ms=modal_state(op)
    P('  collision result: modal now %r buttons=%s | POSTs seen %s | rows unchanged %s' % (ms['popup'], ms['buttons_visible'], [r for r in resp if r[1]=='POST'], sched()==s0))
    time.sleep(1.5); P('  stray delete after 1.5s? POSTs', [r for r in resp if r[1]=='POST'], 'rows', sched()==s0)
    o.close()
    P('set firebase:', set_notification_mode(b,'firebase'))
save('ux1_modal_keys_fallback_collision.txt','\n'.join(out))
