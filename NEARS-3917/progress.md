# NEARS-3917 QA evidence (branch de807eecf vs base 9b6729523), emulator-5600, light mode
Backend: own artisan serve from the branch worktree on :8127 (DB copy multi_food_db_qa_bug3917, --no-reload), fronted by a logging pass-through proxy on :8117 (app compiled with API_HOST=10.0.2.2:8117). Proxy log lines carry the app's X-Request-Id and the backend's echoed X-Request-Id (equal in every row).
Shared DB canary before and after: max(orders.id)=91415, business_settings id 228 = 0.

Matrix (per row: cache-empty observed / site-1b line / new INFO / GET cart/list count / cart populated)
1  logged-in no Remember me, flag ON   BASE  : cache empty yes (only cacheModuleId::g:* pref, no u: key; site-1b line) / yes / NO  / 0 / no  (row1_base*.log)
1  same                                 BRANCH: cache empty yes / yes / YES / 1 (config 200 then cart/list 200, cart_rows=1) / yes (row1_branch*.log)
2  logged-in WITH Remember me + cached module u:<acct> (flag ON) BASE: 3 GET / no site-1b / no INFO ; BRANCH: 3 GET (same shape: 1 before config, 2 after) / no site-1b / no INFO -> no double fetch
3  guest with cached module g:<id> (flag ON) BRANCH: no site-1b / no INFO / 3 GET (1 before config, 2 after; same shape as row 2)
4  guest, cache pref removed (flag ON) BRANCH: site-1b yes / INFO yes / 1 GET cart_rows=1
5  flag OFF logged-in no cache: BASE x2 vs BRANCH x2: identical line sequence (only env line "within 1km of selected address" differs), 0 cart/list, no new INFO, config 200 + 2x "splash: deeplink resolved"/"splash: routing" (cache leg + client leg) in every run
6  unauthed (pm clear, no token/guest id) BRANCH: config 200, "deeplink resolved"/"routing", no site-1b, no INFO, 0 cart/list, no crash
7  latch: second config load in-process (location confirm -> "location: triggering config data fetch") BRANCH: exactly 1 "cold-start basket load" INFO in the process; 2nd config load added 2 more "deeplink resolved" and 1 cart/list identical to BASE (r7_base vs r7_branch)
8  backend down at cold start with cached config, cache empty: BRANCH: local leg routes, client leg fails (+ one bounded retry), no INFO, 0 cart/list (accepted residual K6); every failure paired with [FAIL] line
9  K7 (see k7_race_be_proxy_excerpt.log): UI cannot add an item inside the ~0.3s trigger window (module tap + Add >= 6s). With the trigger GET response artificially held 45s (proxy), an add made meanwhile is on the server (DB row) but missing from the basket UI after the stale response lands. BASE with a held module-tap cart GET behaves identically -> pre-existing stale-response overwrite, not a regression.
AC-LOG: [FAIL]/[ERR] set identical base vs branch on the same flow (only FirebaseInit/KilledLaunch/FcmToken env failures, no google-services.json); no [ERR] anywhere; only new INFO line: "cart: cold-start basket load triggered reason=no_cached_module".
AC4: git diff 9b6729523..de807eecf -- UserApp/lib/features/splash/screens/splash_screen.dart is empty (0 bytes); site-1b line still emitted in rows 1/4/5/8, followed by the new line only on flag ON.
Automated: flutter test test/features/splash -> 276 passed, 0 failed (includes cold_start_basket_load_test.dart).
Instrument limit: the module-choose home has no bottom nav or cart affordance, so "populated" is evidenced by the cart/list 200 response (cart_rows=1) consumed by CartController plus the later Basket screen, not a badge read at that instant.
