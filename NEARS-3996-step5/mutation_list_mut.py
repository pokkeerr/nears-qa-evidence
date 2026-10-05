#!/usr/bin/env python3
"""AC4 spot-check mutants for NEARS-3996 step 5 (scratch copy only). usage: mut.py [ids...]"""
import subprocess, sys, os, shutil, filecmp, difflib, json
LIVE='/Users/Apple/Projects/nears-NEARS-3996-u5-step5/UserApp'
WT='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3996-s5/qa/mut/wt/UserApp'
OUT='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3996-s5/qa/mut/out'
os.makedirs(OUT,exist_ok=True)
O='lib/features/store/controllers/store_catalog_owner.dart'
C='lib/features/store/controllers/store_controller.dart'
# (id, file, [(old,new,which)], description) ; which: 'only' (must be unique) | 'last'
M=[
('M01',O,[("      rating: _rating == -1 ? null : _rating,","      rating: _rating,",'only')],'browse request: rating -1 sentinel no longer mapped to null (arg list)'),
('M02',O,[("      lowerValue: _lowerValue == 0 ? null : _lowerValue,","      lowerValue: _upperValue == 0 ? null : _upperValue,",'only')],'browse request: lowerValue reads upper (arg swap)'),
('M03',O,[("      _itemListSessionId++; // NEARS-1109\n      _retryLastGridLoad = () => getStoreItemList","      _retryLastGridLoad = () => getStoreItemList",'only')],'getStoreItemList page-1 reset no longer bumps the session id'),
('M04',O,[("    _searchText = '';\n    _itemListSessionId++; // NEARS-1109\n  }","    _searchText = '';\n  }",'only')],'initSearchData no longer bumps the session id'),
('M05',O,[("    _port.clearOffersSelection();\n    if (itemSearching) {","    if (itemSearching) {",'only'),("    }\n    update();\n  }\n}","    }\n    _port.clearOffersSelection();\n    update();\n  }\n}",'last')],'setCategoryIndex: offers-selection clear moved AFTER the loader call (order)'),
('M06',O,[("_retryLastGridLoad = () => getStoreItemList(storeID, 1, type, true);","_retryLastGridLoad = () => getStoreItemList(storeID, 1, type, false);",'only')],'retry closure re-fires with notify=false'),
('M07',O,[("_retryLastGridLoad = () => getStoreItemList(storeID, 1, type, true);","_retryLastGridLoad = () => getStoreItemList(storeID, offset, type, true);",'only')],'retry closure captures the live offset instead of 1'),
('M08',O,[("if (offset > 1 && requestSessionId != _itemListSessionId) {","if (offset > 1 && requestSessionId == _itemListSessionId) {",'only')],'stale page-2 guard inverted'),
('M09',O,[("} else if (offset == 1 && requestSessionId == _itemListSessionId) {","} else if (offset == 1) {",'only')],'search failure path loses the superseded-request session guard'),
('M10',C,[("  void notify() => _controller.update();\n}","  void notify() {}\n}",'last')],'_StoreCatalogPort.notify bridge becomes a no-op (last class in file)'),
('M11',C,[("String get registeredStoreType => Get.find<StoreController>().type;","String get registeredStoreType => _controller.type;",'only')],'port: registeredStoreType reads this controller instead of the registered one'),
('M12',C,[("  set itemListSessionId(int value) =>\n      _controller._catalog.itemListSessionId = value;","  set itemListSessionId(int value) =>\n      value;",'only')],'grid port (offers family): session id write no longer reaches the catalog owner'),
('M13',C,[("  void dedupeAndPartitionStoreItems() =>\n      _controller._catalog.dedupeAndPartitionStoreItems();","  void dedupeAndPartitionStoreItems() => null;",'only')],'grid port: offers page-2 dedupe/partition forward dropped'),
('M14',C,[("    _catalog.resetItemsFailed(); // NEARS-1088: never carry a grid error into a new store\n","",'only')],'getStoreDetails no longer resets the grid-failed flag on a new store'),
('M15',C,[("  set retryLastGridLoad(void Function()? value) =>\n      _controller._catalog.setRetryLastGridLoad(value);","  set retryLastGridLoad(void Function()? value) =>\n      value;",'only')],'grid port (offers family): retry slot write no longer reaches the catalog owner'),
('M16',O,[("    if (offset == 1 || _storeItemModel == null) {\n      _type = type;","    if (offset == 1) {\n      _type = type;",'only')],'getStoreItemList: page>1 with a null model no longer takes the reset branch'),
('M17',O,[("      showCustomSnackBar('write_item_name'.tr);\n      return true;","      showCustomSnackBar('write_item_name'.tr);\n      return false;",'only')],'empty-query search returns false instead of true'),
('M18',C,[("      _catalog.setCategoryIndex(index, itemSearching: itemSearching);","      _catalog.setCategoryIndex(index);",'only')],'facade setCategoryIndex drops the itemSearching argument'),
]
TESTS=['test/features/store/store_catalog_owner_test.dart','test/features/store/store_catalog_facade_wiring_test.dart','test/baseline/store/store_catalog_family_characterization_baseline_test.dart','test/features/store/store_catalog_extraction_source_scan_test.dart']
FL='/Users/Apple/Tools/flutter/bin/flutter'
def run(ids):
    for mid,f,edits,desc in M:
        if ids and mid not in ids: continue
        live=os.path.join(LIVE,f); tgt=os.path.join(WT,f)
        assert filecmp.cmp(live,tgt,shallow=False),'scratch not pristine before '+mid
        src=open(live).read(); new=src
        for old,nw,which in edits:
            if which=='only':
                assert new.count(old)==1,(mid,'old count',new.count(old))
                new=new.replace(old,nw)
            else:
                i=new.rfind(old); assert i>=0,(mid,'last not found'); new=new[:i]+nw+new[i+len(old):]
        assert new!=src
        open(tgt,'w').write(new)
        diff=''.join(difflib.unified_diff(src.splitlines(1),new.splitlines(1),'live/'+f,'mut/'+f,n=0))
        open(f'{OUT}/{mid}.diff','w').write(diff)
        res=[]; red=None
        for t in TESTS:
            p=subprocess.run(['python3',os.path.expanduser('~/.nears/bin/mem-guard.py'),'--label','s5qa-mut','--max-gb','6','--wait-s','3600','--',FL,'test',t],cwd=WT,capture_output=True,text=True)
            txt=p.stdout+p.stderr; open(f'{OUT}/{mid}__{os.path.basename(t)}.log','w').write(txt)
            last=[l for l in txt.splitlines() if ' +' in l and l[:2].isdigit()]
            res.append((os.path.basename(t),p.returncode,(last[-1].split(' ',1)[1] if last else '')[:60]))
            if p.returncode!=0: red=os.path.basename(t); break
        shutil.copyfile(live,tgt)
        restored=filecmp.cmp(live,tgt,shallow=False)
        rec={'id':mid,'file':f,'desc':desc,'diff_hunks':[l for l in diff.splitlines() if l.startswith('@@')],'results':res,'first_red':red,'restored_cmp':restored,'verdict':'KILLED' if red else 'SURVIVED'}
        open(f'{OUT}/results.jsonl','a').write(json.dumps(rec)+'\n'); print(json.dumps(rec),flush=True)
        assert restored
if __name__=='__main__': run(sys.argv[1:])
