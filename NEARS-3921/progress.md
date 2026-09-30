# NEARS-3921 QA [8] progress (fix-cycle 0)

Env: emulator-5600 (AVD NEARS_2414_QA). Private backend: php artisan serve :8101 from the ticket worktree, DB `nears3921_qa`, a copy of multi_food_db. Server DB proven: /api/v1/config returned cross_module_basket=true (flipped on the copy only; the shared DB stays 0).
Branch app: com.izzes.nears.nears_nears_3921_group_vat_per_store_rou @ 08b1f6810. Base app: detached scratch worktree @ 19d9b7c67, package com.izzes.nears.nears_nears_3921_base_scratch. Both built with API_HOST=10.0.2.2:8101.

Fixtures (5% tax, no coupon, discounts table empty for 12/13/49, no flash line, item discount 0):
- AC1: Popcorn#198 (store 12, 19.73, raw tax 0.9865) + Breakfast Cereal#210 (store 13, 15.56, raw tax 0.778). round(sum) = 1.76; sum of rounded = 1.77.
- AC2: Rice 5kg#202 (store 12, 5.35, raw tax 0.2675) + Veggie Supreme Pizza#547 (store 49, module 2, 16.13, raw tax 0.8065). round(sum) = 1.07; sum of rounded = 1.08.

| AC | status | evidence | logs |
|---|---|---|---|
| 1 | PASS | base VAT 1.76 / Total 37.05 (RED). Branch VAT 1.77 / Total 37.06. Placed 91420 (tax 0.99, amount 20.72) + 91421 (tax 0.78, amount 16.34): 1.77 / 37.06 | clean (group/place 200). The only [FAIL] lines are env ones: Firebase, GPS, and a phone-less address PlaceOrderBlocked precondition |
| 2 | PASS | base VAT 1.07 / Total 22.55 (RED). Branch VAT 1.08 / Total 22.56. Placed 91428 (tax 0.27, amount 5.62) + 91429 (tax 0.81, amount 16.94): 1.08 / 22.56. ASAP, no schedule option | clean |
| 3 | PASS | curl probes: 200 with keys tax_amount (raw), tax_status, tax_included, product_price, total_addon_price, total_discount. App [NET] get-Tax http_status=200 x2 per checkout, on both base and branch pids | clean |
| 4 | PASS | Popcorn single-store: base VAT 0.99 / Total 20.72, branch VAT 0.99 / Total 20.72 | clean |
| 5 | PASS | 80/80 on the 2 named files. 106/106 with the captured-rows, throw-safety and single-emit files added. Independent mutation (scratch worktree, sum raw then round) turns both NEARS-3921 pins RED: 22.59 vs 22.58, 3.002 vs 3.001 | n/a |
| 6 | PASS | live: item 210 status=0 on the copy (restored afterwards). Store 13 get-Tax returned 403, VAT = 0.99 (store 12 only), no error text in the tree | `[FAIL] endpoint=/api/v1/customer/order/get-Tax http_status=403 type=ApiFailure msg="checkout: group per-store tax non-200"` |
