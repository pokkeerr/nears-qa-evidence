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

## Verdict
AC1: met — 3/3 confirmed-process-dead attempts, all reproduced module-select-instead-of-Wallet.
AC2: met — grepped logcat broadly for KilledLaunchNotificationFailure/killed-launch getInitialMessage/[FAIL]/[ERR]: zero matches in all 3 captures. Correctly diagnosed as non-exception (getInitialMessage did not throw); root cause identified above.
AC3: NOT met — live demonstration shows a killed-and-relaunched wallet push does NOT route to Wallet; genuine gap confirmed, filed as task_bug for follow-up fix (expected/planned outcome per this ticket's own framing, not a defect in this pass's diff).
