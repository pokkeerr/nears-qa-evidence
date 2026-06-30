# NEARS-662 + NEARS-663 QA progress (live)

Device: emulator-5554 | worktree feat/NEARS-662-oos-plus-card @ b30d15b4 | UserApp pid 14958
Backend: http://10.0.2.2:8000 (up). Login: customer@nears.com (login event fired). Zone 1 (Dhaka demo).

## Checkpoints
- Pre-flight: baseUrl=http://10.0.2.2:8000 (real local backend) OK. Backend up (302). Build booted from worktree.
- Onboarding cleared, logged in, GPS set to zone 1 (store 4/2 reachable).
- Item 17 Double Bacon Burger stock=0 store 4 (Burger Palace, Food, isShop=false). In-stock contrast item 16 Classic Cheeseburger stock=10.
- Store 2 Fresh Mart Grocery (module 1 grocery) OOS item 61534. NOTE: grocery still maps isShop=false (only ecommerce→true; no ecommerce module seeded).

## AC verdicts (live)
- AC1 (662) PASS: store 4 Recommended-For-You ItemCard rail — Double Bacon Burger (OOS) "+" is GREY/disabled; Classic Cheeseburger (in-stock) "+" is MINT. shot store-recommended.png / ac3-instock-added.png.
- AC2 (662) PASS: a11y tree shows only ONE "Add To Cart" semantics (in-stock card); OOS cards have NONE. Tapping grey "+" x3 → no add_to_cart event, no cart/add, no stepper, badge stayed 1; tap fell through to card onTap→item detail. logs clean.
- AC3 (662) PASS: in-stock mint "+" → 📊 add_to_cart {item_id:16, price:8.99} + cart/add [200] + badge 1→2 + stepper "− 1 +" expanded + persisted in cart. shot ac3-instock-added.png.
- AC5 (662) PASS: OOS item = Double Bacon Burger item 17 stock=0 on Recommended For You rail (exact named repro).
- AC4 (662) PASS: ItemWidget All Products grid (store 4) renders fine; Veggie Burger item 18 "+" → 📊 add_to_cart {item_id:18} + cart/add [200]; Double Bacon Burger shows active "− 1 +" stepper (module.stock gate off → ItemWidget keeps OOS items active = documented divergence). item_widget.dart NOT in diff. shot ac4-itemwidget-grid.png.
- AC7 (663) PASS: NearsIcon('add')→Symbols.add (Material Symbols font) in BOTH active(mint/textOnMint) + disabled(grey/textMuted) states, size 22; byte-identical to ItemWidget's _addControl NearsIcon('add',22). Old Icons.add_rounded/add_shopping_cart_rounded removed. Visual: store-recommended.png.
- NOTE isShop=true branch NOT live-reachable: isShop only true for moduleType==ecommerce; no ecommerce module seeded. Both branches share identical `outOfStock ? disabledAddCircle : CartCountView(...addCircle)`; covered by unit test + code parity. Grocery still maps isShop=false.

## Regression sweep
- Grocery store (Fresh Mart, store 2) Recommended ItemCard rail renders fine (in-stock mint "+"); OOS fixture 61534 NOT in any grocery ItemCard rail (only search-list + ItemWidget All-Products, both out of 662 scope, both correctly show active "+"). shot freshmart-store.png / search-sparkling.png.
- Card-level tap (not the "+") on OOS Double Bacon Burger ItemCard → opened item detail (card onTap unchanged, not in diff). PASS.
- ItemWidget grids unaffected (AC4). PASS.
- RTL/Arabic PASS: Burger Palace recommended ItemCard rail in Arabic — OOS overlay "إنتهى من المخزن" present, OOS grey "+" pinned bottom-END (→ bottom-LEFT in RTL), in-stock mint stepper bottom-END, rail order mirrored, no overlap/clipping, ui_errors clean. shot rtl-store-recommended2.png / rtl-itemcards.png.
- In-stock add persisted across navigation (cart-contents.png shows 2 line items).

## Logs / automated
- Whole-session log scan: 0 [FAIL]/[ERR], no exceptions/overflows/red-screens, no non-200 API. Firebase native disabled (no google_app_id) — analytics observed via 📊 debug-mirror lines (valid path).
- flutter test test/common/widgets/ → All 143 passed (exit 0); both NEARS-662 cases pass: "out-of-stock + exposes no add-to-cart control", "in-stock + keeps the active add-to-cart control".

## Device state note
- Added test items 16 + 18 to customer@nears.com online cart during AC3/AC4 (item 17 pre-existing). App left in Arabic (next run's flutter run reinstalls → resets to English default). Non-blocking.

## VERDICT: PASS (662 + 663). No task_bugs. No blocking regressions.
