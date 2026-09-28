# NEARS-3831 QA [8] fix-cycle-1 build — progress checkpoint

Backend: /Users/Apple/Projects/nears-NEARS-3831-cart-stamp @ ffa92027b (:8431, `--no-reload`, DB multi_food_db_nears3831_qa; freshness-check PASS)
DB proof: copy flag=1 while multi_food_db flag=0 -> GET /api/v1/config cross_module_basket=True (flag-proofs.log)

| AC | status | evidence | log |
|---|---|---|---|
| AC1 | PASS | flag ON, user 1, header 1, item 673 (store 58, module 3) -> 200, carts.id 978 module_id=3 | clean |
| AC5 | PASS | 2nd identical add header 1 -> row 978 qty 2 (no new row); header 2 -> qty 3; header 3 -> qty 4 | clean |
| AC2 | PASS | update row 978 under header 1 -> module_id stays 3; no header -> 3 | clean |
| AC4 | PASS | get-Tax header 1 store 58 -> product_price 62.32 (= 31.16 x 2); header 3 same | clean |
| AC3 | PASS | place header 1 store 58 COD sched 10:00 -> 200 order 91416 module_id=3, 1 order_detail (item 673 qty 2) = 1 cart row, cart emptied | clean (header/store mismatch WARN as designed by NEARS-3830) |
| SEC flag ON | PASS | guests 1968/1969 same item under headers 1/2 -> both module 3, one row each; G1 list shows only its own row; G1 token + G2 id -> 401; G1 update G2 row -> 404 unchanged | clean (deliberate negatives log [FAIL] guest.token.rejected) |
| AC2 heal | PASS | flag OFF add hdr1 -> row 993 module 1; flag ON get-Tax hdr1 -> 0 (known residual, NEARS-3862); flag ON update hdr1 -> row 993 module 3; get-Tax -> 31.16 | clean |
| AC-REG | PASS | base f7c6943ef server (:8432, git archive) vs 3831 (:8431), same copy, flag OFF, 17 identical steps: status codes + normalized bodies identical, DB stamps identical (hdr!=item -> 1, hdr==item -> 3, no hdr -> item 3, update hdr2 -> 2, update no hdr -> 3), place hdr1 -> order module 3 w/ header-stamped row, contrast get-Tax 0 / place 403 empty_cart on both (ac-reg-compare.log) | clean (3830 mismatch WARN only) |
| AC-LOG | PASS (phpunit-only) | Nears3831CartStampItemModuleTest: flag_on_update_with_item_store_missing_uses_item_module_and_warns, update_with_no_resolvable_module_fails_404_and_logs, flag_off_..._does_not_warn -> green, keys == [endpoint, cart_id, item_id] | n/a |
| AC-TEST | PASS | targeted 40 tests / 190 assertions OK; targeted + regression set 222 / 945 OK | n/a |
| Sweep | PASS | remove-item by id under foreign header works; remove-all is header-keyed (flag ON leaves store-stamped row; out of scope -> NEARS-3833) | clean |
| Regression bug | pre-existing | single-store place-order gate_failure 403s (empty_cart, order_time) emit no [WARN]/[FAIL] (bug-place-order-gate-failure-silent.log) | n/a |

Teardown: :8431 + :8432 stopped, multi_food_db_nears3831_qa dropped, multi_food_db untouched (flag 0, 75 carts, cart 319 unchanged).
