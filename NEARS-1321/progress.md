# NEARS-1321 — QA cycle 2 (conflict-resolution re-QA)

Build: worktree feat/NEARS-1321-store-origin-label @ f7f715f4 · device emulator-5554 (Pixel_10_Pro) · UserApp com.izzes.nears v3.8.0
Fresh build proof: uninstalled old APK → `assembleDebug` (16.6s) → fresh app-debug.apk installed (firstInstallTime==lastUpdateTime 2026-07-20 14:28:23) → live Dart VM Service http://127.0.0.1:59694.
Root cause of cycle-1 FAIL: prior run's live `flutter run` was booted from the WRONG worktree (nears-NEARS-1322-cart-rails, base c945c085, lacks the chip code) → it inspected a stale/wrong APK. Environment artifact, not a defect.

- AC1 (chip on Buy It Again Mango card): PASS — zone 1, user 6. Chip "Nears Mart" (storefront icon + ellipsized name) renders on Mango card below the 10% OFF badge. Evidence: reqa-c2-buyitagain-mango-chip.png. Log: GET /api/v1/customer/order/buy-it-again → 200, clean.
- AC2 (multi-store distinguishable): PASS — zone 2 (Abu Dhabi, saved addr id 45). Rail shows distinct chips per card: ABU DHABI FRESH MARKET, TEST STORE. Evidence: reqa-c2-buyitagain-multistore-z2-a.png / -b.png. Log: buy-it-again → 200, clean.
- AC3 (no chip leak): PASS (spot-check) — Fruits & Vegetables category grid: no store chip. + automated negative test green.

Automated backstop: 8/8 passed (item_widget_store_origin_test + buy_it_again_store_origin_parse_test).
Pre-existing (regression lane, non-blocking): 3 flakes in test/helper/destination_resolver_test.dart (engineer-flagged, unrelated).
