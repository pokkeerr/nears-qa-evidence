# NEARS-3809 QA progress (fix_cycle 0, code 1b2e67b08, emulator-5560, backend :8309 clock-pinned 2026-09-28 03:00 Asia/Dubai)
- AC1 PASS: cart/add food item 16/121 (store 4) + 22 (store 5) closed-now schedule_order=1 -> 403 store_closed; ar message = المتجر مغلق في وقت الطلب
- AC2 PASS(gate)/200 via PHPUnit: grocery 40, 2 & pharmacy 433 pass the store gate (next gate out_of_zone/cart_item_limit reached; no insert)
- AC3 PASS: order/place schedule_at 12:00 food 4/5 -> 403 order_time; [WARN] food_preorder_store_closed x3; grocery/pharmacy controls pass gate (coupon 403)
- AC4 PASS(gate)/200 via PHPUnit: immediate at open food 49 passes gate (coupon 403); immediate at closed food 4 -> old $store->open arm, no food WARN
- AC5 PASS: item 14 (Burger Palace) sheet: notice store_closed_cant_order, CTA 'Store is closed' enabled=false, no Schedule Order; item_unavailable_shown(store_closed) x1
- AC7 PASS: store page (Burger Palace) quick-add Classic Cheeseburger -> [WARN] add blocked reason=store_closed source=item_add store_id=4 item_id=16; no POST; carts max id unchanged 947. List cards (store_details=null) fail open pre-existing -> server 403 backstop
- AC6 PASS: Nears Mart (grocery, closed-now, schedule_order=1) Rice 5kg sheet: notice 'your order will be scheduled for later', CTA 'Schedule Order' enabled=true; no item_unavailable_shown
- X Arabic/RTL PASS: Hummus Bowl (117) sheet ar notice 'المتجر مغلق · يفتح في 10:00 · الطلب المسبق غير متاح', CTA 'المتجر مغلق' disabled, Close mirrored to left; API ar message store_is_closed_at_order_time = المتجر مغلق في وقت الطلب
- AC8 UNVERIFIABLE-live: only closed-food cart in DB (user 6) is unparseable in-app (cart/list add_ons int ids) and is the live session's; needs 1 carts row delta; widget tests cover slot section/notice; Place Order snackbar branch has NO test
## QA-caused DB writes (disclosed, all reversed via product endpoints)
- 12:01:58 carts 949 (item 16 x2) + 950 (item 121) for user 6: AC1 probes ran before the clock pin was actually active (php -S skips auto_prepend_file when a router script is given). Removed via DELETE /customer/cart/remove-item 949,950 -> cart restored to pre-probe rows 939,940,942,944-947.
- 03:00 (pinned) carts 951 (items.id 14 Organic Almond Milk) for user 6: campaign quick-add model mix-up (pre-existing bug). Removed via remove-item 951.
- incidental app writes: oauth token (API + app login), users.cm_firebase_token for user 6 overwritten by emulator-5560 login (live session device may stop receiving pushes for customer@nears.com until it re-logs in).
- orders max id 91394 unchanged across the whole run; order_groups count 13 unchanged.
