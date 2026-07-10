# NEARS-1030 QA Evidence — GET /api/v1/search/trending (BACKEND-ONLY, curl-only)

**Verdict: PASS**
**Date:** 2026-07-10
**Branch:** `feat/NEARS-1030-search-trending` @ tip `a7b7a7b6` (contract mirror) / `920bcc5e` (feature)
**Served:** worktree `Admin/` on `127.0.0.1:8030`, `OTEL_SDK_DISABLED=true`, `DB_DATABASE=multi_food_db_test` (TEST TWIN — trending_searches migration already applied there by the build; live `multi_food_db` untouched — its migration remains a documented deploy-time grant, NOT run in QA).
**Automated backstop:** `vendor/bin/phpunit tests/Feature/TrendingSearchesTest.php` → 9/9 pass, 37 assertions.
**DB note:** no UI consumer yet (contract mirror is a URI constant only) — pure API gate.

## Seed (customer_search_logs, test twin, all created_at = now)
| query | zones (JSON) | module_id | rows |
|---|---|---|---|
| milk | [1] | 1 | 5 |
| bread | [1] | 1 | 3 |
| eggs | [1] | 1 | 1 |
| dates | [2] | 1 | 4 |
| water | [1,2] | 1 | 2 (multi-zone) |
| coffee | [1] | NULL | 3 (cross-module) |

## Built aggregate (trending_searches, after `search:build-trending`)
```
zone_id  module_id  query   search_count  rank
1        NULL       coffee  3             1
1        1          milk    5             1
1        1          bread   3             2
1        1          water   2             3
1        1          eggs    1             4
2        1          dates   4             1
2        1          water   2             2
```
`water` ([1,2]) correctly exploded into BOTH zone-1 and zone-2 partitions.

## Curl matrix — results
Base: `GET http://127.0.0.1:8030/api/v1/search/trending`

| # | AC | Request | Status | Body | Result |
|---|---|---|---|---|---|
| 1a | Zone isolation + freq order | `zoneId:[1]` `?module_id=1` | 200 | `{"trending":["milk","bread","water","eggs"]}` | PASS — freq desc, zone-2 `dates` absent |
| 1b | Zone isolation (zone 2) | `zoneId:[2]` `?module_id=1` | 200 | `{"trending":["dates","water"]}` | PASS — zone-1 milk/bread/eggs absent |
| 2 | Fail-closed missing header | no `zoneId` | 403 | `{"errors":[{"code":"zone_id","message":"Zone id required"}]}` | PASS — no default/zone-1 leak |
| 3a | Fail-closed malformed | `zoneId: not-a-json-array` | 403 | `{"errors":[{"code":"zone_id",...}]}` | PASS |
| 3b | Fail-closed malformed | `zoneId: {}` | 403 | `{"errors":[{"code":"zone_id",...}]}` | PASS (not 200-empty, not 500) |
| 3c | Fail-closed malformed | `zoneId: null` | 403 | `{"errors":[{"code":"zone_id",...}]}` | PASS |
| 4 | Idempotency | `search:build-trending` ×2 | — | content-diff of 7 rows = IDENTICAL | PASS — id/computed_at churn only (delete()+insert()) |
| 5 | Privacy | `zoneId:[1]` `?module_id=1` | 200 | `{"trending":["milk","bread","water","eggs"]}` | PASS — leak-scan (user_id/search_count/result_*/module_id/zone_id/id/rank/computed_at) → NONE present |
| 6a | Module bucket (with) | `zoneId:[1]` `?module_id=1` | 200 | `["milk","bread","water","eggs"]` | PASS — module-1 bucket |
| 6b | Cross-module (NULL) | `zoneId:[1]` (no module_id) | 200 | `{"trending":["coffee"]}` | PASS — NULL bucket differs, `coffee` only |
| 7 | Multi-zone explosion | `zoneId:[1,2]` `?module_id=1` | 200 | `{"trending":["milk","dates","water","bread","eggs"]}` | PASS — `water` present (counts summed 2+2=4, tie-broken query-ASC vs dates) |
| 8 | Empty state | `zoneId:[999]` `?module_id=1` | 200 | `{"trending":[]}` | PASS |
| 9 | Schedule + CLI-only | `schedule:list` / route grep | — | `search:build-trending` daily `0 0 * * *`; `search:purge-logs` daily + `wallet:reconcile-stale-reservations` */5 intact; 0 web routes reference the command | PASS |
| 10 | BE log hygiene | full matrix run | — | 0 new `local.ERROR`/`[FAIL]` lines; 0 `trending_queries` occurrences; no query/zone/user in any trending log line | PASS |

## Idempotency detail (AC4)
Build run 1: `Rebuilt trending_searches: 7 row(s)`. Build run 2: `7 row(s)`.
Content snapshot `(zone_id, module_id, query, search_count, rank)` diff across the two runs = empty (identical). Only `id` (56–62 reassigned) and `computed_at` refreshed — expected from the transactional `delete()+insert()` replace (not `truncate()`), which preserves atomicity.

## AC7 merge math (multi-zone)
zone1/mod1 {milk5,bread3,water2,eggs1} ⊕ zone2/mod1 {dates4,water2}
→ summed: milk5, dates4, water(2+2)=4, bread3, eggs1
→ sort count-DESC, query-ASC tie-break: milk, dates, water, bread, eggs ✓ (matches response).

## Schedule (AC9)
```
0 0 * * *  php artisan search:purge-logs
0 0 * * *  php artisan search:build-trending
*/5 * * * *  php artisan wallet:reconcile-stale-reservations
```
No web route references `build-trending` / `BuildTrendingSearches` (grep of `routes/`).

## Verdict: PASS — 10/10 cells, automated 9/9. No defects. Live `multi_food_db` migration remains a documented deploy-time grant (not run).
