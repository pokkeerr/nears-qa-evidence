# NEARS-530 QA progress (phase 8, fix cycle 0) - emulator-5570, worktree @354f0e03a, own backend :8530 / DB nears_qa_530
- AC1: FAIL (partial) - no 404 (items/details/628 200 x2), MediQuick store-profile pushed, full Sunscreen SPF50 sheet over it, dismiss -> store-profile; BUT persisted active module 1 -> 3 and Home renders Pharmacy (scope: "home module still A"). bug-crossmodule-link-switches-active-module.log
- AC2: PASS - pharmacy active; module=pharmacy and module=3 both: 200 x2, store pushed, sheet full, dismiss -> store; module stays 3. logs clean
- AC3: PASS - id=999999 module=pharmacy (grocery active): 404 x2 with paired [FAIL], standalone "Item not found" sheet, no store pushed, Back -> Home (grocery); module stays 1
- AC4: PASS - 6-file suite 30/30 green @354f0e03a; pre-fix scratch copy: 5 RED (cross_module_slug) + 2 RED (item_detail_modal_nav) by assertion, resolver file compile-RED
- AC5: PASS - module=no-such-module and module=99 (grocery active): no crash, module stays 1, 404 + paired [FAIL], standalone not-found; Back -> Home grocery. Tests green
- Fix-in-run (coldstart f1): PASS - f1 (item 404) + f1 (out-of-zone) green; live killed-app link id=628 module=pharmacy -> items/details 200 x2, no 403, sheet over MediQuick store, dismiss -> store
- Regression: out-of-zone item 32 -> 403 + ZoneWarningDialog (PASS); plain store deep link keeps active module (PASS, control)

# fix cycle 2 (delta) - emulator-5662, worktree @8f4fd7d55, own backend :8530 / DB nears_qa_530, build w/ API_HOST=10.0.2.2:8530 + WEB_HOSTED_URL
- AC4 backstop: 8-file set 36/36 green @8f4fd7d55
- AC1 (module=pharmacy, Grocery active): PASS - items/details/628 200 x2, stores/details/mediquick-pharmacy-abu-dhabi 200, full Sunscreen SPF50 sheet over MediQuick, Close -> store-profile with content, Back -> Home Grocery (7 grocery / 0 pharmacy markers); prefs moduleId 1 -> 1; log 'initial route module=grocery-food' + 'not from deeplink, skipping module fetch', no 'module=pharmacy', no 'module match found'; no [FAIL]/[ERR]
- AC1 (module=3, Grocery active): PASS - 200 x2 + store 200, sheet over MediQuick, Close -> store-profile (5 store markers), Back -> Home Grocery (7/0); prefs moduleId stays 1; no 'initial route module=3', no 'module match found'; no [FAIL]/[ERR]
- Control plain store link (Grocery active): PASS unchanged - store-route pass defers to StoreScreen, store 200 renders, Back -> Home Grocery, moduleId stays 1
- Cold start cross-module item link (force-stop, Grocery persisted): PASS - items/details/628 200 x2, no 403, stores/details 200, sheet over MediQuick, Close -> store-profile. Note: persisted module becomes 3 via the NEARS-2721 itemDetails cold-start _waitForModule (route_helper.dart:1226-1241, untouched by NEARS-530) - pre-existing/by-design, followup only
- AC2 same-module (Pharmacy active) slug + numeric: PASS - 200 x2, store 200, sheet, Close -> store-profile, moduleId stays 3; no [FAIL]/[ERR]
- AC3, AC5, out-of-zone: reused prior PASS (success-path-only change; branches untouched)
