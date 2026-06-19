# NEARS-459 QA progress (live checkpoints)
Device: emulator-5554 | Branch: feat/NEARS-459-pusher-late-init-track @ 12ecf029

## Automated backstop — PASS
cmd: flutter test order_tracking_screen_test.dart + guest_track_order_screen_test.dart + order_controller_test.dart
result: 54/54 passed. Covers: in-flight->spinner, loaded+null->NearsEmptyState (not spinner), loaded+order->GoogleMap, isGuestTrackLoaded flag transitions.

## AC-1 (headline crash: LateInitializationError on dispose) — PASS
- Real production OrderTrackingScreen mounted with websocketEnabled:false (exact crash condition) + disposed: GREEN (3/3).
- Controlled local revert of the fix (late PublicChannel) -> all 3 tests RED with:
  "LateInitializationError: Field 'publicChannel' has not been initialized." (ac1-late-init-repro-proof.log)
- Restored fix -> GREEN. Crash is fixed AND guarded by a regression test.
- Live on-device in-app path to OrderTrackingScreen requires a RUNNING order (Track FAB gated on isRunning/shouldShowTrackDeliveryButton). Seeded data for user 6 (customer@nears.com, 39 orders) + all seeded users = ZERO ongoing orders (Ongoing tab shows "No ongoing orders"). DB-mutation forbidden -> cannot create a running order. Live in-app screen-mount demonstrated via the real-widget backstop instead; data gap noted as a Data-DoR followup.

## Regression: My Orders list opens — PASS (regression-my-orders-list.png)
## Regression: Ongoing tab — "No ongoing orders" empty state renders — PASS (regression-ongoing-empty.png)

## AC-2 (not-found empty state) — PASS (via real-widget backstop; no authed live path to invalid id)
- Authed tracking screen for an invalid id is reachable ONLY via the Track FAB (isRunning-gated) -> unreachable for seeded data (no ongoing order) without DB mutation. Stated, per AC fallback.
- Widget backstop "loaded with NO order shows NearsEmptyState, not a spinner" PASSES against the REAL OrderTrackingScreen. NearsEmptyState renders Icons.search_off_rounded + 'no_order_found' + 'no_order_found_subtitle' + 'back' CTA wired to Get.back (verified in code + widget).
- i18n: no_order_found_subtitle present en/ar (real) + bn/es (EN fallback) — confirmed.

## AC-3 (Pusher happy path) — UNVERIFIABLE (dev Pusher disabled) + load-path NO-REGRESSION confirmed live
- Dev build websocketEnabled:false -> real-time Pusher path not exercisable (no staging). Marked unverifiable per AC.
- Valid order load path confirmed live: order #27 (delivered/delivery) renders Order Tracking stepper + map + Order Summary + Delivery Details normally (ac3-valid-order-map-details.png). Widget test "loaded WITH an order shows GoogleMap" PASSES. No regression to the load path.

## AC-4 (Crashlytics) — NOT VERIFIABLE NOW (out-of-band post-ship). firebase_crashlytics_enabled:false in dev (confirmed in boot logs).

## Regression: valid order details + map + tracking timeline render — PASS (ac3-valid-order-map-details.png)
## Regression: app survives background->foreground on a trackOrder-bearing screen — PASS (no crash signatures)
## Live device logcat: ZERO LateInitializationError / Null-check / EXCEPTION CAUGHT across entire session — PASS
## Refund-request: button gated on delivered && !parcel && refundActiveStatus && no-campaign — pre-existing gating, outside NEARS-459 scope; order ecosystem trackOrder load path proven healthy.
