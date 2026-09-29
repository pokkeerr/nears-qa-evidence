# NEARS-3891 QA [8] — verdict PASS (device-free, backend test-harness only)

Branch `fix/NEARS-3891-fcm-harness` @ `82e6be1f7` (git rev-parse verified; tree clean before and after), base `53b314d4a` (ancestor verified).
No device/emulator/lock/app boot (profile: device-free ticket). No backend server needed (phpunit only), so the `Backend:` line is n/a: `phpunit against private per-worktree DB clone multi_food_db_test_nears_nears_3891_fcm_harness`.
Every phpunit run went through `sandbox-phpunit.sh` (pre-flight sandboxed curl must rc 137, else refuses; then phpunit under sandbox-exec deny tcp 80/443 + SIGKILL). No direct vendor/bin/phpunit call. No credentials, .env, business_settings or Firebase config touched; controls use a Config override with a runtime-generated RSA key.
lessons_read: 88 (selector exit 0).

## 1. Instrument validity
- sandboxed `curl https://example.com` rc=137, `curl http://example.com` rc=137; unsandboxed curl HTTP 200.
- sandboxed `/dev/tcp/127.0.0.1/3306` open (loopback MySQL fine).
- benign local test under wrapper: `Nears3891OutboundHttpGuardTest --filter test_p5` -> OK (1 test, 1 assertion), exit 0.
- The wrapper pre-flight fired (rc 137 curl) on every phpunit invocation (visible as the "Killed: 9 ... curl" line in each run).

## 2. AC1(d) positive controls on UNTOUCHED base 53b314d4a (throwaway test, deleted; source: qa-control-test-source.php.txt)
Each control run in its own wrapped process (`--filter`), Config-override creds, no DB row.
| Path | exit (no fakes) | exit (both hosts faked + firebase.messaging double) |
|---|---|---|
| Helpers::sendNotificationToHttp -> fcm POST (oauth pre-cached) | 137 | 0 (returned true) |
| Helpers::getAccessToken -> oauth2 | 137 | 0 |
| NotificationTrait::sendNotificationToHttp -> fcm POST (oauth faked; trait bound to a test class overriding get_business_settings so the DB row is never read) | 137 | 0 |
| NotificationTrait::getAccessToken -> oauth2 | 137 | 0 |
| Kreait singleton via POST /subscribeToTopic as super admin | 137 | 0 (200) |
Note: my first Firebase-singleton control returned exit 0 / HTTP 500 because MY generated service-account lacked `type: service_account` (Kreait ServiceAccount mapper threw before any network). That was a control defect, found by `withoutExceptionHandling`, fixed, then killed 137. Documented so the 137 is not read as first-try luck.
Raw (non-Http::) egress on base: `DmEarningInvoiceTest` exit 137, `AdminRouteSmokeTest` exit 137 (mPDF font/CSS fetch, fonts.googleapis.com / cdnjs).
Files: qa-controls-base.txt.

## 3. AC1(a)(b)(c) on branch 82e6be1f7
- Proof file: `Nears3891OutboundHttpGuardTest` exit 0, OK (11 tests, 40 assertions): P0 non-FCM host prevented; P1/P1b unfaked push gets default 200 from BOTH senders + recorded; P2 per-test 500/401 fakes on the FCM hosts still win (anti-shadow); P3/P3b/P4 AC2; P5 negative controls; P6 both firebase singletons inert doubles; P7/P7b raw-curl proxy refusal + env restore.
- Http::fake / push families: 46 files (grep -rlE Http::fake|FakesFcmOAuth|fakeFcmOAuth|Http::assert|Http::recorded|preventStrayRequests + Nears3282/2923 globs) each run alone: all exit 0 (qa-branch-per-file-results.txt), plus `DmEarningInvoiceTest` exit 0 (4 tests, 7 assertions). Includes 2986, 3011, 3539, 2428, 2464, 3537, 3639, 2923, GroupOrderPlacementTest (unedited).
- ONE controlled FULL sandboxed run (no filter, --log-events-text to scratchpad): exit 1, NO 137/kill. Tests 3033, Assertions 20808, Failures 1, PHPUnit Deprecations 1, Skipped 1; Time 07:29.729, Memory 995.00 MB (limit 1024M; base 995.00 MB). Sole failure = `ConfigContractTest::test_decimal_precision_is_two_not_whole_dirhams` (NEARS-2019 EXPECTED RED, identical on base: 3022 tests / 1 failure; branch adds the 11 proof tests = 3033).
- laravel.log delta (offset 2455232 -> 2798248, 343016 bytes) counts: `cURL error` 3, `Could not resolve` 3, `FCM Exception` 2, `Failed to connect` 0, `FCM notification send exception` 0, `FCM OAuth token request exception` 0, `StrayRequestException` 0, `without a matching fake` 0, `FCM Send Success` 421 (informational only, not a discriminator; faked 200 logs it). The 3 cURL/Could-not-resolve lines are Laravel's SIMULATED `Http::failedConnection()` text (vendor Factory.php:211) from tests that fake it on purpose (project_ids nears-test-project-2986-conn, nears-test-project-3011 for FCM; Nears3011 `pushFailedConnection()` sequence for the oauth "Firebase Token Generation Exception"); with no sandbox kill in the same run they cannot be real egress (a real resolve would connect on 443 and be SIGKILLed). Base baseline (no-kill policy) was 47 real transport-failure lines.
- Raw non-Http egress listing: only the mPDF font/CSS fetch in `AdminRouteSmokeTest` (route admin.report.generate-statement) and `DmEarningInvoiceTest::test_returns_pdf_for_token_owner`; both are killed on base (exit 137) and are contained on the branch by the opt-in `refuseRawCurlEgress()` dead-loopback-proxy, i.e. diverted, not sandbox-clean by construction. Severity Low (GET of public font CSS, no credentials/PII/FCM). Residual: gateways/SMS/`CustomerAuthController new Client`/translate helper/SendSmartNotifications are not `Http::`-guarded and were not reached by this suite (no kill).

## 4. AC2
- Proof file P3/P3b/P4 green (above).
- Mutation 1 (needle `without a matching fake`, `StrayRequestException` string and the instanceof branch neutralised) in `tests/Support/ScansStrayRequestLogs.php`: proof file exit 1, P3, P4, P3b RED (3 failures).
- Mutation 2 (only the `without a matching fake` needle changed): P3, P4, P3b RED again.
- Restored byte-identical: md5 cfe2cdd866f00d482d40c0e90d1b3f6e before == after, `git diff --stat` empty, `git status --short` empty.
- Independent end-to-end (not the proof file's internal catch): in the base-probe worktree I copied the branch's TestCase + 2 Support traits in with 3 throwaway tests that swallow an un-faked `Http::get` in `try/catch` + `Log::error`: real-logger test FAILS ("Un-faked outbound HTTP request swallowed by production code"), `Log::spy()` test FAILS, faked control passes; exit 1, 3 tests / 2 failures. All reverted (`git checkout`, files removed); base-probe `git status --short` empty.

## 5. AC-LOG / scope
`git diff --name-only 53b314d4a..HEAD`: Admin/tests/Feature/{AdminRouteSmokeTest,DmEarningInvoiceTest,Nears3891OutboundHttpGuardTest,VendorRegister403DiagnosisTest}.php, Admin/tests/Support/{GuardsOutboundHttp,ScansStrayRequestLogs}.php, Admin/tests/TestCase.php, docs/solutions/NEARS-3891-phpunit-outbound-http-guard.md. Nothing outside Admin/tests/** and docs/solutions/NEARS-3891-*.md; none under Admin/app, config, database, seeders, .env; none of Nears3856BackendLoggingGapsTest / GroupOrderPlacementTest / CartModuleIdGuardTest. Secret grep on the diff (`private_key|nears-1d39b|BEGIN|AIza|client_secret`): only 2 hits, both the identifiers `private_key_bits`/`'private_key' => $privateKey` around a runtime-generated openssl key; no `BEGIN` PEM literal, no project id literal. No production log line added (no Admin/app change).

## 6. Regression sweep
The full suite is the sweep (item 3): 3033 tests, only the known pre-existing NEARS-2019 failure. The 3 touched non-proof files: diffs are 1-2 lines and only ADD a guard call (`refuseRawCurlEgress()` in AdminRouteSmokeTest and DmEarningInvoiceTest; a scoped `Http::fake(['api.pwnedpasswords.com/*' => 200])` in VendorRegister403DiagnosisTest setUp); no assertion changed or removed. Each passes (AdminRouteSmokeTest OK 3 tests/9 assertions, route sweep still executed=359 incl. generate-statement 200; DmEarningInvoiceTest OK 4/7; VendorRegister403DiagnosisTest OK 5/15).

## Observations (non-blocking)
- Assertions 20808 vs engineer-reported 20806 (+2): same test count (3033); non-blocking count variance, not a failure.
- `[FAIL] OpenTelemetry export failed; Laravel logger unavailable` stderr line appears identically in the base full run (pre-existing, unrelated).
- Guard is TestCase-scoped: 11 test files extend plain PHPUnit\Framework\TestCase (no Laravel app, so no Http facade guard applies); the sandbox is the only net there (no kill observed).
