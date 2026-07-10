# NEARS-1029 QA progress — cycle 0 (2026-07-10)

Build: worktree `/Users/Apple/Projects/nears-NEARS-1029-search-logs` @ `5f39ebe6`, base `7cf8783c`.
Constraint honored: live `multi_food_db` NOT migrated (verified `information_schema` count = 0 for `customer_search_logs`); isolated `multi_food_db_test` has the table. Feature tests = primary AC evidence; live smoke exercises AC5 resilience on the real stack with the table absent.

| AC | Verdict | Evidence | Logs |
|----|---------|----------|------|
| AC1 auth search writes 1 row (captured scalars, parsed zone ids, module pin / NULL for global) | PASS (tests) — NOT-DEMONSTRABLE-LIVE until deploy migration | `phpunit-customer-search-log.txt`: `test_unified_search_authenticated_writes_exactly_one_row` + `test_global_search_..._null_module_and_summed_totals` green | clean |
| AC2 guest search: 200, no write | PASS (tests + LIVE) | test `test_guest_search_writes_no_rows` + `live-smoke-ac5.txt` §5–7: guest 200, 0 new [FAIL], token absent from log | clean |
| AC3 purge: 90-day boundary, `--days` override, daily schedule | PASS (tests + schedule LIVE) — purge-on-real-table NOT-DEMONSTRABLE-LIVE | tests `test_purge_command_retention_boundary_and_days_override` (89-keep/91-drop, --days=7) + `test_purge_command_is_registered_in_the_live_schedule`; LIVE `schedule:list` → `0 0 * * * php artisan search:purge-logs` (`schedule-and-1027-smoke.txt`) | clean |
| AC4 remove_account deletion chain (only that user) | PASS (tests) — NOT-DEMONSTRABLE-LIVE (would mutate live DB; table absent) | test `test_remove_account_purges_only_that_users_rows` green | clean |
| AC5 write failure never surfaces (fire-and-forget) | PASS (tests + LIVE DEMO) | test byte-identity under injected failure; LIVE: table absent on live DB → auth unified search **HTTP 200 normal body** + `[FAIL] customer-search-log write {error: QueryException, request_id: af994ad0-…}` (`live-smoke-ac5.txt` §1–2) | expected [FAIL] only |
| AC6 query text never in logs; error class + request id only | PASS (tests + LIVE) | test Log::listen sweep; LIVE: query token `Nears1029LiveZebraQA` occurs **0×** in entire laravel.log; [FAIL] carries error class + request_id + correlation_id (`live-smoke-ac5.txt` §3–4) | clean |

Migration to apply at deploy: `php artisan migrate --path=database/migrations/2026_07_10_120000_create_customer_search_logs_table.php`

## Automated backstop
- Full suite (run 1): 777 tests, 4 errors + 1 failure — ALL on unrelated surfaces (3 × MySQL deadlock 1213 on `business_settings`/`storages` from concurrent test-DB access, 1 coupon-null, 1 DM-parcel OTP 500). `phpunit-full-suite.txt`
- The 4 failing classes re-run isolated: 26/26 green → environmental flakes.
- Full suite (rerun): **777 tests, 6919 assertions, 0 errors, 0 failures** (EXIT=0). `phpunit-full-suite-rerun.txt`
- `CustomerSearchLogTest`: **9/9 green**, testdox transcript `phpunit-customer-search-log.txt`.

## Regression sweep
- 8 response pairs (unified+global × apple+milk × guest+auth), worktree :8029 vs base :8000: **all IDENTICAL** after masking host-derived `*_full_url` image URLs (worktree `storage/app/public` media is gitignored → placeholder fallback; pure environment artifact). `regression-byte-compare.txt`
- First-pass `glo-milk-auth` pair: primary returned a **429** (shared `CACHE_DRIVER=database` rate limiter + background traffic); refetched after window → identical. Worktree side of that same first pass returned an unexplained 137KB body with no [FAIL] line; **full burst replayed: 8×200 stable sizes, exactly 4 [FAIL]s, no other log lines — not reproducible**, recorded as observation only.
- NEARS-1027 global-search smoke: normal → 200; `name=a` → 403 min-2 validation body; throttle headers active (`X-RateLimit-Limit: 30`). `schedule-and-1027-smoke.txt`
- OTel export error on artisan shutdown = known collector-down dev condition (NEARS-267 OpenObserve not running) — pre-existing, unrelated.
