# NEARS-3830 QA [8] cycle 0 — progress checkpoint

Backend: /Users/Apple/Projects/nears-NEARS-3830-module-from-store @ b89c23142 (:8130, freshness-check PASS)
DB backup: /private/tmp/claude-501/-Users-Apple-Projects-nears/19315c20-7616-4951-9fdf-d3ff66f7c689/scratchpad/nears3830-preqa-1790631311.sql

| AC | status | evidence (see api-evidence.log) | log |
|---|---|---|---|
| AC1 buy-now | PASS | header 1 / zone 2 / store 58 buy-now digital -> 200, order 91399 module_id=3 | clean (mismatch WARN as designed) |
| AC1 cart | PASS | user 1 cart row 972 stamped module 1; place w/o buy-now header 1 -> 200 order 91400 module_id=3, cart emptied | clean |
| AC2 delivery | PASS | store 1 header 10 zone 1 -> order 91401 module_id=1 original_delivery_charge=1.00 (module 1 fixed 1.00; module 10 NULL rates would give 0.00); equals header==store 91402 | clean |
| AC2 surge | UNVERIFIABLE-live | surge_prices/surge_price_dates 0 rows; phpunit (d) x2 green | n/a |
| AC3 cap | PASS | store 58 header 1 COD qty7 (377.58) -> 203 order_amount, MAX(id) unchanged 91402 | clean |
| AC3 mirror | PASS | store 12 header 3 COD 567.00 -> 200 order 91403 module_id=1 | clean |
| AC-LOG | PASS | mismatch WARN on every header!=store call, correct keys, no raw header/PII; header==store (91402, group child 91407) -> no line; module_zone_missing unreachable live (0 eligible stores), phpunit covers | clean |
| AC-REG | PASS | 91402 same shape; get-Tax header1/cart1/store58 -> product_price 114.16 (control header3 -> 0); parcel 91405 stamped header module 10 | clean |
| AC-TEST | PASS | 69 tests / 399 assertions OK | n/a |
| Sweep update_payment_method | PASS | 91404 (header1, store58, 377.58) -> PUT payment-method COD -> 203, row unchanged | clean |
| Sweep group place | PASS | group 3f64a660 children 91406 (store58) module 3, 91407 (store35) module 1 | clean |
| Regression candidate parcel | CONFIRMED | 91405 parcel COD 1005 > module-5 cap 1000 placed with header 10 | silent (no log) |
