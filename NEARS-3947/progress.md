# NEARS-3947 QA progress (phase 8, fix-cycle 0)

Build under test: worktree /Users/Apple/Projects/nears-NEARS-3947 (feat/NEARS-3947-group-payment-resume) @ 96107e7ad, base 1e58fe464.
Backend HEAD: /Users/Apple/Projects/nears-NEARS-3947 @ 96107e7ad, :8147 (php artisan serve --no-reload, DB nears_qa_3947), freshness PASS. Logging proxy :8148 -> :8147 (method/path/ids/status/rid only; token values never logged; /payment/<gw>/* is NEVER forwarded: 302 -> /payment-fail, no gateway call).
Backend BASE: detached worktree /Users/Apple/Projects/nears-NEARS-3947-qabase @ 1e58fe464, :8149, same DB copy (for the AC-BE byte diff).
DB proof: copy-only footer_text marker NEARS3947-COPY-MARKER served by GET /api/v1/config on :8147 and :8149. Copy fixture: guest_checkout_status id138 0->1 (copy only).
Shared invariants BEFORE: multi_food_db max(orders.id)=91415; business_settings id228=0; order_groups=15; payment_requests=75.
Device: emulator-5680 (spare AVD NEARS_2424_QA booted by this run, qemu pid 66803, ppid 1); lock NEARS-3947.

## AC-BE (API) head vs base
- AC-BE PASS: 3 keys appended last in both branches (?order_id= and no-id) for group 3f64a660 (user 1); null for non-group #91404/#91402 (user 6); every other key identical in order+value vs BASE :8149 (tokens compared by presence). acbe-head-vs-base.log
- AC-BE amount control PASS: redeem of HEAD token -> 302 Location /payment/paypal/pay; payment_requests 131.85 == group_amount_due 131.85. acbe-redeem-amount.log
- AC-SEC IDOR PASS: guest B on guest A child -> []; guest B no-id -> []; guest B presenting guest A id -> 401 (+1 guest.token.rejected); user B on user A child -> []; garbage bearer -> 401 (both branches); guest 1 vs user 1 -> []. Constructed owner-mismatch (copy fixture 91407 is_guest 0->1) -> 3 keys null + exactly ONE "[WARN] payment failed group unresolved" (keys endpoint, reason=group_owner_mismatch, order_id, group_id, request_id) per request, both directions; restored -> mints again. acsec-idor.log, acsec-guestN-vs-userN.log
- AC-SEC replay PASS: COD-switch 91406 (real PUT) -> token null, amount 23.97 (payable child only) in all 3 reads; old token -> 403 order-state, payment_requests 1 -> 1. Cancel 91417 (guest A, real PUT) -> token null, amount 19.11; old token -> 403 order-state, 0 -> 0. acsec-replay-cod.log, acsec-replay-cancel.log
- D1 resume sheet (user 1, group 3f64a660 after COD switch of 91406): ids '#91407' (== server payable set), amount 23.97 (== server), notice row (one a11y node) in Pay Now's slot + Switch + Cancel; no Pay Now. d1-*.png/.xml
- Single-order control PASS (user 6, #91404 non-group): 'Order ID' #91404 377.58, Pay Now/Switch/Cancel, no group reads. s1-*.png/.xml
- G1 group 1217a218 (flag OFF, UI-placed, PayPal): #91421 3.73 + #91422 19.11 = 22.84. AC5 landing PASS: 'Orders #91421, #91422', due 22.84, Pay Now+Switch+Cancel. ac5-g1-failed-screen.log/.png/.xml
- AC5 Pay Now PASS: method sheet group mode = Cash + Online only (no wallet despite 15.84 balance, no offline); Paypal -> payment-mobile?group_id=1217a218 + token, row 22.84 == group_amount_due. ac5-g1-paynow-group-webview.log
- AC4 token+cash PASS (G1 after restart): ids '#91421, #91422', 22.84, Pay Now + Switch + Cancel. ac4-g1-resume-sheet-token-cash.*
- CRITICAL regression PASS: order details #91421 Pay Again -> single sheet (Total 3.73, Wallet/Cash/Online/Offline), Paypal -> payment-mobile?order_id=91421, row attribute=order 91421 3.73. ac6-payagain-single-child.log
- AC5 failed-screen Switch PASS: PUT payment-method 91421 + 91422 (both), DB both pending/COD; app logs clean. ac5-g1-failed-screen-switch-whole-group.log
- AC4 Cancel (resume sheet) PASS: G4 05d45efb -> PUT cancel 91427 + 91428, both canceled by customer. ac4-g4-resume-sheet-cancel-whole-group.log
- AC6 method sheet (from resume sheet Pay Now) Cash PASS: G3 773bdfe9 rows Cash+Online only; Cash -> PUT payment-method 91425 + 91426, both COD; no paymentAfterDigitalCancel single call. ac6-g3-method-sheet-cash-whole-group.log
- RESOLVING inert PASS (G2, 15s proxy delay on group/details): 2x 'Loading...' skeletons; Pay Now/Switch/Cancel present, enabled=false. ac4-g2-resume-sheet-resolving.*
- FAILED resolve PASS (G2, injected 500): 'Something went wrong' + Retry + 'Back to Home' = two distinct clickable nodes, no stale ids/amount; paired [FAIL] lines (correlation_id == proxy rid); Retry -> resolves. ac4-g2-failed-retry-leave.log, ac4-g2-resume-sheet-failed-retry-leave.*
- RTL/AR PASS (G2, app language Arabic): sheet + failed screen id runs '#91423, #91424' not reversed by pixel (comma gapL 6-7px / gapR 17-21px, '#' leads, narrow '1' at index 2); failed-screen label at right. rtl-ar-id-run-crops-sheet-top-failed-bottom.png, rtl-ar-id-run-pixel-check.log
- P4 PASS (server + device, AR): G6 f866c16b partial child #91432 (unpaid COD row) and G5 3e2794ea paid-while-pending #91430 are NOT in ids ('#91431' / '#91429') and NOT in amount (3.73 == server group_amount_due), token null -> AR notice (one node) + Switch + Cancel. p4-server-payable-set.log, p4-g6-device.log, p4-g5-device.log
- G6 Cancel (AR) -> both children canceled incl. partial child. p4-g6-device.log
- FINDING (pre-existing, regression lane): G5 Switch PUT both 91429 and the PAID 91430 -> 91430 pending/paid/cash_on_delivery. bug-switch-targets-paid-child-no-server-guard.log
- AC4 Switch (resume sheet) PASS: G2 d3448968 -> PUT payment-method 91423 + 91424, both COD. ac4-g2-resume-sheet-switch-whole-group.log
- FLAG ON (copy id228=1, shared stays 0) MIXED G7 c515a195 (Nears Mart grocery + The Grill House restaurant, UI-placed): failed screen 'Orders #91439, #91440' 65.05, Pay Now + Cancel, NO Switch (server cash false); method sheet = online only. mixed-g7-failed-screen.log
- Zero-methods PASS (G7, copy zone1 cod=0 dp=0, token present): row 'No payment method is available for this basket' (one node), Proceed enabled=false, tap -> no toast/no request/no log. ac6-zero-methods.log
- Refusal (INSTRUMENTED, proxy forced group_amount_due=0 on the no-id read): one toast 'Payment method is not available' + exactly one [FAIL] 'payment sheet: group resume refused ...'; sheet stays; 0 requests. ac6-refusal-toast-instrumented.log
- Mixed no-token + no-cash PASS (G7 after #91439 cancelled via real API): ids '#91440', 45.94 == server, notice + Cancel ONLY; Cancel -> 91440 canceled. mixed-g7-notoken-nocash-cancel.log
- Guest gate PASS (guest 1972 group cd5f3aab): failed screen ids + 22.84, token present server-side, NO Pay Now, NO notice, Switch + Cancel. ac5-guest-gate.log
- Failed screen FAILED-resolve + Leave PASS (2x injected 500): 'Something went wrong' + Retry + 'Back to Home' two nodes; 0 PUT; Back to Home -> home. ac5-failed-screen-failed-resolve-leave.log
- AC-LOG PASS: 11 minted group tokens + generic Crypt prefix eyJpdiI6 -> 0 hits in laravel.log, flutter run log, adb logcat -b all, proxy log; planted-token control 1/1 in each; live-capture controls positive. aclog-token-absent.log
- Backstop: phpunit (sandbox deny 80/443, control exit 137) filter GroupPaymentTest|Nears3957|Nears3902|Nears3856|PaymentTokenBindingTest|OrderPaymentFailed|Nears3840|Nears3947 -> 222 tests / 2888 assertions OK (1 PHPUnit deprecation). flutter test test/features/{checkout,order,dashboard} (pinned 3.41.9) -> 2193 passed, 0 failed (incl. payment_failed_dialog_group*, NEARS-3944/3956 dialog tests).
