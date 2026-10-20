# NEARS-4275 slider spike (Maestro 2.11.0, emulator-5584 Pixel_10_Pro_2, VendorApp debug BASE_URL=http://10.0.2.2:8275, clone multi_food_db_qa4275_1020a), 2026-10-20 ~13:17-13:20 +04
Order 91417 (V-prepare, confirmed) open in Order Details; label node 'Swipe to Process' b=[481,2811][863,2880]; its a11y parent is the whole screen [0,0][1344,2920] (the slider is not its own node).
1. swipe from {containsChild: {text: Swipe to Process}, point: "3%, 50%"} direction RIGHT -> COMPLETED, but the containing node is the screen, so 3% = x~40 = the left-edge back gesture: the app went BACK to the order list; DB still confirmed (processing NULL). INVALID form.
2. swipe from {text: Swipe to Process} direction RIGHT (default duration 400 ms) -> COMPLETED, no transition (DB confirmed). The drag from the label centre covers ~half the Dismissible width (threshold 0.5) at sub-fling speed.
3. swipe from {text: Swipe to Process} direction RIGHT duration 150 -> COMPLETED, DB 91417 order_status=processing processing=2026-10-20 13:19:57; screen header 'Order #91417\nOrder is  Processing'. PASS: element-relative (anchored on the label element), no screen coordinate.

# Green loop (6 build), clone multi_food_db_qa4275_1020a, backend :8275, emulator-5584, wrapper scripts/qa-maestro-run.sh unchanged
Fixture 91446-91451 (ops-fixture.sh), then:
- VendorApp control: FAIL (a flow failed), log CLEAN; failed at the marked wrong assertion -> docs/qa-evidence/NEARS-4275/maestro/20261020-135659-98832
- VendorApp ops/ (3 flows): PASS, log CLEAN (3 x withdraw-method 403 known-noise) -> docs/qa-evidence/NEARS-4275/maestro/20261020-135825-3219
- DeliveryApp control: FAIL (a flow failed), log CLEAN; failed at the marked wrong assertion -> docs/qa-evidence/NEARS-4275/maestro/20261020-140133-26991
- DeliveryApp ops/ (3 flows): PASS, log CLEAN (9 GlobalKey known-noise) -> docs/qa-evidence/NEARS-4275/maestro/20261020-140231-31230
Clone after: 91446 confirmed, 91447 processing, 91448 handover, 91449 handover dm 23, 91450 picked_up dm 23, 91451 delivered/paid.
Earlier rounds that shaped the flows: vendor 03 failed on the low-stock sheet race (20261020-134959-62649); rider 02 failed on the pop-back screen (20261020-134040-10374); both GlobalKey runs DIRTY before the cited entries (20261020-134040-10374, 20261020-134505-28169).
