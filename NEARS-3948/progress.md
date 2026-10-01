# NEARS-3948 QA [8] - live evidence (first pass, fix_cycle 0)

Tested HEAD: e7e2da8058816ef4c430e29958576e5ca73f5c46 (fix/NEARS-3948-free-delivery-eligible), clean.
Device: emulator-5630 (AVD Pixel_10_Pro), UserApp flavored package `com.izzes.nears.nears_nears_3948_free_delivery_eligible`, debug build from the lane worktree, `--dart-define API_HOST=10.0.2.2:8150`.
Backend: own `php -S` on :8150 from the lane worktree Admin/ (router wrapper = QA instrument that records selected request bodies; Laravel's own server.php is the router), DB `multi_food_db_qa_bug3948` (private copy). DB proof: `/api/v1/config` returned `free_delivery_over` values that only the copy carries. Shared DB checked at end: orders max id 91415, business_settings 228 = 0, no QA coupons.
Light mode only. Pixel/layout out of scope; money shown/charged, gating, copy, logs only.

Client value = fee shown on the checkout row / Delivery Fee line. Placed value = `orders.delivery_charge` of the placed child (see orders-placed-on-private-copy.tsv; X-Request-Ids in place-request-ids.txt).

| Cell | Setup (private copy) | Client shows | Placed child delivery_charge | Result |
|---|---|---|---|---|
| C1 AC1/AC2 straddle | 2 grocery stores (12: 130.00, 14: 130.84), over=100, coupon 30% | no coupon: 0.00 / 0.00; with coupon: 1.00 / 1.00 (eligible 91.00 / 91.59) | 1.00 / 1.00 (orders 91418/91419) | PASS |
| C1b budget | coupon 30% max_discount 39 (first-come) | A 1.00, B 0.00 | A 1.00, B 0.00 (91422/91423) | PASS |
| C1c threshold between stores | over=91.5, coupon 30% | A 1.00, B 0.00 | A 1.00, B 0.00 (91433/91434) | PASS |
| Ticket repro, single store (AC3) | subtotal 20, amount coupon 2, over=19 | no coupon Free; with coupon +1.00 | 1.00 (91429) | PASS |
| C3 AC4 group | over=0, no coupon, group | 1.00 / 1.00 | 1.00 / 1.00 (91426/91427) | PASS |
| C3 AC4 single | over unset (config serves 0), single store | +1.00 | 1.00 (91428) | PASS |
| C3 boundary | single, coupon 2, over=18 (eligible 18) | Free | 0.00 (91430) | PASS |
| C3 boundary-1c | over=18.01 | +1.00 | not placed (server rule is >=, unrounded) | PASS (client only) |
| C4 AC5 vendor free_delivery coupon on store 12 | over=1000 | A 0.00, B 1.00 | A 0.00, B 1.00 (91437/91438) | PASS |
| C4 AC5 min_purchase 130.50 | A 130.00 below, B 130.84 above | A 1.00, B 0.00 | A 1.00, B 0.00 (91441/91442) | PASS |
| C4 AC5 discount-arm store_wise [12] 30% | over=100 | A 1.00, B 0.00 | A 1.00, B 0.00 (91487/91488) | PASS |
| AC-REG single-store free_delivery coupon | over=1000 | Free | 0.00 (91443) | PASS |
| C5 AC6 undecidable | store_wise coupon, data `[12,"abc"]` (server accepts, client cannot parse) | 1.00 / 1.00 (not Free) | A 1.00, B 0.00 (91446/91447): shown-higher residual per advisor-product -003 | PASS |
| C6 AC7 referral | first-order user (ref bonus 5), subtotal 20, over=18 | Free | 0.00, ref_bonus_amount 5 (91448) | PASS |
| C6 Retry | same user, forced 500 on delivery-quote, then Retry | "Something went wrong Retry" + paired [FAIL]; Retry -> Free, request amount 15.0 | n/a | PASS |
| C7 mixed-module | flag on (copy), grocery 14 + pharmacy 58 | P30: pharmacy 0 / grocery 1; FDALL(over 1000): pharmacy 1 / grocery 0; all_store: 0 / 0 | oracle group/validate amounts.delivery_charge identical (oracle-group-validate-mixed.txt) | PASS |
| C8 quote body | all cells | group: store subtotals 130.84 / 130.0 even with coupon applied; single: orderAmount (20.0, 18.0 coupon-net, 15.0 referral-net) = unchanged | n/a | PASS |
| C8 take_away | no take-away toggle reachable via UI on this build | n/a | n/a | UNVERIFIABLE live (code path untouched by diff) |
| C2 F1 re-price | slow-quote instrument (6s/20s) | apply: one quote pair, rows Free -> 1.00; remove: one pair, rows -> Free; Place Order tap while pending logged `[WARN] checkout: place order tap blocked - pricing not settled`, skeleton rows | n/a | PASS |

Automated: `flutter test test/features/checkout test/features/cart test/features/coupon` -> `+2094: All tests passed!`.

Logs: undecidable line appears exactly once per compute (app-log-excerpts.txt), reasons token only, no ids/PII. No other unexpected [FAIL]/[ERR]; /coupon/list 500 observed only after the injected malformed-data coupon rows (regression candidate, below).

Regression candidate: GET /api/v1/coupon/list returns 500 (`count(): Argument #1 ($value) must be of type Countable|array, null given`, correlation_id e29190fb-3038-405b-acdc-6eb834222f26) whenever any active coupon has malformed `data` (store_wise `garbage{`, zone_wise `[bad`); disabling those two rows restores 200. App paired it with `[FAIL] coupon list load failed`. Pre-existing backend; only reachable via corrupt data.
