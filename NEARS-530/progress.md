# NEARS-530 QA progress (phase 8, fix cycle 0) - emulator-5570, worktree @354f0e03a, own backend :8530 / DB nears_qa_530
- AC1: FAIL (partial) - no 404 (items/details/628 200 x2), MediQuick store-profile pushed, full Sunscreen SPF50 sheet over it, dismiss -> store-profile; BUT persisted active module 1 -> 3 and Home renders Pharmacy (scope: "home module still A"). bug-crossmodule-link-switches-active-module.log
- AC2: PASS - pharmacy active; module=pharmacy and module=3 both: 200 x2, store pushed, sheet full, dismiss -> store; module stays 3. logs clean
- AC3: PASS - id=999999 module=pharmacy (grocery active): 404 x2 with paired [FAIL], standalone "Item not found" sheet, no store pushed, Back -> Home (grocery); module stays 1
- AC4: PASS - 6-file suite 30/30 green @354f0e03a; pre-fix scratch copy: 5 RED (cross_module_slug) + 2 RED (item_detail_modal_nav) by assertion, resolver file compile-RED
- AC5: PASS - module=no-such-module and module=99 (grocery active): no crash, module stays 1, 404 + paired [FAIL], standalone not-found; Back -> Home grocery. Tests green
- Fix-in-run (coldstart f1): PASS - f1 (item 404) + f1 (out-of-zone) green; live killed-app link id=628 module=pharmacy -> items/details 200 x2, no 403, sheet over MediQuick store, dismiss -> store
- Regression: out-of-zone item 32 -> 403 + ZoneWarningDialog (PASS); plain store deep link keeps active module (PASS, control)
