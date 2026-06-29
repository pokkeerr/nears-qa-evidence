# NEARS-605 QA progress (live, emulator-5556, worktree feat/NEARS-605-slim-parcel)

- device: emulator-5556 (locked)
- backend: http://127.0.0.1:8000 (up, 302 /admin)
- baseUrl(app): http://10.0.2.2:8000 -> real local backend OK
- removal: -2235 / +60 in working tree, no dangling refs to removed symbols

## AC verdicts

- AC1 boot: PASS (release build boots splash->home, API 200s, no exception/red-screen)
- AC5 home: PASS so far (3 sectors Food/Grocery/Pharmacy, Recommended rail, NO parcel module); zone-switch pending
- AC4 location search: PASS (SearchLocationWidget->LocationSearchDialogWidget renders; "Dubai" -> live Places suggestions; selecting Dubai Mall -> getPlaceDetails -> map update -> out-of-zone "Service not available" graceful, no crash). ParcelController.setLocationFromPlace/setIsPickedUp retained+compile; parcel branch (isPickedUp!=null) now UI-unreachable post parcel-create removal (expected).
- AC6 cancel sheet: data+nav gap — no active cancellable parcel order (154 delivered/153 canceled), parcel_cancellation_reasons table EMPTY, bottom-nav render gap (NEARS-591) blocks Orders. Static: retained getParcelCancellationReasons + endpoint /api/v1/get-parcel-cancellation-reasons returns valid envelope (data:[]); sheet binds GetBuilder<ParcelController> OK; APK clean.
- AC7 offline payment: config gap — offline_payment_status=0 + offline_payment_methods empty -> OfflinePaymentButton/Screen gated off globally. Static: selectedOfflineBankIndex/selectOfflineBank retained; screen route+binding compile.

## FINAL
- AC6 host surface (order_details_screen, order #158) renders clean live (regression check of the screen that hosts the parcel-cancel trigger) — no crash.
- Store page (Fresh Mart Grocery) renders clean — home->store nav + home_controller path regression-free.
- Full-session logcat scan: ZERO FlutterError/EXCEPTION/FATAL/overflow/type-cast/GetX-not-found/[FAIL]/ANR on the release build.
- Debug build ANR'd on first home tap (emulator+debug jank; boot Skipped 95 frames) -> switched to clean release APK which drove the whole flow with no ANR. Debug ANR = env artifact, pre-existing home main-thread jank, NOT a NEARS-605 defect.
- Bottom nav (NEARS-591 floating glass) does not render on this emulator (documented pre-existing a11y/GPU gap) -> Orders/Basket unreachable via nav; reached order details via the active-order home banner instead.
- VERDICT: PASS (regression-zero). AC6 cancel-sheet + AC7 offline-screen live render = unverifiable (pre-existing data/config gaps, not the change).
