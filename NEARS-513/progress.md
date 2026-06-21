# NEARS-513 QA progress — checkpoint log
Device: emulator-5556 | Build: feat/NEARS-513-checkout-address-zone | Backend: 127.0.0.1:8000 / multi_food_db
Light mode only (dark deferred).

## Pre-flight
- baseUrl -> http://10.0.2.2:8000 (Android local backend) OK
- Backend serving: api/v1/config 200 OK
- Demo data verified: user6 addr45=zone2, addr46=zone1; user1(james) 0 addr; store1=zone1, store12=zone2

## AC verdicts (appended as observed)

- AC-1 PASS: customer@nears.com checkout (store1/Nears Mart zone1) shows saved address "Demo Zone — Dhaka" (addr46) by default, no forced re-pick. ac1-checkout-saved-address-instore1.png
- AC-4 setup PASS (in-zone store1+addr46): NO out-of-zone notice, Place Order present+enabled, no runtime errors.

- AC-3 PASS (logged-in saved-address): store1(zone1)+addr45(zone2) -> inline notice "This address is outside the store's delivery zone." shown, Place Order DISABLED (faded ~50%), tap = no-op, order count stayed 41 (no order). ac3-out-of-zone-notice-store1-addr45.png
- AC-3 re-enable PASS: switch back to addr46(zone1) -> notice CLEARS, button solid/enabled. ac3-notice-cleared-back-inzone.png
- AC-4 zone-aspect PASS: in-zone store1+addr46 -> NO notice, button enabled, flow passes isOutOfZone guard (reaches downstream COD-limit validation). NOTE: store1 has contradictory config (min_order=20 AED vs max-COD=10 AED) blocking a real COD placement -> pre-existing, unrelated to zone fix. Will demo clean placement via store12.

- AC-4 PASS (in-zone places): store12(zone2)+addr45(zone2) cross-check ALLOWED -> NO notice, order #160 created (store_id=12, 17 AED, pending), push "order 160 successfully placed". ac4-order160-placed-store12-inzone.png

- AC-3 cross-check PASS: store12(zone2)+addr46(zone1) -> notice shown, Place Order disabled (symmetric zone check). ac3-crosscheck-store12-addr46-blocked.png

- AC-2 PASS: james.wilson@demo.com (0 saved addresses in DB) -> checkout Delivery Address shows inline entry form (Name / Contact Person Number / Address field + View more details), NO saved-address thumb strip, no blank gap. ac2-james-no-saved-inline-form.png
- AC-2 regression PASS: user WITH saved address (customer@nears.com, AC-1) still sees their saved address on checkout.
- OBSERVATION (pre-existing, non-zone): james's inline form Name/Phone pre-filled "Customer Nears / 565811199" (prior session carry-over) rather than James's own profile. Not a zone-fix defect; logged as followup.

- AC-3 GUEST path: NOT live-demonstrable in this env. business_settings.guest_checkout_status=0 (guest checkout disabled platform-wide; "Nears login-only" per NEARS-528). Guest checkout shows "Please login to continue" before any delivery-address entry. Map-picker+TypeAhead zoneId-stamping code IS present (guest_delivery_address.dart both desktop showGeneralDialog + mobile Get.bottomSheet onPicked paths) and unit-tested (checkout_zone_guard_test "isOutOfZone — guest (guestAddress)" group). Logged-in path (same selectedDeliveryAddress/isOutOfZone predicate) demonstrated live both zone directions. ac3-guest-checkout-disabled-login-required.png
- AC-3 take_away exemption: order-type toggle not surfaced in this reskin checkout/cart/store UI (delivery-only checkout per NEARS-512). Exemption verified by code (isOutOfZone returns false for take_away + widget guard !takeAway && isOutOfZone) + passing unit test "take_away with an out-of-zone address is NOT blocked".
- AC-5 page-split: no UI (no duplicate Checkout/Place-Order screen) — n/a, confirmed single checkout screen throughout.

- AC-3 server 403 defense: verified by code (PlaceNewOrder.php zoneAndStoreValidationCheck -> match(!$zone => status_code 403, code 'zone', message out_of_coverage_area); zone resolved via Zone::where(id,store.zone_id)->whereContains('coordinates', Point(lat,lng)) line 768). Live synthetic call returned 500 (my minimal body missing fields -> modules() on null at line 168, BEFORE the zone net; no order created). Client guard already blocks reaching this endpoint with an out-of-zone address (demonstrated live). No backend change in this ticket.

- AC-3 RTL/Arabic PASS: store1(zone1)+addr45(zone2), AR locale -> notice "هذا العنوان خارج نطاق توصيل المتجر." renders right-aligned, warning icon mirrored to RIGHT (start), NO overflow (ui_errors clean), full checkout mirrored, Place Order ("وضع النظام") disabled. ac3-rtl-arabic-out-of-zone-notice.png
- AC-3 loading/no-flash PASS: notice did NOT flash before zone resolved on address selection — appeared only after the selected address's zone was determined (insertAddresses notify:true + reactive GetBuilder).

## Regression sweep (bounded)
- In-zone checkout end-to-end PASS: order #160 placed successfully (store12+addr45 in-zone).
- Address book PASS: My Address shows "2 delivery spots" both saved addresses intact, Add New Address works. Unaffected.
- Address selection sheets PASS: Edit-address / Change-Location selection sheets worked throughout (logged-in customer + checkout).
- No red-screens / RenderFlex overflows / exceptions across the whole run (ui_errors clean on home/checkout/My Address; flutter log clean of FlutterError).
- AC-2 inline form PASS for james; AC-1 saved address PASS for customer.
