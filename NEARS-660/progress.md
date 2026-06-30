# NEARS-660 QA progress (live, append-as-observed)
Device: emulator-5554 (com.izzes.nears), worktree feat/NEARS-660-logout-clear-address @6cd242f7
Backend: http://10.0.2.2:8000 (host :8000 up)

## Live observations
- Fresh install → lang(English) → skip intro → notif+location granted (GPS preset AbuDhabi).
- Guest GPS auto-saved 6ammart_user_address = AbuDhabi zone[400,2], contact null.
- Login A = customer@nears.com → home zone-2 (Abu Dhabi) stores. login analytics fired {method: phone}.
- Switched A to seeded saved address "Demo Zone — Dhaka" (zone 1) → home zone-1 stores (Corner Grocer/Fresh Mart/Nears Mart/Organic Paradise).
- AC1 PRESENT: 6ammart_user_address present w/ PII: name "Customer Nears", phone +971565811199, addr "Demo Zone — Dhaka", lat23.81796/lng90.36602, zone_id1. [shot ac1-present-A-zone1-home.png]
- A zone-1 confirmed in log: get-zone-id?lat=23.81796&lng=90.36602 inZone=true; sectors_shown {zone_id:1}.
- Pre-existing WARN: "payment-failed details parse failed: _TypeError" on running order #158 (unrelated -> regression candidate).
- AC5 part1 PASS: Checkout (A, addr set) pre-fills Name="Customer Nears", Phone="565811199" (+971), Address="Demo Zone — Dhaka". [shot ac5-checkout-prefill-A-1.png]
- AC1 ABSENT PASS: after A menu-logout, 6ammart_user_address count=0, zero residual PII; only guest_id remains. [ac1-absent-after-logout.log, shot ac1-absent-guest-profile.png]
- Logout fired guest re-mint (/auth/guest/request); post-logout get-zone-id used in-memory residual Dhaka coords (LocationController in-mem residue = known followup; prefs+header clean).
- AC2 PASS: login B (james.wilson, no saved addr). B prefs userAddress=0, zero A PII. B location calls used RESET coords lat=&lng= then lat=0&lng=0 (NOT A's Dhaka 23.81796) -> "Service not available/Select Location". B did NOT inherit A's zone-1. [shot ac2-B-no-zone-bleed-select-location.png, ac2-B-session-zone-clean.log]
- After GPS re-resolve, B home = zone-2 Abu Dhabi (zone_id 400), B's OWN zone, never A's zone-1. authed customer/* = 200.
- get-zone-id empty/0 coords -> 403/404 -> [FAIL] "unhandled api response" (PRE-EXISTING location-feature over-log; code unchanged by 660; backend logged no error). Regression candidate, non-blocking.
- AC4: covered by passing unit test (no-address clearSharedData completes, no address) + live with-address logout ran clean. (Select-Location screen hides nav -> no-address UI logout not drivable.)
- 401 path: genuine ApiChecker 401 needs server-side token revoke (DB write, read-only rule forbids) or VM-eval (unavailable). Token-tamper+hot-restart preserved in-memory token (no effect, restored). Verified via code-identity: ApiChecker(api_checker.dart:43) -> clearSharedData(removeToken:false) -> SAME auth_repository body (clearSharedAddress L284 + updateHeader-null L301); removeToken:false only skips cm-firebase-token POST. Live-equivalent via menu logout.
- AC5 part2 PASS: B (logged in AFTER logout cycle) Checkout pre-fills B's OWN data: Name="James Wilson", Phone="01600000001", Address="F93G+HW5...Abu Dhabi". Clearing did NOT break pre-fill; NO A PII (Customer Nears/565811199) in B's checkout. [shot ac5-checkout-prefill-B-after-cycle.png]

## Verdict & backstop
- AC3 PASS: guest->login A (A own zone), A->logout->B (B clean of A), B->logout->login A (A re-login starts with CLEARED address -> must re-select). No prior-session address survived any cycle.
- Same-user A re-login: userAddress absent on re-login (cleared), home="Select Your Location" (must re-set) — consistent with fix.
- Automated backstop: flutter test test/features/auth/ -> 67 passed (incl. clear_shared_data_address_test.dart 2/2: AC1+AC2 header reset, AC4 no-address no-throw). [ERR] lines are intentional error-path tests.
- Runtime errors: none (Dart MCP get_runtime_errors clean).
- VERDICT: PASS. task_bugs: none. regression_bugs: get-zone-id empty-coords [FAIL] noise (pre-existing), payment-failed parse [WARN] (pre-existing). followups: LocationController in-memory location residue post-logout (prefs+header clean; same family as conductor's CheckoutController/_address note).
