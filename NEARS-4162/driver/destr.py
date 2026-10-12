from q import *
DB='multi_food_db_qa4162'
OW4=('john.smith@demo.com','123456789'); OW5=('maria.garcia@demo.com','123456789')
EMAIL='qa4162.emp5@nears-qa.test'; PW='Qa#4162-Emp!x9Zk'
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
IMG=IMGDIR+'emp400.png'
def wait_end_modal(op, timeout=25000):
    op.wait_for_function("() => { const p=document.querySelector('.swal2-popup'); return p && getComputedStyle(p).display !== 'none' && /session|suspend|inactive|store/i.test(p.innerText); }", timeout=timeout); time.sleep(0.4)
def admin_req(ap, method, path, data=None):
    tok=csrf_of(ap)
    return ap.evaluate("""async ([m,p,t,d]) => { const fd = new URLSearchParams(d||{}); const r = await fetch(p,{method:m, body: m==='DELETE'? null : fd, headers:{'X-CSRF-TOKEN':t,'X-Requested-With':'XMLHttpRequest','Accept':'application/json'},credentials:'same-origin'}); return {status:r.status, url:r.url, redirected:r.redirected, body:(await r.text()).slice(0,160)}; }""",[method,path,tok,data])
with Browser() as b:
    a=b.ctx(); ap=login(a,'admin','admin@admin.com','123456789')
    # ---------- 1a : admin denies application (route admin/store/update-application/{id}/{status})
    P('=== 1a owner !status: admin POST admin/store/update-application/4/0 (the real application-deny action; route accepts any store id)')
    owners=[]
    for i in range(4):
        c=b.ctx(); login(c,'vendor',*OW4); owners.append(c)
    P(' vendor 4 status before:', sql(DB,'select status from vendors where id=4'))
    P(' admin deny:', admin_req(ap,'POST','/admin/store/update-application/4/0',{'rejection_note':'QA4162 1a'}))
    P(' vendor 4 status after:', sql(DB,'select status from vendors where id=4'))
    for i,c in enumerate(owners[:3]):
        d=fetch(c,'GET','/vendor-panel/',list(SHAPES)[i]); P(row(d)); P('   log:', d['fail_line_sample'])
    d=fetch(owners[3],'GET','/vendor-panel/','nav'); P('NAV control', row(d), 'FAIL lines', d['fail_lines'], 'all lines', d['all_log_lines_for_rid'])
    P(' admin approve (restore):', admin_req(ap,'POST','/admin/store/update-application/4/1',{}))
    P(' vendor 4 status/store status after restore:', sql(DB,'select v.status, s.status from vendors v join stores s on s.vendor_id=v.id where v.id=4'))
    # 1a UI modal copy + screenshot
    P('=== 1a UI modal (account inactive copy)')
    o=b.ctx(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor',*OW4)
    op.goto(BASE+'/vendor-panel/item/add-new', wait_until='domcontentloaded'); time.sleep(1.5); fill_item(op,'QA4162 1a')
    admin_req(ap,'POST','/admin/store/update-application/4/0',{'rejection_note':'QA4162 1a'})
    op.locator('#item_form button[type=submit]').click(); wait_end_modal(op); ms=modal_state(op)
    P(' MODAL', ms['popup'], 'buttons', ms['buttons_visible'], '#loading', ms['loading_display'], 'toasts', ms['toasts'])
    op.screenshot(path='%s/ux_account_inactive_modal_1a.png' % EVD)
    op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P(' post-OK', op.url)
    admin_req(ap,'POST','/admin/store/update-application/4/1',{})
    o.close()
    # ---------- 1d-ii : employee of a store the admin deletes
    P('=== 1d-ii employee null store: employee logged in, admin deletes the store (admin DELETE admin/store/delete/5)')
    ow=b.ctx(); owp=login(ow,'vendor',*OW5)
    owp.goto(BASE+'/vendor-panel/custom-role/create', wait_until='domcontentloaded')
    owp.evaluate("() => { document.querySelector('#name').value='QA4162 Role5'; document.querySelector('#nameen').value='QA4162 Role5'; document.querySelectorAll('input[name=\"modules[]\"]').forEach(c=>{c.checked=true}); }")
    owp.locator('button.btn--primary[type=submit]').first.click(); owp.wait_for_load_state('domcontentloaded'); time.sleep(1)
    P(' role toasts', owp.locator('.toast-message').all_inner_texts())
    owp.goto(BASE+'/vendor-panel/employee/add-new', wait_until='domcontentloaded')
    owp.fill('#f_name','Qa'); owp.fill('#l_name','Emp5'); owp.fill('#phone','+971501234165')
    owp.evaluate("() => { const s=document.querySelector('#role_id'); const opt=[...s.options].find(o=>o.text.includes('QA4162')); s.value=opt.value; $(s).trigger('change'); }")
    owp.set_input_files('#customFileUpload', IMG); owp.fill('#email',EMAIL); owp.fill('#signupSrPassword',PW); owp.fill('#signupSrConfirmPassword',PW)
    owp.locator('button.btn--primary[type=submit]').first.click(); owp.wait_for_load_state('domcontentloaded'); time.sleep(1.5)
    P(' employee toasts', owp.locator('.toast-message').all_inner_texts(), '| rows:', sql(DB,"select id,store_id from vendor_employees where email='%s'" % EMAIL))
    ecs=[]
    for i in range(4):
        c=b.ctx(); login(c,'vendor_employee',EMAIL,PW); ecs.append(c)
    # one real UI tab for modal copy
    eo=b.ctx(); eo.add_init_script(INIT_TOASTS); ep=login(eo,'vendor_employee',EMAIL,PW)
    ep.goto(BASE+'/vendor-panel/item/add-new', wait_until='domcontentloaded'); time.sleep(1.5)
    P(' admin delete store 5:', admin_req(ap,'DELETE','/admin/store/delete/5'))
    P(' store 5 exists after:', sql(DB,'select count(*) from stores where id=5'), '| employee store_id', sql(DB,"select store_id from vendor_employees where email='%s'" % EMAIL))
    for i,c in enumerate(ecs[:3]):
        d=fetch(c,'GET','/vendor-panel/',list(SHAPES)[i]); P(row(d)); P('   log:', d['fail_line_sample'], '| all lines for rid:', d['all_log_lines_for_rid'])
    d=fetch(ecs[3],'GET','/vendor-panel/','nav'); P('NAV control', row(d), 'FAIL lines', d['fail_lines'], 'all lines', d['all_log_lines_for_rid'])
    ep.evaluate("() => { const s = document.querySelector('#category_id'); s.value = s.options[1].value; $(s).trigger('change'); }")
    wait_end_modal(ep, 15000); ms=modal_state(ep)
    P(' UI MODAL (employee, no store)', ms['popup'], 'buttons', ms['buttons_visible'], '#loading', ms['loading_display'])
    ep.screenshot(path='%s/ux_no_store_modal_1d-ii.png' % EVD)
    ep.locator('.swal2-confirm').click(); ep.wait_for_url(lambda u:'/login/' in u); P(' post-OK', ep.url)
save('ac1_destructive_1a_1d-ii.txt','\n'.join(out))
