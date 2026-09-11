# NEARS-3503 QA evidence — vendor order-list N+1 residuals

Device-free ticket (Backend/Laravel only). Verified against:
1. Worktree's own `phpunit` suite (`Nears2999VendorOrderListQueryCountTest`), run twice live by QA (not trusted from the engineer's report) — 4/4 green both times, `multi_food_db_test_nears_nears_3503_vendor_order_n1_residua` (isolated per-worktree test DB, `DatabaseTransactions`).
2. Worktree's own `artisan serve` (port 8071) booted against the REAL seeded dev DB (`multi_food_db`), hit with a real vendor login (`demo.store@gmail.com` / vendor id 1) and real bearer token, for all 3 endpoints (`GET /api/v1/vendor/all-orders`, `/completed-orders?status=all`, `/canceled-orders`) — all 200, response JSON saved here.
3. `php artisan tinker` calls (read-only SELECTs) against the same real dev DB directly invoking `VendorController::get_all_orders/get_completed_orders/get_canceled_orders`, wrapped in `DB::listen()` to count real live query volume:
   - `get_all_orders`: 200, **14 queries**
   - `get_completed_orders`: 200, **14 queries**
   - `get_canceled_orders` (POST-fix): 200, **14 queries**
   - `get_canceled_orders` LEGACY shape (`->with('customer')` only, pre-fix simulated inline against the same live DB): **31 queries for only 6 orders** (vs. 14 for the fixed path serving up to 25) — establishes the PRE vs POST baseline for `get_canceled_orders` fresh, live, on real data (this endpoint had zero prior baseline per the ticket).
4. `Admin/storage/logs/laravel.log` mtime unchanged (20:53, before any of the above live calls) — zero `[FAIL]`/`[ERR]` lines attributable to any of the 3 endpoints under test.
5. Regression sweep: `current-orders` (untouched sibling) and `profile` both 200, unaffected.

Saved response bodies:
- `ac1-all-orders-response.json`
- `ac2-completed-orders-response.json`
- `ac3-canceled-orders-response.json`

Store-less-order (min/max_delivery_time == 0, not null) branch has no reachable live fixture in the seeded dev DB (no orphaned `store_id` rows found) — covered instead by the dedicated phpunit unit test `test_store_less_order_min_and_max_delivery_time_stay_zero_not_null`, which constructs the fixture directly and passed live (real Laravel boot, real Eloquent, real transactional test DB).
