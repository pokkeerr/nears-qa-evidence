# NEARS-463 QA progress checkpoint

Branch feat/NEARS-463-cross-app-hardening @ 3ab7c7d3 · device emulator-5554 (reclaimed stale lock)

## Backstops
- Backend `CartStoreClosedTest`: 4/4 PASS (closed->403, closed+schedule_order->200, increment-closed->403, open->200).
- UserApp `api_client_get_query_test`: 8/8 PASS (AC-3 ?k=v append + AC-4 no-query byte-identical).
- DeliveryApp `api_client_redact_headers_test`: 9/9 PASS.
- VendorApp `api_client_redact_headers_test`: 9/9 PASS.

## Live backend contract (curl, customer token)
- AC-1 backend: Store 8 (closed,no-sched) item145 -> HTTP 403 store_closed. PASS
- Exempt: Store 9 (closed,sched_order=1) item52 -> HTTP 200 allowed. PASS (backstop-confirmed live)
- Open control: Store 1 (active=1) item1 -> HTTP 200 allowed. PASS

## Live app demonstrations
- AC-2 DeliveryApp (debug, live login Ali Hassan): login POST /auth/delivery-man/login fired (200).
  - Auth HEADER redacted -> "Bearer qOcv9gR..." GOOD.
  - BUT request BODY still logs cleartext: "API Body: {phone: +971565..., password: <pw>}" -> FAILS AC-2.
  - Secondary: bearer token also leaks via ?token= URI query string in GET logs (header redaction doesn't cover it).
  - Note: debugPrint routes to flutter-run stdout (I/flutter via get_app_logs), NOT adb logcat `flutter` tag this session.
  - Post-login dashboard stuck on "Loading..." due to FirebaseMessaging.getToken failing (emulator can't reach Firebase) — ENV issue, not NEARS-463; login itself returned 200.
- AC-2 VendorApp (debug, live login organicshop@demo.com): login POST /auth/vendor/login fired (200).
  - Auth HEADER redacted -> "Bearer AcUCv1p..." GOOD. No ?token= in URIs (vendor uses header only).
  - BUT login BODY logs cleartext "API Body: {email: organicshop@demo.com, password: <pw>, vendor_type: owner}" -> FAILS AC-2.
  - WORSE: update-fcm-token BODY logs the FULL raw bearer token in cleartext + the fcm device token.
  - Separate "-----Device Token-----" debugPrint also leaks fcm token (pre-existing, non-api_client).
  - Post-login dashboard loaded fine (vendor/profile, current-orders, notifications all 200) — regression clean.
- AC-2 OVERALL: FAIL (both apps leak login credentials/token via request BODY on debug). Header redaction works.

- AC-1 UserApp live (zone 2 / Abu Dhabi):
  - CLOSED Store 8 (Abu Dhabi Fresh Market): item detail shows "Store closed · opens at 08:00 · advance ordering unavailable" + disabled CTA "Store is closed"; quick-add attempt -> backend [403] /customer/cart/add store_closed; item NOT added (cart badge empty). PASS.
  - Backend message "Store is closed at order time" surfaces via api_client handleResponse->ApiChecker.checkApi->showCustomSnackBar(statusText) on the 403 (verified by code path; front-line UI is the disabled button + banner).
  - EXEMPT Store 9 (Organic Shop, schedule_order): item detail shows "Schedule Order" CTA; tap -> [200] cart/add, "Item added to cart". PASS (Option B not regressed).
  - OPEN control (Vegan Market, item 243): "Add To Cart" -> [200] cart/add, "Item added to cart". PASS.
  - add_to_cart analytics fired PII-safe (item_id/price/qty only) on both successful adds.
- AC-3 (getData query append): NO live caller passes query map (101 getData calls, 0 with query:) — engineer correct. getData routes uri through appendQuery() (verified line 482). Relies on unit test 8/8 PASS.
- AC-4 (no-query GETs unaffected): UserApp home/config/banners/module all loaded normally (200), app fully usable; unit test asserts byte-identical no-query URLs. PASS.
- UserApp session: ui_errors clean (no red-screen/overflow).
- DB: store state untouched (read-only); QA-created transient cart rows (147,148,150) cleaned up.

## VERDICT: FAIL — AC-2 (headline security AC) fails: login request BODY leaks credentials/token on debug build (both apps). AC-1/AC-3/AC-4 + all backstops PASS.

## fix_cycle 2 delta re-QA — AC-2 (2026-06-19)
- branch feat/NEARS-463-cross-app-hardening @762efd56 | device emulator-5554
- AC-2 DeliveryApp: PASS — login POST /api/v1/auth/delivery-man/login logged URI+redacted header only, NO API Body line; all token= query params masked to token=***; bearer truncated. evidence: delivery-login-flow.log
- automated: DeliveryApp flutter test api_client_redact_headers_test.dart = all passed
- AC-2 VendorApp api_client: login POST /api/v1/auth/vendor/login logged URI+redacted header only, NO API Body (PASS for api_client surface). evidence: vendor-login-flow.log
- AC-2 BUG (FAIL): VendorApp + DeliveryApp print FULL FCM device token in cleartext on login via _saveDeviceToken() (kDebugMode/debugPrint) — auth_repository.dart. NEARS-463 fix did not remove it. evidence: bug-fcm-device-token-cleartext-login.log
- automated: VendorApp flutter test api_client_redact_headers_test.dart = all passed
- VERDICT: FAIL — AC-2 not fully met; fcm token still leaks in cleartext on debug login (AC-2 says "NO fcm token anywhere").
