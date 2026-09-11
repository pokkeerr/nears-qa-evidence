# NEARS-3464 QA progress checkpoint

- Device: emulator-5558 (wave56) rejected for GPS/geo-fix instrumentation (known pool issue per nav-guide §5.11 gotcha area / memory lesson "pick-map-camera-idle-qa-instruments" — get-zone-id 404'd after geo fix despite direct backend curl confirming zone-1 match for the same coords). Switched to emulator-5566.
- Backend: shared primary-tree `php artisan serve` on :8000 (Admin/ in /Users/Apple/Projects/nears), confirmed 200 + zone-1 lookup working directly.
- Unit backstop: `flutter test test/features/store/store_details_get_notify_test.dart` — 3/3 PASS (cached-data notify, fresh-fetch pre-await notify, terminal finally exactly-once regression).
- Review lessons: 68 active selected; most relevant to this fix: `getx-retry-missing-preawait-notify` (this IS the exact bug class fixed), `isloading-flag-omitted-try-catch-sibling-methods`, `stale-async-writeback-seals-new-session`.

## FINAL VERDICT: FAIL

Both new `update()` calls (store_controller.dart:916, :921) run synchronously inside
`getStoreDetails()`, itself called synchronously from `initState()` in both live
call sites (store_screen.dart, cart_screen.dart) — throws Flutter's
"setState() or markNeedsBuild() called during build." Reproduced live twice on
store screen (caught, logged [FAIL]) and once on cart screen (UNCAUGHT async error).
Matches the exact hazard checkout_controller.dart already defends against via
NEARS-2709's addPostFrameCallback deferral — this fix reintroduces it without
the deferral. AC1's cache-hit branch is unreachable from any live call site
(all 3 callers pass name=null) — UNVERIFIABLE live, unit-pinned only.

Evidence published: https://github.com/pokkeerr/nears-qa-evidence/tree/main/NEARS-3464
Jira comment posted: NEARS-3464 comment id 19696.
Teardown complete: qa-run-stop.sh run for both 5558/5560, packages uninstalled,
both device locks released.

---

## Fix-cycle 2 (delta re-QA, 2026-09-11)

- HEAD 9c82557d7, stacked on 470de2100 (defers both update() calls via
  `WidgetsBinding.instance.addPostFrameCallback`) + c61c7da95 (original fix).
- Device: emulator-5566 (5556/5558/5560/5562 either occupied-without-lock or
  below the 800MB disk floor even after `qa_disk_reclaim --clean`; 5566 had
  936944 KB free, above floor). Backend: shared primary-tree `php artisan
  serve` on :8000 (read-only, no DB mutation).
- AC2(a) store_screen.dart initDataCall path — opened 2 distinct stores from
  Home (Corner Grocer, Daily Fresh Market) directly: both rendered content
  cleanly, 0 [FAIL]/[ERR] matches, no FlutterError/setState-during-build in
  raw logcat. Screenshots: ac2a-store1-corner-grocer.png,
  ac2a-store2-daily-fresh-market.png.
- AC2(b) cart_screen.dart initCall path (the prior UNCAUGHT crash site) —
  entered cart screen twice (fresh entry + re-entry after checkout Get.back()):
  both times 0 errors, cart rendered normally (multi-store basket, 3 items).
  Screenshot: ac2b-cart-screen.png.
- AC3 finally-block-fires-once — spot-checked checkout_controller.dart's own
  getStoreDetails call site (line 169-170) twice: once landing on the
  out-of-zone panel (paired [FAIL] log, expected per NEARS-1025/2582), once
  on the full happy-path checkout screen (pricing/address/ETA rendered, no
  flicker/double-render). Unit-pinned by
  store_details_get_notify_test.dart's SchedulerBinding-based exactly-once
  test (independently re-ran: 5/5 pass). Screenshot:
  ac3-checkout-happy-path.png.
- Full-session sweep: `adb logcat -d | grep -iE
  "setState\(\) or markNeedsBuild\(\)|FlutterError|Unhandled Exception|EXCEPTION CAUGHT"`
  → zero matches across the entire run (store↔cart↔checkout, 2 stores, 2
  checkout entries).
- **Non-blocking regression finding (pre-existing, unrelated to this fix):**
  navigating cart_screen → Get.back() while the cart held 2 out-of-zone
  items + 1 in-zone item transiently landed on store_screen's generic
  "This store could not be loaded" failure view instead of the in-zone
  store actually being browsed (Daily Fresh Market) — a race in the SHARED
  mutable `StoreController._store` field across the concurrent per-cart-item
  background validation fetches cart_screen fires (NEARS-2582). Tapping
  Retry recovered immediately to the correct store. No FlutterError, no
  setState-during-build — a data race, not a rebuild-during-build defect,
  and the postFrameCallback timing this ticket changes does not affect
  WHICH fetch's response lands in `_store` last (only WHEN the notify
  fires). Pre-exists this fix; filed as regression_bugs, does not affect
  verdict. Screenshot:
  regression-multistore-cart-back-load-failure.png.

### FINAL VERDICT: PASS

Evidence published: (this push) — see gallery link in Jira comment.
Teardown complete: qa-run-stop.sh on emulator-5566, package
com.izzes.nears.nears_nears_3464_store_details_update uninstalled, device
lock + account lock (customer@nears.com) released.
