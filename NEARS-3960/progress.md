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

# FIX CYCLE 2 delta re-QA (emulator-5590, UserApp debug @ 0cc129423 pkg com.izzes.nears.nears_nears_3960_store_cap_remirror, backend :8120 on nears_qa_3960, flag 228=1)
- Backstop: flutter test pricing_service_checkout_test.dart + cart_adopt_server_own_discount_test.dart -> 90 passed (85+5)
- AC3: git diff ddd578e8b..HEAD -- UserApp/lib: cart_controller.dart adds _adoptServerOwnDiscount (null-guarded assigns) + item-id match loop; no catch/toast/error state/AppLogger. NONE confirmed.
- R1 (case 3, default store-page add, ADD 200, no cart GET): checkout 100.00/-5.00/+4.75/99.75; confirm 5.00/99.75 no notice; order 91431: 99.75, store_discount 5.00; req e99d7ff1-566f-482f-9d0c-67c6b561cc26 -> PASS
- R2 (case 11, cap 1.00, default adds Alpha20+Beta10, ADDs 200, no cart GET): checkout 30.00/-1.00/+1.45/30.45 + "You got 1.00 additional discount"; confirm 1.00/30.45 no notice; order 91432: 30.45, store_discount 1.00, lines 0.67/0.33; req bed86a1f-488f-42c2-8d4a-0bea95618e90 -> PASS
  (note: cart screen preview showed Discount -3.00 before checkout; R1 cart screen showed -10.00 — see followup)
- R3 (case 4, store 91112 min 32 max 0: FoodA20+Addon5 via detail sheet [sheet add fired cart/list], then FoodB10 store-page Add To Cart default path, ADD 200, no cart GET after): checkout 35.00/no Discount/+1.75/36.75; confirm 35.00/1.75/36.75 no notice; order 91433: 36.75, store_discount 0.00, add-on 5.00; req d11a4203-fdd1-4d19-a301-c7806b8a0f88 -> PASS
- R4 (own-0 Alpha20 alone, cap 1.00, default add, ADD 200, no cart GET): checkout 20.00/-1.00/+0.95/19.95 + "You got 1.00 additional discount"; confirm 1.00/19.95 no notice; order 91434: 19.95, store_discount 1.00; req 886dd6a1-595e-409f-a9fc-7667a4d8c615 -> PASS
- R5 (campaign "+" add, Food home "Just for You" card "Tasty Food Favorites" = item_campaigns 14, no refresh): ADD 200 but server row = carts item_id 14 item_type App\Models\Item (Organic Almond Milk, store 3, module 1) @25.00 -> server item id "matches" (14==14) only by id collision; adopted item_discount = Almond Milk's 0.
  cart screen -2.50 / checkout 25.00 no Discount / confirm 0.00 + "Your order total has been updated" / place 403 "You can not place empty orders" (paired [FAIL] corr 9b8e4b73-e57f-4839-bfb7-3fa278be5097 == BE "[WARN] order placement rejected - gate"). No order. -> FINDING (see bug-campaign-add-wrong-server-row.log/png)
- R6 (Example A qty 2 Large 40, flat own 3, 10%, max 999999; sheet add): checkout 80.00/-8.00/+3.60/75.60 + "You got 2.00 additional discount"; confirm 8.00/75.60 no notice; order 91435: 75.60, store_discount 8.00; line 40.00 x2 discount_on_item 8.00 'precentage'; req e3fb156a-652c-4694-a496-40a75ec707fd -> PASS
  Order details render (#91435): "Quantity: 2, x 2, 36.00, struck 40.00, You saved 8.00" -> perUnit 4.00 = 8/2, chargedUnit 36.00 -> PASS
  product_discount render (#91425, prior cycle order): Tomatoes "x1 10.98 struck 13.39 saved 2.41", Bell Peppers "x1 19.07 struck 21.19 saved 2.12" -> unchanged, PASS
- R7-A (Example A qty 1, max 999999, sheet add): checkout 40.00/-4.00/+1.80/37.80 + banner 1.00 (pay 36.00 pre-VAT); confirm 4.00/37.80 no notice; order 91436: 37.80, store_discount 4.00, line 4.00 'precentage'; req 8425c5e2-cf42-42be-9627-921e706203b8 -> PASS
- R7-B (Example B Small 20, flat own 3, max 999999, sheet add): checkout 20.00/-2.00/+0.90/18.90, no extra banner (pay 18.00 pre-VAT); confirm 2.00/18.90 no notice; order 91437: 18.90, store_discount 2.00; req 26c28be0-d495-43a8-8a58-6ac738653476 -> PASS
- R8a (FlashRice20 own 18% flash 10% FIRST, then Beta10; 10%, max 999999; default adds, ADDs 200, no cart GET): checkout 30.00/-3.00/+1.35/28.35 + banner 1.00; confirm 3.00/28.35 no notice; order 91438: 28.35, store_discount 1.00, flash 0.80+1.20, lines flash_sale 2.00 / precentage 1.00; req 670b2e61-743f-4914-b642-ebe2e481e495 -> PASS
- R8b (Beta10 FIRST, then FlashRice20; same store/discount; default adds, ADDs 200, no cart GET): checkout 30.00/-3.00/+1.35/28.35 + banner 1.00; confirm 3.00/28.35 no notice; order 91439: 28.35, store_discount 1.00, flash 0.80+1.20, lines precentage 1.00 / flash_sale 2.00; req 450c0cb6-0bfc-492e-9955-3a3ea380a37d -> PASS (both orders identical)
- R10 regression (case 1 Tomatoes own 18% + Bell Peppers, 10%, max 999999; default adds THEN module switch -> 4x cart/list GET 200): checkout 34.58/-4.53/+1.50/31.55 + banner 2.12; confirm 4.53/31.55 no notice; order 91440: 31.55, store_discount 4.53, product_discount 2.41/2.12; req a9a9135b-3091-4139-b8d4-e88aa17fc82c -> PASS (== prior 91425)
- Findings: (a) R5 campaign rail add -> wrong server row (pre-existing isCampaign:false) + cycle-2 id-only adoption copies wrong row's item_discount; (b) Basket summary ignores cap/floor/min (pre-existing calc) - see bug-*.log
## Cycle-2 AC verdicts
- AC1 [behav]: PASS on the DEFAULT add path - cap-binding R1 (91431), R2 (91432), R4 (91434) and min-failing R3 (91433): checkout == confirm == charged, no "total updated" step.
- AC2 [api]: PASS - 90/90 client tests (85 pricing incl. 29-case parity fixture + 5 adopt tests); fixture blob db002a2b2 unchanged; Admin bytes unchanged since prior 284/284 backend PASS (delta = test comment only).
- AC3 [api]: PASS - cycle-2 UserApp/lib diff adds no non-success branch.
- Shared multi_food_db: max order 91415, bs228 0 (verified at end). Copy disc 1 restored to max 5.00.
