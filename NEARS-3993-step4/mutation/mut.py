#!/usr/bin/env python3
# NEARS-3993-s4 QA mutation spot re-runs on the scratch detached worktree qa/tip (TIP bytes). One flutter invocation per file via mem-guard, 25 s gap between invocations.
import subprocess, sys, hashlib, json, time, re, os
Q='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s4/qa'
W=Q+'/tip'; UA=W+'/UserApp'; OUT=Q+'/mutation'; os.makedirs(OUT,exist_ok=True)
CALC='UserApp/lib/features/cart/domain/helpers/cart_totals_calculator.dart'
CTL='UserApp/lib/features/cart/controllers/cart_controller.dart'
T='test/baseline/cart/'
ST=T+'cart_totals_state_baseline_test.dart'; INV=T+'cart_totals_invalidation_order_baseline_test.dart'
SB=T+'cart_totals_calculator_server_basis_baseline_test.dart'; CB=T+'cart_totals_calculator_baseline_test.dart'
RL=T+'cart_totals_facade_row_lists_baseline_test.dart'; IU=T+'cart_totals_calculator_inputs_untouched_baseline_test.dart'
MI=T+'cart_member_inventory_source_baseline_test.dart'; FS=T+'cart_facade_scope_baseline_test.dart'; CS=T+'cart_totals_calculator_source_baseline_test.dart'
CEN=T+'cart_mutation_census_source_baseline_test.dart'
INVBLOCK="""    // NEARS-3771: every cart mutation lands here, so this is the one place a
    // changed basket can drop the now-stale multi-store fee/tax summary.
    if (Get.isRegistered<PricingSummaryController>()) {
      Get.find<PricingSummaryController>().invalidateGroupFeesIfBasketChanged();
    }
"""
M=[
 ('E22','invalidation BEFORE the calculation (controller)',CTL,
  "    _totals.calculationCart(cartList, _cartList, _storeSnapshot);\n"+INVBLOCK,
  INVBLOCK+"    _totals.calculationCart(cartList, _cartList, _storeSnapshot);\n",[INV,ST]),
 ('E03','accumulator reset dropped: _itemPrice (calculator)',CALC,"    _itemPrice = 0;\n","",[ST,CB]),
 ('E19','isFoodVariation sticky in the global pass (calculator)',CALC,
  "    for (var cartModel in cartList) {\n      isFoodVariation = ModuleHelper.getModuleConfig(",
  "    for (var cartModel in cartList) {\n      isFoodVariation = isFoodVariation || ModuleHelper.getModuleConfig(",[ST,CB]),
 ('E08','availableList always true (calculator)',CALC,
  "      _availableList.add(\n        DateConverter.isAvailable(\n          cartModel.item!.availableTimeStarts,\n          cartModel.item!.availableTimeEnds,\n        ),\n      );",
  "      _availableList.add(true);",[ST,CB]),
 ('S1','server basis all-or-nothing: unresolved store skipped instead of returning null (calculator)',CALC,
  "      if (server == null) {\n        return null;\n      }","      if (server == null) {\n        continue;\n      }",[SB,CB]),
 ('S2','server basis: live = last store only instead of any store (calculator)',CALC,
  "      live = live || server.live;","      live = server.live;",[SB,CB]),
 ('D01','per-store pass: isFoodVariation sticky (calculator subTotalForRows)',CALC,
  "    for (final CartModel cartModel in rows) {\n      isFoodVariation = ModuleHelper.getModuleConfig(",
  "    for (final CartModel cartModel in rows) {\n      isFoodVariation = isFoodVariation || ModuleHelper.getModuleConfig(",[SB,CB]),
 ('L1','literal moved by one: a literal (+1) in the food-term of the enforced total is not testable alone; use the 0 -> 1 in enforcedTotal food term',CALC,
  "(isFoodVariation ? variationWithoutDiscountPrice : 0);","(isFoodVariation ? variationWithoutDiscountPrice : 1);",[SB,CB]),
 ('F06','facade swaps the row lists (controller)',CTL,
  "_totals.calculationCart(cartList, _cartList, _storeSnapshot);","_totals.calculationCart(_cartList, cartList, _storeSnapshot);",[RL,ST]),
 ('I01','inputs: basketRows.removeLast() at the end of calculationCart (calculator)',CALC,
  "      _subTotal = serverBasis.subTotal;\n    }\n  }","      _subTotal = serverBasis.subTotal;\n    }\n    basketRows.removeLast();\n  }",[IU,CB]),
 ('B01','stray member in the facade: leftover double _subTotal (controller)',CTL,
  "  double get subTotal => _totals.subTotal;","  double _subTotal = 0;\n  double get subTotal => _totals.subTotal;",[MI,FS,CS]),
 ('E28','facade returns itemPrice instead of subTotal (controller)',CTL,
  "    return _totals.subTotal;\n  }\n\n  int? getCartId","    return _totals.itemPrice;\n  }\n\n  int? getCartId",[ST,INV]),
 ('M27','freeDeliveryProgress reads itemPrice (controller)',CTL,
  "    return _totals.subTotal /\n        Get.find<SplashController>()","    return _totals.itemPrice /\n        Get.find<SplashController>()",[ST]),
 ('G1','getter cross-wired: addOns -> variationPrice (controller)',CTL,
  "  double get addOns => _totals.addOns;","  double get addOns => _totals.variationPrice;",[ST,CS,FS]),
 ('L01','census literal moved by one: arg:calculationCart 1 -> 2 (test file)','UserApp/'+CEN,
  "        'arg:calculationCart': 1,","        'arg:calculationCart': 2,",[CEN]),
]
def sh(c,**k): return subprocess.run(c,shell=True,capture_output=True,text=True,**k)
def run_test(f,idn):
    n=f.replace('/','_')
    log=f'{OUT}/{idn}-{n}.log'
    r=sh(f'cd {UA} && python3 ~/.nears/bin/mem-guard.py --label NEARS-3993-s4-qa-mut --max-gb 6 --wait-s 3600 -- /Users/Apple/Tools/flutter/bin/flutter test --no-pub --reporter expanded {f} > {log} 2>&1; echo $?')
    rc=r.stdout.strip()
    last=sh(f"grep -a -E '^[0-9:]+ \\+[0-9]+' {log} | tail -1 | sed -E 's/^[0-9:]+ //'").stdout.strip()
    return rc,last
sel=sys.argv[1:]
for idn,desc,path,old,new,tests in M:
    if sel and idn not in sel: continue
    p=W+'/'+path
    before=hashlib.sha256(open(p,'rb').read()).hexdigest()
    s=open(p).read()
    assert s.count(old)==1,(idn,'old text count',s.count(old))
    open(p,'w').write(s.replace(old,new))
    diff=sh(f'cd {W} && git diff -U0 -- {path}').stdout
    open(f'{OUT}/{idn}.diff','w').write(diff)
    landed=bool(diff.strip())
    res=[]
    killed=False
    if landed:
        for t in tests:
            rc,last=run_test(t,idn)
            res.append((t.split('/')[-1],rc,last))
            time.sleep(25)
            if rc!='0': killed=True; break
    sh(f'cd {W} && git checkout -- {path}')
    after=hashlib.sha256(open(p,'rb').read()).hexdigest()
    clean=sh(f'cd {W} && git diff --stat').stdout.strip()==''
    rec=dict(id=idn,desc=desc,landed=landed,tests=res,result='KILLED' if killed else 'SURVIVED',restored_byte_equal=(before==after),git_diff_stat_empty=clean)
    open(Q+'/mutation.jsonl','a').write(json.dumps(rec)+'\n')
    print(json.dumps(rec),flush=True)
print('MUT-ALLDONE',flush=True)
