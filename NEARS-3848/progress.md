# NEARS-3848 QA [8] — fix cycle 0 — progress

Env: emulator-5554 (Pixel_10_Pro AVD, lock NEARS-3848), UserApp built by scripts/qa-run.sh --root <worktree> --dart-define API_HOST=10.0.2.2:8149
(APK = <worktree>/UserApp/build/app/outputs/flutter-apk/app-debug.apk, pkg com.izzes.nears.nears_nears_3848_mixed_asap_eta).
Backend: /Users/Apple/Projects/nears-NEARS-3848-mixed-asap-eta @ 81e89a88a, `php artisan serve --no-reload :8148`, DB qa_3848 (private copy; worktree .env DB_DATABASE=qa_3848).
App -> QA body-logging proxy :8149 -> :8148 (dry-run switch refuses */place with 403 qa_dry_run; stale-config switch rewrites GET /api/v1/config cross_module_basket=false).
DB proof: GET /api/v1/config on :8148 = cross_module_basket true while multi_food_db id=228 = 0.
Copy fixtures: user 6 cart rows; store_schedule day 3 for 35/57/49; stores.order_place_to_schedule_interval=120 for 35.
Orders placed (copy only): group f621e637-35b3-4068-baab-575cc2f0a3e1 -> 91424 (store 35) + 91425 (store 57). Nothing else placed.

- AC1 [ui] PASS — mixed (35 grocery + 57 pharmacy): no TimeSlotSection in a11y at 3 scroll positions (a11y-ac1-mixed-checkout-en-pos{1,2,3}.xml); positive control same-module shows 'Preference Time'+'Instant' (a11y-ac3-same-module-2store-picker-en.xml). Per-store rows 'Test Store ~18 min' / 'Green Cross ~29 min'; hero pill 'Arriving in ~18 min' = lead store (known gap NEARS-3852/3851). Note->Payment spacing matches section rhythm (ac1-mixed-checkout-note-to-payment-en.png). No Stitch/DLS ref supplied -> final visual to ux-review. logs clean.
- AC2 [behav] PASS — group/validate + group/place bodies: no schedule_at key top-level or per store; server stored scheduled=0 (ac2-mixed-place-request-bodies.log). logs clean.
- AC3 [behav] PASS — flag ON same-module 2-store: picker visible, TimeSlotBottomSheet opens, validate body schedule_at=2026-09-30 01:01 (ac3-same-module-schedule-at-bodies.log).
- AC4 [behav] PASS (live part) — per-store rows carry own ETA (~18 vs ~29 min; store delivery_time 1-15 min vs 20-40 + distance). '—' fallback not arrangeable live (straight-line distance never null for stores with coords) -> unit proof mixed_basket_eta_per_store_test.dart.
- AC5 [behav] PASS — stale client flag (proxy config rewrite; server flag ON): validate schedule_at=2026-09-30 04:01 -> real server 403 reason=mixed_basket_asap_only; sheet dismissed, snackbar visible over checkout, picker reset to 'Instant' (a11y-ac5-..., ac5-mixed-asap-only-403.log).
- AC6(a) PASS — Grocery header, lead 35 'No slots are available' today; mixed basket -> validate valid=true + group/place sent (place = dry) (ac6a-mixed-no-slots-not-blocked.log). Positive control same-module same state -> [FAIL] reason=select_a_time, no request (ac6a-positive-control-same-module-select-a-time.log).
- AC6(b) PASS — 57 closed (08:00) -> validate store_closed store_ids=57, [FAIL] logged, nothing placed.
- AC-REG PASS — flag OFF single-module: picker visible, /order/place schedule_at=2026-09-30 04:01 (acreg-flag-off-single-module-schedule-at.log).
- V4 UNVERIFIABLE live — reskin's only buy-now entry is a campaign item; campaign items carry available_date_starts which hides the picker by the base rule. Unit proof buy_now_mixed_cart_schedule_test.dart.
- AC-LOG PASS — [FAIL] ... reason=mixed_basket_asap_only via AppLogger, correlation_id == X-Request-Id e8f0d79a-..., no PII.
- Scope 4 PASS — mixed + closed FOOD 49: ClosedStoreNotice renders, Place blocked [FAIL] reason=store_is_closed store_ids=49. Pre-existing: notice shows lead store's opening time (bug-closed-notice-shows-lead-store-opening-time.*).
- RTL PASS — AR mixed checkout: no picker (3 dumps), pill EN x159-524 -> AR x839-1185; row ink EN name x132-322/fee x884-1057 -> AR name x1021-1211/fee x297-437.
- Regression: fee breakdown / cash / per-store fee rows render; no [ERR]/overflow in app logs. Pre-existing: first listed slot sent as ASAP (bug-first-listed-slot-placed-as-asap.*).
- Backstop: flutter test test/features/checkout/ -> 633/633 passed.
