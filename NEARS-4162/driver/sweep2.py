from q import *
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
OW4=('john.smith@demo.com','123456789')
with Browser() as b:
    o2=b.ctx(); p2=login(o2,'vendor',*OW4); P('login landed', p2.url, '| dashboard 200:', fetch(o2,'GET','/vendor-panel/','nav')['status'])
    p2.goto(BASE+'/logout', wait_until='domcontentloaded'); d=fetch(o2,'GET','/vendor-panel/','nav'); P('logout ->', p2.url, '| next plain nav status', d['status'], 'loc', d['location'])
    d=fetch(o2,'GET','/vendor-panel/','xrw_any'); P('ajax after logout (1e)', row(d))
    p3=login(o2,'vendor',*OW4); P('re-login landed', p3.url)
    # plain guest navigation: 302 home
    g=b.ctx(); d=fetch(g,'GET','/vendor-panel/item/list','nav'); P('guest plain navigation:', d['status'], d['location'], 'FAIL lines', d['fail_lines'])
save('sweep_login_logout.txt','\n'.join(out))
