# NEARS-713 QA evidence — get-combined-data category_ids scalar guard

Verdict: **PASS** — worktree backend `feat/NEARS-713-categoryids-scalar-guard` @ 74a85428 (fix commit atop),
served locally on 127.0.0.1:8001 against read-only dev DB `multi_food_db` (zone 2 / module 1, term "Apple").

Endpoint: `GET /api/v1/get-combined-data?list_type=item&data_type=searched` → `SearchController::get_searched_products`
Fix: `is_array($category_ids) && count($category_ids) > 0` guard at L53 (mirror of brand_ids guard L58).

## category_ids ACs (live curl)

| AC | Call | HTTP | total_size | Result |
|----|------|------|-----------|--------|
| AC4a | category_ids absent (baseline) | 200 | 6 | unfiltered (ids 254,263,290,293,308,96) |
| AC4b | category_ids=[] | 200 | 6 | unfiltered — empty array skips filter (== baseline) |
| AC1  | category_ids=5 (scalar int) | 200 | 6 | unfiltered — guard skips (was 500 pre-fix) |
| AC2  | category_ids="foo" (scalar str) | 200 | 6 | unfiltered — guard skips |
| AC3a | category_ids=[4] (Fresh Fruits) | 200 | 2 | filtered → ids 254,290 (Red Apples); Apple Juice cat-10 excluded |
| AC3b | category_ids=[3] (parent) | 200 | 2 | filtered via parent_id → 254,290 |
| AC3c | category_ids=[999999] (nonexistent) | 200 | 0 | empty → proves real filter, not a no-op |

AC5: laravel.log — 0 new lines across all calls; no TypeError / count() / 500. clean.

## NEARS-707 regression re-check (same endpoint/method)

| Check | Call | HTTP | total_size | Result |
|-------|------|------|-----------|--------|
| REG1 | brand_ids=5 (scalar) | 200 | 6 | unfiltered — 707 guard holds |
| REG2 | brand_ids=[1] (array) | 200 | 0 | filter runs, narrows (no branded items seeded zone 2) |
| REG3 | brand_ids="foo" (scalar str) | 200 | 6 | unfiltered |
| REG4 | filter=top_rated | 200 | 6 | 200, no error |
| REG5 | category_ids=5 & brand_ids=7 (both scalar) | 200 | 6 | both guards skip together |

## Automated backstop
`vendor/bin/phpunit --filter GetCombinedDataCategoryIdsGuardTest` → **OK 4/4, 29 assertions** (test DB multi_food_db_test; dev DB untouched). 2 PHPUnit framework deprecations (non-blocking).
