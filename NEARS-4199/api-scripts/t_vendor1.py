import sys; sys.path.insert(0,'.')
from api import *
import datetime
R=[]
def chk(name, ok, detail=''):
    R.append((name, ok)); print(('PASS ' if ok else 'FAIL ')+name+(' | '+str(detail) if detail else ''))
def full(nm, ep, **p):
    p.setdefault('limit',200); p.setdefault('offset',1); p.setdefault('with_filters',1)
    return get(nm, ep, p)
# --- shape
s,j,h=full('V1','vendor/current-orders')
fb=j['filters']
chk('block keys', set(fb.keys())=={'applied','counts_omitted','items','sort'} or set(fb.keys())>={'applied','counts_omitted','items'}, sorted(fb.keys()))
print('item keys:', [i['key'] for i in fb['items']])
chk('item 11-key', all(set(i.keys())=={'key','request_key','request_keys','type','names','quick','options','selection','bounds','unit','presets'} for i in fb['items']), set(fb['items'][0].keys()))
chk('status tiles pending/conf/proc/hand/picked = 23/8/5/5/4', opts(fb,'status')==[('pending',23,False),('confirmed',8,False),('processing',5,False),('handover',5,False),('picked_up',4,False)], opts(fb,'status'))
chk('total_size 46', j['total_size']==46 and len(j['orders'])==46, (j['total_size'],len(j['orders'])))
print('sort:', json.dumps(fb.get('sort'))[:300])
for k in ('payment_method','payment_status','order_type','campaign_only','placed_days'):
    print(k, opts(fb,k), items(fb).get(k,{}).get('bounds'), items(fb).get(k,{}).get('presets'))
tot=j['total_size']
for k in ('payment_method','payment_status','order_type'):
    chk(f'sum({k}) == total', sum(c for _,c,_ in opts(fb,k))==tot, sum(c for _,c,_ in opts(fb,k)))
# --- unflagged
s,ju,h=get('V1','vendor/current-orders',{'limit':200,'offset':1})
chk('unflagged key set', set(ju.keys())=={'total_size','limit','offset','orders'}, sorted(ju.keys()))
chk('unflagged total 46', ju['total_size']==46)
# --- filters block only offset<=1
s,j2,h=full('V1','vendor/current-orders',limit=10,offset=2)
chk('no block at offset 2', 'filters' not in j2, list(j2.keys()))
# --- status select
for st,n in (('pending',23),('confirmed',8),('processing',5),('handover',5),('picked_up',4)):
    s,j3,h=full('V1','vendor/current-orders',status=st)
    ok = j3['total_size']==n and len(j3['orders'])==n and all((o['order_status']==st or (st=='confirmed' and o['order_status'] in('confirmed','accepted'))) for o in j3['orders'])
    chk(f'status={st} -> {n}', ok, (j3['total_size'], set(o['order_status'] for o in j3['orders'])))
    if st=='pending':
        # counts ignore own selection
        chk('own-selection ignore: status counts unchanged under status=pending', opts(j3['filters'],'status')==[(v,c,v=='pending') for v,c,_ in opts(fb,'status')], opts(j3['filters'],'status'))
        print(' under pending: pm', opts(j3['filters'],'payment_method'), 'ot', opts(j3['filters'],'order_type'))
# --- combos
s,jc,h=full('V1','vendor/current-orders',status='pending',payment_method='cash_on_delivery')
print('combo count', jc['total_size'], 'applied', jc['filters']['applied'])
chk('combo AND rows', all(o['order_status']=='pending' and o['payment_method']=='cash_on_delivery' for o in jc['orders']), jc['total_size'])
s,jc2,h=full('V1','vendor/current-orders',status='pending',payment_method='cash_on_delivery,wallet',order_type='take_away')
print('combo2', jc2['total_size'], [(o['order_status'],o['payment_method'],o['order_type']) for o in jc2['orders']][:5])
chk('combo2 AND rows', all(o['order_status']=='pending' and o['payment_method'] in('cash_on_delivery','wallet') and o['order_type']=='take_away' for o in jc2['orders']))
s,jc3,h=get('V1','vendor/current-orders',raw_qs='with_filters=1&limit=200&offset=1&payment_method[]=cash_on_delivery&payment_method[]=wallet&payment_status=unpaid')
print('combo3 array', jc3['total_size'], [(o['payment_method'],o['payment_status']) for o in jc3['orders']][:4])
chk('combo3 rows', all(o['payment_method'] in('cash_on_delivery','wallet') and o['payment_status']=='unpaid' for o in jc3['orders']))
# option count vs list for each payment_method option
for v,c,_ in opts(fb,'payment_method'):
    s,jj,h=full('V1','vendor/current-orders',payment_method=v)
    chk(f'payment_method={v} count==list', jj['total_size']==c==len(jj['orders']), (c,jj['total_size']))
for v,c,_ in opts(fb,'order_type'):
    s,jj,h=full('V1','vendor/current-orders',order_type=v)
    chk(f'order_type={v} count==list', jj['total_size']==c==len(jj['orders']), (c,jj['total_size']))
for v,c,_ in opts(fb,'payment_status'):
    s,jj,h=full('V1','vendor/current-orders',payment_status=v)
    chk(f'payment_status={v} count==list', jj['total_size']==c==len(jj['orders']), (c,jj['total_size']))
# campaign
s,jk,h=full('V1','vendor/current-orders',campaign_only='1')
chk('campaign_only=1 ids', sorted(ids(jk))==[91417,91419,91421,91425], sorted(ids(jk)))
chk('campaign_only offered (present in block)', 'campaign_only' in items(jk['filters']), list(items(jk['filters'])))
s,jk2,h=full('V1','vendor/current-orders',campaign_only='1',status='pending')
print('campaign+pending', sorted(ids(jk2)))
print(json.dumps(items(fb).get('campaign_only'))[:400])
open('state_fb_v1.json','w').write(json.dumps(fb))
print('FAILS:',[n for n,o in R if not o])
