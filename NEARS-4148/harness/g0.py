import sys; sys.path.insert(0,'.')
from q import *
E=Ev('g0-base-red-and-fixed-same-arms.txt','G0 BASE RED (port 8149 scratch tree = base VendorController+LoginController, no RegistrationSession) vs FIXED (8148), attacker jar, same arms, distinct victims')
pend=sql("select s.id from vendors v join stores s on s.vendor_id=v.id where v.status is null order by s.id").split()
E.line('pending victim store ids (SELECT vendors.status IS NULL): '+' '.join(pend))
E.line('retired package id (nears4145-qa-retired): '+sql("select id from subscription_packages where package_name='nears4145-qa-retired'")+'  rental: '+sql("select id from subscription_packages where package_name='nears4145-qa-rental'")+'  eligible: 1')
RET=sql("select id from subscription_packages where package_name='nears4145-qa-retired'")
def arm(srv, label, victim, params, method='POST', path='/vendor/payment', jar=None, follow=True):
    j=jar or Jar(srv,'attacker'); 
    if not j.token: j.apply_page()
    b=counts([victim]); 
    d=dict(params); 
    r=j.req(method,path,data=d if method=='POST' else None) if method=='POST' else j.req('GET',path+'?'+'&'.join(f'{k}={v}' for k,v in params.items()))
    a=counts([victim])
    E.line(f'[{srv}] {label}: {method} {path} victim={victim} params={ {k:v for k,v in params.items() if k!="_token"} } -> {summarize(r)}')
    if r.status_code>=500: E.line('   body excerpt: '+re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',r.text))[:140])
    loc=r.headers.get('Location')
    if follow and loc and loc.startswith(SERV[srv][0]):
        r2=j.req('GET',loc[len(SERV[srv][0]):]); E.line(f'   follow GET {loc[len(SERV[srv][0]):]} -> HTTP {r2.status_code} toasts={toasts(r2.text)}')
    elif loc: E.line('   (redirect leaves the app: gateway link)')
    E.line(f'   DB before {b}'); E.line(f'   DB after  {a}'); E.line(f'   => {delta(b,a)}')
    L=logs(r.rid,srv); E.line(f'   rid={r.rid} log lines({len(L)}): '+(' || '.join(l[:300] for l in L) or 'none'))
    return j,r
which=sys.argv[1]
if which=='base':
    # victims: first three pending
    va,vb,vc=pend[0],pend[1],pend[2]
    j=Jar('base','attacker'); j.apply_page()
    E.line('--- BASE arms (attacker jar has only GET /vendor/apply: session + _token) ---')
    arm('base','(a) nonexistent package 999999 + free_trial',va,dict(store_id=va,package_id='999999',payment='free_trial'),jar=j)
    arm('base','(b) RETIRED package + free_trial',vb,dict(store_id=vb,package_id=RET,payment='free_trial'),jar=j)
    arm('base','(c) RETIRED package + paypal (active gateway)',vc,dict(store_id=vc,package_id=RET,payment='paypal'),jar=j)
    arm('base','(AC1) GET /vendor/back non-owner reads victim step page',vc,dict(store_id=vc),method='GET',path='/vendor/back',jar=j)
    # commission-flip victim: created by an OWNER jar at base (model none)
    o=Jar('base','owner'); o.apply_page(); r,email,pw=register(o,'b0'); 
    E.line(f'owner jar creates a real victim on base via POST /vendor/apply: {summarize(r)} body={r.text[:160]}')
    vid=sql(f"select s.id from stores s join vendors v on v.id=s.vendor_id where v.email='{email}'")
    E.line(f'victim {vid}: {counts([vid])["store"+vid]}')
    arm('base','(AC1) NON-OWNER business_plan commission-base flips victim store_business_model',vid,dict(store_id=vid,business_plan='commission-base'),path='/vendor/business-plan',jar=j)
if which=='fixed':
    pend=[p for p in pend]
    va,vb,vc=pend[3],pend[4],pend[5]
    j=Jar('fixed','attacker'); j.apply_page()
    E.line('--- FIXED arms (same attacker shape, DIFFERENT victims; attacker jar has only GET /vendor/apply: session + _token) ---')
    arm('fixed','(a) nonexistent package 999999 + free_trial',va,dict(store_id=va,package_id='999999',payment='free_trial'),jar=j)
    arm('fixed','(b) RETIRED package + free_trial',vb,dict(store_id=vb,package_id=RET,payment='free_trial'),jar=j)
    arm('fixed','(c) RETIRED package + paypal (active gateway)',vc,dict(store_id=vc,package_id=RET,payment='paypal'),jar=j)
    arm('fixed','(AC1) GET /vendor/back non-owner',vc,dict(store_id=vc),method='GET',path='/vendor/back',jar=j)
    o=Jar('fixed','owner'); o.apply_page(); r,email,pw=register(o,'f0')
    E.line(f'owner jar creates a real victim on FIXED via POST /vendor/apply: {summarize(r)} body={r.text[:160]}')
    vid=sql(f"select s.id from stores s join vendors v on v.id=s.vendor_id where v.email='{email}'")
    E.line(f'victim {vid}: {counts([vid])["store"+vid]}')
    arm('fixed','(AC1) NON-OWNER business_plan commission-base on victim',vid,dict(store_id=vid,business_plan='commission-base'),path='/vendor/business-plan',jar=j)
    # owner positive control for the same victim (proves victim IS steppable by its owner)
