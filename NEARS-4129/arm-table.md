# NEARS-4129 arm table (observed; clone multi_food_db_qa4129; wallet vendor 4 earning 1200 / withdrawn 800 / pending 100 = balance 300; package 1 = 50)
| Arm | BASE (87f15d3b0 controllers on scratch copy, :8130) | FIXED (b20e5698885c, :8129) |
|-----|------|-------|
| AC1 admin A (no bill) N=2 parallel | +50 withdrawn, 2 grants (RED, lost update) | +100, 2 grants |
| AC1 admin A N=5 | +50, 5 grants | +250, 5 grants |
| AC1 admin B (bill 25) N=2 | +75, rows paid 75,75 | +125, rows 75,50 |
| AC1 admin B N=5 | +125 (run2; run1 +75), 5 grants | +275, rows 75,50,50,50,50 |
| AC2 admin A drained to 50 (5 serial buys) then 2 parallel | BOTH succeed (two grants, one debit; ends 0.00, masked) | 1 success + 'Insufficient balance in wallet' toast, ends 0.00 |
| AC2 case C single (326>300) | refused, wallet identical, NO [FAIL] line | refused, wallet byte-identical, 1 [FAIL] insufficient_balance, correlation_id == X-Request-Id |
| AC3 single renew A | +50, 1 row, toast Renewed | +50, 1 row, toast Renewed |
| AC3 single shift A->pkg 2 | refund 32.143 credited, withdrawn +9.99, 1 txn, old sub status 0, new sub, toast Shifted | same shape (refund 32.157 time-prorated), toast Shifted |
| AC5 API B N=2 overlapping | +150, paid 75/75 (stale-bill re-charge CONFIRMED) | +125, paid 75/50 |
| AC5 API B strictly sequential pair | +125, 75 then 50 (green) | +125, 75 then 50 (green) |
| line(2) lost-update arm, API A (no bill) N=2 / N=5 | +100 / +250 (REFUTED: NEARS-3523 lock holds) | +100 / +250 |
| API AC2 A drained then 2 parallel | 1x200 + 1x403 (3523 lock) ends 0.00 | 1x200 + 1x403 ends 0.00 |
| AC6 API fail pkg (shift, renew) | HTTP 200 application placed + refund credit 32.14 committed + old sub status 0 (RED) | HTTP 500 {errors:{message:'Something went wrong'}}, 5 tables byte-identical, 1 [FAIL] grant_failed each |
| AC6 admin fail pkg (renew, shift) | toast Something went wrong BUT shift commits refund 32.14 + old sub status 0 | toast Something went wrong, byte-identical, 1 [FAIL] grant_failed each |
| control pkg 1 on same clone | grants | grants (+50) |
| AC7 log shape | old '[FAIL] subscription wallet purchase failed' with manual request_id (seen on nopkg/arrpkg) | '[FAIL] subscription.api_purchase_refused' {store_id,reason}+correlation_id, no request_id |
