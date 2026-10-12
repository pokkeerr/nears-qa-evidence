from q import *
DB='multi_food_db_qa4162'
OW=('john.smith@demo.com','123456789')
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
def owners(b,n):
    cs=[]
    for i in range(n):
        c=b.ctx(); login(c,'vendor',*OW); cs.append(c)
    return cs
def navflash(ctx, path='/vendor-panel/'):
    # follow redirects, report final url + whether copy present
    rid=str(uuid.uuid4())
    r=ctx.request.fetch(BASE+path, headers=dict(NAV, **{'X-Request-Id':rid}), max_redirects=10)
    t=r.text()
    return r.url, r.status, ('session has expired' in t.lower()), ('suspended' in t.lower())
with Browser() as b:
    a=b.ctx(); ap=login(a,'admin','admin@admin.com','123456789')
    tok=lambda: sql(DB,"select left(sha2(coalesce(login_remember_token,''),256),8) from vendors where id=4")
    # ---------- 1b
    cs=owners(b,4)
    t0=tok(); P('=== 1b setup: 4 owner sessions; vendor token', t0)
    P('approved-owner XHR control (200 expected):', row(fetch(cs[0],'GET','/vendor-panel/','xrw_any')))
    P('admin suspend', admin_post(ap,'/admin/store/status/4/0')); P('admin reactivate', admin_post(ap,'/admin/store/status/4/1'))
    P('vendor token after suspend->reactivate:', tok(), 'CHANGED' if tok()!=t0 else 'UNCHANGED')
    for i,c in enumerate(cs[:3]):
        d=fetch(c,'GET','/vendor-panel/',list(SHAPES)[i]); P(row(d)); P('   log:',d['fail_line_sample'])
    d=fetch(cs[3],'GET','/vendor-panel/','nav'); P('NAV control(no follow)', row(d), 'FAIL lines:', d['fail_lines'], 'all lines for rid:', d['all_log_lines_for_rid'])
    cs2=owners(b,1)
    # second nav control with follow on a fresh stale session is not possible (session consumed); do another stale pair below
    # ---------- 1b nav follow: new stale session
    n=owners(b,1)[0]
    admin_post(ap,'/admin/store/status/4/0'); admin_post(ap,'/admin/store/status/4/1')
    P('NAV control (follow) 1b copy:', navflash(n))
    # ---------- 1e
    g=b.ctx()
    P('=== 1e: no cookie')
    for s in SHAPES:
        d=fetch(b.ctx(),'GET','/vendor-panel/',s); P(row(d), 'all lines for rid:', d['all_log_lines_for_rid'])
    d=fetch(b.ctx(),'GET','/vendor-panel/','nav'); P('NAV control', row(d), 'FAIL lines:', d['fail_lines'], 'all:', d['all_log_lines_for_rid'])
    # ---------- door + keyed guest
    cs=owners(b,4)
    P('=== 4155 door + keyed guest: suspend with 4 live owner sessions')
    P('admin suspend', admin_post(ap,'/admin/store/status/4/0'))
    for i,c in enumerate(cs[:3]):
        s=list(SHAPES)[i]
        d=fetch(c,'GET','/vendor-panel/',s); P('DOOR  ',row(d), '| suspended_lines:', len(grep_log(d['rid'],'vendor.session_suspended')), 'refused_lines:', d['fail_lines'])
        d=fetch(c,'GET','/vendor-panel/',s); P('KEYED ',row(d), '| suspended_lines:', len(grep_log(d['rid'],'vendor.session_suspended')), 'refused_lines:', d['fail_lines'])
    d=fetch(cs[3],'GET','/vendor-panel/','nav'); P('NAV control door', row(d), 'FAIL lines:', d['fail_lines'], 'suspended_lines:', len(grep_log(d['rid'],'vendor.session_suspended')))
    P('admin reactivate', admin_post(ap,'/admin/store/status/4/1'))
save('ac1_owner_arms.txt','\n'.join(out))
