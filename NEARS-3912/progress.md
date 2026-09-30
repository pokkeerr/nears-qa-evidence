# NEARS-3912 pre-build repro (base d591a3c75) - progress

- Device emulator-5556 (lock NEARS-3912), UserApp pkg com.izzes.nears.nears_nears_3912_group_offline, API_HOST=10.0.2.2:8112
- Backend: /Users/Apple/Projects/nears-NEARS-3912-group-offline/Admin/public @ d591a3c75, DB nears_qa_3912 (proven via processlist)
- Basket: store 1 Nears Mart (Rice 5kg x2) + store 2 Fresh Mart Grocery (Coca Cola 500ml x4), module 1, zone 1 address 46

| AC | status | evidence |
|---|---|---|
| AC1 | REPRODUCED | payment sheet "Choose Payment Method" lists Cash on Delivery, Pay Via Online, **Pay Offline** (clickable) on the 2-store basket; repro-ac1-payment-sheet-pay-offline-offered.png + repro-ac1-payment-sheet.a11y.xml |
| AC2 | REPRODUCED | Pay Offline + NEARS-2647 Bank Transfer -> Place Order -> Confirm & place order -> POST group/validate http_status=403 (correlation 4f59e297-1609-42eb-9d7b-b6481d76f660); BE `[WARN] group order rejected - validation` fields=["payment_method"] store_count=2; group/place never called; copy orders/order_payments/offline_payments/order_transactions/wallet_transactions unchanged; repro-ac2-client.log, repro-ac2-backend.log, repro-ac2-after-confirm.png |

# NEARS-3912 post-fix QA [8] (HEAD 4e6ce3aae) - progress
- Device emulator-5554 (lock NEARS-3912), pkg com.izzes.nears.nears_nears_3912_group_offline, API_HOST=10.0.2.2:8112
- Backend: /Users/Apple/Projects/nears-NEARS-3912-group-offline/Admin/public @ 4e6ce3aae (freshness PASS), DB nears_qa_3912 (processlist)
- Shared before: bs228=0, MAX(orders.id)=91415
- AC3 window start 2026-09-30 09:03:49 (laravel.log had 1 line = RED control)
- Scope1 UI: multi-store collapsed payment header = Cash on Delivery only; sheet = Cash on Delivery + Pay Via Online (Paypal, Razor pay) + Select, Pay Offline count 0 (base dump count 1). fix-ac3-checkout-payment-section.{png,a11y.xml}, fix-ac3-payment-sheet-multistore.{png,a11y.xml}. UX 7a clean.
- Scope6 cash pick: after COD Select, reopening sheet keeps COD change-panel expanded (COD-selected state); 'dropped a method' logcat count 0.
- AC3 PASS: COD group order placed: client validate 200 (09:06:05) + place 200; server spans port 8112 validate trace 9459e797 / place trace f76b8ee9 (= laravel.log correlation ca5ca02c); copy orders 91418 (store1) + 91419 (store2) cash_on_delivery group 93db4bbb; predicate grep -cF 'group order rejected - validation' on laravel.log lines 2..EOF = 0; RED control line 1 = 1. fix-ac3-backend.log
- AC4 part1: single-store (Nears Mart Rice x2) sheet offers Pay Offline (clickable) + COD + online. fix-ac4-payment-sheet-single-store.a11y.xml
- Scope4 stale pick: picked Pay Offline + NEARS-2647 Bank Transfer (header 'Offline Payment(NEARS-2647 Bank Transfer)'), added Fresh Mart Coca Cola x4, re-entered checkout -> header 'Cash on Delivery'; 0 'dropped a method' lines. Checkout entry resets the pick (resetPaymentMethodForNewCheckout -> -1, then shouldDefaultToCash -> 0), so the pick cannot survive the cart round-trip -> on-device path not reachable; rely on unit test. fix-scope4-stale-pick-checkout.a11y.xml
- UX7b Arabic multi-store sheet: COD + online present, 'الدفع دون اتصال' count 0, labels right-anchored (x..1251). fix-ux7b-payment-sheet-multistore-ar.{png,a11y.xml}
- Scope3 (copy bs228 0->1 at ~09:21, restored 1->0 after, cache:clear on copy each time): mixed basket Nears Mart+Fresh Mart (grocery) + The Grill House Chef Salad (food, store 39; Burger Palace closed until 10:00) + pre-existing user-6 carts (store 57 zone2, store 59 zone3). Sheet: COD + Pay Via Online, Pay Offline count 0. cash_removed=false (probe valid=false due to out-of-zone rows). fix-scope3-mixed-flagon-*.
- AC4 PASS: single-store Nears Mart Rice x2 -> Pay Offline + NEARS-2647 Bank Transfer -> Place Order -> Confirm -> OfflinePaymentScreen (bank info) -> transaction ID QA3912TXN01 -> Complete -> "Order payment details submitted successfully!" order #91423. client order/place 200 + order/offline-payment 200; copy orders 91423 offline_payment 28.40; offline_payments 51 pending. fix-ac4-offline-order-submitted.{png,a11y.xml}
- regression candidate: offline form Amount 26.00 vs order 28.40 (bug-offline-form-amount-stale.log)
- Shared after: bs228=0, MAX(orders.id)=91415
