# NEARS-2156 QA progress

Device: emulator-5556, package com.izzes.nears, customer@nears.com (user id 6).
Backend: primary tree Admin (port 8000, QUEUE_CONNECTION=sync), served the requests (worktree Admin/.env absent, not needed - no backend code changes this ticket).

## Attempt 1 — REPRODUCED
- am kill retried, confirmed dead (pidof empty) TWICE: once before push trigger, once again right before tap (background-message handler had briefly relaunched the process to post the notification; killed again before tap so the tap itself is a genuine cold start).
- Admin add-fund push (0.01 AED, customer_id=6) triggered via web driver, confirmed via wallet_transactions row id=36 (transaction_type=add_fund_by_admin) and system-tray "Fund added" notification.
- Tapped notification -> landed on module-select screen ("What are you shopping for?" / Food & Restaurant / Grocery & Food / Pharmacy tiles), NOT Wallet.
- logcat: fresh process (pid 12570), "route: building splash route, hasData=false" then "route: initial route module=grocery-food" (default fallback, not wallet route).
- Grep for KilledLaunchNotificationFailure / killed-launch getInitialMessage / [FAIL] / [ERR] in the full captured logcat: ZERO matches. getInitialMessage() did not throw.
- Evidence: docs/qa-evidence/NEARS-2156/logcat-attempt1-full.log

## Attempt 2 — REPRODUCED
- am kill retried: dead confirmed on try 2 (pre-push), dead confirmed on try 1 (pre-tap, after the background-message handler had woken the process to post the notification).
- Tapped "Fund added" notification -> landed on module-select ("What are you shopping for?"), NOT Wallet.
- logcat: "route: building splash route, hasData=true" (getInitialMessage DID return non-null data this time) -> "splash: routing" fires TWICE in the same cold start -> first pass fetches /api/v1/customer/wallet/bonuses + /api/v1/customer/wallet/transactions (wallet-screen prefetch, i.e. it WAS routing toward Wallet) -> second "splash: routing" pass immediately follows -> "route: initial route module=grocery-food" (default dashboard) wins.
- Zero KilledLaunchNotificationFailure / [FAIL] / [ERR] lines.
- Evidence: docs/qa-evidence/NEARS-2156/logcat-attempt2-full.log

## Attempt 3 — REPRODUCED
- am kill retried: dead confirmed on try 2 (pre-push), dead confirmed on try 1 (pre-tap).
- Same outcome and same double-"splash: routing" log pattern as attempt 2 (hasData=true, wallet endpoints prefetched, then overwritten by the grocery-food default).
- Zero KilledLaunchNotificationFailure / [FAIL] / [ERR] lines.
- Evidence: docs/qa-evidence/NEARS-2156/logcat-attempt3-full.log, docs/qa-evidence/NEARS-2156/attempt3-module-select-mislanding.png

## Root cause (code-read, not a fix — for the follow-up ticket)
`UserApp/lib/features/splash/controllers/splash_controller.dart`:
- `_fetchConfigData()` (line ~197-218) does a LOCAL cache-probe fetch, calls `_handleConfigResponse(..., notificationBody, ...)` (correctly threaded through), THEN on line 213 awaits a follow-on CLIENT (real network) fetch: `await _fetchConfigData(loadModuleData: loadModuleData, loadLandingData: loadLandingData, source: DataSourceEnum.client);` — this recursive call OMITS `notificationBody:` entirely, so it silently defaults to `null`.
- `_handleConfigResponse` (line 226) calls `routeFn(body: notificationBody)` (line 277) whenever `canRoute` and not `fromMainFunction`/`fromDemoReset` — this fires on BOTH the local-probe pass (body = the real wallet notification, routes to Wallet via `splash_route_helper.dart`'s `NotificationType.add_fund -> RouteHelper.getWalletRoute`, matching the observed wallet/bonuses+wallet/transactions prefetch) AND the client pass (body = null, since it was dropped -> falls into `_handleUserRouting()` -> `DestinationResolver.resolveAndNavigate()` -> lands on the default module dashboard).
- The client pass runs SECOND and its `Get.offNamed(...)` navigation wins, so the correct wallet navigation from the local pass is silently clobbered.
- This is a genuine timing/parameter-drop bug, NOT an exception — consistent with AC2's own prediction that absence of KilledLaunchNotificationFailure means "the bug, if real, is NOT an exception but likely a timing/null-return issue elsewhere in the chain."
- Fix locus for follow-up: thread `notificationBody` (and ideally `canRoute`/`fromMainFunction`/`fromDemoReset`) through the line-213 recursive `_fetchConfigData` call, or gate the second `routeFn` call so a notification-driven route isn't re-evaluated with a null body.

## Verdict (cycle 0)
AC1: met — 3/3 confirmed-process-dead attempts, all reproduced module-select-instead-of-Wallet.
AC2: met — grepped logcat broadly for KilledLaunchNotificationFailure/killed-launch getInitialMessage/[FAIL]/[ERR]: zero matches in all 3 captures. Correctly diagnosed as non-exception (getInitialMessage did not throw); root cause identified above.
AC3: NOT met — live demonstration shows a killed-and-relaunched wallet push does NOT route to Wallet; genuine gap confirmed, filed as task_bug for follow-up fix (expected/planned outcome per this ticket's own framing, not a defect in this pass's diff).

## Fix-cycle 1 delta re-QA (commit a037cb67) — closing TB-2156-1

Device: emulator-5556 (same pool device), package com.izzes.nears, customer@nears.com (user id 6,
same login carried over from cycle 0 — FCM token confirmed still registered, no re-login needed).
Backend: primary tree Admin (port 8000, QUEUE_CONNECTION=sync) — same as cycle 0.

**Tooling gotcha found and corrected mid-run:** `adb shell am force-stop <pkg>` sets Android's
"stopped" component flag, which blocks the implicit `com.google.android.c2dm.intent.RECEIVE`
broadcast FCM uses to wake a killed app — confirmed live via `GCM: broadcast intent callback:
result=CANCELLED` + repeated `AlarmManager: FcmRetry` re-arms in logcat, and the resulting cold
start actually showed `hasData=false` (no notification payload at all) plus a contaminating
duplicate "Fund added" notification once the retry eventually landed. Cross-checked against cycle
0's own captured logcat: the kill event there shows `Zygote: Process ... exited due to signal 9
(Killed)`, i.e. cycle 0 used `am kill` (kills only cached/background processes, does NOT set the
stopped flag), not `am force-stop`. Corrected to `am kill` for both clean attempts below; the one
force-stop-contaminated attempt was discarded (not counted, evidence not kept in the gallery).

- **Attempt 1 (clean) — Wallet reached.** am kill confirmed dead (pre-push) -> admin add-fund POST
  (reference NEARS-2156-c1-clean-attempt1) -> background handler briefly woke the process to post
  the notification -> am kill again, confirmed dead (pre-tap) -> exactly one fresh "Fund added"
  notification in the tray -> tapped it. logcat: `hasData=true`, `splash: routing` fires twice (both
  legs), local leg prefetches `/api/v1/customer/wallet/bonuses` + `/api/v1/customer/wallet/transactions`,
  **zero** `route: initial route module=...` fallback line this time, zero [FAIL]/[ERR]. UI landed on
  Wallet ("Wallet Amount" / "Wallet History" / "Add fund by admin" transaction rows).
  Evidence: cycle1-attempt1-logcat.log, cycle1-attempt1-notification-tray.png, cycle1-attempt1-wallet-landing.png
- **Attempt 2 (clean) — Wallet reached.** Same recipe (reference NEARS-2156-c1-clean-attempt2), same
  outcome: hasData=true, both routing legs fire, zero fallback-module line, zero [FAIL]/[ERR], landed
  on Wallet.
  Evidence: cycle1-attempt2-logcat.log, cycle1-attempt2-notification-tray.png, cycle1-attempt2-wallet-landing.png
- **Regression — normal cold launch (no notification), 1 check.** am force-stop (fine here — no FCM
  wake dependency, launched explicitly via `am start`) -> confirmed dead -> `am start`. logcat:
  `hasData=false` (no notification body, correctly null on both legs), `route: initial route
  module=grocery-food` fires as before, zero [FAIL]/[ERR]. UI landed on the default module-select
  ("What are you shopping for?" tiles) — unchanged from pre-fix behavior; the fix does not leak a
  stale/local-leg body into a non-notification launch.
  Evidence: cycle1-regression-cold-launch-logcat.log, cycle1-regression-cold-launch-moduleselect.png

**Automated backstop:** `flutter test test/features/splash/splash_controller_test.dart` — 43/43
passed, including the new NEARS-2156 regression test
(`notificationBody survives the local->client recursion`) pinning both legs' `routeFn` calls to
carry the wallet body.

## Verdict (cycle 1)
AC3: **met** — 2/2 confirmed-process-dead attempts (clean `am kill` recipe) now land on Wallet, not
module-select. TB-2156-1 closed. Regression check (normal cold launch) confirms unchanged default
routing. AC1/AC2 reused from cycle 0 (unaffected surface, no overlap with files[] beyond the one
already-verified splash_controller.dart routing path, which is exactly what AC3 re-verifies).
