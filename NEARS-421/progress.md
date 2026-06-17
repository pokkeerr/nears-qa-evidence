# NEARS-421 QA progress (live, checkpointed)
device: emulator-5554 (Android 17 / API 37), branch feat/NEARS-421-closed-store-schedule @95d8d74e
GPS: Abu Dhabi 24.40,54.45 (zone 2)
backend: http://10.0.2.2:8000 (local)
analyze: 5 changed files, 0 issues
backstop test: 21/21 GREEN

## AC1 (Branch A item DETAIL) — PASS
- Banner: "Store closed · opens at 00:00 · your order will be scheduled for later" (schedule, warning-toned sunken card)
- CTA: "Schedule Order  |  د.إ. 10" ENABLED, price suffix kept
- Tapped Schedule Order -> add-to-cart flow -> "Item added to cart" -> Store-9 cart now active
- shot: 01-branchA-detail-schedule-banner.png
- no flutter/runtime errors
## AC4 opening-time format — PASS (detail): shows "00:00" = HH:MM (not 00:00:00)

## AC1 (Branch A item BOTTOM SHEET) — PASS
- Reached via cart-item edit (grocery module routes tiles to detail; bottom sheet is the cart-edit/food path; same widget tree). "Scrim"+"Total Amount" confirm it's the modal sheet.
- Banner: "Store closed · opens at 00:00 · your order will be scheduled for later" (schedule)
- CTA: "Schedule Order" ENABLED (CustomButton)
- shot: 02-branchA-bottomsheet-schedule-banner.png
- NOTE: grocery-module store tiles route to item_details (not bottom sheet) by design (item_controller.navigateToItemPage L819 — bottom sheet only for food/showRestaurantText). Bottom sheet exercised via cart edit. Same banner+CTA logic.

## AC2 (Branch A checkout time-slot required) — PASS
- Proceed to Checkout with Store-9 cart -> checkout shows "Preference Time" section + "Store is closed" placeholder (no slot chosen)
- Tapped picker -> modal time-slot sheet (Today/Tomorrow tabs + Schedule btn). active=0 store -> no bookable slot ("Store is closed" both tabs)
- Tapped Place Order -> BLOCKED, stayed on checkout, NO order placed, no confirmation screen. Source gate checkout_controller L1205-1218: closed-slot/empty-slots -> snackbar "store_is_closed"/"select_a_time", returns. scheduleOrder=true path = "select_a_time".
- STOPPED before placing any order (DB-safety honored).
- shots: 03-checkout-preference-time, 04-timeslot-picker, 05-placeorder-blocked
- no runtime errors

## AC3 (Branch B Store 8 item DETAIL) — PASS
- Item "Tomatoes" / Abu Dhabi Fresh Market (Store 8)
- Banner: "Store closed · opens at 08:00 · advance ordering unavailable" (blocked, error-toned)
- CTA: "Store is closed" -- a11y node enabled=false, clickable=false (DISABLED, non-tappable). NO price suffix.
- Tapped disabled CTA -> nothing happened (no add-to-cart, no dialog). Confirmed non-interactive.
- shot: 06-branchB-detail-blocked-banner.png
## AC3 bottom sheet (Branch B): NOT live-reachable in grocery module (tiles route to detail; bottom sheet path is cart-edit, but a blocked item can't be added to cart). Same blockClosed CTA logic shared (item_bottom_sheet.dart L499-505) + covered by widget test "blocked variant shows cant-order copy". Verified by code + test, not separately live.
## AC4 format — PASS (Branch B): "08:00" real opening time = HH:MM (not 08:00:00). Strong confirmation.

## AC5 (OOS precedence) — UNVERIFIABLE LIVE (verified by code + test)
- No item in stores 8/9 has stock<=0 (min stock=31, DB SELECT). DB-safety rule forbids forcing stock=0 to fabricate OOS.
- Source confirms precedence: item_details L132-133 `isOos = stockEnabled && stock<=0; showClosedNotice = storeClosed && !isOos`; CTA L395 OOS label first. bottom_sheet L169-173 same.
- Widget test "OOS takes precedence over the closed/schedule treatment" -> GREEN.
- Marked unverifiable(live) not FAIL: logic + automated test confirm it; only the live fixture is missing.

## AC6 (Dark mode) — PASS
- Dark toggled ON. Branch B Tomatoes detail: blocked banner on dark navy sunken NearsSurfaceCard, light onSurface text fully legible, error icon visible. "Store is closed" CTA disabled (muted). "08:00" legible.
- shots: 07-dark-settings.png, 08-branchB-detail-DARK.png

## AC7 (RTL/Arabic + LTR clock) — PASS
- Switched to Arabic. Branch B Tomatoes detail: RTL layout mirrored. Banner Arabic copy "المتجر مغلق · يفتح في 08:00 · الطلب المسبق غير متاح".
- Clock "08:00" renders LEFT-TO-RIGHT (digits in order 0-8-:-0-0, NOT reversed) inside the RTL sentence -> bidi LRE/PDF fix confirmed. CTA "المتجر مغلق" disabled.
- shot: 09-branchB-detail-ARABIC-rtl-clock.png

## State restore — DONE: English + light mode restored (shot 10-restored-en-light-settings.png; dark toggle OFF, EN).

## AC8 (open-store regression) — PASS
- Veggie Market (Store 18, active=1, open) item "Tomato Sauce": NO closed banner, CTA "Add To Cart | د.إ. 7" enabled, In Stock.
- Tapped Add To Cart -> add-to-cart flow fired (cross-store reset dialog) = CTA interactive & normal. No false-block.
- shot: 11-openstore-no-banner.png

## AC9 (deep-link fail-open) — UNVERIFIABLE LIVE (verified by code + test)
- The "store not loaded" null-store_details state is a transient race not feasibly reproducible on a real device (item-details always fetches full payload incl. store_details regardless of entry path; deep-link host in manifest is the demo 6ammart-web host, separate concern).
- Source guard store_open_status.dart L28-29: `if (storeDetails == null) return false` (fail-open). Backend 403 at place-order is the hard backstop.
- Widget tests "deep-link / null store_details -> fail-open (not closed)" + "CTA matrix deep-link -> fail-open (enabled, no notice)" -> GREEN.
- Marked unverifiable(live) not FAIL.
## PRE-EXISTING (regression note): AndroidManifest deep-link host still 6ammart-web.6amtech.com (demo). Not in NEARS-421 scope; runtime baseUrl correct (local). Pre-existing.
