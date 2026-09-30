# NEARS-3931 QA progress (phase 8, cycle 0)

- Private DB: nears_qa_3931; backend :8131 = /Users/Apple/Projects/nears @ f21331fb8 (Admin byte-identical to base 9cad53f6b), proven via /config footer_text marker.
- Shared invariants BEFORE: business_settings id=228 = 0; max(orders.id) = 91415.
- Discount facts (copy): discounts id=1 store_id=1 10% percent, 2026-08-01..2027-08-30, 00:00:00-23:59:59, min_purchase 0, max 999999 (ACTIVE). items.id=97 Rice 5kg price 15.03, own discount 18% percent. flash_sale_items id=36 (flash_sale 1, published, 2026-06-30..2027-01-11) item 97, 10% percent, available_stock 46 (ACTIVE).
- AC1 PASS (base 9cad53f6b, emulator-5554): basket Rice 5kg x2 -> payment sheet Total Bill 26.00 -> confirm sheet "order total has been updated" 28.40 -> order #91416 -> OfflinePaymentScreen "Amount 26.00 AED"; DB order_amount 28.40. Divergent, stale figure shown. Logs: no [ERR]/[FAIL] on the placement action (launch-time Firebase [FAIL]s are worktree env residue).
- AC2 PASS (fix 2c28a8ebd): same basket, checkout sheet 26.00 -> confirm 28.40 -> order #91417 -> OfflinePaymentScreen "Amount 28.40 AED"; DB order_amount 28.40.
- AC3 PASS: proxy trace POST /api/v1/customer/order/place 200 body total_ammount=28.4, order_id 91417; == DB == screen.
- AC4 PASS: [INFO] checkout: offline form amount orderID=91417 amount=28.4 source=server rid=14812482-c455-4583-a531-66299f5eef01 == request X-Request-Id == echoed response header.
- Regression: offline form submit (txn QA3931TXN) -> 200, offline_payments id 51 pending, order 91417 pending.
- AC5 PASS: COD #91418 (order_amount 28.40) -> order tracking, no offline-form log line, no [FAIL]/[ERR].
- Backstop: flutter test test/features/checkout 744 pass; place_order_offline_total_test.dart 13/13.
