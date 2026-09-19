
## 8-fix4 (C8 delta, 2026-09-19, emulator-5554, sha c31b05f38, backend :8636)
- C8 live: NEARS3636EXP card (only card) shows "EXPIRES IN 2 DAY(S)" / AR "تنتهي خلال 2 يوم"; device clock 14:37 +04, expire_date "2026-09-21" -> 00:00 local = ~33h -> ceil(33/24)=2. Other 7 cards: no tag.
- EN 1.0x / AR 1.0x / AR 1.3x tag fully visible; EN 1.3x tag TRUNCATED "EXPIRES IN 2 ..." (reproduced twice) -> bug-c8-expiry-tag-truncated-en-1.3x.png
- Analytics: view_promotion expiring_count=1, coupon_apply_tapped coupon_id=21 expiring_soon=1 (multi-store basket -> routed to Basket, no apply).
- API raw expire_date id 21 = "2026-09-21" (date-only) -> c8-api-raw-expire-date.log
- Logs: 0 [FAIL]/[ERR]/RenderFlex since first Coupons load.

## 8-fix5 (FINAL delta, 2026-09-19, emulator-5556 (own AVD Pixel_10_Pro_2), sha d7a093f83, backend :8636 own server)
- Env: backend :8636 pid died once mid-run (own server, after 4 cart/update socket failures at 15:33:11-26, logged [FAIL] socket transport = env, not product); restarted, re-did the qty taps.
- Basket: single store Fresh supermarket, Dish Soap 500ml x5, Items Total 40.25, Discount -6.84, store total 33.41.
- R7 PASS: HIMIN 'Add 24,966.59 AED more to use' (25000-33.41=24966.59); NEARS2924QA 'Add 466.59 AED more' (500-33.41); Apply en=false on both; eligible cards (PCT, AMT, FDOK, BND, BND2, EXP) sort before the ineligible ones. dump f5-r7-himin-eligibility-dump.xml
- R5 partial: EXP card label '...NEARS3636EXP 10% off ELIGIBLE EXPIRES IN 3 DAY(S)' (only card with the tag). device 15:3x +04.
- Env note: first cart-remove of Cream Cheese (store 35) was tapped while my own backend was down -> UI removed it optimistically, server row 853 stayed -> server-side multi-store cart -> get-Tax 403 'Please select items from the same store' retry loop (1/s). App relaunched (adb force-stop + monkey), Cream Cheese re-synced, removed again with server up (DB SELECT: only cart row 855 Dish Soap for user 6/is_guest 0/module 1). Guest rows 34/36 (is_guest=1) irrelevant.
- R1 PASS (15:40): Coupons Apply NEARS2924PCT (coupon_apply_tapped coupon_id 16 -> coupon_applied result success source coupons_page) -> Basket (5x Dish Soap, 33.41) -> Proceed with NO edit -> checkout 'NEARS2924PCT · 3.34 AED OFF', Coupon Discount -3.34, Total 31.57. shots f5-r1-*.png, dump f5-r1-checkout-dump.xml. 0 [FAIL]/[ERR].
- R2a PASS (15:42): Apply PCT -> Basket qty 5->4 (26.73, still >= min 20) -> Proceed -> 'Apply coupon or promo code' placeholder, no Coupon Discount row. 0 FAIL/ERR. f5-r2a-*.png
- R2b PASS (15:44): Apply PCT -> qty 4->2 (13.36 < min 15) -> Proceed -> placeholder, no coupon. f5-r2b-*.png
- R2c positive control PASS (15:45): qty back to 4 (26.73), Apply PCT, Proceed no edit -> 'NEARS2924PCT · 2.67 AED OFF' (10% of 26.73). f5-r2c-*.png
- R3 UNVERIFIABLE (both sub-rows): the only campaign in module 1 (item_campaigns 16, store 8) is not rendered on any Grocery surface (JustForYou is Food/Shop only; no campaign banners in zone-2 module-1), and the only unexpired coupons are module 1 (ids 16,17,21,22, plus 15/18-20); FOODIE15 (id 5, module 2) and PHARMA20 (id 6, module 3) expired 2026-09-06 -> a Coupons-page coupon cannot be armed for a Food/Pharmacy store, so a live campaign/prescription run would only prove 'different store => cleared', which the pre-cr-2 code also did (vacuous). No data improvised.
- R4 PASS (15:46-15:49): Apply PCT (coupon_applied success 15:46:55) -> Profile -> Logout(Yes) -> Sign In customer@nears.com (login {method: email}) -> re-pick address 'Abu Dhabi - United Arab Emirates' (zone reset to out-of-zone after login, app behavior) -> Basket (server cart back: Dish Soap x4 26.73, same store 13) -> Proceed -> 'Apply coupon or promo code', no Coupon Discount row. f5-r4-*.png. 0 FAIL/ERR.
- OBS (Low, analytics): view_promotion {screen: coupons, source: profile_menu} fires on every CouponController.getCouponList() incl. background loads by home_controller (L104/L361) and around checkout entry, i.e. while the Coupons page is not visible (logcat 15:48:43, 15:49:21, 15:49:45).
