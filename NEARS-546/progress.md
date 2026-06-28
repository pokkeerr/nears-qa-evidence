# NEARS-546 QA progress (live, emulator-5556, customer@nears.com)

- Backend up :8000, cache:cleared. Coupons confirmed: NEARS10(id3)=percent/10/min20/max15/mod1; WELCOME5(id4)=amount/5/min15/max5; FOODIE15(id5)=percent.
- Automated backstop: CouponDiscountTypeTest 4/4 GREEN.
- AC5 PASS: NEARS10 badge "10% OFF" (not "AED 10 off"); WELCOME5 "5AED OFF". evidence AC5-coupon-badge-10pct-off.png (zone1)
- AC1 PASS: zone1 Nears Mart Mango subtotal 23 AED + NEARS10 -> Coupon Discount -2 AED (=10%, NOT flat -10), Total 21 AED. evidence AC1-nears10-applied-summary.png
- AC6 BLOCKER in zone1: module_zone(mod1,zone1).maximum_cod_order_amount=10 -> COD blocked for any NEARS10 order (min subtotal 20). Pre-existing config, NOT coupon bug. COD-cap toast properly logged (AppLogger.error paired -> no silent-fail). Moving AC6 to zone2/mod1 (cap 1000).
- AC2 PASS: Ghee x5 = 200 subtotal + NEARS10 -> Coupon Discount -15 AED (capped at max_discount; 10%=20 floored to 15). evidence AC2-maxcap-200subtotal-15cap.png
- AC3 PASS: Cola 16 subtotal + NEARS10 -> REJECTED (min purchase 20), Total stays 16, discount 0. Log: coupon_controller.dart:127 "the_minimum_item_purchase_amount_for_this_coupon_is 20 but you have 16". evidence AC3-minfloor-16subtotal-rejected.png + AC3-rejection-toast.png
- AC4 PASS: Cola 16 subtotal + WELCOME5 -> Coupon Discount -5 AED flat, Total 11. evidence AC4-welcome5-coupondiscount-line.png
- AC6 PASS: placed order #162 (zone2/mod1 store13 Fresh supermarket, Lemon Soda 22 subtotal, COD). DB orders.coupon_discount_amount=2.00 (=10%, NOT old flat 10.00), order_amount=19. Display "-2"==DB charge 2.00. evidence AC6-db-charge-crosscheck.log + AC6-order162-placed-confirmation.png + AC6-order162-summary-coupon.png
- REGRESSION PASS: checkout renders with coupon (total 20) and without (22); removing NEARS10 via X restores total 22; no crash in apply/remove or inline coupon strip (NEARS-500). evidence REG-coupon-applied-before-remove.png + REG-coupon-removed-total-restored.png
- PRE-EXISTING (not NEARS-546): cart_count_view.dart:64 RenderFlex overflow 36px (=known NEARS-630); pusher WS errors (no local Reverb). Both non-blocking.
- VERDICT: PASS (6/6 ACs).
