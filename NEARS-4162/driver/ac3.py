import sys, traceback
from q import *
DB='multi_food_db_qa4162'
OW4=('john.smith@demo.com','123456789'); OW13=('freshsupermarket@demo.com','123456789')
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
FALSE_OK=('Successfully','added','updated','Added','Updated','generated','success')

def end_session(ap, store_id, mode):
    if mode=='suspended':
        admin_post(ap,'/admin/store/status/%d/0' % store_id)
    else:
        admin_post(ap,'/admin/store/status/%d/0' % store_id); admin_post(ap,'/admin/store/status/%d/1' % store_id)
def restore(ap, store_id, mode):
    if mode=='suspended': admin_post(ap,'/admin/store/status/%d/1' % store_id)

def sc(b, ap, key, site, cred, store_id, path, prep, trigger, mode, shot=False):
    P('---- %s  [%s]  owner=%s store=%d session-end=%s' % (key, site, cred[0], store_id, mode))
    o=b.ctx(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor',*cred)
    resp=[]
    op.on('response', lambda r: resp.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if ('/vendor-panel/' in r.url and r.request.resource_type in ('xhr','fetch')) else None)
    try:
        op.goto(BASE+path, wait_until='domcontentloaded'); time.sleep(2)
        prep(op)
        resp.clear()
        end_session(ap, store_id, mode)
        trigger(op)
        op.wait_for_function("() => { const p=document.querySelector('.swal2-popup'); return p && getComputedStyle(p).display !== 'none' && /session|suspend|inactive/i.test(p.innerText); }", timeout=25000)
        time.sleep(0.5)
        ms=modal_state(op)
        P('  responses:', [r for r in resp if r[3]=='ended' or r[0]>=400] or resp)
        P('  MODAL text=%r buttons_visible=%s cancel=%s confirm_focused=%s | #loading=%s loading_seen_during=%s latch=%s' % (ms['popup'], ms['buttons_visible'], ms['cancel_visible'], ms['confirm_focused'], ms['loading_display'], ms['loading_seen'], ms['latch']))
        bad=[t for t in ms['toasts'] if any(w in t for w in FALSE_OK)]
        P('  toasts:', ms['toasts'], '| false-success toast:', bad or 'none')
        n_modals=op.evaluate("() => document.querySelectorAll('.swal2-popup').length")
        P('  swal popups in DOM:', n_modals)
        if shot: op.screenshot(path='%s/ac3_%s.png' % (EVD,key)); P('  shot ac3_%s.png' % key)
        op.locator('.swal2-confirm').click()
        op.wait_for_url(lambda u: '/login/' in u, timeout=15000)
        P('  OK -> url', op.url)
        res='PASS' if (ms['loading_display']=='none' and not bad and ms['buttons_visible']==1 and n_modals==1 and '/login/vendor' in op.url) else 'FAIL'
        P('  RESULT', res)
    except Exception as e:
        P('  EXCEPTION', type(e).__name__, str(e)[:300]); res='ERROR'
        try: P('  state', modal_state(op))
        except Exception: pass
    finally:
        restore(ap, store_id, mode)
        o.close()
    return res

# ---- preps / triggers
def prep_item_new(op): fill_item(op,'QA4162 stuck item')
def trig_submit_item(op): op.locator('#item_form button[type=submit]').click()
def trig_submit_edit(op): op.locator('#product_form button[type=submit]').click()
def prep_attr(op):
    op.evaluate("() => { const s=document.querySelector('#choice_attributes'); [...s.options].forEach(o=>o.selected=(o.value=='1')); $(s).trigger('change'); }")
    op.wait_for_selector('#customer_choice_options .bootstrap-tagsinput input', state='visible', timeout=10000)
def trig_tag(op):
    inp=op.locator('#customer_choice_options .bootstrap-tagsinput input').first
    inp.click(); inp.type('S'); inp.press('Enter')
def trig_gen_value(op):
    op.locator('#item_form_2 button[type=submit]').click()
def prep_food_variation(op):
    op.locator('#add_new_option_button').click(); time.sleep(0.5)
    op.locator('input[name="options[1][name]"]').fill('QA Size')
    op.locator('input[name="options[1][min]"]').fill('1'); op.locator('input[name="options[1][max]"]').fill('1')
    op.locator('.add_new_row_button[data-count="1"]').click(); time.sleep(0.5)
    op.evaluate("() => { document.querySelectorAll('#option_price_view_1 input').forEach((e,i) => { e.value = (e.type == 'number') ? '1' : ('Opt' + i); e.dispatchEvent(new Event('input', {bubbles: true})); }); }")
def trig_food_gen(op): op.locator('#item_form button[type=submit]').click()
def prep_ad(op): fill_ad(op,'QA4162 stuck ad')
def trig_ad_submit(op): op.locator('form button[type=submit]').last.click()

ONLY=sys.argv[1:]
SC=[
 ('T1_add-new_item.store','product/index:383 (3a)',OW4,4,'/vendor-panel/item/add-new',prep_item_new,trig_submit_item,'suspended',True),
 ('T2_add-new_combination','product/index:316 (3b)',OW13,13,'/vendor-panel/item/add-new',prep_attr,trig_tag,'expired',False),
 ('T3_edit_item.update','product/edit:572 (3a)',OW4,4,'/vendor-panel/item/edit/16',lambda op:None,trig_submit_edit,'expired',False),
 ('T4_edit_combination','product/edit:504 (3b)',OW13,13,'/vendor-panel/item/edit/203',prep_attr,trig_tag,'suspended',False),
 ('T5a_bulk_combination','bulk-import:448 (3b)',OW13,13,'/vendor-panel/item/bulk-import',prep_attr,trig_tag,'suspended',False),
 ('T5b_bulk_variation-generate','bulk-import:477 (3c)',OW13,13,'/vendor-panel/item/bulk-import',prep_attr,trig_gen_value,'expired',True),
 ('T6_bulk_food-variation','bulk-import:513 (3c)',OW4,4,'/vendor-panel/item/bulk-import',prep_food_variation,trig_food_gen,'suspended',False),
 ('T7_ad_create','advertisement/create:531 (3d)',OW4,4,'/vendor-panel/advertisement/create',prep_ad,trig_ad_submit,'expired',True),
 ('T8_ad_edit','advertisement/edit:584 (3d)',OW4,4,'/vendor-panel/advertisement/1000001/edit',lambda op:None,trig_ad_submit,'suspended',False),
]
results={}
with Browser() as b:
    a=b.ctx(); ap=login(a,'admin','admin@admin.com','123456789')
    for key,site,cred,sid,path,prep,trig,mode,shot in SC:
        if ONLY and not any(key.startswith(x) for x in ONLY): continue
        results[key]=sc(b,ap,key,site,cred,sid,path,prep,trig,mode,shot)
P('SUMMARY', results)
save('ac3_%s.txt' % ('_'.join(ONLY) or 'all'), '\n'.join(out))
