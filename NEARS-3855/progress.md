# NEARS-3855 QA progress (emulator-5600, unsuffixed control build of 56697cbaf, backend :8155 on nears_qa_3855)
- AC4 add_to_cart: FA+mirror module_id=1 (item 97/store 1; 91152/91158), =2 (91154/91159), =3 (91156/91160) — PASS
- AC4 search_add_to_cart: FA+mirror module_id 1/2/3 matching the add — PASS
- AC4 cart_quantity_changed: FA+mirror module_id 3 (663/57), 1 (91152), 2 (91154) — PASS
- AC4 remove_from_cart: mirror module_id 4,4 (removeStoreFromCart store 59, per-row), 3 (row remove 663), 1 (stepper_to_zero 97). FA: NONE — pre-existing currency-less value throws in _safe (regression bug)
- AC1 partial: view_cart 2-store basket store_count=2 module_count=2 (FA+mirror); 4-store basket store_count=4 module_count=3 (mirror)
- AC1 PASS: view_cart store_count=3 module_count=3; begin_checkout store_count=3 module_count=3 (FA-SVC 12:19:57/12:20:07)
- AC2 PASS: ONE group_order_placed {store_count=3, basket_store_count=3, order_sub_order_count=3, module_count=3, group_id=b4dd4384-...} + ONE purchase {transaction_id=b4dd4384-..., store_count=3, module_count=3, value=65.89 AED} FA-SVC 12:22:26; orders 91434/5/6 order_group_id=b4dd4384-... wallet
- AC5 PASS: loaded store records 91158:1 91159:2 91160:3 -> 3 distinct == logged 3 at begin_checkout/purchase/group_order_placed
- AC5 measurement: copy DB (read-only) basket stores 91158:1,91159:2,91160:3 (3 distinct); /api/v1/stores/details/{id} on :8155 -> module_id 1/2/3; app [NET] stores/details/9115{8,9},91160 http_status=200 (records loaded, no CartStoreModuleFailure for them); logged module_count=3 at begin_checkout, group purchase, group_order_placed
- AC3 PASS (single-store, flag ON): purchase {transaction_id=91437, store_count=1, module_count=1, tax, shipping kept} FA 12:27:28; group_order_placed count in window = 0; order 91437 order_group_id NULL
- AC3 flag-OFF (copy 228=0, served cross_module_basket=false): basket Basmati(91158 m1)+Rice 5kg(store 1 m1): view_cart store_count=2 module_count=1; begin_checkout store_count=2 module_count=1 (FA). Not placed (packet caps live orders at one group + one single).
- AC-REG: 0 literal null/0 module params; 0 PII hits; existing params intact (single purchase keeps tax/shipping; group_order_placed keeps basket_store_count/order_sub_order_count/source)
- AC-TEST/backstop: flutter test test/helper test/features/cart test/features/checkout @56697cbaf -> 3033 pass / 1 error == in-scope baseline (route_helper_item_details_coldstart f1); 29 NEARS-3855-relevant tests green incl. group_place_clear_basket_call_site (moduleCount 2 over emptied basket), 200-no-group_id, fallback window, buy-now
- AC6/AC7 PASS: events doc § NEARS-3855 rule sentence verbatim (:1183), collision note, deprecated basket_store_count, purchase/group_order_placed text amended; spec SHIPPED header, PLANNED=0, not-live sentence gone; 22 spec citations verified at 133c98fd4 incl. :890 second remove site

## Delta re-QA cycle 1 @aa8a11900 (emulator-5600, unsuffixed control build of aa8a11900, backend :8155 from git-archive copy of aa8a11900 on nears_qa_3855b)
- AC4 remove_from_cart (FA) PASS: leg 2 whole-store (removeStoreFromCart, gate-card Remove store 59): FA-SVC 12:53:57.676/.685 items 688,689 module_id=4 currency=AED (one per row); leg 1 row remove (Remove Cough Syrup 100ml -> confirmRemoval): FA-SVC 12:54:10.022 item 663 module_id=3 currency=AED value=144.6608; leg 1b stepper_to_zero: FA-SVC 12:54:27.459 item 390 module_id=2 currency=AED. Mirror 4 == FA 4; 0 FA lines missing currency/module_id. Control add_to_cart FA-SVC 12:53:23.092 module_id=2 currency=AED.
- Logs: no exception/[ERR] from the remove actions; window [FAIL]s are the expected out_of_coverage pre-flight/CartStoreModuleFailure lines for Abu Dhabi stores 57/59 (device in Dhaka zone fixture), same as prior pass.
- Backstop: flutter test test/features/cart @aa8a11900 bytes -> 838 pass, 0 fail (incl. cart_remove_undo_and_substitution_test 16/16).
- regression_bug: view_item (item_controller.dart:1068) value without currency -> mirror 1 / FA 0 at 12:54:57, positive control FA add_to_cart/view_item_list 12:55:28 (bug-view-item-never-reaches-ga4.log)
