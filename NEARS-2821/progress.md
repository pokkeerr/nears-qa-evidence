# NEARS-2821 QA progress

## Cycle 2 (delta re-QA, express lane, sha 8fc67f220)

- AC1 [api] GET order/details?order_id=91174 (worktree backend, port 8001) -> HTTP 200. `item_details` now
  resolves as JSON `null` for BOTH rows (id 136, id 137) — confirmed the `?? []` fallback removal landed;
  no `[FAIL]`/array-offset lines appended to laravel.log for either request (file unchanged pre/post call).
  PASS.
- AC3 [api] GET order/details?order_id=1 (control, same customer) -> HTTP 200, `item_details.id=52` /
  `item_details.id=58` populated exactly as before, shape unchanged. No log finding. PASS.
- AC2 [ui] UserApp (emulator-5562, --dart-define=API_HOST=10.0.2.2:8001) Order History -> order #91174
  details screen: the ORIGINAL TypeError (order_details_model.dart:55, List-vs-Map) is gone — confirms the
  backend fix landed correctly. BUT the screen still crashes, now via a DIFFERENT unguarded null: order
  91174's rows also carry `add_ons: null` (pre-existing, not touched by this ticket's diff), and
  `OrderController.computeOrderFinancials` (order_controller.dart:763) does `orderDetails.addOns!` with no
  null guard inside the items-price loop. Before this fix, the screen ALWAYS crashed earlier at model-parse
  time, so this line was never reached for order #91174 — the item_details fix newly exposes it. Result:
  full red error screen ("Null check operator used on a null value"), not the sparse-but-alive render the
  fix-cycle packet expected. FAIL for AC2 (breaks_ac: true) — filed as task_bug, still blocks Done.
  Evidence: ac2-order91174-details-cycle2.png, bug-order-controller-addons-null-typeerror.log

## Cycle 1 (QA-lite [m4])

- AC1 [api] GET order/details?order_id=91174 -> HTTP 200, item_details=[], no [FAIL]/array-offset in laravel.log for correlation. PASS.
- AC3 [api] GET order/details?order_id=1 (control, same customer) -> HTTP 200, item_details.id=52 populated as before. PASS. No log finding.
- AC2 [ui] UserApp Order History -> order #91174 details screen: no HTTP 500, no red-screen, but an UNCAUGHT client-side TypeError fires
  (logged, paired AppLogger [FAIL]): `type 'List<dynamic>' is not a subtype of type 'Map<String, dynamic>'` at
  order_details_model.dart:55 (`OrderDetailsModel.fromJson`). Root cause: backend fix's `?? []` fallback serializes to JSON `[]`
  (array) when item_details was null, but the client's guard is `json['item_details'] != null ? Item.fromJson(...) : null` —
  a non-null empty ARRAY now reaches `Item.fromJson` which expects a Map, throwing. Screen renders only the status banner,
  item rows never build. FAIL for AC2 (breaks_ac: true). Evidence: ac2-order91174-details.png, bug-item-details-list-not-map-typeerror.log
