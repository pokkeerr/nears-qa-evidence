from q import *
DB='multi_food_db_qa4162'
EMAIL='qa4162.employee@nears-qa.test'; PW='Qa#4162-Emp!x9Zk'
SET='/vendor-panel/business-settings/store-setup'
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
def sched(): return sql(DB,"select group_concat(id order by id) from store_schedule where store_id=4")
def wait_end_modal(op, timeout=25000):
    op.wait_for_function("() => { const p=document.querySelector('.swal2-popup'); return p && getComputedStyle(p).display !== 'none' && /session|suspend|inactive/i.test(p.innerText); }", timeout=timeout); time.sleep(0.4)
def emp(b):
    o=b.ctx(); o.add_init_script(INIT_TOASTS); op=login(o,'vendor_employee',EMAIL,PW)
    resp=[]
    op.on('response', lambda r: resp.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if ('/vendor-panel/' in r.url and r.request.resource_type in ('xhr','fetch')) else None)
    op.goto(BASE+SET, wait_until='domcontentloaded'); time.sleep(2)
    return o,op,resp
def trigger(op):
    op.locator('.delete-schedule').first.click(); op.wait_for_selector('.swal2-confirm', state='visible'); op.locator('.swal2-confirm').click()
def finish(op, resp, label, shot=None):
    wait_end_modal(op); ms=modal_state(op)
    P(' [%s] responses %s' % (label, [r for r in resp if r[3]=='ended' or r[0]>=400]))
    P(' [%s] MODAL %r buttons=%s #loading=%s toasts=%s' % (label, ms['popup'], ms['buttons_visible'], ms['loading_display'], ms['toasts']))
    if shot: op.screenshot(path='%s/%s' % (EVD, shot))
    op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P(' [%s] post-OK url %s  (employee login URL expected /login/vendor-employee)' % (label, op.url))
with Browser() as b:
    a=b.ctx(); ap=login(a,'admin','admin@admin.com','123456789')
    s0=sched()
    P('=== AC7 arm i (1d-i): owner saves the employee form while the employee tab is open')
    o,op,resp=emp(b)
    ow=b.ctx(); owp=login(ow,'vendor','john.smith@demo.com','123456789')
    owp.goto(BASE+'/vendor-panel/employee/edit/2', wait_until='domcontentloaded'); owp.locator('form button.btn--primary[type=submit]').first.click(); owp.wait_for_load_state('domcontentloaded'); time.sleep(1.5)
    P(' employee is_logged_in now:', sql(DB,'select is_logged_in from vendor_employees where id=2'))
    resp.clear(); trigger(op); finish(op,resp,'i')
    P(' schedule rows unchanged:', sched()==s0); o.close(); ow.close()
    P('=== AC7 arm iii (1d-iii): admin suspends the store, employee acts')
    o,op,resp=emp(b)
    P(' admin suspend', admin_post(ap,'/admin/store/status/4/0')); resp.clear()
    trigger(op); finish(op,resp,'iii','ac7_employee_inactive_store_modal.png')
    P(' admin reactivate', admin_post(ap,'/admin/store/status/4/1')); P(' schedule rows unchanged:', sched()==s0); o.close()
    P('=== AC7 arm iv (1d-iv): employee tab idle through suspend -> reactivate')
    o,op,resp=emp(b)
    admin_post(ap,'/admin/store/status/4/0'); admin_post(ap,'/admin/store/status/4/1'); resp.clear()
    trigger(op); finish(op,resp,'iv'); P(' schedule rows unchanged:', sched()==s0); o.close()
save('ac7_employee_ui.txt','\n'.join(out))
