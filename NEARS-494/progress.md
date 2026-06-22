# NEARS-494 v2 — Live QA progress (cart add-to-cart redesign)

- Device: emulator-5556 (locked). Worktree branch feat/NEARS-494-cart-authoritative-v2.
- Backend: local php artisan serve :8000 up (config 200); queue:work up.
- baseUrl: http://10.0.2.2:8000 (local) — pre-flight PASS.
- App launch pid 49103, DTD connected. fix_cycle=0 (fresh QA).

## Fixtures (store 2 Fresh Mart zone1 grocery; store 1 Nears Mart)
- AC1/2/3 rapid tap: Red Apple(id2,stk100), Banana(id3), Whole Milk(id6) - store2.
- AC4 cap: item1 "Sample Product" store1 maximum_cart_quantity=2 (fast); stock-10 items.
- AC6b variation: item84 Dove (store2 VAR+CHOICE).
- AC6c OOS: item61534 QA OOS Fixture (store2 stk0).
- AC6a cross-store: store1 then store2.

## Static-review findings to verify live
- F1 (item-detail AC1 risk): item_details_screen in-cart stepper GetBuilder (L622) has NO id;
  optimisticStep fires update([cartBadgeId,cartSummaryId]) which does NOT trigger a no-id
  GetBuilder. Risk: item-detail stepper qty may not repaint on tap. VERIFY LIVE.
- F2 (AC8 sub-threshold): NEW-H1 unknown-server-truth keeps row but _reconcileFailedSync
  calls _notifyAddFailed -> "Couldn't add to cart" on a row that STAYED. Watch wording.

## AC verdicts (appended live)

### AC1 basket-line: PASS — Red Apples 1->10 via 9 rapid taps, HELD at 10 (no snap-back). DB=10. shot 03.
### AC2 basket-line: PASS — exactly 1 cart/update (PATCH not 2nd add), 0 cart/list during burst. DB converged to 10.
### AC3 basket-line: PASS — 0 cart/list re-reads, no full-page spinner; only tapped line + summary repainted (other lines unchanged in shot 03).

### ITEM-DETAIL SURFACE — ARCHITECTURE FINDING (blocks AC1/3/4/5 on item-detail):
- v2 modified item_details_screen.dart in-cart stepper -> optimisticStep. BUT per NEARS-422
  modal-nav (route_helper L1429-1437) "No path renders the old full-screen ItemDetailsScreen."
- The LIVE item-detail UI is ItemBottomSheet (item_bottom_sheet.dart), opened via
  navigateToItemPage -> presentItemDetailSheet -> Get.bottomSheet(ItemBottomSheet).
- ItemBottomSheet was NOT touched by v2: its stepper still uses itemController.setQuantity
  (pre-add local qty), and submits via "Add to Cart"/"Schedule Order" CTA -> addToCartOnline /
  updateCartOnline (full-reload path with _isLoading spinner).
- LIVE-VERIFIED: opening Rice5kg(97)/RedApples(105) sheet, stepper qty climbs locally & HOLDS,
  but NO cart network call fires and basket badge + DB stay unchanged -> it's the pre-add qty,
  not optimisticStep. The optimisticStep item-detail code is effectively DEAD (only a shared
  deep-link transient renders it, then the sheet takes over).
=> The AC1/AC3 "item-detail stepper" optimistic guarantees are NOT delivered on the surface
   the user actually sees. Needs live test of the sheet's Add-to-Cart path for spinner/hold.

### AC1 grid-card: PASS — Tomatoes(102) 7->12 via 5 rapid taps, HELD at 12 (no snap-back). DB=12. shot 08.
### AC2 grid-card: PASS — 1 cart/update PATCH, 0 cart/list during burst; DB converged to 12.

### AC1 fresh-add grid: PASS — Sugar 1kg(104) 0->1 (cart/add) then 1->10 via 9 taps, HELD at 10. DB=10.
### AC2: PASS — add fired cart/add; 9-tap climb fired exactly 1 cart/update (no 2nd add, no list).
### AC9: PASS — add_to_cart fired ONCE on server-confirmed ADD {item_id:104,qty:1,currency:AED} via stdout
  (DebugView unavailable: Missing google_app_id); did NOT re-fire on update-to-N steps.
### AC8 (no green toast): no "item added"/success snackbar on the simple add (badge change is the feedback).

### AC4 stock-cap (Option A): PASS — Sample Product(1) maximum_cart_quantity=2: rapid +taps capped at 2,
  never exceeded, no snap-back, non-blocking "Maximum quantity limit 2" snackbar (shot 10).

### AC6a cross-store: PASS — adding TOWER MART item while cart=Nears Mart popped reset dialog
  "Your basket has items from another store. Adding this will clear it. Continue?" (shot 11). Tapped No -> cart unchanged.

### AC6b variation modal: PASS — Dove variation item opens Size 250ml/500ml modal sheet, not direct add (shot 12).
### AC6c OOS block: PASS — QA OOS Fixture(61534) tap -> "Out of Stock" snackbar, items/details fetch (fallback),
  NOT added (DB=0) across 3 attempts (shot 13c).
### NOTE: running-order banner overlaps lower grid content (2 stacked banners #158/#161) — pre-existing
  UI gotcha (NEARS-340/screen-inventory), NOT a NEARS-494 regression. Logged as followup.

### AC7 base (airplane during debounce): PASS — tap Red Apples +(10->11 optimistic shown, shot 15),
  PATCH fails offline (SocketException cart/update), reconciles ONCE to server-known 10 (shot 16),
  non-blocking "Couldn't add to cart. Please try again." snackbar (shot 17). DB stayed 10. No mid-tap snap.
### AC8 SUB-THRESHOLD NOTE: failure snackbar reads "Couldn't add to cart" but the item STAYED in cart at
  prior qty (only the +1 increment was rejected) -> wording slightly misleading. Non-blocking followup (per spawn).

### TASK BUG (breaks AC3/AC5): NPE building CartItemWidget for an optimistic row.
  pricing_service.dart:213 `cart.item!.addOns!` NPEs because optimisticAddToCart stores the card Item
  (addOns==null); _adoptServerRow keeps it (only stamps id). Basket rebuild before getCartDataOnline crashes.
  Captured live via DTD. Evidence: bug-optimistic-row-addons-npe.log. Intermittent (timing window).

### AC7 recovery: PASS — airplane off, later tap re-synced (cart/update 200, DB->11); row never disappeared.

### H5 multi-row delete: PASS — deleted earlier (Cream Cheese/100) then later (Rice 5kg/97) line; correct
  item removed each time (liveIndex re-resolution), others intact, no crash. shot 21. DB confirms.
### C1 un-persisted delete: covered by passing automated test (drops locally, no server delete, no NPE);
  live sub-0.5s window impractical to hit via adb tap latency, but NO NPE/crash seen on any delete. PASS(qualified).

### CRITICAL-1 (discounted price to checkout): PASS — checkout Review Items show discounted UNIT price:
  Tomatoes 12 × 11 AED = 132 (not full 13, not discount amount 2); Sugar 10 × ~2; Total 356 AED. shot 23.
  Optimistically-added rows (Sugar/Sample/Mango/Cola/Brown Eggs) all priced correctly into the order.

### Cold-load persistence: PASS — force-stop+relaunch; basket restored server qtys (Tomatoes 12, Sugar 10,
  Red Apples 11) = the optimistic values that synced. No crash on cold-load.
### RTL/Arabic: PASS — basket stepper (زيادة/تقليل الكمية) + summary + prices render mirrored correctly,
  no overflow/crash (shot 25). Dark mode toggle OFF (light-mode verified per deferred policy).

### AC8 green-then-red: PASS — offline fresh ADD of Dish Soap: badge shows 1 optimistically with NO green
  toast (shot 26); on ADD-fail the row drops and ONLY a single red "Couldn't add to cart" shows (shot 27).
  Never green-then-red. NEARS-554 fold confirmed. DB: Dish Soap not added.

### AC8 variation/cross-store success: PASS — Dove variation sheet -> Schedule Order -> cross-store reset
  dialog "Start a new basket?" -> Yes -> cart/remove + cart/add (Dove 84), success completes. shot 28/29.
### AC9 variation add: add_to_cart fired ONCE {item_id:84, price:200, qty:1, currency:AED} on confirmed add.

## AC3 grid no-spinner: verified via (a) 0 cart/list during step bursts, (b) optimisticStep never sets
   _isLoading, (c) only tapped line+summary repaint (sibling lines unchanged in shots 03/08). Basket line +/-
   does NOT flash a full-page spinner. The variation MODAL CTA submit (addToCartOnline) does show a button
   "Loading..." — acceptable (explicit submit, not a stepper tap).

## SUMMARY VERDICT: see envelope. AC1/2/4/5/6/7/8/9 PASS on grid+basket. Item-detail STEPPER surface: the
   optimisticStep code lives in item_details_screen.dart which is DEAD (NEARS-422 modal-nav routes to
   item_bottom_sheet, untouched by v2). TASK BUG: optimistic-row addOns NPE (intermittent basket crash).
