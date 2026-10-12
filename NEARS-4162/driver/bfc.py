import sys
from q import *
exec(open('ux1.py').read().split("with Browser() as b:")[0].split("out=[]")[0])
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
DB='multi_food_db_qa4162'
OW4=('john.smith@demo.com','123456789')
def end(ap, mode):
    admin_post(ap,'/admin/store/status/4/0')
    if mode=='expired': admin_post(ap,'/admin/store/status/4/1')
def wait_end_modal(op, timeout=25000):
    op.wait_for_function("() => { const p=document.querySelector('.swal2-popup'); return p && getComputedStyle(p).display !== 'none' && /session|suspend|inactive/i.test(p.innerText); }", timeout=timeout); time.sleep(0.4)
def run(label, bf):
    pw=sync_playwright().start()
    kw={'headless':True}
    if bf: kw['ignore_default_args']=['--disable-back-forward-cache']; kw['args']=['--enable-features=BackForwardCache']
    br=pw.chromium.launch(**kw)
    try:
        a=br.new_context(); ap=login(a,'admin','admin@admin.com','123456789')
        o=br.new_context(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor',*OW4)
        op.goto(BASE+'/vendor-panel/item/add-new', wait_until='load'); time.sleep(1.5); fill_item(op,'QA4162 bfc')
        op.evaluate("() => { document.querySelector('#default_name').dataset.marker='live-dom-not-reloaded'; }")
        end(ap,'expired')
        op.locator('#item_form button[type=submit]').click(); wait_end_modal(op)
        op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P('[%s] after OK: %s' % (label, op.url))
        bk=[]; op.on('response', lambda r: bk.append((r.status, r.url.replace(BASE,''), r.headers.get('cache-control'), r.from_service_worker)) if r.request.resource_type=='document' else None); op.go_back(wait_until='load'); time.sleep(2)
        st=op.evaluate("() => ({url: location.href, marker: (document.querySelector('#default_name')||{dataset:{}}).dataset.marker || null, pageshows: window.__pageshows || null, latch: !!window.nearsPanelSessionEnded, loading: (document.querySelector('#loading')||{}).style ? getComputedStyle(document.querySelector('#loading')).display : null})")
        P('[%s] after Back:' % label, st, '| document responses during Back:', bk)
        if st['marker']=='live-dom-not-reloaded' and st['pageshows'] and any(p['persisted'] for p in st['pageshows']):
            P('[%s] bfcache ENGAGED (pageshow persisted=true, live DOM marker retained)' % label)
            op.locator('#item_form button[type=submit]').click(); wait_end_modal(op, 15000)
            ms=modal_state(op); P('[%s] SECOND refusal on the restored page: modal %r buttons=%s #loading=%s latch=%s' % (label, ms['popup'], ms['buttons_visible'], ms['loading_display'], ms['latch']))
            op.screenshot(path='%s/f1_bfcache_second_modal.png' % EVD)
            op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P('[%s] post-OK %s' % (label, op.url))
        else:
            P('[%s] bfcache not engaged in this engine config (reloaded: url=%s); HARNESS-ONLY for the persisted path' % (label, st['url']))
            try:
                fill_item(op,'QA4162 bfc2')   # category change fires a page ajax (get-categories) = the second refusal on the restored page
                wait_end_modal(op, 15000)
                ms=modal_state(op); P('[%s] SECOND refusal on the back-restored (reloaded-from-cache) page: modal %r buttons=%s #loading=%s latch=%s' % (label, ms['popup'], ms['buttons_visible'], ms['loading_display'], ms['latch']))
                op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P('[%s] post-OK %s' % (label, op.url))
            except Exception as e:
                P('[%s] second refusal on the back-restored page FAILED: %s %s' % (label, type(e).__name__, str(e)[:200]))
    finally:
        br.close(); pw.stop()
run('default-playwright-chromium', False)
run('bfcache-enabled-flags', True)
save('f1_bfcache.txt','\n'.join(out))
