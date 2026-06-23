# QA Progress — NEARS-580 (DeliveryApp) / NEARS-581 (VendorApp) — Firebase Performance wiring

Device: emulator-5554 (lock pid 25754). Worktree: /Users/Apple/Projects/nears-perf-rum @ feat/NEARS-580-581-perf-rum (base origin/feat/log-system 0bf6f3ca, uncommitted).
Build: debug, flutter 3.41.9. Backend http://127.0.0.1:8000 = HTTP 200.

## Pre-flight (both apps)
- [PASS] Diff = exactly as specified: +firebase_performance ^0.11.4+2; rename _setupCrashlytics->_setupCrashlyticsAndPerformance; +setPerformanceCollectionEnabled(collectionEnabled) inside existing try/catch, gated on firebaseReady. collectionEnabled = !kDebugMode.
- [PASS] No HttpMetric/newTrace/network traces added (only the collection-enable seam) -> no URL/token PII path.
- [PASS] No gradle perf plugin added -> release upload deferred (568 AC6b / 296 pattern).
- [PASS] baseUrl -> 10.0.2.2:8000 (Android local backend), not demo server, both apps.

## Worktree Firebase-config gap (resolved for QA)
- Worktree was missing android/app/google-services.json (gitignored -> not copied by `git worktree add`). Primary tree HAS them (config-assets/{delivery,vendor}/ + installed). Copied canonical per-app files into worktree apps (still gitignored; diff unchanged = 5 intended files). This is a worktree-setup gap, NOT a code defect -> drift note.
- First (no-config) run: Firebase.initializeApp() failed -> firebaseReady=false -> _setupCrashlyticsAndPerformance() SKIPPED (incl. new perf line). App still cold-started + rendered splash (AC4 resilience demonstrated organically). But a PRE-EXISTING analytics crash (AnalyticsService ctor eagerly reads FirebaseAnalytics.instance, di.init main.dart:98, analytics_service.dart:28 — files NOT in this diff) threw [core/no-app] and stalled splash->signin. Regression_bug, not task_bug.

## AC results — DeliveryApp (NEARS-580), debug build, emulator-5554
- AC1 cold-start clean + reach first screen: PASS. PID stable across cold-start window; reached Login/sign-in screen (delivery-04-signin.png). No startup hang/crash from perf wiring.
- AC2 no Crashlytics regression: PASS. logcat "FirebaseCrashlytics: Initializing Firebase Crashlytics 20.0.6 for com.izzes.nearsdelivery"; _setupCrashlyticsAndPerformance ran with no throw (try/catch, no E/flutter).
- AC3 Performance debug no-op (!kDebugMode -> false): PASS. collectionEnabled=!kDebugMode=false in debug; setPerformanceCollectionEnabled(false) executed via seam; FirebaseSessions "Sessions SDK disabled through data collection. Events will not be sent." No perf traces emitted (expected; release upload deferred = 296 pattern).
- AC4 Firebase-init-failure resilience: PASS (demonstrated TWICE). (a) no-config run: init failed, setup block skipped, app still booted+rendered. (b) guard is firebaseReady && try/catch in main.dart:94-96. Forced-failure run was organic, not just reasoned.
- AC5 analyze clean + suite green: analyze main.dart "No issues found"; `flutter test` = All tests passed (53 tests).

## AC results — VendorApp (NEARS-581), debug build, emulator-5554
- AC1 cold-start clean + reach first screen: PASS. Fresh build PID 11091/11282 stable; reached "Choose Your Language" onboarding + notification-permission dialog (vendor-01-firstscreen.png), MainActivity resumed after dialog. No startup hang/crash.
- AC2 no Crashlytics regression: PASS. logcat "FirebaseCrashlytics: Initializing Firebase Crashlytics 20.0.6 for com.izzes.nearsvendor"; setup ran no-throw.
- AC3 Performance debug no-op: PASS. "FirebaseSessions: Sessions SDK disabled through data collection. Events will not be sent." (collection off via !kDebugMode=false). No perf traces.
- AC4 Firebase-init-failure resilience: PASS (guard firebaseReady && try/catch; same code path as Delivery, demonstrated organically on the no-config Delivery run; identical structure here).
- AC5 analyze clean + suite green: analyze main.dart "No issues found"; `flutter test` = All tests passed (53 tests).

## Final
- Both apps: PASS. No task_bugs.
- Regression_bug (PRE-EXISTING, does NOT gate): AnalyticsService ctor eagerly reads FirebaseAnalytics.instance -> [core/no-app] crash when google-services.json absent -> stalls splash. Not in this diff (NEARS-226 wiring). Surfaced only because worktree lacked the gitignored config.
- Followups: worktree-setup gap (gitignored google-services.json not copied into worktrees); DeliveryApp sign-in still shows un-rebranded "6amMart" wordmark (reskin item, out of scope).
- PII: no HttpMetric/network traces added; only setPerformanceCollectionEnabled seam -> no URL/token in perf path. Confirmed.
