# NEARS-3449 QA progress log

Surface: headless Laravel backend (no Flutter/mobile UI). No device lock needed
(device-free ticket). DB-mutating QA -> own DB clone + own `php artisan serve`
per profile "Backend/DB contention" rule.

## Setup
- Isolated DB clone: `multi_food_db_qa3449` (mysqldump of `multi_food_db`, 162 tables).
- Isolated backend: `DB_DATABASE=multi_food_db_qa3449 php artisan serve --host=127.0.0.1 --port=8020`
  (shared dev backend on :8000 untouched).
- Vendor login: ts@ts.com / store_id=35 / module_id=1 / zone_id=2 (vendor id 26).
- Customer login: customer@nears.com / user_id=6 / zone_id=2.
- Fixtures created directly via SQL INSERT into coupons/orders (same shape as the
  ticket's own Nears3449...Test.php fixtures) — real DB rows, not mocked.

## AC1a — general limit branch self-count (coupon N3449AC1A, order 91357)
PUT /api/v1/vendor/update-order-amount -> HTTP 200 (not 406). PASS.
CONTROL-A (coupon N3449CTLA, orders 91363/91364 — a GENUINE second redemption,
not a self-count): editing order 91364 -> HTTP 406. Proves the fix targets only
the self-count, not a blanket bypass.

## AC1b — first_order branch self-count (coupon N3449AC1B, order 91358)
Existing qualifying orders for user 6 (excl. order under test) = 77; limit set to 78.
PUT /api/v1/vendor/update-order-amount -> HTTP 200 (not 406). PASS.
(First attempt at limit=73 mis-set the fixture math relative to sibling fixture
orders also counting as "prior orders" for user 6 -- corrected to 78, re-verified 200.)

## AC2 — total_uses accounting on repeated edits (coupon N3449AC2, free_delivery,
limit=null, total_uses seeded to 1 = placement value; order 91359)
3x PUT /api/v1/vendor/update-order-amount (amounts 60/70/80), each HTTP 200.
total_uses after each edit: 1, 1, 1 (never 2/3/4). PASS.

## AC3 — web/API parity (coupons N3449AC3W/N3449AC3A, orders 91360/91361, both
total_uses seeded to 1)
Web surface driven via `php artisan tinker` invoking
`App\Http\Controllers\Vendor\OrderController::edit_order_amount` directly under an
authenticated `vendor` guard session against the SAME live DB clone (the
Store-Panel login form is CAPTCHA-gated -- same technique the ticket's own
regression test uses for this surface, `callWeb()` in
Nears3449CouponTotalUsesEditAccountingTest.php, its documented sanctioned
fallback). 3x edits (60/70/80): total_uses stays 1.
API surface driven via curl PUT (same as AC2). 3x edits: total_uses stays 1.
Final: web total_uses=1, api total_uses=1 -- parity. PASS.

## AC4 — regression test suite
`vendor/bin/phpunit --filter Nears3449CouponTotalUsesEditAccountingTest` -> 5/5 pass.
`vendor/bin/phpunit --filter Nears3431VendorFreeDeliveryCouponGateTest` -> 6/6 pass.
(Runs against the isolated phpunit twin DB, not the QA clone -- unaffected by the
QA clone's fixture rows.)

## Regression sweep (placement-time is_valide call sites, unchanged behavior expected)
- CouponController::apply (customer-facing coupon-apply, /api/v1/coupon/apply):
  static-confirmed call site still passes only 5 args (no exclude_order_id).
  Live: coupon N3449REG (limit=1, already 1 genuine prior order) -> GET apply ->
  HTTP 406 "Coupon usage limit over" (unchanged). Positive control: fresh unused
  coupon N3449REGOK -> HTTP 200 (endpoint isn't just always-406). Both PASS.
- OrderTaxService::getCouponData (/api/v1/customer/order/get-Tax): static-confirmed
  call site also unchanged (still 5-arg is_valide call, no exclude_order_id).

## Logs
grep for `[FAIL]`/`[ERR]` and `production.ERROR`/`production.WARNING` in
Admin/storage/logs/laravel.log around the live session window: 0 matches. All
`testing.*` channel entries present in the file are from the UNRELATED phpunit
full-suite run (isolated test DB, different log channel) -- not this ticket's
live HTTP session.
