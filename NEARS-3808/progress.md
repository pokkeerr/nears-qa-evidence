# NEARS-3808 QA progress (phase 8, cycle 0) — emulator-5562, UserApp built from worktree @ 046da4281, backend :8308 from worktree
- AC1 PASS — grid card (store_items_grid) quick-add of item 18: POST cart/add 200, add_to_cart fired, row 953 created; also sheet-add item 18 + Extra Cheese (row 952, add_on_ids [1]); item 17 grid quick-add (update path) 3->4->3 clean.
- AC2 PASS (shared path) — menuRow card not on this base; store List view (NItemCardLayout.row) item 17 add 3->4->3, cart/update 200, no exception.
- AC3 PASS — cold relaunch, cart/list 200 x2, Veggie Burger row shows ", 1 Addons" -> "Addons: Extra Cheese (1)", Burger Palace subtotal 46.56 = 3x11.69 + 9.99 + 1.50.
- AC4 PASS — debug mirror: add_to_cart {item_id: 18, price: 11.49 ...} and {item_id: 18, price: 9.99 ...}; FA logcat unavailable (Firebase init fails on suffixed package).
- AC5 PASS — no [FAIL]/[ERR] on cart path; only pre-existing Firebase/FCM/location + search-results semantics asserts.
- AC6 PASS — cart/list add_ons objects == addons ids on every row incl. selected-add-on row; 0 item_add_ons_skipped.
- AC7 PASS — phpunit 2/2 (42 assertions), flutter test 8/8.
- Cart restored (contents identical; Veggie Burger row id 945->953; price column rewritten by app update path).
