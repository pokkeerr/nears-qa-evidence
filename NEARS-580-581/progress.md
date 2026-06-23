# QA Progress — NEARS-580 (DeliveryApp) / NEARS-581 (VendorApp) — PARITY DELTA pass

PARITY-DELTA re-QA: firebase-perf gradle plugin + perf_http HttpMetric wrapper on api_client (5 verbs).
Baseline (pubspec + main.dart setPerformanceCollectionEnabled seam) already PASSED a prior pass — NOT re-run here.

Device: emulator-5554 (lock pid 31990). Worktree: /Users/Apple/Projects/nears-perf-rum @ feat/NEARS-580-581-perf-rum (uncommitted).
Build: debug, flutter 3.41.x. Backend http://127.0.0.1:8000 /api/v1/config = HTTP 200. google-services.json present in both apps.

## Static / seam review (delta)
- [PASS] gradle perf plugin: settings.gradle.kts declares com.google.firebase.firebase-perf 1.4.2 apply-false; app/build.gradle.kts applies it INSIDE `if (hasGoogleServices)` alongside crashlytics. Both apps. Correctly gated.
- [PASS] perf_http.dart: sanitizeUrl reduces URL to scheme://host/path (drops query + userinfo). start()/stop() both wrapped in try/catch returning null/no-op on any failure -> Performance failure can never break a request.
- [PASS] api_client.dart: all 5 verbs (GET/POST/multipart-POST/PUT/DELETE) wrapped start->http call->stop. The actual http.* call and handleResponse() are UNCHANGED; PerfHttp is purely additive around them. Both apps (5x start, 5x stop each).
- [PASS] PII: Delivery endpoints carry ?token= directly in the URI (app_constants.dart L26/28/30). sanitizeUrl drops the query string so the token never reaches the HttpMetric URL. Raw URL is never logged on the perf path (start passes sanitizeUrl(url) into newHttpMetric).

## AC-tests (delta) — both apps
- [PASS] DeliveryApp `flutter test` = All tests passed (58 tests), incl. 5 new perf_http sanitizeUrl tests (run isolated +5 confirmed).
- [PASS] VendorApp `flutter test` = All tests passed (58 tests), incl. 5 new perf_http sanitizeUrl tests.

## AC-build / AC-no-regression / AC-perf-debug-no-op — live

### DeliveryApp (NEARS-580) — emulator-5554, debug
- [PASS] AC-build: `flutter build apk --debug` => "Built app-debug.apk" with firebase-perf plugin applied. firebase-perf SDK 22.0.5 in debugRuntimeClasspath (plugin genuinely applied, not skipped). Installed + launched -> reached LOGIN screen (delivery-delta-01-firstscreen.png). MainActivity resumed, PID stable. No Gradle/build failure, no startup crash.
- [PASS] AC-no-regression: boot config GET = 200 (`[NET] endpoint=/api/v1/config http_status=200`). Drove a real login (phone +971565656656 / pw) -> login POST authenticated (Bearer token minted) -> authenticated profile/latest-orders GETs = 200 -> reached Home dashboard (Orders/Earnings/Profile, balance د.إ 150 rendered exactly as before). All flowed through PerfHttp-wrapped api_client. No new exception. ui_errors clean (no red-screen/overflow). (delivery-delta-03-home-loggedin.png, delivery-delta-api-success.log)
- [PASS] AC-perf-debug-no-op: no perf-trace noise/crash in debug; firebase-perf SDK bundled but quiet (collection gated !kDebugMode, proven in prior baseline pass). No defect for absent debug traces (296 pattern, release-deferred).
- [PASS] AC-PII: logged URLs show ?token=*** (NEARS-463 log mask) on delivery-man/profile?token= + latest-orders?token=. PerfHttp.sanitizeUrl independently drops the whole query before the HttpMetric URL (unit test + seam). No raw token on perf path. No PerfHttp/HttpMetric error in logcat.

### VendorApp (NEARS-581) — emulator-5554, debug
- [PASS] AC-build: `flutter build apk --debug` => "Built app-debug.apk" with firebase-perf plugin applied. firebase-perf SDK 22.0.5 in debugRuntimeClasspath. Installed + launched -> Firebase init OK -> reached "Choose Your Language" onboarding (vendor-delta-01-firstscreen.png). MainActivity resumed. No Gradle/build failure, no startup crash.
- [PASS] AC-no-regression: boot config GET = 200 (`[NET] endpoint=/api/v1/config http_status=200`). Selected English -> Next -> Sign In screen. Drove a real vendor login (ahmed.khan@demo.com/owner) -> POST /auth/vendor/login = 200 -> token minted (Bearer 0zfktse..., vendorType: owner) -> update-fcm-token POST = 200 + vendor/profile GET fired -> reached dashboard (low-stock business notification rendered normally). All through PerfHttp-wrapped api_client (GET+POST verbs). No new exception. ui_errors clean. (vendor-delta-04-loggedin.png, vendor-delta-api-success.log)
- [PASS] AC-perf-debug-no-op: no perf-trace noise/crash in debug; SDK bundled but quiet (collection gated !kDebugMode). 296 pattern, release-deferred.
- [PASS] AC-PII: Authorization header masked (Authorization: ***/Bearer 0zfktse...) in api_client log. PerfHttp.sanitizeUrl reduces URL to scheme://host/path before the HttpMetric. Unit test green. No PerfHttp/HttpMetric error.

## FINAL — PARITY DELTA
- DeliveryApp (NEARS-580): PASS. VendorApp (NEARS-581): PASS.
- No task_bugs. Both Android builds compile + launch with the firebase-perf gradle plugin; live API calls (incl. login POSTs that mint tokens, and ?token= GETs on Delivery) all flow through the PerfHttp seam non-regressed; PII sanitized; 58/58 tests each.
- regression_bugs: none NEW from this delta. (Prior pass logged a PRE-EXISTING AnalyticsService eager-init crash that only triggers when google-services.json is absent — not reproduced here since both apps have the config; not in this diff. Carried as a followup note, does not gate.)
- followups: (1) worktree-setup gap — gitignored google-services.json isn't copied into `git worktree add` worktrees (had to be seeded manually); (2) both Delivery + Vendor login screens still show the un-rebranded "6amMart" wordmark (reskin item, out of scope for this perf ticket).
