# NEARS-3979 QA progress (HEAD 946fd2f36, emulator-5570, backend :8179 own worktree, DB nears_qa_3979, proxy :8180)
- AC8 PASS: preview VAT 1.75/Total 38.75, confirm sheet 38.75, placed orders 91575+91576 sum order_amount 38.75, VAT 1.75. get-Tax store12 carries coupon_code Q3976M20 (coupon_discount_amount 5.0), store14 no code.
- AC9 PASS: Clear -> VAT 2.00/Total 44.00 (bodies code-less); re-apply -> 1.75/38.75, no checkout reopen. NOTE AC9 text "Total 39.00" is the with-coupon pre-fix figure; no-coupon total = 40+2+2 = 44.00.
- AC8 placed: orders 91575(12: 16.75, tax 0.75)+91576(14: 22.00, tax 1.00) = 38.75 / VAT 1.75. group/place coupon_code Q3976M20 amount 5.0.
- AC10 PASS: Q3979P10 both stores carry code (coupon_discount_amount 2.0 each, tax 0.9 each); preview VAT 1.80/Total 39.80, confirm 39.80; placed 91579+91580 = 39.80, VAT 1.80.
- AC11 FD PASS: Q3976FD15 get-Tax bodies code-less both stores (coupon_discount_amount 0.0); preview VAT 2.00/Delivery 0.00/Total 42.00 == placed 91583+91584 = 42.00 VAT 2.00. (FD coupon sheet stays open after apply - observed, not in diff scope.)
- AC11 no-coupon PASS: code-less bodies; preview VAT 2.00/Total 44.00 == placed 91587+91588 = 44.00, VAT 2.00.
- AC12 single-store PASS: store 12 5x4 + Q3976M20: single get-Tax (single-store body, distance 0.956, coupon_code+5.0), VAT 0.75, Total 16.75 (path untouched).
- AC12 mixed PASS: flag ON, store12 (grocery) + store49 Spice Route (restaurant): per-store get-Tax bodies code-less with Q3976M20 applied (coupon_discount_amount 0.0, no coupon_code); group/validate carries code (as before). Preview Total 62.28 (not placed).
DML(private copy nears_qa_3979): coupons id=24 Q3976M20 status 1->0 at 23:27:29
DML: coupons id=24 status 0->1 (restore) 23:28:12
DML: coupons id=24 status 1->0 (forced refusal) 23:30:01
DML: coupons id=24 status 0->1 23:30:57
DML: coupons id=24 status 1->0 after apply GET (race) 23:31:33
DML: coupons id=24 status 0->1 (restore after failed race) 23:31:56
DML: coupons id=24 status 1->0 delayed flip 23:32:08
- AC15 PASS: basket 20+20, Q3976M20 applied (preview 38.75 w/ 15 tip=53.75 prior), coupon flipped inactive between coupon/apply and get-Tax. get-Tax store12 [code] -> 403 {"errors":[{"code":"coupon","message":"Coupon expire"}]} then code-less retry -> 200 (tax 1.00). Exactly 1 [FAIL] "checkout: group per-store tax non-200" (logcat). Store 14 body code-less 200. UI: VAT 2.00, Total 54.00 (incl 15 tip), Place Order enabled, no Retry row.
DML: coupons id=24 status 0->1 FINAL RESTORE 23:33:12
- TRUNCATED Q3979F25 (informational): store12 get-Tax code (coupon_discount_amount 20.0 -> tax 0), store14 code-less (tax 1.00). Preview VAT 1.00 / Total 18.00; charged orders 91597 (1.00, tax 0) + 91598 (16.75, tax 0.75) = 17.75, VAT 0.75. Preview HIGHER by 0.25 = 5% x 5.00 (never lower). 
- CAP8 (informational, exact): store12 code (8.0, tax 0.60), store14 code-less (1.00); preview VAT 1.60/Total 35.60 == placed 91601+91602 = 35.60, VAT 1.60.
- SW12 first attempt: item 61 stock exhausted by my own 6 placed orders x10 (69->9): store14 code-less get-Tax 403 stock "Large Brown Eggs Is out of stock" (blockReason stock), 1 [FAIL] non-200 for store14, store12 body carries Q3976SW12 (4.0 -> tax 0.80). Fixture side-effect, not a defect. Re-run with qty 4 for eggs (no DML).
- SW12 (informational) PASS: store 12 code Q3976SW12 (tax 0.80), store 14 (out of scope, qty 4 = 8.00) code-less 200 (tax 0.40), no 403, Total not withheld; preview VAT 1.20/Total 27.20 == placed 91605+91606 = 27.20, VAT 1.20; no [FAIL] other than GetPosition noise.
