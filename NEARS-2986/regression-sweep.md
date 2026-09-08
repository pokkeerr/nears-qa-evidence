# Regression sweep — live-demoed results (all against real HTTP API + real seeded DB)

| # | Scenario | Order/result | Evidence |
|---|---|---|---|
| 3 | Multi-line cart, different addon sets/line | order 91214, store 4 | item16(cheese+bacon)=3.50 total_add_on_price, item115(jalapenos x2)=2.00, item117(none)=0.00 — all correct. Confirms the `Collection::whereIn` positional-desync fix (NEARS-2920/2986). |
| 4 | Item + ItemCampaign mix | order 91215, store 4 | order_details: item_id=16/item_campaign_id=NULL and item_id=NULL/item_campaign_id=14 — separate columns, both formatted (63/56 keys resp.), batching stayed separate per model. |
| 5 | Prescription item, no attachment | store 7 (pharmacy) | 403 `{"code":"prescription","message":"Prescription is required for this order"}` |
| 6 | Addon from another store | item16(store4) + addon id 5(store5) | 403 `{"code":"addon","message":"Invalid add-on selection"}` — NEARS-2920 guard intact post-batching |
| 7a | Buy-now flow | order 91218 (is_buy_now=1, direct cart JSON, item6 x2) | cart row 804 (item4, added via normal add-to-cart, untouched by buy-now) verified STILL PRESENT after order 91218 — buy-now correctly skips the bulk-delete |
| 7b | Normal flow delete, no orphans | order 91219 (store2, cart rows 804+new item6 row) | both grocery(module1) rows deleted; sibling pharmacy(module3) row 805 for the SAME user untouched — no cross-module over-deletion |
| 8/13 | Group order, per-store isolation | group_id 2c8dd39a…, orders 91223(store2)+91224(store36) | order_details cross-checked: 91223 carries only items {6,3}, 91224 only {343,346} — zero cross-store leakage |
| 9 | Flash-sale stock decrement | order 91217, item 507 (pharmacy, module stock=true) qty2 | items.stock 128→126, flash_sale_items.available_stock 52→50, sold 7→9 — both decremented correctly. (Separately confirmed food-module items do NOT decrement stock — `config('module.food')['stock']=false`, pre-existing/unrelated business rule, not this diff.) |
| 10 | FCM cache | see ac3-fcm-cache-hit.log | PASS |
| 11 | Concurrency/no-oversell | item 11 drawn down to stock=1, two near-simultaneous `order/place` calls | one succeeded (order 91221, stock 1→0), the other correctly saw `empty_cart` (cart already consumed by the winner's commit) — no oversell, no negative stock. CAVEAT: `php artisan serve`'s built-in dev server processes requests serially by default, so this exercises "rapid double-submit" more than a true simultaneous multi-worker DB race; the diff does not touch lock/isolation semantics at all (confirmed via `grep lockForUpdate` — only the pre-existing coupon-row lock exists, untouched), so behavior is structurally guaranteed identical to pre-fix. |
| 12 | Error paths unchanged | various | empty_cart 403, invalid qty(0) 403, addon-count-mismatch 403 `add_on_qtys`, different-store-item 403 `different_stores`, coupon(expired) 403 `coupon` — all pre-existing codes/shapes, unchanged |
