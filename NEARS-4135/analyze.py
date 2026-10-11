import json
b=json.load(open('out-base/_summary.json')); r=json.load(open('out-branch/_summary.json'))
rows=[]; ok=True
for lab in b['files']:
    fb=b['files'][lab]; fr=r['files'][lab]
    removed=sorted(set(fb['paths'])-set(fr['paths'])); added=sorted(set(fr['paths'])-set(fb['paths']))
    base_keys=fb['key_paths']
    exact = (removed==base_keys) and not added
    leaf_ok = all(p.rsplit('.',1)[-1] in ('temp_token','cm_firebase_token','social_id') for p in removed)
    rows.append((lab,fb['code'],fr['code'],len(base_keys),len(removed),len(added),len(fb['value_hits']),len(fr['value_hits']),len(fr['key_paths']),exact and leaf_ok))
    ok &= exact and leaf_ok and fb['code']==fr['code']
print("label base_code branch_code base_keypaths removed added base_valhits branch_valhits branch_keypaths exact")
for x in rows: print(*x)
print("ALL EXACT:",ok)
print("bodies base",b['bodies'],"json",b['json_bodies'],"branch",r['bodies'],r['json_bodies'])
print("base totals: keypath hits",len(b['key_hits']),"value hits",len(b['value_hits']),"rawkeyname",len(b['rawkeyname_hits']))
print("branch totals: keypath hits",len(r['key_hits']),"value hits",len(r['value_hits']),"rawkeyname",len(r['rawkeyname_hits']))
print("sample base paths:", sorted({p for l,p in b['key_hits']})[:20])
print("customer.info branch top-level+userinfo paths:")
for p in r['files']['customer.info']['paths']: print("  ",p)
