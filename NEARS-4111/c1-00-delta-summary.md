# NEARS-4111 delta re-QA (cycle 1), TIP 45cea2277 vs BASE c891fda8c (only production change vs c4af5bb5e: Helpers.php `amount: $zeroBasket ? 0 : $price` to CalculateTaxService::getCalculatedTax)

Setup (same method as cycle 0, files prefixed c1-): fresh clone multi_food_db_qa4111 of multi_food_db_test; BASE :8572 and TIP :8571 as `php -d pcre.jit=0 -S` from scratch detached worktrees with their own vendor copy; listener cwd verified; backend-freshness-check PASS on both; marker business_name NearsQA4111 served by both; routes only, no DML. Order-wise 10% VAT proven ACTIVE by a paid-basket control (qty 2 -> tax 0.8 on both servers, c1-00-setup-state.log).
Note: the branch was later rebased (tip now 82cb7a7ee); tested sha is the packet's 45cea2277, still resolvable.

| Row | BASE | TIP | file |
|---|---|---|---|
| Float drift 123.45 @100%, ORDER-WISE VAT, get-Tax qty 1/2/3/7 | 1.4210854715202005e-15 / 2.842170943040401e-15 / 5.684341886080802e-15 / 1.1368683772161604e-14 | tax_amount exactly 0 (JSON `0`) x4; place qty 1,3: order tax 0.00, order_amount 1.00 | c1-ex1-... |
| AC1 get-Tax @100% qty 1+2, VAT off/on | 500 x4 | 200 tax 0 x4 | c1-ac1-ac2-... |
| AC2 place, VAT off/on | 403 generic x4 + [FAIL] new_place_order failed | 200 x4, order_amount 1.00 = delivery 1.00, tax 0.00, no [FAIL] | c1-ac1-ac2-..., c1-log-summary-... |
| AC3 admin edit/update | 500/500 | 302/302 edited 0->1, money unchanged | c1-ac3a-... |
| AC3 Admin POS / Store Panel POS | 500/500 each | 200/200 each, orders stored (1.00 / 0.00, tax 0.00) | c1-ac3b-..., c1-ac3c-... |
| 100% STORE discount | quote 500, place 403, POS 500 | 200 / 200 / 200 | c1-ex3-... |
| free line + paid packaging 0.50 | 500 / 403 | tax 0.05, order_amount 1.55; paid control identical (0.85 / 10.35) | c1-ex4-... |
| Controls: paid, 25% discount (VAT off/on) | - | BASE == TIP x4 (tax 0 / 0.8 and 0 / 0.6) | c1-ac4a-... |
| Control: referral bonus nets basket to 0 (take-away, VAT off/on) | - | BASE == TIP x2, order_amount 0.00, update 302 edited 1 | c1-ac4b-..., c1-ac4c-... |
| AC5 price-0 add-on, qty 1+2, VAT off/on | quote 500 / place 403 | quote 200 (0.4 / 0.8 VAT on, 0 off), place 200 (tax 0.40 / 0.80 on, 0.00 off) | c1-ac5-... |

Withdrawn row (conductor decision): 100% flash sale, unreachable by any route, test-level coverage by the conductor. phpunit not run by QA.
