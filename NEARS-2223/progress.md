# NEARS-2223 QA progress log

- AC1 (no/invalid nonce -> 401, no mutation): PASS. Live curl, isolated backend (port 8090,
  DB copy multi_food_db_qa_nears2223). No-nonce -> 401, store_business_model unchanged
  ('none' -> 'none'). Invalid/garbage nonce -> 401, unchanged. Confirmed via DB SELECT.
- AC2 (valid nonce grants once, replay rejected): PASS ONLY in a narrow non-default
  config variant (both business models enabled, no business_plan/package_id sent at
  register() time). FAILS under the real/default config (subscription_business_model=0)
  — the nonce is dead on arrival due to a pre-existing, unrelated cache:clear side
  effect on Store::save(). See bug-nonce-wiped-by-store-saved-observer.log.
- AC3 (exactly one structured log line, no PII): FAILS on the granted path — LOG_LEVEL=warning
  (real config, both worktree and primary .env) silently drops the Log::info() grant line.
  Denied path (Log::warning) is fine. See bug-log-info-level-swallowed.log.
- AC4 (rate limit, 6th request -> 429): PASS. Live curl, 5x 401 then 429 on the 6th.
- Cross-store scoping: code logic PROVEN correct via isolated tinker test (mint for
  store X, consume attempt with wrong store Y -> false, cache preserved; consume with
  correct store X -> true). Live HTTP cross-store test (stores 91115/91116) was
  CONFOUNDED by the same cache-wipe defect (a later registration wiped store A's nonce
  before the cross-store attempt), so the HTTP-level cross-store test result on its own
  is not trustworthy in isolation — the tinker-isolated proof stands in for it.
- TTL expiry: PASS. Forged well-signed nonce with past expiresAt (correct HMAC via
  config('app.key')) -> 401 live via curl.
- F1 regression (drive real UserApp registration -> business_plan): reproduced the
  headline defect LIVE end-to-end on emulator-5558 — register() 200, business_plan()
  401 (nonce already dead), UserApp then silently routes to the customer home screen
  with NO error dialog shown to the user. Screenshots: bug-nonce-wiped-choose-plan.png,
  bug-nonce-wiped-silent-401-home.png.
- Regression spot-check (authenticated-bearer branch, cancelSubscription, checkProductLimits):
  static diff confirms zero changes to those code paths; live check confirms their
  validators fire before authorizeStore is ever reached (403 on missing required
  params), consistent with pre-existing, unmodified behavior.
- Automated backstop: RegistrationNonceTest 9/9 green, SubscriptionStoreAuthTest 11/11
  green — both green BECAUSE phpunit.xml forces CACHE_DRIVER=array (not the shared
  'database' driver) and the tests never round-trip through register()'s real
  Store::save() chain, and the log test uses Log::spy() which bypasses real
  LOG_LEVEL filtering. Confirmed as a real environment/test gap, not a false alarm.
- UserApp flutter test: test/features/business/subscription_retry_route_test.dart
  15/15 pass, including the NEARS-2223-F1 (base64 "+" URL corruption) pinned tests —
  the CLIENT-side URL-encoding fix from fix-cycle-1 is correctly pinned and holds.

## Fix-cycle 2 re-QA (2026-08-19, emulator-5558, backend :8090, DB multi_food_db_qa_nears2223 REUSED)

Real config confirmed: Admin/.env CACHE_DRIVER=database, LOG_LEVEL=warning (both
matched what phpunit.xml would otherwise override — see the phpunit.qa-realcache.xml
throwaway-config technique used below, deleted after use, never committed).

- **Bug 1 re-verify: PASS.** Live curl against the real (non-array-cache) backend,
  BOTH register() response branches:
  - Commission branch (store 91124): register() 200 -> business_plan() 200 (granted)
    -> replay 401. No cache-wipe defect; nonce survives the full save chain.
  - Subscription/package branch (store 91125, subscription_business_model flipped to
    1 in the ISOLATED QA-clone DB only, cache:clear'd): register() 200 (package_id=1)
    -> business_plan(payment_gateway=wallet) reached real business logic ("Insufficient
    balance in wallet", i.e. past the authz gate) -> replay 401.
  - THEN drove the REAL UserApp registration form end-to-end on emulator-5558 (fresh
    business name/logo/cover/location/module/delivery-time/owner-info/password, all
    live-typed and live-tapped, no shortcuts) through Submit -> Subscription Base ->
    "QA Single-Store Fixture" package (50 AED, PAID, not a free-tier package) ->
    landed on SubscriptionPaymentScreen ("You are one step away!") -> "Continue with
    7 day free trial" -> Confirm -> "Congratulations!! Registration Success". Logcat:
    `[NET] endpoint=/api/v1/auth/vendor/register http_status=200` then
    `[NET] endpoint=/api/v1/vendor/business_plan http_status=200`, zero [ERR]/[FAIL],
    `ui_errors` clean. DB: store 91126 store_business_model='subscription', package_id=1.
    This is the exact path that FAILED in cycle 1 (register 200, business_plan 401,
    silent home redirect) — now completes cleanly end to end.
    Evidence: cycle2-bug1-live-ui-registration-success.png.
- **Bug 2 re-verify: PASS.** grep Admin/storage/logs/laravel.log for
  `subscription.allow_pending` after all of the above: every grant AND every denial
  (stores 91124/91125/91126/91127) logged at `production.WARNING`, fields limited to
  `store_id`+`outcome` (+`trace_id`/`correlation_id`, IDs not PII) — no
  `registration_nonce`, no other PII. Both outcomes observable under the real
  LOG_LEVEL=warning, confirming the info-level-swallowed defect is closed.
- **Bug 3 re-verify: PASS, live, real 401 (not synthetic).** Registered a second
  fresh store (91127) via the real UI through Subscription Base -> package -> Pay Via
  Online -> Paypal -> Confirm; the FIRST Confirm legitimately granted+consumed the
  nonce (business_plan 200, redirect_link returned) exactly like a real user's first
  attempt. Cancelled the stuck payment webview (no real gateway configured in this
  sandbox), returned to SubscriptionPaymentScreen, tapped Confirm a second time —
  this replays the now-consumed (single-use) nonce, producing a GENUINE backend 401
  (not forged/mocked). Result: (1) logcat
  `[FAIL] endpoint=/api/v1/vendor/business_plan http_status=401 type=ApiFailure
  msg="business plan submission failed"` — the paired AppLogger.failure fires;
  (2) a11y dump immediately after the tap shows `content-desc="Something went wrong"`
  — the visible failure snackbar actually renders; (3) the app stayed on
  SubscriptionPaymentScreen — NO silent redirect to home (the cycle-1 defect).
  Evidence: cycle2-bug3-visible-failure-snackbar.png.
- **Regression spot-checks (previously PASS in cycle 1, not re-driven end-to-end,
  confirmed still holding): all PASS.**
  - AC1 (no/invalid nonce -> 401, no mutation): curl, store 91126, no-nonce and
    garbage-nonce both 401, store_business_model unchanged ('subscription').
  - AC4 (rate limit, 6th request -> 429): curl loop against a fresh store_id
    (999999), 5x 404 (store not found, past the limiter) then 429 on the 6th —
    confirms the limiter runs pre-controller as designed.
  - Cross-store scoping: tinker, mint for store 91124, consume attempt with store
    91125 -> denied; consume with correct store 91124 -> granted.
  - TTL expiry: tinker, forged well-signed nonce (correct HMAC via config('app.key'))
    with an already-past embedded expiresAt -> denied.
  - Authenticated-bearer branch: `cancel-subscription` / `check-product-limits`
    (both unauthenticated-in-this-curl) -> 403 (validator fires before
    authorizeStore), consistent with pre-existing unmodified behavior.
- **Automated backstop:**
  - `vendor/bin/phpunit --filter RegistrationNonceTest`: 11/11 green under BOTH
    phpunit.xml's pinned CACHE_DRIVER=array AND a genuine CACHE_DRIVER=database run
    (via a throwaway phpunit.qa-realcache.xml with the `<server CACHE_DRIVER>`
    override stripped — phpunit.xml's XML `<server>` values are immutable-override
    shell env, so `CACHE_DRIVER=database vendor/bin/phpunit` alone does NOT actually
    switch drivers; confirmed via `cache`-table row count in the private test DB
    after the real-cache-driver run: 4 rows written, 0 leftover lock rows — i.e. the
    database cache driver, and its `Cache::lock`, genuinely executed). Config file
    deleted after use, never committed.
  - `vendor/bin/phpunit tests/Feature/Security` (full folder, bounded regression):
    507/508 green, 1 error = `ZoneContainsSqlInjectionTest` (pre-existing, unrelated,
    tracked separately per the fix-cycle-2 packet — not re-filed).
  - `flutter test test/features/business/ test/features/auth/`: 295/295 pass,
    including `business_service_failure_surface_test.dart` (T1/T2/T3, new this
    cycle) and the NEARS-2223-F1 URL-encoding tests in
    `subscription_retry_route_test.dart` (now 18/18 in that file, +3 for the
    failure-surface tests folded into the same run).
- **Verdict: PASS.** All 3 cycle-1 defects closed and re-verified live against the
  REAL (non-phpunit-overridden) config, on a genuinely replayed nonce, not a
  synthetic one. No new regressions found in the bounded sweep.
