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
