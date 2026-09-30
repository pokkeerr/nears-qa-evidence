# NEARS-3912 pre-build repro (base d591a3c75) - progress

- Device emulator-5556 (lock NEARS-3912), UserApp pkg com.izzes.nears.nears_nears_3912_group_offline, API_HOST=10.0.2.2:8112
- Backend: /Users/Apple/Projects/nears-NEARS-3912-group-offline/Admin/public @ d591a3c75, DB nears_qa_3912 (proven via processlist)
- Basket: store 1 Nears Mart (Rice 5kg x2) + store 2 Fresh Mart Grocery (Coca Cola 500ml x4), module 1, zone 1 address 46

| AC | status | evidence |
|---|---|---|
| AC1 | REPRODUCED | payment sheet "Choose Payment Method" lists Cash on Delivery, Pay Via Online, **Pay Offline** (clickable) on the 2-store basket; repro-ac1-payment-sheet-pay-offline-offered.png + repro-ac1-payment-sheet.a11y.xml |
