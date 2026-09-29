# NEARS-3885 QA (backend-only, no device) - cycle 0

Backend: /Users/Apple/Projects/nears-NEARS-3885-group-money-rounding @ 4679dd9f2 (php -S 127.0.0.1:8103, private DB multi_food_db_qa_bug3885; freshness check PASS)
DB proof: cross_module_basket flipped 0->1 on the copy only; GET /api/v1/config on :8103 returned true, shared multi_food_db stayed 0.
Pins mirror Nears3885GroupMoneyRoundingTest on the COPY only (VAT 5% deactivated to match the test DB, admin free delivery off, distance billing 2.5/km, fees 1.125 / 1.255, tips as per case). Everything restored afterwards.
Response payment_token values redacted. Server generates its own X-Request-Id (inbound header ignored): the id in each *.hdr file is the one grepped in laravel.log.

## Per-precision (tip 1.5 store 12, additional charge 1.125, packaging 1.255)
| p | single store 12 stored | group children (12 / 13) | response total_amount | round(sum) |
|---|---|---|---|---|
| 0 | 24.00 (base 23.88) | 24.00 / 47.00 | 71 | 71 |
| 1 | 23.40 (base 23.38) | 23.40 / 47.10 | 70.5 | 70.5 |
| 2 | 23.38 (unchanged) | 23.38 / 47.10 | 70.48 | 70.48 |

## Residue (p=2, fees 0): positive control raw float sum vs round
- res_above children 19.50 + 44.74: raw 64.24000000000001, response 64.24 raw text
- res_below children 19.54 + 44.72: raw 64.25999999999999, response 64.26 raw text
- mixed p1 (12 + food 51) 23.40 + 33.80: raw 57.199999999999996, response 57.2; validate per-store amounts == stored (p0 24/34, p1 23.4/33.8)

## AC2b partial_payment group, RESIDUE_ABOVE (raw 64.24000000000001)
- wallet 64.24 -> 403 partial_payment; orders 199->199, order_groups 20->20, wallet unchanged; log line reason=wallet_covers_total (ac2b_403_expected_logline.log)
- wallet 64.23 -> 200 group_placed, wallet allocations 19.49 + 44.74 (0.01 unpaid)

## Gates (p=2)
- wallet == stored 21.87 -> 200; 21.86 -> 203 order_amount (no order)
- partial wallet == stored 20.76 -> 200; 20.77 -> 203 partial_payment (no order)
- COD cap == stored 21.87 -> 200; cap 21.86 -> 203 order_amount (reason cod_cap, no order)
- p1: wallet 23.38 vs new stored 23.40 -> 203 Insufficient balance

## AC-REG p=2 stored: 23.38 / 20.76 / 21.87 / 22.13 / 19.50 == expected base
## BE-log: be-log-check.txt - 0 [FAIL]/[ERR] on any request id; expected WARN rejection lines present on the 403/203 requests (channel live)
## Automated: phpunit Nears3885GroupMoneyRoundingTest|Nears3856BackendLoggingGapsTest|PersistedMoneyRoundingGateTest = 75 tests OK, 1475 assertions
