# NEARS-3834 QA progress (phase 8, fix-cycle 0) - device-free API QA
| AC | status | evidence | logs |
|---|---|---|---|
| AC1 | PASS | flag ON, no header, zoneId=[1]: 9 rows, module_id {1,2,3}, all zone 1, modules active + module_zone-linked | clean (0 lines for rid) |
| AC2 | PASS | moduleId 1 -> {1,2,3,38} m1 only; moduleId 2 -> {4,5,39} m2 only; bodies byte-identical flag ON vs OFF | clean |
| AC3 | PASS | 'garbage' and 99999 -> 200 [] + exactly 1 WARN per request id, flag ON and OFF; bodies byte-identical across flags | 1 expected [WARN] per call, no ERR |
| AC4 | PASS | live on copy: module 3 status=0 -> 7,42 dropped, 7 rows m{1,2} stay; module_zone(2,1) deleted -> 4,5,39 dropped, 6 rows m{1,3} stay; both restored, 9 rows again | clean |
| AC-LOG | PASS | call-site context keys exactly {code,endpoint,http_status,reason,request_id} (+ pipeline trace_id/correlation_id); no raw header, no user_id/lat/lng; absent header 0 WARN both flags | as expected |
| AC-REG | PASS | flag OFF absent [], m1 {1,2,3,38} == SQL prediction, m2 {4,5,39}, garbage [] + WARN; post-restore bodies identical to baseline | clean |
| AC-TEST | PASS | phpunit --filter: 19 tests / 288 assertions OK, 1 pre-existing HotTableFilterIndexMigrationTest deprecation; OrderTraitZoneScopingTest unedited | n/a |
| AC-DOC | PASS | cross-module-basket.md S11 present; each clause matches observed behaviour | n/a |

## Fix-cycle 2 delta (HEAD c20e28552, scope refactor) — other rows reused from cycle 0 (comment 22129)
| AC | status | evidence | logs |
|---|---|---|---|
| AC1 | PASS | flag ON, no header: 9 rows m{1,2,3}, body byte-identical to cycle 0 | clean |
| AC2 | PASS | moduleId=1: {1,2,3,38} m1 only, byte-identical to cycle 0 | clean |
| AC4 | PASS | m3 status=0 -> 7,42 dropped (7 rows m{1,2}); module_zone(2,1) deleted -> 4,5,39 dropped (6 rows m{1,3}); restored -> 9 rows; all byte-identical to cycle 0 | clean |
| AC-REG | PASS | flag OFF absent -> [] before and after the ON window | clean |
