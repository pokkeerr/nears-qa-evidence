# NEARS-684 QA progress checkpoint

- Ticket: NEARS-684 — cart add/update 500 (SQLSTATE 23000 module_id null) when moduleId header absent
- Worktree: /Users/Apple/Projects/nears-NEARS-684-cart-null-module @ feat/NEARS-684-cart-null-module 7e6fb167
- Runtime proof of FIXED code: autoloader ReflectionClass(CartController)->getFileName() ==
  <worktree>/Admin/app/Http/Controllers/Api/V1/CartController.php ; contains `?? $item->module_id` (FIX PRESENT)
- Live surface: `php artisan serve` from worktree on :8384, DB override DB_DATABASE=multi_food_db_test
  (throwaway copy — real multi_food_db never mutated). Config env override confirmed reaching config().
- Device/DB: no device lock (backend); read-only on real dev DB.

| AC | verdict | evidence |
|----|---------|----------|
| 1 add no-header authed | PASS | phpunit test_add_without_module_header_returns_200_and_persists_item_module (200, module_id=item) |
| 1 add no-header guest  | PASS | curl guest 990002 item52 -> 200, non-empty, carts.module_id=1==item.module_id |
| 2 BE-log no SQLSTATE   | PASS | laravel.log 28->28 lines; grep SQLSTATE[23000]/module_id-null/[FAIL] cart/add -> NONE |
| 3 with-header regression | PASS | curl moduleId=2 header on item(module1) -> persisted module_id=2 (header wins); moduleId=1 -> 1 |
| 4 dup-row guard        | PASS | curl re-add guest 990002 -> ONE row id877 qty 1->2; phpunit test_readd..increments_single_row |
| 5 update no-header     | PASS | phpunit test_update_without_module_header_returns_200_and_keeps_module (200, module non-null) |
| 6 ItemCampaign path    | UNVERIFIABLE | zero item_campaigns rows in multi_food_db / _test / _qa337; code path model-agnostic + item_campaigns.module_id NOT NULL |

- Regression: cart list 200 (row returned), remove-item 200 (row deleted), store-closed guard 403 still fires. Max-qty via green cart-security group.
- Automated: CartNullModuleTest 3/3; cart-security group 14/14; full Feature suite 387/387 (1582 assertions), only 2 PHPUnit doc deprecations.
- Pre-existing (not this ticket): 2x SQLSTATE[42S22] "Unknown column food_details" in order_details insert, testing.INFO, from a prior order-placement test in test DB.
