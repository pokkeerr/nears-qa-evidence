import sys
from q import *
DB='multi_food_db_qa4162'
OW4=('john.smith@demo.com','123456789')
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
def open_pos(b, hold_add=False):
    o=b.ctx(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor',*OW4)
    resp=[]
    op.on('response', lambda r: resp.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if ('/vendor-panel/' in r.url and r.request.resource_type in ('xhr','fetch')) else None)
    op.goto(BASE+'/vendor-panel/pos', wait_until='domcontentloaded'); time.sleep(3)
    return o,op,resp
def open_quick(op, pid):
    op.locator('.quick-View[data-id="%s"]' % pid).click()
    op.wait_for_selector('#quick-view .add-To-Cart', state='visible', timeout=15000); time.sleep(0.6)
def add_click(op): op.locator('#quick-view .add-To-Cart').click()
def cart_text(op): return op.evaluate("() => (document.querySelector('#cart')||{}).innerText.replace(/\\s+/g,' ').slice(0,200)")
def wait_end_modal(op):
    op.wait_for_function("() => { const p=document.querySelector('.swal2-popup'); return p && getComputedStyle(p).display !== 'none' && /session|suspend|inactive/i.test(p.innerText); }", timeout=25000); time.sleep(0.5)
def end(ap, mode):
    admin_post(ap,'/admin/store/status/4/0')
    if mode=='expired': admin_post(ap,'/admin/store/status/4/1')
def restore(ap, mode):
    if mode=='suspended': admin_post(ap,'/admin/store/status/4/1')
with Browser() as b:
    a=b.ctx(); ap=login(a,'admin','admin@admin.com','123456789')
    P('=== AC6 CONTROL POS: add-to-cart success (approved not-held owner)')
    o,op,resp=open_pos(b); open_quick(op,115); add_click(op); time.sleep(2.5)
    ms=modal_state(op); P(' toasts', ms['toasts'], 'swal', ms['popup'], 'resp', [r for r in resp if 'pos/' in r[2]]); P(' cart:', cart_text(op))
    P('=== AC6 CONTROL POS business 403 (place order with no customer/payment): own toast, session alive, no modal')
    op.evaluate("() => { window.__toasts = []; }"); resp.clear()
    op.locator('.place-order-submit').first.click(force=True); time.sleep(2.5)
    ms=modal_state(op); P(' toasts', ms['toasts'], 'modal', ms['popup'], 'resp', [r for r in resp if 'pos/' in r[2]], 'latch', ms['latch'])
    d=fetch(o,'GET','/vendor-panel/','xrw_any'); P(' session alive after business refusal:', d['status'])
    o.close()

    P('=== AC5 / pos:616 add-to-cart refused (session expired between page load and click)')
    o,op,resp=open_pos(b); open_quick(op,116); end(ap,'expired'); resp.clear()
    add_click(op); wait_end_modal(op)
    ms=modal_state(op); P(' responses', [r for r in resp if 'pos/' in r[2]], 'MODAL', ms['popup'], 'buttons', ms['buttons_visible'], '#loading', ms['loading_display'], 'toasts', ms['toasts'], 'cart:', cart_text(op))
    op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P(' post-OK', op.url); o.close()

    P('=== AC5 / pos:723 updateCart refused: add-to-cart 200 held, session ended, then released -> success runs updateCart() -> refused')
    o,op,resp=open_pos(b); open_quick(op,117)
    state={'released':False}
    def handler(route):
        r=route.fetch()           # real server round trip: add-to-cart 200 recorded
        end(ap,'expired')         # session ends AFTER add-to-cart succeeded, BEFORE the page's updateCart()
        route.fulfill(response=r)
    op.route('**/vendor-panel/pos/add-to-cart', handler)
    resp.clear(); add_click(op)
    wait_end_modal(op)
    ms=modal_state(op)
    P(' responses', [r for r in resp if 'pos/' in r[2]]); P(' MODAL', ms['popup'], 'buttons', ms['buttons_visible'], '#loading', ms['loading_display'], 'toasts', ms['toasts'])
    P(' #cart text (must not contain login page):', cart_text(op), '| login html pasted?', op.evaluate("() => /Sign In|login|password/i.test(document.querySelector('#cart').innerText)"))
    op.screenshot(path='%s/ac5_updatecart_modal.png' % EVD)
    op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P(' post-OK', op.url); o.close()

    P('=== AC5 / pos:256 place-order chained .fail (duplicate toast) under a marker-held owner')
    o,op,resp=open_pos(b); open_quick(op,118); add_click(op); time.sleep(2.5)
    P(' cart before:', cart_text(op)); op.evaluate("() => { window.__toasts = []; }")
    end(ap,'suspended'); resp.clear()
    op.locator('.place-order-submit').first.click(force=True); wait_end_modal(op); time.sleep(1.2)
    ms=modal_state(op); P(' responses', [r for r in resp if 'pos/' in r[2]], 'MODAL', ms['popup'], 'toasts(.fail duplicate expected)', ms['toasts'], '#loading', ms['loading_display'])
    op.screenshot(path='%s/ac5_placeorder_double_surface.png' % EVD)
    op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P(' post-OK', op.url)
    restore(ap,'suspended'); o.close()
save('ac5_pos.txt','\n'.join(out))
