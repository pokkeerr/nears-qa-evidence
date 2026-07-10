# NEARS-1025 — QA cycle-3 (delta re-QA) progress

Branch feat/NEARS-1025-cart-add-zone-validation @ aebfbf2d
Device emulator-5554 (Android), UserApp from worktree, backend :8000 (primary Admin; cycle-3 touched no BE files).
Zone data: Corner Grocer store 36 = zone 1; Test Store 35 = zone 2 (self-delivery). Customer user 6: addr46 "Demo Zone — Dhaka" zone1, addr45 "Abu Dhabi" zone2.

VERDICT: PASS

| AC / focus | result | evidence |
|---|---|---|
| AC11 crash: pick saved addr from Change Location (zoneData:null), no red-box/_TypeError | PASS | 3 pick transitions, zero _TypeError/Null-check/EXCEPTION in flutter log; ac11-checkout-after-abudhabi-pick.png |
| in-zone pick → shimmer→real pricing (non-self store) | PASS | Corner Grocer + Demo-Zone addr: ETA ~22min, Total, Place Order, no error frame; ac-inzone-realpricing.png |
| delivery-charge subtree self + non-self on null-zoneData addr | PASS | Test Store (self-delivery) in-zone real pricing ac-selfdelivery-inzone.png; Corner Grocer (non-self) ac-inzone-realpricing.png; unit test 31/31 both branches |
| out-of-zone panel still shows for out-of-coverage addr | PASS | Corner Grocer(z1)+Abu Dhabi(z2) → "This address is outside the store's delivery zone.", no crash; ac11-checkout-after-abudhabi-pick.png |
| order-success dialog on such addr | PASS | orderID=176 COD placed, POST 200, success dialog→tracking, log window clean; ac-order-tracking-after-place.png |
| BE cart/add zone guard fail-closed (absent/empty header reject; valid accept) | PASS (Rule-4 reuse + backstop) | phpunit CartAddZoneGuardTest 8/8, 46 assertions |

Automated backstop: phpunit CartAddZoneGuard 8/8; flutter checkout tests 31/31 (incl null-zoneData both store types).

Non-blocking followup: [FAIL] get-zone-id 404 from OrderTrackingScreenState._loadData→getCurrentLocation (order_tracking_screen.dart:60) — emulator GPS outside seeded zones; properly logged (correlation_id), no crash; unrelated to fix (fix never touched order_tracking). followup-getzoneid-404-ordertracking.log
