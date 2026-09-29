# NEARS-3842 QA progress (phase 8, fix_cycle 0)
Device emulator-5570 · build 282fb772e (feat/NEARS-3842-cart-per-store-groups) · pkg com.izzes.nears.nears_nears_3842_cart_per_store_groups · user 5 (robert.taylor@demo.com)
Backend: /Users/Apple/Projects/nears-NEARS-3842-cart-per-store-groups @ 282fb772e (php artisan serve --no-reload :8242, DB nears_qa_3842 private copy; flag=1 on copy only)
Copy fixtures: store_configs s4 extra_packaging_amount 3.5, s2 1.25; store_schedule s4 opening 00:00; admin_free_delivery_option=free_delivery_by_order_amount, free_delivery_over=100
- AC-TEST PASS: backstop cart+checkout+coupon 915 passed/0 failed; the 4 named files 37/37
- AC1 PASS: 2 sections; header nodes "Nears Mart, Grocery, 1 Item, 13.53 AED" / "Burger Palace, Restaurant, 2 Items, 55.82 AED", no duplicate child text; steppers separate Buttons; shot ac1-mixed-cart-two-sections-light.png, matches UX spec 1.2
- AC7 PASS: active module grocery (addOn=false), food addOn=true -> Addons row shown
- AC5 (null) module null -> null, info "cart initCall: mixed basket, module left unset stores=2"; BUT [FAIL] items/suggested 403 x2 (task bug, bug-suggested-items-403-module-null.log)
- AC3 FAIL(module-null state): min-order bar A unchanged on B edits (PASS part), but delivery fee rows both 1.00->0.00 on a B edit with module null; no delivery-quote; bug-mixed-null-module-delivery-fee-zero.{log,png}
- AC6 PASS(literal, at checkout start module null->null, info 'cart prepareCheckout: mixed basket, module left unset stores=3'); FINDING: checkout_controller NEARS-726 block sets module=1 ~1s later (finding-checkout-screen-sets-module.log)
- AC2 PASS: sec B Add More Items -> /store/burger-palace?id=4 module=2, Back -> /cart; pkg cards B 3.50 / C 1.25 only (A none); toggle in C -> B checked; summary Extra Packaging (+) 4.75; cutlery toggle in C -> B checked; captions under each card
- AC3 PASS (module set): edit A Rice 1->2 -> A 13.53->27.05 min met, B/C unchanged, 3x delivery-quote 200 all 1.00
- AC8 PASS (mixed): isFreeDeliveryPromoActive=false, no 'more for free delivery' text, subtotal 89.52 < 100
- AC-LOG PASS: [FAIL] CartStoreModuleFailure store_id=2 (details 500 -> row-module fallback) + store_id=4 module_id=2 (badge omitted), ids only; UI degraded accordingly; AC5 skip logs [INFO]. aclog-degraded-per-store.log + aclog-degraded-cart-a11y-dump.xml
- AC-REG flag ON same-module {Nears Mart, Fresh Mart} PASS: module null->1 (NEARS-726), mixed=false (= server isMixed{1,2}=false), one-row headers, single basket-wide 'Add More Items', promo '66.30 AED more for free delivery' + progress (AC8 shown-control). shot acreg-flag-on-same-module-basketwide-promo.png
- AC4 PASS: client mixed=true for {1,2,4} = server CrossModuleBasket::isMixed(Store module_ids)=true; {1,2} false=false; {4,39} server false; divergent campaign case unit test
- RTL PASS: ar_SA, header row mirrored, subtotal LTR-pinned, row 2 mirrored, '1 غرض' singular, caption 'ينطبق على جميع المتاجر في سلتك' under each card, long AR module name ellipsizes (translation 269 lengthened on copy, restored to مطعم). shots rtl-ar-mixed-cart-long-module-ellipsis.png, rtl-ar-long-module-name-ellipsis-header.png. Note: module-null AR cart shows NO fee/ETA rows (same quote-skip bug)
- AC-REG flag OFF PASS: Grocery tile -> Basket tab, one-row headers, basket-wide Add More Items, promo '66.30 AED more for free delivery', You May Also Like rail, module 1, no [FAIL]

# fix-cycle 1 delta (build 130cd1d0d, emulator-5570, backend worktree :8242 @ 130cd1d0d on nears_qa_3842)
- AC-TEST PASS: flutter test test/features/cart test/features/checkout test/features/store -> +1322 All tests passed
- AC5 PASS (module null): before-open null -> after-load null (x3 opens), "cart initCall: mixed basket, module left unset stores=3", 3x items/suggested 200 (was 403), store 4 rail = 7 items all module 2 store 4, 'You May Also Like' present, no [FAIL]
- AC3 PASS (module null): first open 3x delivery-quote 200 -> fees 1:1.00 2:1.00 4:1.00 (was 0.00, 0 quotes); decrement Red Apple in Fresh Mart (non-first) 2->1 -> only Fresh Mart sub 6.65->3.33 + bar met->'not reached'; Nears Mart 27.05 met + Burger 25.87 unchanged; 3x quote 200, fees stay 1.00, module still null; shot fc1-ac3-module-null-edit-B-fees-quoted.png
- AC3 PASS (module set=1): increment Red Apple 1->2 -> Fresh Mart 3.33->6.65 only, single cart/update, fees 1.00 each
- NEW TASK BUG: module null + "+" on any row -> forcefullySetModule(cartList[0]) flips module to 1 + home reload race reverts the increment (1->2->1), reproduced 2/2 (Soup/Burger 09:36, Red Apple/Fresh 09:39); control with module set clean. bug-mixed-null-module-increment-flips-module-and-reverts.log
- AC-REG flag ON same-module {Nears Mart, Fresh Mart} PASS: module null->1 (NEARS-726), mixed=false, one-row headers, basket-wide Add More Items, promo 'more for free delivery', 2x quote 200 fees 1.00, 2x suggested 200, rail present
- AC-REG flag OFF PASS: Grocery tile -> Basket, module 1, one-row headers, Add More Items, promo, 2x quote 200 fees 1.00, 2x suggested 200, rail present
