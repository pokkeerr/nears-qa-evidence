# NEARS-378 QA progress (live, fix_cycle 0)

Backend: patched worktree `/Users/Apple/Projects/nears-NEARS-378-vendor-guard/Admin` on `php artisan serve :8001`, real `multi_food_db` (read-only).
Owner: organicshop@demo.com (vendor 6, store 9, 15 items). Foreign item: id 203 (store 13). Employee: NONE seeded (0 rows) -> cite phpunit.

VERDICT: FAIL (one task-bug breaks AC6 no-regression).

- AC1 (read owner, list): PASS — get-items-list total_size 15, all 15 items store_id=9, zero leak.
- AC1b (read owner, details own id 52): PASS — HTTP 200, Strawberries, store_id 9.
- AC2 (cross-store deny owner, foreign id 203): PASS — HTTP 404 product-001 "Not found", no name/store_id 13 leak.
- LIVE STORESCOPE PROOF: PASS — get-items-list live SQL shows `store_id = 9 and store_id = 9` (explicit guard + ARMED StoreScope) -> scope arms in a real HTTP request (live-storescope-sql.log).
- AC3 (write-deny owner, foreign id 203 status toggle): PASS — HTTP 404, findOrFail before save; DB item 203 status unchanged (=1).
- AC4 (employee): PASS via phpunit (no employee seeded live) — `test_employee_request_scopes_items_to_employee_store` + employee seeding test green.
- AC5 (phpunit 5 suites): PASS — 17/17 (44 assertions), 2 framework deprecations only.
- AC6 (no-regression read end-to-end): FAIL — `/vendor/profile` regresses 200(base) -> 500(patched). StoreScope arms inside get_profile's un-qualified items() count; get_store_id() -> auth('vendor')->user() NULL -> "read property id on null" (Helpers.php:2213). Only profile affected (7 other token endpoints 200). See bug-vendor-profile-500.log.
