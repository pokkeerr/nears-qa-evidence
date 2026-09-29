# NEARS-3878 exact-cent before/after (QA live run, code 977ae9912, private DB copy, scale 2)

Fixture: user 6, COD, zone 2, stores 12 (items 12.00) and 13 (items 26.67), module_zone fixed delivery 3.55, VAT 5% order_wise, coupon = 10% percent, max_discount 1.00, limit 1 (code redacted).

| | items | coupon | tax | delivery | payable |
|---|---|---|---|---|---|
| AFTER (live, order 91420) s12 | 12.00 | 1.00 | 0.55 | 3.55 | 15.10 |
| AFTER (live, order 91421) s13 | 26.67 | 0.00 (coupon_applied stays true) | 1.33 | 3.55 | 31.55 |
| AFTER total | 38.67 | 1.00 | 1.88 | 7.10 | 46.65 (response total_amount 46.65) |
| BEFORE s12 (engineer-computed, NOT re-run live) | 12.00 | 1.00 | - | - | 15.10 |
| BEFORE s13 (engineer-computed, NOT re-run live) | 26.67 | 1.00 | - | - | 30.50 |
| BEFORE total (engineer-computed) | | 2.00 | | | 45.60 |

Live AFTER numbers equal the engineer's recorded AFTER numbers to the cent. Customer pays 1.05 more than at base (coupon cap now honoured basket-wide).

Reconciliation (items - coupon + tax + delivery): s12 12.00-1.00+0.55+3.55=15.10; s13 26.67-0.00+1.33+3.55=31.55.

## Tie case (C7)
The engineer's example "4.375% of 12.00" is NOT a real tie on the shipped schema: coupons.discount is decimal(24,2), so 4.375 is stored as 4.38 (QA read the row back: 4.38). 12.00*4.38% = 0.5256, a non-tie. A tie needs items*pct to end in exactly .xx5 with pct at 2 dp: QA used items 12.50 (item 576 price set to 2.50 in the copy, qty 5) and a 5.00% coupon: 0.625 -> 0.63.
Live (order 91442, single store 51, header moduleId=1, store module 2): coupon_discount_amount 0.63, tax 0.59, delivery 0.00, order_amount 12.46; 12.50-0.63+0.59+0.00 = 12.46 (reconciles exactly). get-Tax preview: discount 0.63, tax 0.5935 -> 12.50-0.63+0.5935 = 12.4635 -> 12.46 == placed order_amount.
BEFORE for the tie (not re-run live): discount subtracted unrounded 0.625 but stored 0.63, so order_amount 12.5-0.625+0.59 = 12.465 -> 12.47 vs parts 12.46.
