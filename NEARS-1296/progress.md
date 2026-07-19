# NEARS-1296 QA progress (AC2 live E2E)
- API direct GET cancellation-reasons?type=customer -> 200, total_size=4, ids 2/3/4/5 with en+ar translations. PASS (source-of-truth for dialog).

## AC2 live E2E diagnosis (2026-07-19 ~05:00)
- Device: emulator-5556 (locked). Backend :8000 serves multi_food_db (verified .env + live SELECT via API).
- Pre-installed APK (v3.8.0, installed 03:19 by another session, likely NEARS-1295/qa1295) threw ApiFailure(status:0) on EVERY endpoint (banners/module/stores/running-orders/order-list). AppLogger [FAIL] fired correctly (logging contract OK).
- OS-level nc/ping/curl emu->10.0.2.2:8000 = HTTP 200; host curl = 200. Emulator reboot did NOT clear it => stale APK dialing wrong host (wrong --dart-define baseUrl), not env.
- Remedy: fresh `flutter run` from primary UserApp source (dev defaults -> baseUrl http://10.0.2.2:8000). Build in progress.

## AC2 E2E RESULT — PASS (2026-07-19 05:11)
- Fresh dev build (baseUrl 10.0.2.2:8000) => all endpoints 200.
- Home running-order banner "More" -> My Orders -> Ongoing -> Order #176 (pending, store 35, user 6).
- Cancel Order -> dialog listed EXACTLY the 4 seeded reasons: Ordered by mistake / Found a better price elsewhere / Taking too long / Changed my mind. cancellation-reasons GET=200. (This was the bug: previously empty.)
- Selected "Taking too long" -> Submit -> POST /order/cancel=200.
- DB: order 176 order_status='canceled', cancellation_reason='Taking too long', canceled_by='customer', canceled=2026-07-19 05:11:13 (matches POST 05:11:13.724).
- UI: order-details shows "Cancelled, Order #176" + note "Taking too long". Regression: 176 left Ongoing (now 162/165/169/170); Cancelled tab loads.
- Correlation: laravel.log records failures only; a 200 cancel emits no error line, so X-Request-Id-in-laravel.log is observable on FAIL paths only. Server-side correlation proven via DB mutation at exact POST timestamp + exact reason. No [FAIL] during any AC2 action.
