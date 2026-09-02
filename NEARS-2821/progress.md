# NEARS-2821 QA-lite [m4] progress

- AC1 [api] GET order/details?order_id=91174 -> HTTP 200, item_details=[], no [FAIL]/array-offset in laravel.log for correlation. PASS.
- AC3 [api] GET order/details?order_id=1 (control, same customer) -> HTTP 200, item_details.id=52 populated as before. PASS. No log finding.
- AC2 [ui] UserApp Order History -> order #91174 details screen: no HTTP 500, no red-screen, but an UNCAUGHT client-side TypeError fires
  (logged, paired AppLogger [FAIL]): `type 'List<dynamic>' is not a subtype of type 'Map<String, dynamic>'` at
  order_details_model.dart:55 (`OrderDetailsModel.fromJson`). Root cause: backend fix's `?? []` fallback serializes to JSON `[]`
  (array) when item_details was null, but the client's guard is `json['item_details'] != null ? Item.fromJson(...) : null` —
  a non-null empty ARRAY now reaches `Item.fromJson` which expects a Map, throwing. Screen renders only the status banner,
  item rows never build. FAIL for AC2 (breaks_ac: true). Evidence: ac2-order91174-details.png, bug-item-details-list-not-map-typeerror.log
