from q import *
DB='multi_food_db_qa4162'
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
with Browser() as b:
    o=b.ctx(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor','john.smith@demo.com','123456789')
    resp=[]
    op.on('response', lambda r: resp.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if ('/vendor-panel/item' in r.url and r.request.resource_type in ('xhr','fetch','document')) else None)
    op.goto(BASE+'/vendor-panel/item/add-new', wait_until='domcontentloaded'); time.sleep(1.5)
    fill_item(op,'QA4162 ctl item 2'); resp.clear()
    op.locator('#item_form button[type=submit]').click(); time.sleep(1.2)
    ms=modal_state(op); P('PRODUCT ADD control: toasts', ms['toasts'], 'modal', ms['popup'], 'resp', resp[:3])
    time.sleep(3); P('  lands on', op.url); 
    price0=sql(DB,"select price from items where id=16")
    op.goto(BASE+'/vendor-panel/item/edit/16', wait_until='domcontentloaded'); time.sleep(2); resp.clear()
    op.evaluate("() => { document.querySelector('#unit_price').value='11.5'; }")
    op.locator('#product_form button[type=submit]').click(); time.sleep(1.2)
    ms=modal_state(op); P('PRODUCT UPDATE control: toasts', ms['toasts'], 'modal', ms['popup'], 'resp', resp[:3], 'price before/after', price0, sql(DB,"select price from items where id=16"))
    save('ac6_product_controls.txt','\n'.join(out))
