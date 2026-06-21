# NEARS-494 QA progress (live, emulator-5556)

Started Sun Jun 21 20:51:46 UTC 2026


## Pre-flight (PASS)
- Device: emulator-5556 (locked), worktree boot from nears-NEARS-494-cart-optimistic-add/UserApp
- baseUrl -> http://10.0.2.2:8000 (local backend, config 200)
- Backend: php artisan serve :8000 running; zone 1 (demo)
- Logged in: customer@nears.com (Customer Nears) -> /api/v1/auth/login 200
- Analytics: FA/DebugView UNAVAILABLE on this build (Missing google_app_id). Observing `📊 analytics:` stdout lines instead.

## Test data
- Discounted simple (CRITICAL-1): item 8 Orange Juice 1L 5.00@15%=4.25; item 5 Tomato 2.00@10%=1.80 (store 2)
- Variation: item 84 Dove Whitening Body Spray (store 2)
- OOS: item 61534 QA OOS Fixture (store 2)
- Cross-store: store 2 vs store 3 Organic Paradise

## AC1 PASS — instant optimistic add (Tomatoes item 102)
- Tap "+" -> card flips Add->stepper instantly; ONLY call = [200] /cart/add (NO /items/details/ pre-fetch; old two-round-trip gone). shot 01-ac1-tomatoes-added.png
## AC2 PASS — addToCartOnline POST fires async + persists
- [200] /api/v1/customer/cart/add; DB carts row 173 item 102 qty 1 persisted.
## AC7 analytics — add_to_cart fired once, PII-safe
- 📊 add_to_cart {item_id:102, price:13.39, quantity:1, currency:AED, value:13.39} (IDs/numbers only, no name). FA channel disabled on build; observed via app stdout.
## CRITICAL-2 PASS — PATCH on pre-existing persisted row (Mango item 99)
- Mango pre-existing qty 1 (server cart_id 172) -> tap "+" -> [200] /cart/update (PATCH) then /cart/list resync. NO /cart/add.
- DB truth AFTER: carts row 172 item 99 quantity=2, stored_price 45.96=22.98x2. Increment PERSISTED. (pre-fix: PATCH silently skipped)

## CRITICAL-1 PASS — discounted price at checkout (NOT discount amount)
- Tomatoes (added optimistically this session, 13.39@18%) shows at Checkout Review: "1 × 11 AED = 11 AED" (discounted unit ~10.98), NOT 2.41 (discount amt).
- Rice 5kg (15.03@18%=12.32): Checkout Review "1 × 12 AED = 12 AED", NOT 2.70.
- Order Summary: Subtotal 74 AED (pre-discount item sum 45.96+15.03+13.39=74.38) − Discount 5 AED (item discounts 2.70+2.41≈5) = correct discounted item total ~69. Price model intact.
- shots: 02-cart-discounted, 03-checkout-prices, 04-order-summary. No price/type exceptions in logs.

## AC5 PASS — rapid taps coalesce (Watermelon item 103)
- 5 taps in ~1s -> network: exactly 1 [200]/cart/add + 1 [200]/cart/update + 1 /cart/list. analytics add_to_cart fired 1x.
- DB truth: carts row 174 item 103 quantity=5 (correct final). No duplicate/competing POSTs. shot 05.

## AC3 — rollback (PARTIAL: cart-correct, but contradictory toast)
- Offline tap "+" -> /cart/add SocketException -> card reverts to Add To Cart; NO phantom DB row (cart stays Rice/Mango/Tomatoes/Watermelon only). GOOD.
- EN error toast: "Couldn't add to cart. Please try again." (confirmed ui_list). AR toast string present: "تعذّرت الإضافة إلى السلة. يرجى المحاولة مرة أخرى."
- DEFECT: showCartSnackBar() ("Item added to cart" + View Cart, GREEN) fires OPTIMISTICALLY before POST resolves -> on failure user sees green "added" THEN red "couldn't add". shots 06/07/08 + bug-optimistic-success-toast-on-failure.png/.log

## AC4 PASS — narrow rebuild scope (only tapped card's count view)
- Before: Tomatoes qty1, Watermelon qty5. Tap Tomatoes "+" -> after: Tomatoes qty2, Watermelon qty5 (unchanged), Mango qty2 (unchanged), siblings still "+".
- update([cartBadgeId(itemId)]) narrows the GetBuilder rebuild to the tapped card only. Backstop widget test `AC4` locks buildsA==2 (tapped rebuilds) / buildsB==1 (sibling NOT rebuilt). shots 09/10.

## Also-verify: VARIATION item PASS (Dove Body Spray item 84)
- Tap "+" -> opens modal sheet (Size: 250ml/500ml, 200-300 AED), fetched /items/details/84, NO /cart/add. Optimistic path returns false for variation items. shot 11.

## Also-verify: OUT-OF-STOCK PASS (QA OOS Fixture item 61534, stock 0)
- Tap "+" -> "Out of Stock" toast, card stays Add To Cart, NO /cart/add (only /items/details/61534 guard re-fetch). shot 12.

## Also-verify: CROSS-STORE PASS (store-1 cart, tap store-2 item 358)
- Tap "+" -> "clear cart?" dialog: "Your basket has items from another store. Adding this will clear it. Continue?" [Yes/No]. NO /cart/add (only /items/details/358). Tapped No -> store-1 cart preserved. shot 13.

## Also-verify: HIGH-3 multi-item in-flight PASS
- Tap A(Tomatoes) then B(Watermelon) back-to-back while A in flight -> 2x /cart/update + 2x /cart/list. Final: Tomatoes 2->3, Watermelon 5->6. Neither optimistic qty wiped by the other's resync. No runtime errors. shot 14.

## AC6 regression PARTIAL (cart screen) PASS
- Cart-screen line +/-: Rice 5kg 1->2->1 via /cart/update + /cart/list, persisted. 
- Remove: Watermelon removed (/cart/remove-item?cart_id=174 + /cart/list), remove_from_cart analytics fired (item 103). 
- Subtotal 101 AED / Discount -10 / Total 91 AED coherent. Substitution prefs default "Call me ASAP".
- Free-delivery progress bar: not shown for store 1 (no admin free-delivery promo configured) = correct, not a defect. shots 15/16.

## AC6 regression (item-details sheet) PASS
- Mango details sheet: in-sheet qty stepper 2->3 -> Total Amount recomputes 23->69 AED (3x23). Modal-over-screen (cart visible dimmed behind, NEARS-422). Dismissed without commit -> cart Mango stays 2. shot 17.
