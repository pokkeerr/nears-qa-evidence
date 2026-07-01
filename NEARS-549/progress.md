# NEARS-549 QA progress — StoreLogic zone-decode hardening

worktree: /Users/Apple/Projects/nears-NEARS-549-zonedecode @ 70784baf
surface: Laravel API (backend), local. Device=backend/local.

## AC1 — Automated backstop (phpunit) — PASS
- Full suite: 420 tests, 5157 assertions, OK (EXIT=0). Time 31s. 1+2 deprecations (pre-existing, non-fatal).
- ParseZoneIdsTest: 2 tests / 14 assertions OK (incl. [{"x":1}], [true], [null], scalar "2", object -> [] fail-closed cases).
- TowerStoresZoneScopingTest: 6 tests / 17 assertions OK (malformed/absent/valid + all_zone_service gating).
- SearchStoresZoneScopingTest (adjacent): 4 tests / 14 assertions OK.
- evidence: phpunit-full.txt

## AC2 — Live fail-closed repro — PASS
- get-stores/all: valid [2]->15 zones[2], [1]->6 zones[1], [1,2]->21. Malformed ("2", bare 2, [{"x":1}], [true], [null], not-json, "null", []) -> ALL total_size 0, HTTP 200, no 500. Absent -> default-zone substitution (zone 2), safe.
- evidence: failclosed-matrix.log

## AC3 — Discounted before/after (intended change) — PASS
- BEFORE (2e506bda): valid [2] -> total_size 533 across zones [1,2,364..373] = cross-zone LEAK. Malformed -> 533 (fail-open).
- AFTER (70784baf): valid [2] -> 14 zones[2]; malformed -> 0. Excluded rows are genuine zone-1 (ids 1,2,3,36,37,38), returned by zone [1]; union [1,2]=20. Not a regression.
- evidence: discounted-before-after.log

## AC4 — Regression sweep — PASS
- latest/popular/top-rated/search: valid [2] zone-scoped, malformed -> 0. recommended 0 (none seeded, not a leak).
- Logs-first: zero local.* [FAIL] for any store-listing endpoint on valid+malformed.

## Pre-existing (regression-candidate, NOT a 549 regression)
- GET /api/v1/stores/nearby -> HTTP 500 SQLSTATE[42000] 1064 (distance selectRaw + unquoted store_business_model/max_order literals). Reproduced on OLD code too. Zone clause correctly wired (SQL: zone_id in (2) valid / 0=1 malformed). Fails safe (aborts, no leak).
- evidence: bug-nearby-preexisting-500.log

