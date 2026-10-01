# NEARS-3960 QA progress (emulator-5590, UserApp debug @ e136e6065, backend :8120 on nears_qa_3960)
- Cell 1 (case 3: Loaf100 own 5%, store 10%, cap 5.00) via store-page "Add To Cart" (optimistic row, no refresh):
  checkout Discount -10.00 / VAT +4.75 / Total 94.75; confirm sheet Discount -5.00, Total 99.75 + "Your order total has been updated" -> FAIL (correction step present)
  -> order 91416: order_amount 99.75, store_discount_amount 5.00 (charged != checkout 94.75)
- Cell 1 same basket after a cart/list refresh (module switch -> getCartDataOnline): checkout Discount -5.00 / VAT 4.75 / Total 99.75; confirm sheet 5.00 / 99.75, no notice
  -> order 91417: order_amount 99.75, store_discount_amount 5.00 == checkout == confirm (refreshed path PASS)
- Cell 2 (case 11: Alpha20 + Beta10, cap 1.00) optimistic rows: checkout Discount -3.00 / VAT 1.45 / Total 28.45; confirm sheet 1.00 / 30.45 + "total updated" notice -> FAIL (same defect)
  -> refreshed path: checkout Discount -1.00 / Total 30.45 / extra banner 1.00; confirm 1.00 / 30.45 no notice; order 91418: 30.45, store_discount 1.00 (PASS)
- Cell 3 (case 4: store 91112 food, FoodA20 + add-on 5.00 [sheet add], FoodB10 [store-page add], 10%, min 32, max 0) optimistic FoodB10:
  checkout Discount -1.00 / VAT 1.75 / Total 35.75; confirm sheet no Discount / Total 36.75 + "total updated" notice -> FAIL (under-states the charge)
  -> refreshed path: checkout no Discount / VAT 1.75 / Total 36.75; confirm same, no notice; order 91419: 36.75, store_discount 0.00, add-on 5.00 (PASS)
- Cell 4a (case 14 Example A: base 10, variation Large 40, flat own 3, 10%, max 999999): checkout Discount -4.00 / VAT 1.80 / Total 37.80, banner 1.00; confirm same, no notice; order 91420: 37.80, store_discount 4.00 (PASS)
- Cell 4b (case 22: Example A, cap 3.50): checkout Discount -3.50 / VAT 1.83 / Total 38.33, banner 0.50; confirm same, no notice; order 91421: 38.33, store_discount 3.50 (PASS)
- Cell 6 (case 28: Example A, max_discount 0 -> floor off): checkout Discount -3.00 / VAT 1.85 / Total 38.85; confirm same, no notice; order 91422: 38.85, store_discount 3.00 (PASS)
- Cell 5 (case 15: ExampleB base 50, variation Small 20, flat own 3, 10%, max 0): checkout Discount -2.00 / VAT 0.90 / Total 18.90, no extra banner; confirm same, no notice; order 91423: 18.90, store_discount 2.00 (PASS)
- Cell 7 (case 10: FlashRice20 own 18% + flash 10%, Beta10, cap 0.50; refreshed): checkout Discount -2.50 / VAT 1.38 / Total 28.88, banner 0.50; confirm same, no notice; order 91424: 28.88, store_discount 0.50, flash 2.00 (0.80+1.20), lines 2.00/0.50 (PASS)
- Cell 10 (case 1 regression: Tomatoes 13.39 own 18% + Bell Peppers 21.19, 10%, max 999999; default store-page adds, no refresh): checkout Discount -4.53 / VAT 1.50 / Total 31.55; confirm same, no notice; order 91425: 31.55, store_discount 4.53, lines 2.41/2.12 (PASS)
- Cell 9 (flag 228 ON on copy, case 11 basket, refreshed): checkout -1.00 / 1.45 / 30.45, banner 1.00; confirm same, no notice; order 91426: 30.45, store_discount 1.00 == flag-OFF order 91418 (PASS)
- Cell 8 (GROUP, flag ON: Nears Mart Alpha20+Beta10 cap 1.00 + Fresh Mart Cheddar 6.00; refreshed): checkout Subtotal 36.00 / Discount -1.00 / VAT 1.75 / delivery 0.00+0.00 / Total 36.75; confirm same, no notice;
  orders 91429 (store 1: 30.45, store_discount 1.00) + 91430 (store 2: 6.30) = 36.75 (group 84cb8789...). No per-store fee/coupon/min divergence observed (evidence only).
- Cell 11: YES. A row without item_discount exists in the CURRENT session, not just from an older cache: listing payload (items/latest) has no item_discount (merged discount only);
  CartController._buildOptimisticRow (cart_controller.dart:2183) builds from it, _adoptServerRow (:1954-1969) stamps only the id, CartScreen.initCall (cart_screen.dart:146-147) refetches only an empty list,
  checkout never refetches. A cart/list refresh (Helpers::cart_product_data_formatting, Helpers.php:331 emits item_discount) fixes it until the next listing add. See bug-optimistic-row-cap-drift.log.
## AC verdicts
- AC1 [behav]: FAIL. Cap-binding (cells 1, 2) and min-failing (cell 3) baskets show a "total updated" correction on the default add-from-listing path; PASS on the refreshed path (orders 91417/91418/91419).
- AC2 [api]: PASS. flutter test pricing_service_checkout_test.dart 85/85, fixture group 29 cases + count gate, fixture blob db002a2b2 == pin; backend Nears3946StoreDiscountRuleTest 284/284 OK on the same tree/fixture.
- AC3 [api]: PASS. git diff 18beead72..HEAD -- UserApp/lib: only pricing_service.dart; no new try/catch, toast, error state, null-return or failure branch; no AppLogger added (engineer's NONE confirmed).
## Automated
- UserApp: flutter test test/features/checkout/pricing_service_checkout_test.dart -> 85 passed
- Admin: scripts/phpunit-isolated.sh --filter Nears3946StoreDiscountRuleTest -> 284 tests, 2064 assertions OK
