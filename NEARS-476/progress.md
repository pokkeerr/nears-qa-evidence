# NEARS-476 QA progress (live checkpoint)
Device: emulator-5556 | branch feat/NEARS-476-remove-parcel-userapp | base c8081d81
Build under test: UserApp reskin, Option A (parcel creation removed, order-flow rendering KEPT)

## AC verdicts (appended as observed)

- AC1 (zone 2 / Abu Dhabi [400,2]): PASS — grid shows Grocery&Food, Food&Restaurant, Pharmacy; NO Parcel tile. API serves parcel module id5 (0 stores) but filter drops it. sectors_shown count=3. logs clean. shot: ac1-ac4-home-grid-zone2-abudhabi.png
- AC4 (zone 2): PASS — 3-row vertical list reflows clean, no gap/empty slot/broken row. shot same.
- AC1 (zone 1 / Demo Dhaka): PASS — grid 3 modules, no Parcel, sectors_shown count=3 zone_id=1, errors clean. shot: ac1-home-grid-zone1-demo.png
- AC2/AC5: PASS — zero callers/string-refs of deleted routes/screens/widgets (code); routes removed from getPages; remaining parcel refs are KEPT order-flow only. Live deep-link to removed /parcel-category delivered to app -> NO crash, stays on home, no parcel screen, no RouteNotFound. shot: (log-based)
- AC3 (historical parcel orders): PASS — #153 Documents(cancelled,zone1) + #154 Small Packages(delivered,zone2) render in history list (Parcel badge, category name, status pill, Delivery ID, fee, View-details-only) AND in order-details (Order Type:Parcel, Parcel Category, Sender/Receiver Details, Charge Pay By, Order Summary, Delivery Fee/Total Amount calc widget). errors clean. shots: ac3-orders-list-with-parcels.png, ac3-parcel-153-details-cancelled.png, ac3-parcel-154-details-delivered.png
- AC3 (normal orders): PASS — #158 grocery details + tracking (Order Tracking timeline, Google Map, Estimated arrival) render clean. List shows #160/#159 normal orders too. Note: no ONGOING parcel order seeded, so parcel order_tracking_screen not live-reachable; code KEPT/untouched, normal-order tracking renders fine, parcel details+calc render fine.
- REGRESSION pickMap map-pick (retained guard): PASS — "Set From Map" opens real PickMapScreen (Google Map + geocode + zone check), NOT NotFound, no crash. pickMap route (route_helper:676 page=='parcel' guard) untouched by diff. The get-zone-id 404 "[FAIL]" is the API's by-design out-of-zone response (404 confirmed via curl), correctly logged w/ correlation_id + user message -> contract-compliant, NOT silent-failure, NOT a regression (location feature untouched). shot: regression-pickmap-renders.png
- REGRESSION RTL/Arabic: PASS — home grid 3 mirrored cards, no Parcel, clean reflow; promo banner = store-promo (not parcel); cold-load in Arabic clean. shot: regression-rtl-arabic-home-grid.png
- REGRESSION offline-payment forParcel: code untouched (only deleted parcel creation widget parcel_payment_method_bottom_sheet.dart); normal-order path unaffected.
- REGRESSION single-module zone: N/A — zones 1/2 keep 3 active-store modules after parcel removal; not newly single-module.
- SMOKE core path: enter Grocery module -> "Good evening" + categories + search render clean.
- AUTOMATED: flutter analyze = 6 info lints (pre-existing, unrelated), 0 errors/warnings. flutter test = 1521/1521 PASS.
- VERDICT: PASS. No task_bugs, no regression_bugs.
