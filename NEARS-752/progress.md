# NEARS-752 QA progress checkpoint

Device: emulator-5556 | worktree build (branch fix/NEARS-752-checkout-zone-transport @168e7f7c)
Login: customer@nears.com (user 6, zone 2) | Backend: 10.0.2.2:8000 (config 200)

## AC / regression outcomes
- AC1 (transport failure NOT sticky) — PASS (test-substantiated + live supporting).
  - Load-bearing test revert->fail (5 transient cases Expected null/Actual []), restore->pass.
  - Live: airplane-mode Place Order -> "Order Failed / Connection to API server failed", NOT
    address_outside_delivery_zone; recovered via Try Again WITHOUT leaving checkout -> order 170 placed.
  - Paired [FAIL] endpoint=/api/v1/customer/order/place http_status=null type=ApiFailure correlation_id=dc7b91de... (PII-safe).
  - Caveat: exact changed branch (refresh on null-zoneIds addr) bypassed live — book addresses carry
    populated zone_ids (backend address_data_formatting), so refresh returns early. Branch proven by test.
- AC2 (genuine 404 blocks) — PASS (test-substantiated + live outcome).
  - Live: Dhaka zone-1 address vs zone-2 store -> "This address is outside the store's delivery zone."
    + Place Order gated, no order created. 404 branch itself proven by test (stamps [], isOutOfZone true).
- AC3 (in-zone happy path) — PASS (live). In-zone address -> Place Order -> order 169 placed (zone 2, COD).
- Regression: in-zone order places (169/170); out-of-zone warning shows + blocks (no order). CLEAN.

## Automated
- flutter test checkout_zone_refresh_transport_test.dart: 7/7 pass (fix); 5 fail on revert; restore pass.
- flutter test test/features/checkout/: 126/126 pass.

## Evidence shots
00 launch | 01 home | 02 checkout in-zone | 03 order placed AC3 | 04 out-of-zone AC2/regression
05 transport-fail not zone-block AC1 | 06 recovery order placed AC1
