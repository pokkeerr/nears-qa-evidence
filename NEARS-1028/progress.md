# NEARS-1028 — Module-less typeahead — QA evidence (curl-only, BE)

- **Verdict:** PASS
- **Under test:** `GET /api/v1/items/item-or-store-search` (module-optional)
- **Worktree:** `feat/NEARS-1028-moduleless-typeahead` @ e9bd4503
- **Backend:** served worktree Admin on `127.0.0.1:8028`, `OTEL_SDK_DISABLED=true`, DB `multi_food_db` (read-only)
- **Date:** 2026-07-10

## Fixtures used
- Cross-module term `Abu Dhabi` — matches zone-2 stores in modules 1/2/3 (store 8 = m1; 47/49/50/51/52 = m2; 53/55/56/57/58 = m3).
- Bidirectional isolation term `Grill House` — store **39** "The Grill House" (zone 1, m2) vs store **47** "The Grill House (Abu Dhabi)" (zone 2, m2).

## Results table

| # | Case | Request (headers) | Expected | Observed | Result |
|---|------|-------------------|----------|----------|--------|
| 1 | Cross-module module-less 200 | OMIT `moduleId`; `zoneId:[2]`, `name=Abu Dhabi`, lon/lat | 200, stores span >1 module in zone 2 | **HTTP 200**; 50 items; 12 stores across **m1** [8,35], **m2** [47,49,50,51,52], **m3** [53,55,56,57,58]; no zone-1 store | PASS |
| 2 | Zone isolation (both directions) | module-less `name=Grill House` | z1 excludes z2-only rec & vice versa | `zoneId:[1]` → stores [39,1] (z2 store **47 absent**); `zoneId:[2]` → stores [47] (z1 store **39 absent**) | PASS |
| 3 | Fail-closed malformed zoneId | module-less; `zoneId` = `{"x":1}` / `"2"` / `null` / `not-a-json-array` | 200 with EMPTY items+stores (never 500) | all 4 → **HTTP 200**, `items=[]`, `stores=[]` | PASS |
| 4 | Missing coords | module-less, `zoneId:[2]`, OMIT lon/lat | 403 longitude-latitude | **HTTP 403** `{"code":"longitude-latitude","message":"Longitude-latitude required"}` | PASS |
| 5 | Pinned regression | `moduleId:1`, `zoneId:[2]`, `name=Abu Dhabi`, lon/lat | module-scoped results only (unchanged) | **HTTP 200**; stores [8,35] (**m1 only**); m2/m3 stores absent — truthy `when()` branch runs identical `whereHas(zone.modules, modules.id=cfg)` | PASS |
| 6 | Except-list scope | `stores/search` + `items/search-suggestion` WITHOUT `moduleId` | still 403 (not except-listed) | both → **HTTP 403** `{"code":"moduleId","message":"Module id required"}` | PASS |
| 7 | Present-but-invalid moduleId | `moduleId:99999`, `zoneId:[2]` | 403 at middleware | **HTTP 403** `{"code":"moduleId","message":"Not found"}` | PASS |
| 8 | BE log hygiene | during full matrix | 0 `local.ERROR`; QueryException = get_class only | **0 new** `laravel.log` lines, **0** ERROR/CRITICAL; no QueryException emitted (fail-closed path = valid `whereIn(zone_id,[])`, no throw) | PASS |

## Automated backstop
`vendor/bin/phpunit --filter ItemOrStoreSearchModulelessTest` → **OK, 5/5 tests, 21 assertions** (2 PHPUnit-level deprecations, not failures).

## Notes
- `parseZoneIds` is the fail-closed gate: object/quoted-string/null/garbage all decode to `[]` → `whereIn('zone_id', [])` → empty result, no `all_zone_service` bypass on the module-less path.
- Items query (NEARS-694, lines 870-875) was NOT touched by 1028 — only the inlined stores query (ItemController) + `StoreLogic::search_stores` gained the `->when(config(...))` guard; pinned-path logic is byte-identical by construction and confirmed live (case 5).
- **Throttle (Low, out of 1028 scope):** endpoint has no per-route throttle — tracked hardening follow-up, NOT a defect of this change.

Raw transcript: `transcript.txt` in this folder.
