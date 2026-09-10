# NEARS-3425 QA progress

## AC1 [behav] — PASS
Two identical back-to-back buy-now POST /api/v1/customer/order/place with the
same X-Idempotency-Key against the live backend (private QA DB clone
multi_food_db_test_qa3425): first -> 200 order_id=91231; replay -> 200,
SAME order_id=91231, same created_at. DB: SELECT COUNT(*) FROM orders WHERE
idempotency_key=... = 1.
Also ran a GENUINE concurrent race (two parallel curl processes, same key):
both resolved to the SAME order_id=91240, DB count = 1.

## AC2 [api] — PASS
Duplicate request returns the SAME order reference (200, same order_id), never
a silent second order. laravel.log grepped scoped to the duplicate request's
X-Request-Id — clean (no [ERR]/[FAIL]). 409 order_already_processing path +
DB-unique-constraint backstop path both covered green by
BuyNowOrderIdempotencyTest.php (8/8, 27 assertions) — falsifiable, calls
production OrderPlacementService directly.

## AC3 [behav] — PASS
Normal single buy-now placement (item 41, fresh key) -> 200, order_id=91232,
1 DB row, ~2.16s (no added latency). Also demonstrated LIVE ON DEVICE via
from-cart checkout (scope item 11, see below) — clean Track Order screen,
0 flutter errors.

## Scope items 1-7 (backend, direct API replay) — all PASS, see envelope ac_table
## Scope item 11 (device, from-cart unaffected) — PASS, order 91239, idempotency_key
   NULL in DB, /api/v1/customer/order/place hit normally, Track Order screen clean.
## Scope items 8/9/10 (device buy-now retry/409/coupon-rotation UI) — UNVERIFIABLE
   ON DEVICE: the only user-reachable "buy-now" UI entry (campaign "Order Now")
   is blocked by a pre-existing, unrelated backend defect (CampaignController::
   get_item_campaigns always throws + silently swallows -> empty list). Filed as
   regression_bugs. AC1/2/3 independently confirmed via direct backend replay
   (explicitly sanctioned by ticket brief) + 17 passing UserApp unit tests
   covering the exact production key-mint/reuse/rotate/409-toast symbols.
## Scope item 12 (ar.json RTL) — reviewed via diff, EN/AR both present, flagged
   NEEDS_NATIVE_REVIEW per doc (non-blocking machine draft, as scoped).
## Scope item 13 (backend regression) — 8/8 BuyNowOrderIdempotencyTest +
   31/31 adjacent order-placement suite tests green.
## Automated backstop — UserApp flutter test: 17/17 green
   (api_client_idempotency_key_test.dart + place_order_idempotency_key_test.dart)
