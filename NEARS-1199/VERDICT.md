# NEARS-1199 — QA verdict: PASS

Test-infrastructure ticket (phpunit test-DB isolation). Backend-only, no device.
Worktree `nears-NEARS-1199-test-db-isolation`, head `faf1ba49`, base `87d10fd0`.
PHPUnit 11.5.55 / PHP 8.5.6. Every check carries a mutation/falsification leg that goes RED on the pre-fix state.

| Check | Result | Evidence | Mutation (goes RED on broken/base) |
|---|---|---|---|
| AC-b: shell `DB_DATABASE` override honoured-or-fails-loud | PASS | `ac-b.out` — `DB_DATABASE=definitely_not_a_db` → loud ABORT, exit 1, never substitutes twin | base `87d10fd0`: identical cmd is GREEN 41 assertions (override silently ignored) — ran live in base worktree |
| AC-c.1: `multi_food_db` hard-abort survives | PASS | `ac-c1.out` — hard ABORT naming real DB, exit 1 | (guard removal would let RefreshDatabase wipe dev DB) |
| AC-c.2: real non-test DB refused on allow-list | PASS | `ac-c2.out` — `multi_food_db_qa337` ABORT on allow-list, not run, exit 1 | — |
| AC-a: two concurrent runs never see each other's writes | PASS | `ac-a-pos-A/B.out` — distinct auto-derived DBs (`..._nears_nears_1199_test_db_isolation` vs `..._peer_b_1199`), both GREEN, isolation test ran (not skipped) | `ac-a-mut-A/B.out` — BOTH forced onto one `mutcheck` DB → BOTH RED, Failures:1, each names the peer (runA↔runB). Anti-vacuity pin holds. |
| SQLi pin: `--drop-stale` injection | PASS | `sec-inject.out` — `TEST_DB_NAME="x'; DROP DATABASE ... zzz_canary; -- "` REFUSED, exit 1, canary survived | (missing assert_disposable would drop the bait) |
| Automated guard test | PASS | `guard-test.out` — TestDbScriptGuardTest 3/3 green | — |
| T4/T5: zero-config full suite, no new failures | PASS | `full-head.out` 974/10357/0F/0E/1skip vs `full-base.out` 969/10349/0F/0E — delta = exactly the +5 new tests | — |
| Clone lifecycle: no orphan accumulation | PASS | `lifecycle.log` — pid clone `..._51911` created then dropped on exit (pass + no-test runs); per-worktree bootstrap DB retained (intended reuse) | — |

Dev DB `multi_food_db` untouched: 156 tables before and after. No `migrate` run. Throwaway DBs (mutcheck, peer_b, zzz_canary) cleaned up.

Verdict: PASS. No task_bugs, no regressions.
