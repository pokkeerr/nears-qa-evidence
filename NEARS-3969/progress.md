# NEARS-3969 QA progress (phase 8, fix cycle 0)
Backend: /Users/Apple/Projects/nears-NEARS-3969-d5-gateway/Admin/public @ a2c2806b1 (:8169, DB nears_qa_3969, --no-reload)
Base control: scratch clone base-Admin (CrossModuleBasket.php @ 45d554c9e) :8170, same DB copy
Device: emulator-5600, UserApp debug from worktree, API_HOST=10.0.2.2:8169

- cell (a) API: fix validate cash 200 cash_removed:false valid:true; base 403 mixed_basket_cash_unavailable + 1 WARN (positive control) — PASS
- cell (a) UI: checkout probe 200 cash_removed=false; sheet shows Cash on Delivery row; placed 2 COD children 91443 (store 12) + 91444 (store 57); 0 [FAIL]; 0 checkout_cash_removed_shown — PASS
- cell (d) same-module 12+13 validate cash/digital: fix vs base byte-identical, 0 log lines — PASS
- cell (e) flag OFF mixed 12+57 validate cash/digital: fix vs base byte-identical — PASS
- cell (b) API (paypal active): validate cash 403 + 1 WARN; place cash 403 + 1 WARN; validate digital 200 cash_removed:true; place digital 200 -> 91447/91448 digital failed — PASS
- cell (c) API: gateway active -> payment-failed cash_on_delivery:false, PUT switch 403 + 1 switch WARN; gateway off -> base control still false/403 (defect), fix true/200 -> 91447 COD pending — PASS
- STALE-CONFIG (C1, app list [] / server [paypal]): checkout open -> 2 FAIL (generic 'unhandled api response' + probe 'no payment method passes'), NO 'no payment method available' FAIL/row; Change sheet = ZERO rows; Place->Confirm->zero-row sheet LOOP x3 with 0 FAIL — FAIL (narrowing N void)
- way out: checkout re-entry NO; Home pull-to-refresh NO (/api/v1/config not refetched); app relaunch YES (config refetched, Paypal row offered)
- cell (b) UI (relaunched, consistent [paypal]): probe 200 cash_removed=true; checkout_cash_removed_shown x1; sheet = Pay Via Online + Paypal, no cash — PASS
- 3846 AC7 regr: relaunch surfaced 'Your payment was Incomplete' for #91448 with gateway active: Pay Now / Cancel Order only, no switch-to-cash — PASS
- 3967 regr: refusal -> toast + Paypal-row sheet, 1 BE WARN, recovery via Paypal works — no new failure
- cell (c) UI: no gateway -> 'Your payment was Incomplete' #91448 offers 'Switch to Cash On Delivery'; gateway active -> not offered — PASS
- NARROWING-N exact shape (handleMixedBasketRejection, cached list []): ONE zero-row sheet, then Place->Confirm reopens zero-row sheet every time (x2), 0 [FAIL] per later tap — LOOP => narrowing N void
- AC7: checkout_cash_removed_shown 0x in cell (a), 1x per checkout in cell (b); no new event names (diff has no analytics change)
- backstop: phpunit Nears3969 17/220 OK, Nears3840 29/444 OK, Nears3908 65/1017 OK; flutter test (3 touched files) 125 passed

# NEARS-3969 delta re-QA (phase 8, fix cycle 1, HEAD d5b7326ef)
Backend: /Users/Apple/Projects/nears-NEARS-3969-d5-gateway @ d5b7326ef (:8169, DB nears_qa_3969 recreated via mysqldump --set-gtid-purged=OFF, --no-reload; /config proved copy: cross_module_basket=true, apml [] vs shared 2 gateways)
Proxy: scratch gwproxy.py :8179 -> :8169; mode "strip" blanks active_payment_method_list on GET /api/v1/config ONLY (falsified: direct [paypal] vs strip [] same second). App: emulator-5600, API_HOST=10.0.2.2:8179. Copy edits: flag 1, zone 2 digital_payment=1, paypal toggled, user-6 cart 12+57, wallet 500/15.84, partial_payment on (last cells), flag 0 (flag-off smoke).
- cell (a) smoke: probe 200 cash_removed=false, Cash row, placed COD 91424/91425, 0 FAIL — PASS
- cart pre-flight: no gateway -> cash 200; gateway (fresh config) -> digital 200 advisory; covering wallet + no selectable gateway -> wallet 200 — PASS (order unchanged)
- FINDING cart stale: app [] / server [paypal] -> pre-flight cash 403 -> blocking notice, Proceed disabled; persists across re-entry and a config refetch; exit = config refetch + basket edit, or relaunch (3851 logic, pre-existing)
- stale_heal: probe cash 403 -> INFO healed=true -> re-probe digital 200 cash_removed=true; 0 FAIL, 0 'unhandled'; section 'Digital Payment (Paypal)'; Change sheet Paypal row; digital placed 91436/91437 (placement only) — PASS
- stale_unhealed (proxy strip): INFO healed=false + FAIL 'no payment method passes' + FAIL 'no payment method available for the basket' (2, distinct); no-method row; Change/Select Payment Method -> no sheet (INFO); Place->Confirm -> toast + 1 FAIL 'place-order blocked reason=no_payment_method_is_enabled' x2; rebuild no repeat — PASS
- re-entry: 2nd stale signal in-entry (address change) -> probe FAIL only, no refresh (INFO count 1); re-enter -> INFO again (1 per entry) — PASS
- stale Place-time 403 healed: no sheet, Paypal auto-picked; FAIL x3 (unhandled + group validate failed same corr id + transient section) — AC5 FAIL
- stale Place-time 403 unhealed: toast only (4 dumps, no sheet), healed=false, no-method row, 1 FAIL/attempt after; FAIL x3 at refusal — AC5 FAIL
- reverse stale (app [paypal], server none): probe 200 cash_removed=false, sheet Cash+Paypal, COD placed 91448/91449, 0 FAIL — PASS
- wallet 500 >= total + stale unhealed: no no-method row, Place->Confirm -> sheet Wallet 500 + Apply — PASS; wallet 15.84 -> no-method row — PASS
- partial wallet (cell b, partial on): Apply -> Paid by wallet 15.84, remaining via Paypal, section 'Digital Payment (Paypal) (Partial)' — PASS
- cell (b) smoke UI: probe digital 200 cash_removed=true, 0 FAIL — PASS
- 3967 consistent refusal: toast + Paypal-row sheet, no cash row (unchanged); FAIL pair pre-existing
- cell (d) same-module 12+13: no probe, no group calls, Cash preselected, sheet Cash+Paypal+Wallet, 0 FAIL — PASS
- flag OFF: module-scoped basket, no group calls, Cash, 0 FAIL — PASS
- -005: gateway visibly selected YES (shot); switch explained on checkout NO (no notice/toast on the open-heal path; analytics only)
- backstop: flutter test 4 checkout files 182 pass; test/features/cart 744 pass
