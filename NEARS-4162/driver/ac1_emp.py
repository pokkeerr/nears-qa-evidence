from q import *
DB='multi_food_db_qa4162'
EMAIL='qa4162.employee@nears-qa.test'; PW='Qa#4162-Emp!x9Zk'
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
def emp_login(b, n):
    cs=[]
    for i in range(n):
        c=b.ctx(); login(c,'vendor_employee',EMAIL,PW); cs.append(c)
    return cs
def tokstate(): return sql(DB,"select left(sha2(coalesce(login_remember_token,''),256),8), is_logged_in from vendor_employees where id=2")
with Browser() as b:
    a=b.ctx(); ap=login(a,'admin','admin@admin.com','123456789')
    # ---- arm 1d-i : owner saves employee form
    cs=emp_login(b,4)   # 3 shapes + 1 nav control
    for i,c in enumerate(cs[:3]): 
        d=fetch(c,'GET','/vendor-panel/',list(SHAPES)[i]); P('PRE', row(d))
    P('state before owner save (md5(token), is_logged_in):', tokstate())
    o=b.ctx(); op=login(o,'vendor','john.smith@demo.com','123456789')
    op.goto(BASE+'/vendor-panel/employee/edit/2', wait_until='domcontentloaded')
    op.locator('form button.btn--primary[type=submit]').first.click()
    op.wait_for_load_state('domcontentloaded'); time.sleep(1.5)
    P('owner saved employee form ->', op.url, op.locator('.toast-message').all_inner_texts())
    P('state after owner save:', tokstate())
    P('=== 1d-i (employee is_logged_in=0) ===')
    for i,c in enumerate(cs[:3]):
        d=fetch(c,'GET','/vendor-panel/',list(SHAPES)[i]); P(row(d)); P('   log:',d['fail_line_sample'])
    d=fetch(cs[3],'GET','/vendor-panel/','nav'); P('NAV control', row(d), 'new FAIL lines for rid:', d['fail_lines'], 'all lines for rid:', d['all_log_lines_for_rid'])
    # ---- arm 1d-iii : suspend
    cs=emp_login(b,4)
    P('=== 1d-iii setup: employees re-logged in; state', tokstate())
    r=admin_post(ap,'/admin/store/status/4/0'); P('admin suspend', r)
    P('stores 4 status/suspended_at:', sql(DB,'select status,suspended_at from stores where id=4'))
    for i,c in enumerate(cs[:3]):
        d=fetch(c,'GET','/vendor-panel/',list(SHAPES)[i]); P(row(d)); P('   log:',d['fail_line_sample'])
    d=fetch(cs[3],'GET','/vendor-panel/','nav'); P('NAV control', row(d), 'FAIL lines:', d['fail_lines'], 'all lines:', d['all_log_lines_for_rid'])
    r=admin_post(ap,'/admin/store/status/4/1'); P('admin reactivate', r)
    # ---- arm 1d-iv : idle through suspend -> reactivate
    cs=emp_login(b,4)
    t0=tokstate(); P('=== 1d-iv setup: employees logged in; state', t0)
    r=admin_post(ap,'/admin/store/status/4/0'); P('admin suspend', r)
    r=admin_post(ap,'/admin/store/status/4/1'); P('admin reactivate', r)
    t1=tokstate(); P('state after suspend->reactivate (token md5 changed?):', t1, 'CHANGED' if t0.split()[0]!=t1.split()[0] else 'UNCHANGED')
    for i,c in enumerate(cs[:3]):
        d=fetch(c,'GET','/vendor-panel/',list(SHAPES)[i]); P(row(d)); P('   log:',d['fail_line_sample'])
    d=fetch(cs[3],'GET','/vendor-panel/','nav'); P('NAV control', row(d), 'FAIL lines:', d['fail_lines'], 'all lines:', d['all_log_lines_for_rid'])
save('ac1_employee_arms.txt','\n'.join(out))
