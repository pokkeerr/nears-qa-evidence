# NEARS-4111 QA setup + AC matrix (tested_sha c4af5bb5e4ae096abc7b82348e4f0ddee6262c7f, code checkpoint 189c703aa, base c891fda8cf9b285fb54e00efb088e55668b09a7f)

Setup
- BASE server = scratch detached worktree @ c891fda8c on 127.0.0.1:8572; TIP server = scratch detached worktree @ c4af5bb5e on 127.0.0.1:8571.
  Each tree has its OWN real copy of Admin/vendor (cp -R, no symlink), its own Admin/.env (only DB_DATABASE, APP_URL, OTEL_SDK_DISABLED=true, SESSION_SECURE_COOKIE=false, LOG_LEVEL=debug edited) and the same passport keys.
  `git diff c891fda8c c4af5bb5e -- Admin/app` = the single Helpers.php hunk (3 insertions, 5 deletions).
- Servers: `php -d pcre.jit=0 -S 127.0.0.1:<port> -t public server.php` (cwd of each listener verified with lsof: the scratch tree; backend-freshness-check.sh PASS on both ports, "not a per-ticket worktree").
- Private DB `multi_food_db_qa4111` (clone of `multi_food_db_test`). Marker: business_name `NearsQA4111` served by BOTH servers via /api/v1/config (the shared multi_food_db still serves "Nears"). multi_food_db and every multi_food_db_test_* DB were never touched.
- Code marker: item 51 at 100% own discount -> BASE quote HTTP 500 `DivisionByZeroError` (log type + Helpers.php:5454 / :5432 throw site), TIP quote HTTP 200 tax 0.
- No raw DML anywhere. Every fixture went through the product's own routes: Admin business-setup (digit, marker), Admin order settings (free delivery, packaging), Admin customer settings (referral), Admin Items bulk-update upload (item discount/price/stock/add-ons), Admin addon store, TaxModule routes (tax + system tax + packaging tax), Admin store discount, Admin flash-sale store/store-product/publish, Admin store toggle (pos_system), Vendor store-setup (packaging), customer sign-up (referred customers), customer login/get-Tax/place, Admin order edit/update/POS, Store Panel POS.
- Customer: customer@nears.com (user 6, zone 2, store 12, module 1), password from users_test_data.md. Admin: admin@admin.com. Store owner: freshlocal@demo.com (vendor 9, store 12).
- Same customer token drives BASE and TIP (one login; the login route is throttled at 5/min).

Harness lessons (so nobody re-learns them)
- First pass had the Vat4111 `taxes` row inactive (the TaxModule add route creates it inactive; activation is GET /taxvat/update-taxvat-status/{id}). The VAT-on rows of that pass were vacuous and were discarded; everything in these logs is the re-run with a live 10% VAT (control quote 8.00 -> tax 0.8).
- Quote/place `cart` must be the JSON STRING (is_buy_now=1); an array body gives `json_decode(): Argument #1 must be of type string` (the one such [FAIL] line in the tip log is my own first malformed request).
- Item 51 stock is consumed by every order: reset through the bulk-update route before each run, else 403 `stock` on both servers.
- admin_free_delivery_status=1 in the clone made every delivery charge 0; AC2 was run with it switched OFF so "order_amount = delivery charge" is 1.00 (fixed zone charge), not 0 = 0.
- Admin POS: never GET /admin/pos between add-to-cart and order (index() clears the session cart).

AC matrix (BASE c891fda8c -> TIP c4af5bb5e), VAT = order-wise 10% off / on

| AC | BASE | TIP | file |
|---|---|---|---|
| AC1 get-Tax item 51 @100%, qty 1 and 2, VAT off and on | 500 `{"message":"Something went wrong"}` x4, log `DivisionByZeroError` | 200 tax_amount 0, total_discount = line total, x4 | ac1-ac2-customer-quote-and-place-100pct-item-base-vs-tip.log |
| AC2 place qty 1 and 2, VAT off and on | 403 generic "Failed to place order" x4, no order row, `[FAIL] new_place_order failed` exception_type DivisionByZeroError Helpers.php:5454 | 200, orders 1.00 = delivery_charge 1.00, total_tax_amount 0.00, no [FAIL] line | same + log-summary-division-by-zero-base-vs-tip.log |
| AC3 Admin edit/update on an order holding the 100% item | edit 500 and update 500 (DivisionByZeroError), order untouched | edit 302, update 302, edited 0 -> 1, order_amount 1.00 / tax 0.00 unchanged | ac3a-admin-order-edit-update-100pct-item-base-vs-tip.log |
| AC3 Admin POS add-to-cart + order | add-to-cart 500, order 500, no order | 200 / 200, order stored: order_amount 1.00, tax 0.00 | ac3b-admin-pos-100pct-item-base-vs-tip.log |
| AC3 extra: Store Panel POS (freshlocal@demo.com, web route) | add-to-cart 500, order 500 | 200 / 200, order stored: order_amount 0.00, tax 0.00 | ac3c-store-panel-vendor-pos-100pct-item-base-vs-tip.log |
| AC4 no discount; 25% partial discount (quote, place, edit/update, Admin POS, Store Panel POS; VAT off/on) | 200/200/302-302/200/200, tax 0 / 0.8 (no disc), 0 / 0.6 (25%) | byte-identical on every captured field (BASE == TIP True x4) | ac4a-controls-no-discount-and-partial-discount-base-vs-tip.log |
| AC4 referral bonus 100% of an 8.00 basket (real sign-up with ref_code, first order), own discount 0 | 200 quote (total_discount 8), place 200 ref_bonus 8.000, admin update 302 | identical (BASE == TIP True x2) | ac4b-..., ac4c-control-referral-bonus-nets-to-zero-take-away-order_amount-0.00-base-vs-tip.log |
| AC5 price-0 add-on on a paid item, no discount, qty 1 and 2, VAT off/on | quote 500, place 403, Admin POS 500/500, Store Panel POS 500/500, Admin edit 500 + update 500 on a tip-placed order; place-time throw site Helpers.php:5432 | quote 200 (VAT on: 0.4 / 0.8 = item only), place 200, POS 200/200 + orders, Store Panel POS 200/200, Admin edit/update 302/302 with money unchanged | ac5-..., ac5b-... |

Extras
| Extra | Result | file |
|---|---|---|
| float drift 123.45 @100%, order-wise VAT | BASE and TIP BOTH quote tax_amount 1.4210854715202005e-15 (not exact 0); placed tax 0.00 | ex1-..., bug-order-wise-float-drift-tax-1e-15.log |
| float drift 123.45 @100%, product-wise VAT | BASE 1.42e-15 (2.8e-15, 5.7e-15, 1.1e-14 for qty 2/3/7), TIP exactly 0 | ex1b-... |
| digit 0 + 0.30 add-on (rounded total 0) | BASE quote 500 / place 403 / POS 500; TIP quote 200, place 200, POS 200, edit 302 | ex2-... |
| digit 0 + 0.60 add-on control (no div-by-zero) | BASE == TIP on every field (so the quote-vs-placed rounding gaps at digit 0 are pre-existing) | ex2b-... |
| 100% STORE discount (Admin store discount route) | BASE quote 500 / place 403 / POS 500; TIP 200 / 200 / 200 | ex3-... |
| 100% FLASH sale | route refuses exactly 100% and any discount_amount >= price (Item_discount_amount_exceeded); 99.99% is accepted but stores discount_amount 4.000 and nets the line to 0.0004 so BASE does not crash either -> a true 100% flash line is unreachable through a route: test-level only | ex3b-..., ex3c-... |
| free line + PAID packaging 0.50 (store packaging on, packaging tax on) | BASE 500 / 403; TIP quote tax 0.05 (packaging 10%), placed order_amount 1.55 = delivery 1.00 + packaging 0.50 + tax 0.05; paid-item control identical on both (tax 0.85, 10.35) | ex4-... |
| free item + PAID add-on 1.00 | BASE == TIP (normal path; add-on taxed) | ex5-... |
| Observation: Admin order pages for the free-goods COD order | details 200, list/pending 200, list/all 200 (order 91809, intact item_details) | observation-admin-order-pages-render-for-free-goods-order.log |

Automated backstop
- NOT re-run by QA: the NEARS-1199 DB guard only accepts multi_food_db_test / multi_food_db_test_<suffix>; QA's single allowed DB name multi_food_db_qa4111 is refused (backstop-phpunit-not-run.log). The engineer's recorded run (78/78 Nears4111, 12/12, 77/77, 689/689) is cited, not verified by QA. Consequence: the true 100% flash line (route refuses it) is NOT demonstrated by QA at any level.
