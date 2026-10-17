import sys; sys.path.insert(0,'.')
from api import *
import datetime
R=[]
def chk(name, ok, detail=''):
    R.append((name, ok)); print(('PASS ' if ok else 'FAIL ')+name+(' | '+str(detail) if detail else ''))
def full(nm, ep, **p):
    p.setdefault('limit',200); p.setdefault('offset',1); p.setdefault('with_filters',1)
    return get(nm, ep, p)
today=datetime.datetime(2026,10,17).date()
def age(o): 
    return (today-datetime.datetime.strptime(o['created_at'][:10],'%Y-%m-%d').date()).days
for ep in ('vendor/current-orders','vendor/completed-orders','vendor/canceled-orders'):
    s,jall,h=full('V1',ep)
    ages=sorted(age(o) for o in jall['orders'])
    print(ep,'total',jall['total_size'],'ages',ages)
    pd=items(jall['filters']).get('placed_days'); print(' bounds',pd and pd['bounds'])
    for lo,hi in ((None,7),(None,30),(None,90),(1,8),(7,30),(30,None),(0,1),(8,26)):
        q={}
        if lo is not None: q['placed_days_min']=lo
        if hi is not None: q['placed_days_max']=hi
        s,j,h=full('V1',ep,**q)
        exp=sum(1 for a in ages if (lo is None or a>=lo) and (hi is None or a<hi))
        chk(f'{ep} days[{lo},{hi}) == {exp}', j['total_size']==exp and all(((lo is None or age(o)>=lo) and (hi is None or age(o)<hi)) for o in j['orders']), (j['total_size'],exp))
# facet counts under days window vs list
s,j,h=full('V1','vendor/completed-orders',placed_days_max=30)
st=opts(j['filters'],'status'); print('history status under 30d',st, 'total', j['total_size'])
chk('history status counts sum==total (no selection)', sum(c for _,c,_ in st)==j['total_size'])
# garbage on days
for lab,q in (('neg min','placed_days_min=-5'),('neg max','placed_days_max=-1'),('inverted','placed_days_min=30&placed_days_max=7'),('nonnumeric','placed_days_min=abc&placed_days_max=xyz'),('array','placed_days_min[]=1&placed_days_max[]=5'),('decimal','placed_days_max=7.9'),('huge','placed_days_max=99999999999999999999')):
    s,j,h=get('V1','vendor/current-orders',raw_qs='with_filters=1&limit=200&offset=1&'+q)
    print(lab, s, j.get('total_size') if isinstance(j,dict) else j, j['filters']['applied'] if isinstance(j,dict) and 'filters' in j else None)
    chk('garbage days '+lab+' 200', s==200)
# search
s,j,h=full('V1','vendor/current-orders'); names={}
for o in j['orders']:
    c=o.get('customer'); names[o['id']]=(c or {}).get('f_name','')+' '+(c or {}).get('l_name','') if c else None
print(list(names.items())[:6])
oid=91420
s,js,h=full('V1','vendor/current-orders',search=str(oid)); print('search id', ids(js)); chk('search id exact', oid in ids(js))
first=[v for v in names.values() if v and v.strip()][0].split()[0]
s,js,h=full('V1','vendor/current-orders',search=first); print('search name',first,js['total_size']); chk('search name narrows', 0<js['total_size']<=46)
chk('search total==facets', sum(c for _,c,_ in opts(js['filters'],'status'))<=js['total_size'])
print(' applied after search', js['filters']['applied'])
# search by case
s,js2,h=full('V1','vendor/current-orders',search=first.upper()); chk('search case-insens', js2['total_size']==js['total_size'], (js2['total_size'],js['total_size']))
# partial / full name
s,js3,h=full('V1','vendor/current-orders',search=first[:3]); print('prefix', js3['total_size'])
# garbage search
for lab,qs in (('65char','search='+'a'*65),('64char','search='+'a'*64),('pct','search=%25'),('under','search=_'),('backslash','search=%5C'),('arabic','search='+urllib.parse.quote('أحمد')),('arr','search[]=abc&search[]=def'),('blank','search=%20%20'),('badutf8','search=%FF%FE'),('sql','search=%27%20OR%201%3D1--'),('big','search='+'b'*7000)):
    s,j,h=get('V1','vendor/current-orders',raw_qs='with_filters=1&limit=200&offset=1&'+qs)
    tot=j.get('total_size') if isinstance(j,dict) else j
    print(lab,s,tot, j['filters']['applied'] if isinstance(j,dict) and 'filters' in j else '-')
    chk('garbage search '+lab+' 200', s==200)
# search wildcard literal: % must not match everything
s,j,h=get('V1','vendor/current-orders',raw_qs='with_filters=1&limit=200&offset=1&search=%25'); chk('search % is literal (0 rows)', j['total_size']==0, j['total_size'])
s,j,h=get('V1','vendor/current-orders',raw_qs='with_filters=1&limit=200&offset=1&search=_'); chk('search _ literal (0 rows)', j['total_size']==0, j['total_size'])
s,j,h=get('V1','vendor/current-orders',raw_qs='with_filters=1&limit=200&offset=1&search=a'+'%25'+'b'); print('a%b',j['total_size'])
s,j,h=get('V1','vendor/current-orders',raw_qs='with_filters=1&limit=200&offset=1&search='+'a'*65); chk('65-char ignored -> all 46', j['total_size']==46, j['total_size'])
s,j,h=get('V1','vendor/current-orders',raw_qs='with_filters=1&limit=200&offset=1&search[]=abc'); chk('search[] ignored -> 46', j['total_size']==46, j['total_size'])
# garbage selection values
for lab,qs in (('unknown status','status=bogus'),('status array','status[]=pending&status[]=confirmed'),('status all','status=all'),('pm bogus','payment_method=bogus'),('pm array','payment_method[]=x&payment_method[]=cash_on_delivery'),('campaign 2','campaign_only=2'),('campaign arr','campaign_only[]=1'),('sort bogus','sort=zzz'),('with_filters true','with_filters=true'),('with_filters 0','with_filters=0')):
    s,j,h=get('V1','vendor/current-orders',raw_qs='limit=200&offset=1&with_filters=1&'+qs if 'with_filters' not in qs else 'limit=200&offset=1&'+qs)
    tot=j.get('total_size') if isinstance(j,dict) else j
    print(lab,s,tot, ('filters' in j) if isinstance(j,dict) else '-', j['filters']['applied'] if isinstance(j,dict) and 'filters' in j else '')
    chk('garbage '+lab+' 200', s==200)
print('FAILS:',[n for n,o in R if not o])
