# NEARS-378 QA progress

## fix_cycle 0 (prior) — VERDICT: FAIL
Owner organicshop@demo.com (vendor 6, store 9). Core security PROVEN (cross-store 404 on foreign id 203/store 13, live SQL store_id guard). FAILED on ONE task-bug: `/api/v1/vendor/profile` 500 (get_store_id null-deref via newly-armed StoreScope in get_profile's items() count). See bug-vendor-profile-500.log.

## fix_cycle 1 (DELTA re-QA, NEARS-537 fix) — VERDICT: PASS
Backend: patched worktree `/Users/Apple/Projects/nears-NEARS-378-vendor-guard/Admin` on `php artisan serve :8001`, real `multi_food_db` (READ-ONLY). Login requires `vendor_type:owner` in body.
Owner (single-store): vendor 6 organicshop store 9. Owner (MULTI-STORE, security-critical): vendor 2 ahmed.khan@demo.com stores [2,6]. Foreign item: id 52 (store 9). Employee: 0 seeded -> phpunit covers.

- AC1a (THE fix — cold-first profile, owner): PASS — server restarted cold, profile = FIRST vendor-token request, vendor 2 -> HTTP 200 (was 500). Zero laravel.log errors. (delta-ac1a-coldfirst-multistore.log)
- AC1b (profile AFTER prior request, scope-arming order): PASS — vendor 6: get-items-list(200,15@store9) -> profile 200 -> profile-again 200, 0 errors. vendor 2 multi-store: get-items-list(200,22@store2) -> profile 200, 0 errors. The exact ordering that previously 500'd now 200. (delta-ac1b-after-prior-request.log)
- AC1c (employee): NONE seeded live -> covered by phpunit VendorProfileStoreScopeTest::test_employee_profile_resolves + VendorItemGlobalScopeTest::test_employee_request_scopes_items_to_employee_store (green).
- AC1d (multi-store own-store resolution, security-critical): PASS — vendor 2 profile out_of_stock_count=1 == store 2 OWN ground truth (stock<=min). NOT 6 (own vendor's 2 stores combined) and NOT 15 (all-stores leak). resolve_owner_store uses constrained $vendor->stores()->first() -> cannot return foreign store. (delta-ac1a-coldfirst-multistore.log)
- AC2 (NEARS-378 core security STILL intact): PASS — owner vendor 2: own item/details/2 -> 200 (Red Apple, store 2); foreign item/details/52 (store 9) -> 404 "Not found", no name/store_id leak; foreign stock-update product_id=52 -> 404 (findOrFail on own-store scope) BEFORE save, DB item 52 stock unchanged (499). Fix did NOT weaken cross-store guarantee. (delta-ac2-cross-store-guard.log)
- AC3 (shared get_store_id ~120 callers, adjacent endpoints): PASS — categories 200 (33); item/stock-limit-list 200 (store_id [2]); category-wise-products 200 (store_id [2]). All own-store-scoped, helper change broke no adjacent read. 4th endpoint item/search 500 = PRE-EXISTING `with(['rating'])` undefined-relation bug, change-INDEPENDENT (ItemController byte-identical to HEAD; trace doesn't touch get_store_id/StoreScope) -> regression_bug lane, does NOT affect verdict. (delta-ac3-adjacent-endpoints.log, bug-vendor-item-search-rating-500.log)
- AC4 (phpunit): PASS — 20/20 (55 assertions), 2 framework deprecations only. Includes 3 NEW VendorProfileStoreScopeTest methods. Up from 17/17 in fix_cycle 0. (delta-ac4-phpunit.log)

regression_bugs (pre-existing, batched to PO): POST /vendor/item/search HTTP 500 (Item has no rating() relationship; bug-vendor-item-search-rating-500.log).
task_bugs: NONE.

THE fix (profile 500) is RESOLVED. Done gate CLEARED.
