# NEARS-694 QA — live evidence summary

Backend: worktree `feat/NEARS-694-itemcontroller-zone-decode` on `php artisan serve :8099` (DB multi_food_db, read-only GETs).
Module 1 (Grocery & Food, all_zone_service=0). Zone 2 = Abu Dhabi (requesting), Zone 1 = demo (cross-zone).
DB reference — zone2 milk items: 151,199,227,235,247,260,282,312,332 (9); zone1 milk items: 6,14,360,369.
zone2 module1 stores: 8,9,12,13,14,16,17,18,19,20,21,22,35,4117,4118 ; zone1: 1,2,3,36,37,38.

## Static (AC1 / AC2)
- AC1: `grep 'json_decode($zone_id' ItemController.php` -> NONE. 3 remaining json_decode are non-zone (category_ids L101, attachment L719, rating L822). PASS.
- AC2: 11 `parseZoneIds` sites across 6 actions (L166,173,305,312,450,457,857,919,963,1197,1219). Group-B L971/976 whereIn use `$zones = parseZoneIds()` (L963). 0 `whereIn(zone_id/zones.id)` bypass parseZoneIds. 0 residual `when(!empty($zones))` gates. PASS.

## Group A — /items/search?name=milk (get_searched_products)  [PRIORITY]
| zoneId | HTTP | total_size | products |
|---|---|---|---|
| [2] valid | 200 | 13 | 199,247,151,227,235,260,282,312,332,166,287,310,339 — ALL zone-2 (DB-verified), zero z1 leak |
| [true] crafted | 200 | 0 | [] fail-closed |
| {} crafted | 200 | 0 | [] fail-closed |
| absent | 200 | 13 | = [2] (setZoneIds backfill to z2 via geo) — expected, not a fail |
Shape keys: total_size,limit,offset,products,categories — intact.

## Group B — /items/common-conditions (get_store_condition_products)
| case | HTTP | result |
|---|---|---|
| omit store_id | 403 | "store id field is required" (contract) |
| store_id=53(z2 pharmacy) zoneId[2] | 200 | total=0 (no seeded condition items; valid-data covered by phpunit) |
| store_id=53 crafted[true] | 200 | 0 — not 500 |
| store_id=53 crafted{} | 200 | 0 — not 500 |
| store_id=0 crafted[true] (browse-all quirk) | 200 | 0 |
Deep browse-all fail-closed (gates removed) proven at method level by phpunit `test_common_conditions_browse_all_crafted_zone_fails_closed` (green).

## Type 4 — /items/item-or-store-search
| case | HTTP | stores | items |
|---|---|---|---|
| name=Market [2] | 200 | 8,13,14,17,18,19,21,22 — ALL zone-2 (DB) | 50 items, all zone-2 (DB) |
| name=Market [true] | 200 | [] | [] fail-closed |
| name=Market {} | 200 | [] | [] fail-closed |
| name=milk [2] | 200 | [] (no store named milk) | 14 items all zone-2 (incl. 62) |
| name=milk [true] | 200 | [] | [] fail-closed |
all_zone_service=1 bypass: no such module seeded -> phpunit `test_item_or_store_search_stores_all_zone_service_bypass_preserved` (green).

## Security smoke (3 not-independently-HTTP-tested actions)
- /items/search-suggestion name=milk: [2]->200 total_size=9 (=exactly the 9 zone-2 milk items) ; [true]->200 total=0 ; {}->200 total=0. FAIL-CLOSED.
- /stores/smart-suggestions: [2]->200 total=10, items 52,62,80,95,96,147,153,154,169,240 all zone-2 (DB) ; [true]->200 total=0 empty. FAIL-CLOSED.
- /items/item-or-store-search items[]: covered above (zone-2 scoped + crafted empty).
- /items/cross-store-search: HTTP 404 -> config-gated (nears.enable_cross_store_search=false) DISABLED; covered by phpunit/static.

## Delegating-action regression spot-check (ProductLogic, hardened 692)
- /items/popular [2]: 200, total=219, first ids 210,216,218,301,338 all zone-2 (DB). No regression.
- (/items/latest requires store_id+category_id — separate contract, not used.)

## phpunit backstop (AC5)
`vendor/bin/phpunit --filter 'ItemZoneScoping|ParseZoneIds' --testdox` -> 11/11 pass, 75 assertions, 0 skips. 2 PHPUnit framework deprecations (non-blocking). See phpunit-testdox.log.

## Logs-first gate ([api])
- laravel.log: no item/zone/search-scoped [FAIL]/ERROR/exception from the live run. The only 2 today-ERROR lines are `testing.ERROR` phpunit fixtures (`/api/_sec_test/boom` redaction test; fake-token social-auth negative test) — pre-existing, unrelated.
- serve.log :8099: 69 normal request timings, zero 500s, zero PHP Fatal/Warning, zero stack traces.
- Crafted headers return HTTP 200 empty (fail-closed by design) — correctly NO error toast / NO [FAIL] (not an error path). CLEAN.
