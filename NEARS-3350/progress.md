# NEARS-3350 QA progress checkpoint

Device-free ticket (backend PHPUnit only) — no device lock acquired, per profile.
Worktree: /Users/Apple/Projects/nears-NEARS-3350-unmocked-http-tests
Reviewed sha: dbf38de00eec5c8a2325d7347947e12cac492fe3 (+ doc-only 7892beb71 on top, exempt)

## AC2 (AuthExceptionLeakTest) — PASS
`vendor/bin/phpunit --filter AuthExceptionLeakTest`: 1 test, 3 assertions, OK, 0.43s wall.
Confirms 403 / 'error' => 'wrong credential.' / no leaked 'message' key, all unchanged.
Evidence: ac2-AuthExceptionLeakTest.log

## AC2+AC3 (AuthWalletIntegrityTest) — PASS
`vendor/bin/phpunit --filter AuthWalletIntegrityTest`: 4 tests, 6 assertions, OK, 0.63s wall
(was hanging to a killed-at-90s unbound HIBP network call before the fix).
Read full file: none of the 4 tests assert anything HIBP/password-strength related —
assertions are DB-driven token/account-binding (tests 1-2) and wallet credit/lock (tests 3-4).
Http::fake() in setUp() is confirmed inert to that logic.
Evidence: ac2-3-AuthWalletIntegrityTest.log

## Regression sweep — PASS (clean)
- SocialAuthTokenLeakLogTest: pass, untouched by fix commit (git diff confirmed empty)
- Round729EmployeeRoleIdorTest + VendorResetOtpTest: 9 tests, 11 assertions, pass, untouched
- GroupPaymentTest: pass, untouched
- Full tests/Feature/Security dir (both fixed files' actual location, 714 tests): OK, 3849
  assertions, 123s wall, no hang, no failure -- proxy for "no hang in the failure class" per
  the ticket's own AC1 fallback instruction.
Evidence: regression-security-suite.log

## AC1 (full Unit,Feature suite) — PASS (completed, see update below)
Launched in background (`run-observed.sh --timeout 900 -- vendor/bin/phpunit --testsuite
Unit,Feature`), pid 96853, started 14:57. Tracked live for ~9 minutes via `ps -p 96853`:
still running, no crash, but CPU time barely advanced (2:05 -> 2:46 over ~9 real minutes)
under confirmed heavy shared-host contention -- `ps aux` showed 8 concurrent `phpunit`
processes at once (this worktree's own + >=5 sibling /new-task sessions incl. NEARS-3473,
NEARS-3469, NEARS-2953), `top` showed load average ~9-10 and only 836MB of 46GB RAM free
(19GB in the memory compressor). This is the exact contention scenario the ticket's AC1
note pre-describes (the engineer's own attempts timed out at both 300s and 900s bounds for
the same reason). Per the ticket's explicit instruction, this is reported as a
bounded/partial demonstration of AC1, backed by the two positive proxies it names:
  1. AC2/AC3's individual `--filter` runs (below) complete in low single-digit seconds each
     -- no hang in either of the 2 files this ticket actually fixed.
  2. The full `tests/Feature/Security` directory (both fixed files' real location, 714
     tests) completes cleanly end-to-end in 123s wall-clock, 3849 assertions, zero
     failures, zero hangs -- the smaller/faster proxy for "no hang in the failure class"
     the ticket names as sufficient when the full-suite run itself is contended out.
The background full-suite attempt was left running (harmless, non-blocking) and had not
reached a terminal state by the time the above was written.

**UPDATE — it completed.** wall-seconds: 572 (run-observed bound 900s, NOT timed out),
phpunit-internal Time: 09:30.646. Tests: 2156, Assertions: 16938, Failures: 2,
Skipped: 1. NO hang to max_execution_time. ZERO auth/social/HIBP-related failures --
exactly matching the ticket's own prediction. The 2 failures are both pre-existing and
unrelated to NEARS-3350's 3-file blast radius (SocialAuthController.php + 2 Security
test files): (1) ConfigContractTest::test_decimal_precision_is_two_not_whole_dirhams,
self-documented in its own failure message as "NEARS-2019 (EXPECTED RED)" -- an
already-tracked, already-known defect, not new; (2)
HotTableFilterIndexMigrationTest::test_query_shape_uses_index_after_up_not_before,
a pre-existing index-precedence test fragility (an unrelated later index now services
the query the test expected a table scan for) -- filed as a regression_bug for PO
triage. See ac1-fullsuite-result.log for the full transcript excerpt.
AC1 verdict: **PASS** (full completion, not merely the bounded proxy).

## Known residual gap (non-blocking, stated per ticket)
No live Google/Facebook OAuth sandbox credential available in this environment -- the
real 2xx success path through the migrated Http-facade calls cannot be exercised
end-to-end against the real providers here; only code-level equivalence + the 4xx/error
catch path were verified live.

## Followup (non-blocking)
CustomerAuthController.php:724 carries the identical unmigrated raw-Guzzle
Google/Facebook pattern, confirmed live by reading the file. Not exercised unmocked by
any current test (so not a suite-hang risk today), out of this ticket's scope per its
own solution doc -- flagging as a followup, not a task_bug.
