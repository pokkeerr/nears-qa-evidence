# NEARS-570 QA progress (live, Android emulator-5554, worktree build 0bf6f3ca)

Build under test: fix/NEARS-570-guest-cart-session @ 0bf6f3ca, UserApp, emulator-5554, debug.
Backend: local Admin php artisan serve :8000 (200 on /api/v1/config).
Evidence channel: Dart MCP get_app_logs (I/flutter `====> API Response: [<status>] <uri>` lines; uri carries the query string incl. guest_id).

## Backend contract confirmed (curl, pre-flight)
- cart/add `?guest_id=` (empty)  -> 401 {"errors":"Unauthorized"}  (reproduces the bug)
- cart/add no guest_id param      -> 401 {"errors":"Unauthorized"}
- cart/add `?guest_id=133` (real) -> 200 + cart row (is_guest:true)  (the cure)
- guest mint POST /api/v1/auth/guest/request -> {"guest_id":133}
- probe cart row cleaned via cart/remove-item API (no raw DB write).

## AC5 — authenticated no-regression (DONE, PASS)
- Logged in customer@nears.com. Entered open store "Fresh local", item "Tones Mild Chili Powder" (item 91), selected size, Add To Cart.
- LOG: `====> API Response: [200] /api/v1/customer/cart/add`  — URL has NO guest_id, returns 200.
- analytics add_to_cart {item_id:91, price:105.0, quantity:1} fired.
- Basket shows the item landed (Mozzarella 200g, Popcorn, Tones Mild Chili Powder).
- Shot: ac5-authenticated-cart.png
- Logged-in cart pre-logout = {Mozzarella 200g, Popcorn, Tones Mild Chili Powder} -> baseline for no-leakage check.

## NEXT
- Logout -> verify cart cleared (no-leakage) -> guest add-to-cart (AC2/AC3 core) -> guest qty/remove/list (step3) -> fresh-guest (step5).

## LOGOUT + GUEST FLOW (DONE) — core fix verified
- Logout (customer@nears.com -> Yes). Post-logout log: `====> API Response: [200] /api/v1/auth/guest/request` (clearSharedData re-mint landed).
- SharedPrefs after logout: `flutter.6ammart_guest_id`=135 (NON-EMPTY); no `cartList` key (persisted local cart cleared).
- AC1: guest Basket accessible post-logout, shows "Your cart is empty" -> shot ac1-guest-cart-empty-post-logout.png
- AC2/AC3 CORE: guest add-to-cart (item 91, open store Fresh local id12):
    `====> API Response: [200] /api/v1/customer/cart/list?guest_id=135`
    `====> API Response: [200] /api/v1/customer/cart/add?guest_id=135`  <- NON-EMPTY guest_id, 200 (was 401). REGRESSION GONE.
    UI: "View Cart" success snackbar (NO "Couldn't add to cart"). analytics add_to_cart fired. shot ac2-ac3-guest-add-success.png
- Step3 other guest ops (all via _guestQuery choke-point, all guest_id=135, all 200):
    increment -> cart/update?guest_id=135 [200]
    decrement -> cart/update?guest_id=135 [200]
    remove    -> cart/remove-item?cart_id=217&guest_id=135 [200] (+remove_from_cart analytics)
    list      -> cart/list?guest_id=135 [200]
- Backend ground truth: guest_id=135 server cart held ONLY the guest's own Chili (item91), NOT the logged-in user's Mozzarella/Popcorn -> NO DATA-LAYER LEAKAGE.
- get_runtime_errors: clean (no red screen / overflow / exception) across whole flow.

## CORRECTION — "Mozzarella/Popcorn in cart" was a MISREAD (NOT leakage)
- Initial read: thought the logged-in user's Mozzarella+Popcorn carried into the guest cart view (suspected in-memory carryover). WRONG.
- Re-inspected the cart screen a11y tree: only "Tones Mild Chili Powder" is a real cart LINE ITEM (has Increase/Decrease quantity + Remove). Mozzarella 200g + Popcorn render as "Organic" product cards with NO qty/remove controls, BELOW "Add More Items".
- Source: cart_screen.dart:476 `suggestedItemView` -> StoreController.getCartStoreSuggestedItemList(store 12) -> a STORE-SUGGESTED CROSS-SELL rail. Those 2 items are suggestions from the same store (Fresh local), not cart contents.
- Backend confirms at every step: guest_id=135 server cart held exactly ONE item (the guest's own). NO LEAKAGE at data OR view layer. No regression_bug to file.

## Step5 fresh-guest (DONE, PASS)
- Cold-relaunched the worktree APK (logged out). Basket = "empty" on cold start (no carryover). Fresh-guest add (item 91, store 12):
    `====> API Response: [200] /api/v1/customer/cart/add?guest_id=135`  + `cart/list?guest_id=135 [200]`
- guest_id=135 persisted across restart (durable guest session). "View Cart" success snackbar. shot step5-fresh-guest-add-success.png
- get_runtime_errors after relaunch+flow: clean.

## NEXT: fresh-guest regression (step5), automated backstop (flutter test), publish, comment.
