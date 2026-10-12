from q import *
DB='multi_food_db_qa4162'
OW4=('john.smith@demo.com','123456789')
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
def wait_end_modal(op, timeout=25000):
    op.wait_for_function("() => { const p=document.querySelector('.swal2-popup'); return p && getComputedStyle(p).display !== 'none' && /session|suspend|inactive/i.test(p.innerText); }", timeout=timeout); time.sleep(0.4)
with Browser() as b:
    P('=== 1e live in browser, POST arm: owner tab open with a filled form, session cookie deleted, submit (expected: CSRF 419 precedes VendorMiddleware; D6 named residual)')
    o=b.ctx(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor',*OW4)
    resp=[]; op.on('response', lambda r: resp.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if ('/vendor-panel/' in r.url and r.request.resource_type in ('xhr','fetch')) else None)
    op.goto(BASE+'/vendor-panel/item/add-new', wait_until='domcontentloaded'); time.sleep(1.5); fill_item(op,'QA4162 1e')
    o.clear_cookies(); resp.clear(); op.locator('#item_form button[type=submit]').click(); time.sleep(4)
    ms=modal_state(op); P(' responses', resp, '| MODAL', ms['popup'], '| #loading', ms['loading_display'])
    o.close()
    P('=== 1e live in browser, GET arm: owner tab open, cookies deleted, then a page ajax GET (category change -> item/get-categories)')
    o=b.ctx(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor',*OW4)
    resp=[]; op.on('response', lambda r: resp.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if ('/vendor-panel/' in r.url and r.request.resource_type in ('xhr','fetch')) else None)
    op.goto(BASE+'/vendor-panel/item/add-new', wait_until='domcontentloaded'); time.sleep(1.5)
    o.clear_cookies(); resp.clear()
    op.evaluate("() => { const s = document.querySelector('#category_id'); s.value = s.options[1].value; $(s).trigger('change'); }")
    wait_end_modal(op, 15000)
    ms=modal_state(op); P(' responses', resp, '| MODAL', ms['popup'], '| #loading', ms['loading_display'], '| toasts', ms['toasts'])
    op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P(' post-OK', op.url)
    P('=== regression sweep: owner login -> dashboard -> logout -> login again')
    o2=b.ctx(); p2=login(o2,'vendor',*OW4); P(' login landed', p2.url, '| dashboard 200:', fetch(o2,'GET','/vendor-panel/','nav')['status'])
    p2.goto(BASE+'/vendor-panel/auth/logout', wait_until='domcontentloaded'); d=fetch(o2,'GET','/vendor-panel/','nav'); P(' logout ->', p2.url, '| next nav status', d['status'], 'loc', d['location'])
    p3=login(o2,'vendor',*OW4); P(' re-login landed', p3.url)
save('ac1e_ui_and_sweep.txt','\n'.join(out))
