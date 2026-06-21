# NEARS-516 QA progress (checkpoint log)

Build: worktree feat/NEARS-516-checkout-map-eta-placement, device emulator-5554 (reclaimed stale NEARS-481 lock)
Backend: http://127.0.0.1:8000 (api/v1/config 200)

## AC verdicts (appended as observed)

- AC-9 (automated backstop): PASS — `flutter test test/features/checkout/ test/features/cart/` => 122/122 passed (incl. new delivery_eta_banner_test.dart: 7 cases).

- AC-3 (Basket mobile, no ETA pill): PASS — Basket for an item-cart shows NO 'arriving in' pill; cart item (Red Apple, qty stepper, price), Add More Items, Substitution Preferences (radios), Subtotal/Discount/Total, Proceed to Checkout all render cleanly. Evidence: basket-mobile-no-pill.png

## ENV NOTE (recovery)
- Initial session was logged in as a stale QA account; recovering required re-login as customer@nears.com. App reinstall via flutter run cleared prefs -> re-onboarded. adb `input text` raced the IME (jumbled email) -> recovered via precise field-tap + char-by-char + GPS fix to Abu Dhabi (24.4538833,54.3773433, zone 2). Active delivery loc = that GPS point (≈ saved address 45).

- AC-1 (<1km): PASS — Fresh local (store 12), CheckoutController.distance=0.957 km (<1.0) per `vehicle/extra_charge?distance=0.957` log. Checkout shows "Arriving in 2-3 hours" mint ETA pill with Review Items immediately below — NO ETA-banner map thumbnail, no empty gap. (The small "Google" map lower is the separate Delivery Address card preview, unrelated to DeliveryEtaBanner.) Evidence: checkout-under1km.png
- AC-4 (pill present, <1km band): PASS — "Arriving in 2-3 hours" pill present on Checkout.

- AC-2 (>=1km): PASS — Eco Market (store 19), CheckoutController.distance=11.051 km (>=1.0) per `vehicle/extra_charge?distance=11.051` log. Checkout shows "Arriving in 2-5 days" mint pill, then a full-width real GoogleMap thumbnail with delivery marker DIRECTLY BELOW the pill (bounds: pill y=417-465, banner map y=528-888 w/ 120px marker, Review Items y=933). ETA pill is ABOVE the map exactly as specified. Contrast with <1km (no map there) proves the gate. Evidence: checkout-over1km.png
- AC-4 (pill present, >=1km band): PASS — "Arriving in 2-5 days" pill present.
- AC-4 OVERALL: PASS — ETA pill present on Checkout in BOTH bands.

- AC-6 (take_away/pickup): VERIFIED-VIA-TEST+CODE — no Delivery/Pickup toggle is surfaced on the Nears checkout for these grocery stores (delivery-only UI path), so the pickup checkout render is not live-reachable with this seed/UI. Covered by DeliveryEtaBanner early-return `orderType=='take_away' -> SizedBox()` (whole banner absent, both bands) + passing widget test "take_away early-return wins regardless of showMap".

- AC-8 dark mode: PASS — Both bands tested in dark mode. >=1km (Eco Market, d=11.051): mint pill (navy text+bolt icon, NOT mint-on-mint) ABOVE dark-styled GoogleMap thumbnail. <1km (Fresh local, d=0.957): mint pill (navy text/icon), NO banner map (Review Items directly below). Evidence: checkout-dark-over1km.png, checkout-dark-under1km.png

- AC-8 RTL/Arabic: PASS — Checkout in Arabic (<1km pill-only path, Fresh local d=0.957). Mint ETA pill renders top-right (RTL), "يصل خلال 3-2 hours" with bolt icon on the TRAILING (left) side, NO overflow. Review Items (مراجعة العناصر) directly below pill — no banner map (gate works in RTL). Evidence: checkout-rtl-under1km.png

- AC-7 (regression / store screen): PASS w/ SPEC-DRIFT NOTE — NearsSpeedBanner class is byte-unchanged (empty diff). HOWEVER the AC premise "Store screen still shows NearsSpeedBanner" is INCORRECT: at base ec4263e7 the ONLY instantiation of NearsSpeedBanner was cart_screen.dart; store_screen.dart never imported/instantiated it (only a doc-comment mention). This change removed that sole usage, so NearsSpeedBanner is now instantiated by NO screen (orphaned but intact). NOT a regression — store screen behavior is unchanged. No new runtime errors/overflows across the whole session (only benign PhFlagUpdateRegistry/GoogleCertificates emulator warning + module-builder debug prints; zero RenderFlex/E-flutter/assertion).
- AC-2 no-coords fallback: VERIFIED-VIA-TEST — not live-reachable (all seeded addresses carry lat/lng; cannot persist a coordless address per QA boundary). Covered by `_buildMapPreview` hasCoords=false -> navy-grid Container path, exercised by the test "showMap:true ... null coords => navy-grid fallback (pin + 120dp box)" (find.byIcon(location_on_rounded) findsOneWidget).
