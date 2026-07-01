# NEARS-694 QA progress (live checkpoints)

- Static AC1: zero raw json_decode($zone_id) in ItemController — PASS (grep, 3 non-zone decodes remain: category_ids/attachment/rating)
- Static AC2: 11 parseZoneIds sites across 6 actions — PASS (grep)

## Live (backend :8099, module1 grocery, zone2=Abu Dhabi)
- phpunit: 11/11 pass, 75 assertions, 0 skips (incl. common_conditions_browse_all_crafted_zone_fails_closed) — AC5 PASS
- /items/search valid[2]: 200, total=13, all zone-2 (verified via DB), zero z1 leak — AC4 PASS
- /items/search crafted[true],{}: 200, total=0, empty — AC3 PASS (fail-closed)
- /items/search absent: 200, total=13 = backfill to z2 (geo=AbuDhabi) — expected, not a fail
- /items/common-conditions omit store_id: 403 required — PASS
- /items/common-conditions valid store53(z2): 200 empty (no seed condition data); crafted[true]/{}: 200 not 500 — AC3 PASS

## FINAL (all ACs demonstrated)
- item-or-store-search: stores[2]=z2 only(8,13,14,17,18,19,21,22), items z2 only; crafted->empty — AC3/AC4 PASS
- search-suggestion: [2] total=9 (=9 z2 milk items), crafted->0 — PASS
- smart-suggestions: [2] total=10 all z2, crafted->0 — PASS
- cross-store-search: 404 config-disabled (phpunit/static covered)
- /items/popular delegating: [2] total=219, z2 ids — regression clean
- logs-first: CLEAN (no run-scoped errors; 2 ERRORs are testing.* fixtures, pre-existing)
- VERDICT: PASS
