import sys; sys.argv=['x']
exec(open('mix.py').read().split('out=[]')[0])
for n,l in [('a mixed 390x2+392x2',[(390,2),(392,2)]),('b flash-only 388+390',[(388,1),(390,1)]),('c non-flash 395',[(395,1)])]:
    r=go(n,l,2,39); o=r['order']; g=r['gettax']
    D=dq(round(g['total_discount'],4)); pv=q2(dq(r['P'])-q2(D)+dq(str(g['tax_amount'])))
    print(n,'| P',r['P'],'| get-Tax disc',round(g['total_discount'],4),'tax',round(g['tax_amount'],4),'preview total',pv,'| placed order',r['order']['id'],'order_amount',o['order_amount'],'sd',o['store_discount_amount'],'fa',o['flash_admin_discount_amount'],'fv',o['flash_store_discount_amount'],'tax',o['total_tax_amount'])
clear()
