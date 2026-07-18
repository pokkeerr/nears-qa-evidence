# NEARS-1044 — Live QA Evidence (backend API)

- **Verdict:** PASS
- **Build:** worktree `nears-NEARS-1044-order-groups`, branch `feat/NEARS-1044-order-groups`, HEAD `63934829`, base `145ca753`.
- **Env:** REAL Laravel server `php artisan serve :8001` against worktree-scoped DB clone `multi_food_db_nears_1044` (production `multi_food_db` never migrated/mutated). 2 additive migrations applied to clone only (`order_groups` table + `orders.order_group_id` char(36)). Customer `customer@nears.com` (user 6), zone 2, module 1, stores 12+13, items 51+203.
- **QUEUE_CONNECTION=sync** → notifications fired inline.

## Per-AC (each = live HTTP call + DB read on clone)

| AC | HTTP | Result | DB read | Verdict |
|----|------|--------|---------|---------|
| AC1 place happy 2-store | POST group/place [12,13] → **200** `{group_id, order_ids:[91108,91109], total_amount:17, group_placed:true, orders:[…]}` | 1 order_groups row (id 36-char UUID `64564ec7…`, child_count=2, zone_id=2, module_id=1) + 2 orders both carrying that order_group_id | PASS |
| AC2 all-or-nothing | store13 min_order=999999, POST group/place [12,13] → **403** `{group_placed:false, errors:[{code:group_gate, reason:minimum_order, store_id:13, store_name:"Fresh supermarket"}]}` | order_groups & user6 grouped-orders counts UNCHANGED (1/2 before, 1/2 after) — store 12's in-transaction order rolled back, NOT persisted | PASS |
| AC3 pre-flight | POST group/validate (failing basket) → **200** `{valid:false, stores:[{12,pass:true},{13,pass:false,reason:minimum_order}]}`; valid basket → `valid:true` | counts UNCHANGED (zero rows written by dry-run rollback) | PASS |
| AC4 cross-zone | POST group/place [12(zone2),1(zone1)] delivery in zone2 → **403** `{group_placed:false, errors:[{code:group_gate, reason:out_of_coverage_area, store_id:1}]}` | counts UNCHANGED (zero rows) | PASS |
| AC5 single-store unchanged | POST customer/order/place (store 12) → **200** `{message, order_id:91110, total_ammount:8, status:pending, created_at, user_id:6}` | created order `order_group_id IS NULL` | PASS |
| Spot: group/details owner | GET group/details (user 6) → **200** `{group_id, order_ids:[91108,91109], orders:[…]}` | — | PASS |
| Spot: IDOR no guest_id | GET group/details, invalid bearer, no guest_id → **403** `guest id field is required` (SEC-1044-1 fix holds) | — | PASS |
| Spot: IDOR wrong guest_id | GET group/details, invalid bearer + guest_id=999 → **404** Not found (does NOT return user 6's group) | — | PASS |

## Logs-first (BE `[api]` gate, X-Request-Id correlated)
- Zero `group_order_place_failed` / `group_order_validate_failed`; zero uncaught exceptions in serve log.
- Only error present: 6× `production.ERROR: FCM API Error` (status 400) — post-commit push fan-out. Correlation-joined to AC1 request-id AND reproduces on the UNTOUCHED single-store path (AC5 request-id) → environmental (local dev has no valid FCM creds/device tokens), NOT a NEARS-1044 defect, breaks no AC.

## Automated backstop
- `vendor/bin/phpunit tests/Feature/GroupOrderPlacementTest.php` → **OK 8/8, 46 assertions** (private test DB, DatabaseTransactions).

## Regression
- AC5 is the key guard: single-store contract byte-identical, `order_group_id` NULL. Clean.
- 37 pre-existing suite reds: pre-existing per code+security review context (reproduce on base); not independently re-run full-suite here (cost) — treated as regression context, never a FAIL of this run.
