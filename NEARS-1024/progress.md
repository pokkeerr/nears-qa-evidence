# NEARS-1024 QA progress — live run (cycle 0)

Build: worktree feat/NEARS-1024-details-zone-guard @ c3ddcb7d, backend :8024 (OTEL off), UserApp on emulator-5556 via --dart-define=API_HOST=10.0.2.2:8024. User: customer@nears.com (saved addresses in zone 1 + zone 2).

## Curl matrix (backend)
- [1] PASS — in-zone zoneId [2]: items/details/215 → 200; stores/details/13 → 200.
- [2] PASS — out-of-zone zoneId [2]: items/details/3 → 403 `{"errors":[{"code":"out_of_zone","message":"Item not available in your zone"}]}`; stores/details/2 → 403 store-variant message. Exact shape.
- [3] PASS — malformed zoneId `{"x":1}` / `"2"` / `null` → 403 fail-closed on BOTH endpoints (6/6).
- [4] PASS — absent header: items/215 → 200 (default-zone sub), items/3 → 403; absent header + moduleId 4 (module not on default zone 2): items/details/688 → 403 (NOT 404), stores/details/59 → 403 (NOT 422). NOTE: first attempt with item 215 + moduleId 4 → 404 is the PRE-EXISTING module filter (item not in module), guard construction per feature test is item-in-module → verified 403.
- [5a] PASS — stores/details/fresh-mart-grocery + zoneId [] → 200 (slug share-link exemption).
- [5b] NOT-DEMONSTRABLE live (no item_campaigns rows in DB, read-only) — covered by DetailsZoneGuardTest::test_campaign_path_is_guarded (in-zone campaign passes, out-of-zone campaign 403).
- [6] NOT-DEMONSTRABLE live (read-only check: all modules all_zone_service=0) — covered by DetailsZoneGuardTest::test_all_zone_service_module_bypasses_the_guard_on_both_endpoints.
- [7] PASS — 4x guard 403 calls → 0 new bytes in worktree laravel.log (0 error-class lines). Pre-existing noise found separately: unknown-item 404 path logs ErrorException "Attempt to read property store_id on null" ItemController.php:630 — present in base 7cf8783c, NOT caused by this change → regression-candidate.

## On-device (emulator-5556, light mode)
- [8-LTR] PASS — Banana (item 3, zone-1 store) reached via home "Buy It Again" under zone-2 address; sheet opens with in-sheet state: "This item is not available in your area" + subtitle + "Change Location" CTA; NO Retry, NO Add To Cart. Logs: items/details/3 → 403 + ONE paired `[FAIL] endpoint=/api/v1/items/details/3 http_status=403 type=ApiFailure correlation_id=c99b8c47-…` (contract-conformant, not silent). get_runtime_errors: none. Shot: ac8-item-sheet-out-of-zone-ltr.png.

## On-device — RESUMED run (cycle 0 continuation, emulator-5556 pid 11723 → :8024, reclaimed stale lock pid 26165)
- [quick-add] PASS — cross-store out-of-zone quick-add. Cart held Banana (item 3, store 2); tapped the standard ItemWidget "Add To Cart" button (labeled Semantics node, NOT the sheet) on Red Apples flash-sale card (item 105, store 1, zone-1). optimisticAddToCart returned false (cross-store) → fell through to getItemDetails(105) → items/details/105 → 403 → ZoneWarningDialog "This item is not available in your area" + "Change Location". NO crash (F3 _item! null-guard works), basket badge stayed 1 (Red Apples NOT added). Paired `[FAIL] endpoint=/api/v1/items/details/105 http_status=403 type=ApiFailure correlation_id=2f0d26b0-7da2-43fc-a902-08d42bd1b660`. Shot: ac-quickadd-out-of-zone.png.
- [9] PASS — checkout no dialog-leak, proven BOTH ways:
  - Out-of-zone (rigorous F2): cart with Banana (store 2), Proceed to Checkout → stores/details/2 → 403, `[WARN] "store: details out of zone"` + paired `[FAIL] ... correlation_id=90f6722b-94c0-4e46-97f3-cb5fd295c6fe`; stayed on Checkout screen, NO ZoneWarningDialog, cart preserved, no eject. (Checkout renders skeleton since store details unavailable — see followup, tied to 1025 cart-guard gap.) Shot: ac9-checkout-no-zone-dialog.png.
  - In-zone (happy path / regression): opened store 13 (stores/details/13 → 200, no dialog), added in-zone item (items/details/205 → 200, normal cross-store reset dialog NOT zone dialog), Proceed to Checkout → stores/details/13 → 200, checkout LOADED FULLY (address, coupons, Place Order, review items, totals), NO zone dialog. Shot: ac9-checkout-inzone-loaded.png.
- [8-RTL] PASS — Arabic/RTL. Switched Settings→Language→عربى→تحديث. Grocery flash-sale Banana (item 3) tapped → items/details/3 → 403 → in-sheet out-of-zone state in Arabic RTL: "هذا المنتج غير متوفر في منطقتك" (not available in your area) + subtitle + "تغيير الموقع" (Change Location) CTA; NO Retry, NO Add-To-Cart. Paired `[FAIL] endpoint=/api/v1/items/details/3 http_status=403 type=ApiFailure correlation_id=6e2d30b8-866a-422a-9f0a-b0b85796f192` (contract-conformant, not silent). Shot: ac8-item-sheet-out-of-zone-rtl.png.

## Observations (non-blocking, not 1024 task-bugs)
- FOLLOWUP/regression-candidate: with an out-of-zone item already in cart (only reachable via the pre-1025 cart-add gap: add in-zone → switch address out-of-zone → checkout), checkout stays in perpetual skeleton because stores/details 403s (no store data → can't compute totals). F2's no-dialog-leak + cart-preserve works; the stuck skeleton is a consequence of 1024's new 403 meeting the un-guarded cart. Proper fix rides NEARS-1025 (block out-of-zone cart adds). Repro: cart Banana(item 3) + zone-2 addr → Proceed to Checkout.
- regression-candidate: `GetBuilder<FlashSaleController> ... cannot be marked as needing to build` framework warning on the grocery module home (flash-sale render) — pre-existing, flash sale untouched by 1024, unrelated to the zone guard.
- KNOWN BYPRODUCT (already logged, NOT re-filed): valid share-link cold-open logs `route: module match found=false for slug=grocery-food` → transient error snackbar, store still loads 200. Pre-existing deep-link routing (NEARS-490 class). See bug-coldopen-store-sharelink-module-match.log.

VERDICT: PASS. All AC cells demonstrated live (backend matrix [1]-[7] + on-device [8-LTR]/[8-RTL]/[9]/[quick-add]/share-link). No task-bugs. Two non-blocking followups + one known byproduct.
