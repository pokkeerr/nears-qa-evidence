# NEARS-1060 backstops

## Automated regression (private test DB, NEARS-1199)
$ vendor/bin/phpunit --configuration phpunit.xml tests/Feature/StoreListCountQueryPerfTest.php
...  3/3 (100%)  Tests: 3, Assertions: 13 (1 PHPUnit deprecation, non-blocking) — OK

## Regression log sweep (scoped grep, laravel.log)
SQLSTATE/QueryException/syntax/Unknown-column on stores|get-data|get_stores|store_schedule|avg_r|whereOpenNow endpoints: NONE (clean).
Pre-existing unrelated .ERROR lines: /stores/reviews 404 (store_id 999999 dummy), /stores/details/{id} 404, FCM API Error — all properly-logged [FAIL], timestamped before this run, not regressions.

## ModuleController store-count badge
Computes active_stores_count via its own Store::active()->selectSub(COUNT(*)); shares no code path with the modified StoreLogic having sites — provably unchanged.
