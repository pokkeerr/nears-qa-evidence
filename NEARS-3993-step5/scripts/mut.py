#!/usr/bin/env python3
import subprocess,hashlib,os,sys,json,time
Q='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s5/qa'
W=Q+'/mut/UserApp'
L='lib/features/cart/domain/helpers/cart_store_snapshot_loader.dart'
C='lib/features/cart/controllers/cart_controller.dart'
F='/Users/Apple/Tools/flutter/bin/flutter'
KILL=['test/features/cart/cart_store_snapshot_loader_test.dart','test/baseline/cart/cart_store_snapshot_fetch_baseline_test.dart','test/baseline/cart/cart_store_snapshot_landing_baseline_test.dart','test/baseline/cart/cart_store_snapshot_loader_source_baseline_test.dart','test/baseline/cart/cart_notify_store_landing_baseline_test.dart','test/baseline/cart/cart_mutation_census_source_baseline_test.dart','test/baseline/cart/cart_member_inventory_source_baseline_test.dart','test/baseline/cart/cart_facade_scope_baseline_test.dart','test/features/cart/cart_group_subtotal_basis_test.dart','test/baseline/cart/cart_screen_minimum_baseline_test.dart']
M=[
 ('S01 rows source reversed (ensureStoreMinimums ids walked backwards)',L,"    for (final int id in ids) {\n      if (_storeMinimumOrder","    for (final int id in ids.toList().reversed) {\n      if (_storeMinimumOrder"),
 ('S02 in-flight dedupe (ensureStoreRecords ??= -> =)',L,"_minimumFetchInFlight[id] ??= _fetchStoreDetailsFor(id)","_minimumFetchInFlight[id] = _fetchStoreDetailsFor(id)"),
 ('S03 skip rule: in-flight half dropped (ensureStoreMinimums)',L,"      if (_storeMinimumOrder.containsKey(id) ||\n          _minimumFetchInFlight.containsKey(id)) {","      if (_storeMinimumOrder.containsKey(id)) {"),
 ('S04 in-flight entry not registered (ensureStoreMinimums)',L,"      _minimumFetchInFlight[id] = fetch;\n",""),
 ('S05 null-record branch: minimum 0 instead of null',L,"_storeMinimumOrder[id] = store?.minimumOrder;","_storeMinimumOrder[id] = store?.minimumOrder ?? 0;"),
 ('S06 null-record failure log condition negated',L,"} else if (ModuleHelper.isCrossModuleBasket()) {","} else if (!ModuleHelper.isCrossModuleBasket()) {"),
 ('S07 landing: recalculate dropped',L,"      _recalculate();\n",""),
 ('S08 landing: notify twice',L,"    _notify();\n  }\n\n  /// Test seam (NEARS-1290)","    _notify();\n    _notify();\n  }\n\n  /// Test seam (NEARS-1290)"),
 ('S09 landing: snapshot write dropped',L,"      _storeSnapshot[id] = store;\n",""),
 ('S10 alias getter copy: loader minimums handed out as a copy',L,"Map<int, double?> get minimums => _storeMinimumOrder;","Map<int, double?> get minimums => Map<int, double?>.of(_storeMinimumOrder);"),
 ('S11 alias getter copy: loader snapshots handed out as a copy',L,"Map<int, Store> get snapshots => _storeSnapshot;","Map<int, Store> get snapshots => Map<int, Store>.of(_storeSnapshot);"),
 ('S12 closure wiring: facade recalculate is a no-op',C,"    recalculate: () => calculationCart(),","    recalculate: () {},"),
 ('S13 closure wiring: facade notify is a no-op',C,"    notify: () => update(),","    notify: () {},"),
 ('S14 facade delegate: rows handed reversed to ensureStoreMinimums',C,"=> _snapshots.ensureStoreMinimums(_cartList);","=> _snapshots.ensureStoreMinimums(_cartList.reversed.toList());"),
 ('S15 ensureStoreRecords: Future.wait -> sequential awaits',L,"      await Future.wait(pending);","      for (final Future<void> p in pending) {\n        await p;\n      }"),
]
def sh(c,cwd=None): return subprocess.run(c,shell=True,cwd=cwd,capture_output=True,text=True)
sh('python3 ~/.nears/bin/mem-guard.py --label NEARS-3993-s5-qa-mutpubget --max-gb 6 --wait-s 3600 -- %s pub get'%F,cwd=W)
out=open(Q+'/mutation.jsonl','a'); os.makedirs(Q+'/mutation',exist_ok=True)
only=sys.argv[1:] 
for mid,rel,old,new in M:
    if only and mid.split()[0] not in only: continue
    path=W+'/'+rel; orig=open(path).read(); h0=hashlib.sha256(orig.encode()).hexdigest()
    if orig.count(old)!=1: print(mid,'OLD-COUNT',orig.count(old)); out.write(json.dumps({'id':mid,'result':'NOT-LANDED(old count %d)'%orig.count(old)})+'\n'); out.flush(); continue
    open(path,'w').write(orig.replace(old,new))
    d=sh('git diff -U0 -- '+rel,cwd=W).stdout
    open(Q+'/mutation/'+mid.split()[0]+'.diff','w').write(d)
    if not d.strip(): print(mid,'EMPTY DIFF'); continue
    res='SURVIVED'; killer=None; detail=''
    for f in KILL:
        r=sh('python3 ~/.nears/bin/mem-guard.py --label NEARS-3993-s5-qa-mut --max-gb 6 --wait-s 3600 -- %s test --no-pub --reporter expanded %s'%(F,f),cwd=W)
        txt=r.stdout+r.stderr
        last=[l for l in txt.split('\n') if l[:5].count(':')==1 and ' +' in l][-1:] 
        loadfail=('Failed to load' in txt) or ('Compilation failed' in txt) or ('Some tests failed' not in txt and r.returncode!=0)
        if loadfail:
            res='COMPILE/LOAD ERROR (not a kill)'; killer=f; detail=txt[-400:]; break
        if r.returncode!=0:
            res='KILLED'; killer=f; detail=(last[0] if last else ''); break
        time.sleep(25)
    open(path,'w').write(orig)
    h1=hashlib.sha256(open(path).read().encode()).hexdigest(); st=sh('git status --porcelain --untracked-files=no',cwd=W).stdout.strip()
    rec={'id':mid,'result':res,'killer':killer,'detail':detail,'restored_byte_equal':h0==h1,'git_status_clean':st==''}
    print(json.dumps(rec)); out.write(json.dumps(rec)+'\n'); out.flush()
    time.sleep(25)
