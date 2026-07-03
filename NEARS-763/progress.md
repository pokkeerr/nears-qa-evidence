# NEARS-763 QA progress

Device: emulator-5558
Started: 2026-07-03T07:33:33Z


## AC1 (empty categoryIds → no crash) — TEST-SUBSTANTIATED
- Post-fix: `flutter test .../product_with_categories_view_bounds_test.dart` AC1 PASS.
- Revert guards → AC1 FAIL with `RangeError (length): Invalid value: Valid value range is empty: 0` (exact empty-list read). Restored → PASS.

## AC2 (stale selectedCategory clamp) — TEST-SUBSTANTIATED
- Post-fix: AC2 PASS.
- Revert guards → AC2 FAIL with `RangeError (length): Only valid value is 0: 2` (stale index 2 vs shrunk list). Restored → PASS.
- Source tree restored to pristine (git status clean).

## AC3 (normal render + filter) — LIVE (emulator-5558, zone 1 pharmacy)
- Switched delivery location to zone 1 (Mirpur, Dhaka) via map picker; pharmacy home loaded basic-medicine rail.
- Rail "الطب الأساسي قريب" (Basic Medicine Nearby) renders 3 products: Paracetamol 500mg, Ibuprofen 400mg, Cold & Flu Relief.
- Filter chips (rail-local): all → 3 products; Pain Relief → Paracetamol+Ibuprofen; Cold & Flu → Cold & Flu Relief; back to all → 3 products.
- ui_errors clean at every step. No RangeError, no red screen.
- NOTE: shop variant (fromShop:true, "best reviewed products") NOT live-reachable — no ecommerce module seeded; shares identical build()/guard, covered by tests + code-path identity.
