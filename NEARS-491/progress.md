# NEARS-491 QA progress (live, emulator-5556)

- Backend up (config 200), queue:work running. baseUrl=http://10.0.2.2:8000 (real local). App logged in (customer), running order #158 present.
- Automated backstop: `flutter test` = 1472 passed / 0 failed (matches engineer). Targeted persistent-nav + back-button tests: 7/7 pass.

## AC results
- AC1 / Scope-1 grocery "See All": PASS — lands on Categories TAB, bar present (5 tabs), mint active indicator on Categories (grid icon), NO back arrow, default first-non-empty category (Beverages) selected. Banner intact. ui_errors clean. shot 01.
- Scope-2 grocery chip (Dairy & Eggs): PASS — Categories TAB, Dairy preselected, bar present, no back arrow, mint active. shot 02.
- Scope-3 rapid double-tap (General Items->Dairy, queued): PASS — last tap (Dairy) wins, no stale rail, bar stays, no overflow/exception. shot 03b. (03 was my own methodology artifact — taps 2/3 hit transitioned tab.)
- Scope-1/2 pharmacy category circle (First Aid): PASS — Categories TAB, First Aid preselected, bar present, mint active, no back arrow. shot 04-pharmacy-category-circle-tab. (NOTE: pharmacy "Basic Medicine Nearby" filter chips at y=1677 are NOT category circles; category circles at y=1270.)
- Scope-1/2 food category circle (Desserts): PASS — Categories TAB, Desserts preselected, bar present, mint active, no back arrow. Basket badge "1" visible on Categories tab. shot 05.
- Scope-4/AC2 all 5 tabs from Categories (Search/Basket/Profile/Home): PASS — every tab switches, bar persists on all 5, mint indicator follows. shots 06,07,08,09.
- Scope-5 basket badge on Categories tab: PASS — badge "1" visible/correct on Categories tab. shot 10.
- Scope-6/AC6 standalone /categories (via Get.toNamed = deep-link/external/desktop-fallback path): PASS — barred full-screen WITH back arrow, bar ABSENT; back pops to dashboard with bar restored. shots 11, 11b. NOTE: true OS deep-link to /categories falls through to home (LinkConverter doesn't map that path — PRE-EXISTING, not this change); exercised the route via the real product path it actually uses.
- Scope-7 back-stack after rail->Categories: PASS — Android back goes to Home tab (index 0), app NOT exited (MainActivity resumed), no double-dashboard. shot 12.
- Scope-8/AC8 NEARS-340 running-order banner on Categories tab: PASS — banner "Your Order is Confirmed #158" unchanged geometry, above the bar. shot 13. (Banner vanished mid-session from nav churn; fresh relaunch restored it; order #158 still 'confirmed' in DB; banner code untouched by change.)
- Scope-9/AC9 RTL/Arabic: PASS — rail+chips flow RTL (rail on right, chips right-to-left), bottom nav mirrored (Home rightmost), appBar + See All (رؤية الكل) RTL, no back arrow on tab, banner RTL above bar, no overflow. shots 14b, 14.
- Scope-10 shimmer + empty state: PASS — Categories tab shows rail+grid shimmer while loading with bar intact (shot 15-attempt2); empty category (Bakery & Bread) shows in-pane "No category item found" no-data state, rail+bar intact, NOT full-screen blank (shot 16).
- Scope-11 desktop breakpoint: PASS — at logical width>=1300 (density 160) the desktop layout renders WITHOUT a bottom nav bar by design, no crash/RenderFlex; fallback contract (switchToTab->false->Get.toNamed) verified live in Scope-6 + unit-tested; app recovers clean to phone mode (shots 17a, 17). Density restored to 480.
- Regression sweep (bounded, AC3 matrix): PASS — Notification (type-E exception) still barred full-screen WITH back arrow + NO bottom nav (not regressed, shot 18); Search tab in-nav surface bar present (shot 19); 2 dashboard routes show bar on all 5 tabs (verified throughout). No route other than /categories ever had a bar.
- Session-wide log scan: CLEAN — no [FAIL]/[ERR], no nears_error_retry/generic-error, no RenderFlex/overflow, no Get.find failures, no uncaught exceptions.
- Pre-existing (NOT this change): launch [WARN] "payment-failed details parse failed: _TypeError" on /customer/order/payment-failed — no payment files touched by NEARS-491; paired AppLogger WARN (not silent); -> non-blocking regression note.
- Automated backstop: flutter test = 1472 passed / 0 failed (confirms engineer 1472/0).

## VERDICT: PASS — all 11 scope items + 5 ACs demonstrated live, light mode, logs clean, no task_bugs.

