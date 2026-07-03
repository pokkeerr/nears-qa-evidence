# NEARS-821 DeliveryApp Wave-1 QA — live progress

Device: emulator-5562 (AVD nears_qa_delivery, Android 14, arm64). Worktree: /Users/Apple/Projects/nears-audit-delivery @ feat/audit-delivery-07 (7a790931). Backend: local artisan serve @127.0.0.1:8000 (app default 10.0.2.2:8000). DB read-only; all state changes via platform UIs (vendor/admin panel, app).

## Environment notes
- google-services.json is gitignored → absent in worktree → Firebase init fails → `AnalyticsService` ctor throws in di.init → runApp never runs (white screen). Provisioned the file from primary tree; clean boot after. PRE-EXISTING latent boot dead-end (get_di.dart:85 unguarded despite _initializeFirebaseSafely=false) — regression-candidate, NOT Wave-1.
- uifind.py live `exec-out uiautomator dump /dev/tty` returns empty on this emulator; dump-to-/sdcard + pull works (helper used). Tooling gap for the guide.
- Chrome DevTools MCP browser held by another agent's profile → used Playwright (uinav_web) fallback for web panels.

## AC checkpoints
- U11 login: PASS — login as d@d.d (+971563456789) then QA DM (+971569990001) reaches dashboard; `[NET] /api/v1/auth/delivery-man/login` 200. Shots 03/05.
- U11 token storage: PASS — FlutterSharedPreferences.xml has NO token/password keys (only user_number + dial codes); FlutterSecureStorage.xml holds encrypted entry. Evidence: key dump in QA report.
- U11 remember-me: PASS — after 401-eject relaunch of login screen, phone prefilled ('563456789'), password field empty.
- Login failure path logging: PASS — transient transport throw logged `[FAIL] endpoint=/api/v1/auth/delivery-man/login http_status=null type=ApiFailure correlation_id=ee5e5133…`; spinner resolved back to "Log In" (no stuck state).
- 401 handling: definitive 401 on latest-orders poll → logged `[FAIL] … http_status=401 correlation_id=4198f985…` → clean eject to login, no crash (cause: QA curl login rotated the single-session token — expected platform behavior).
- U06/U05 BLOCKER FOUND (task_bug, breaks_ac): Profile → Online toggle dead-loops. profile_screen.dart:217 inline check + stale private _checkPermission (profile_screen.dart:499–527) still treat whileInUse as insufficient on Android, while NEARS-878 removed ACCESS_BACKGROUND_LOCATION from the manifest → LocationPermission.always is UNATTAINABLE → education dialog → App-Info settings → re-check → dialog again, forever. Driver can NEVER go online on Android. The U06 fix updated only profile_service.dart (checkPermission), missing the screen-local copy the toggle actually calls (profile_screen.dart:218). Reproduced live 3×: dialog re-shown after every grant/settings round-trip; DB active stays 0. Evidence: bug-online-toggle-permission-loop.png.
- Request tab offline empty-state renders cleanly ("You are offline now…" dialog + "No order request available"), no crash. Shot 06.

## Completed run (final)
- U02 poll: PASS — bg 25s = 0 polls, resume refresh <6s; 28s outage → 4x [FAIL] http_status=null logged, details screen never popped, clean 200 recovery.
- U03: pick-up slider → update-order-status 200 → intended gotoDashboard; COD sheet popped once; running/history lists separate (current-orders vs all-orders). Parcel OTP not live-testable.
- U08: "Amount Collect from Customer: 23 AED" + sheet "Order Amount: 23 AED" == DB order_amount 23.00; delivered; wallet collected_cash 23.00. Shots 08/10.
- U07: sheet data-blocked (isPayable hides Withdraw); binding proven via Add-Withdraw-Method: dropdown 2→1 fields, persisted selected method {"paypal_email":"qa.dm4@nears.demo"}. Shots 13-15.
- U09: earning report real data (shot 16); loyalty/referral/withdraw-list empty states clean; INVOICE FAIL — web route session-gated (HomeController:438) → 403 always. bug-invoice-endpoint-403.log.
- U01: notifications list renders real push rows; tap → detail sheet. Shot 17.
- U12: airplane cold start → Retry state (shot 18); recovery to dashboard, session survived (U11 survival).
- Backstop: flutter test 152/152 pass. Final error sweep clean.
- Findings: blocker online-toggle loop; invoice 403; wallet stuck-spinner (followup); dup-GlobalKey one-frame (followup); pre-existing Firebase-fail boot dead-end (regression-candidate).
- Verdict: FAIL (blocker) — report tasks/audit-2026-07/deliveryapp-wave1-qa.md.
2026-07-03T14:34:57+04:00 U06-A: whileInUse ON first tap -> update-active-status 200, DB active=1, no dialog. corr: clean
2026-07-03T14:37:13+04:00 U06-B: denied->prompt->grant whileInUse->update-active-status 200, DB active=1, no education dialog/loop
2026-07-03T14:42:13+04:00 U06-C: dont-allow->education dialog(once, Cancel clean)->Next->AppInfo settings->grant->recheck fired updateActiveStatus; re-toggle instant, DB active=1, NO dead-loop
2026-07-03T14:54:54+04:00 U09: invoice API 200 x3 (order/referral/loyalty variants), real PDFs saved+opened in viewer, no id param in route
2026-07-03T15:05:51+04:00 U05: GPS off -> accept -> system loc prompt declined -> confirm sheet -> [FAIL] LocationServiceDisabledException logged, dialog closed, toast path, list intact, NO brick. DB: 166 unassigned
2026-07-03T15:13:53+04:00 U02-accept: top card -> order 166 accepted (DB dm_id=1), details screen shows Order ID 166
2026-07-03T15:18:08+04:00 U02-ignore: top card ignored -> exactly 1 card removed (badge 2->1), accepted remaining -> DB 164 accepted; 165 stays unassigned = ignore/accept resolved correct ids. accept-164 client-side timeout (env), server landed it
2026-07-03T15:31:48+04:00 NEW DEFECT: postMultipartData no-timeout silent hang on delivered transition; UI recovered after manual dismiss + poll reconcile (166 Delivered)
