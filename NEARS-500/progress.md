# NEARS-500 QA progress (live, append-as-observed)

- build: worktree /Users/Apple/Projects/nears-NEARS-500-coupon-checkout @ 0b3c3470, branch feat/NEARS-500-coupon-checkout
- device: emulator-5556 (Android), lock held
- backend: http://127.0.0.1:8000 HTTP 200
- baseUrl: http://10.0.2.2:8000 (real local backend, not demo) — OK

## Pre-flight checkpoints
- [x] automated backstop: coupon_section_strip_test.dart 6/6 PASS
- [x] seed data confirmed: NEARS10 (10% cap15 min20 mod1), WELCOME5 (flat5 min15 mod1), FOODIE15 (mod2), PHARMA20 (mod3)
- [x] module scoping confirmed at endpoint: grocery (mod1) coupon list = [NEARS10, WELCOME5] only; FOODIE15 in mod2 only — module-bleed prevented at source

## Live AC checkpoints
- [x] AC-1/AC-6 PASS — grocery all-stores listing scrolled top->bottom (7 positions, pos0..pos6). Promo coupon card (NEARS10 "10% off your order / Min Order of 20") ABSENT at every position. Other rails render: hero banner, Categories, Buy It Again, product grids, Stores grid w/ filter chips. No runtime errors. shots 01-grocery-home-pos0..6.png
- [x] AC-2/AC-3 PASS — grocery (module-1) checkout, cart subtotal AED 20. "Available Coupons" strip renders ABOVE Place Order with non-empty title; chips = NEARS10 + WELCOME5 (horizontal ListView). Manual "Promo Code" field + Apply + "Add Voucher" retained BELOW strip. shot 04-checkout-coupon-strip.png
- [x] Module-bleed PASS — only NEARS10 + WELCOME5 in strip; FOODIE15 (mod2) / PHARMA20 (mod3) ABSENT (also confirmed at endpoint: mod1 list = [NEARS10, WELCOME5]).

## AC-5 apply (NEARS10) — observed
- cart subtotal AED 22 (carrots x11), prior item-discount AED 2 baked in.
- Tapped NEARS10 chip -> chip shows SELECTED (mint fill + check), "COUPON APPLIED" badge, promo field shows NEARS10 w/ clear-X, Total dropped 22 -> 10. shots 05b/05c.
- NOTE: Coupon Discount line = AED 10 (flat), NOT 10% of 22 (~AED 2.20). ROOT CAUSE (pre-existing, NOT NEARS-500): CouponController._processCoupon checks discountType=='percent' but API/DB returns 'percentage' -> percent branch skipped -> raw discount(10) applied as flat amount. NEARS-500 did NOT touch coupon_controller.dart (git-confirmed). Manual Apply path uses identical applyCoupon() -> same bug. => regression_bug (pre-existing), shared by manual+strip. Strip's OWN behavior (apply via existing path, selected state, total decrease) works.
- [x] AC-5 swap PASS — tapped WELCOME5: NEARS10 deselected, WELCOME5 selected, promo field=WELCOME5, Coupon Discount swapped -10 -> -5, Total 22->15 (no double-stack). shots 06a/06b.
- [x] AC-5 toggle-off PASS — tapped applied WELCOME5 again: both chips deselected, COUPON APPLIED badge gone, promo field emptied + Apply restored, Coupon Discount line gone, Total restored to AED 20 (22 - 2 item). shots 07a/07b.
- [x] AC-5 BOUNDARY respected — verified total UPDATE only. NO order placed, NO payment, NO persistence. No runtime errors throughout.
- NOTE: WELCOME5 (amount) computed correctly at AED 5; NEARS10 (percentage) mis-applied as flat 10 per pre-existing controller bug (see bug log). Strip mechanics (apply/swap/toggle/selected-state/total-update) all correct.
- [x] Manual-path parity PASS — typed NEARS10 in promo field + Apply: COUPON APPLIED, Coupon Discount -AED 10 (IDENTICAL flat mis-calc to strip). Confirms percentage-coupon bug is shared/pre-existing, not strip-introduced. Manual promo-entry WORKS with strip present (regression sweep item). Strip chip reflects manually-applied coupon (NEARS10 selected) — bidirectional state sync. shots 08d/08e.
- [x] AC-4 (zero-coupon hide) — NOT live-reachable in seed: both NEARS10+WELCOME5 are global module-1 coupons valid for EVERY grocery store in zones 1&2, so no zero-coupon grocery checkout exists. Strip empty-path hide-logic (coupons.isEmpty -> SizedBox.shrink, manual field preserved) is covered by automated test #2 (PASS) + code review (coupon_section.dart:305). Documented as reasoned per AC-4 instruction.

## Regression sweep
- [x] Dark mode PASS — Dark Mode toggle ON entire run; navy/mint theme renders correctly on strip + chips + checkout (shots throughout). No contrast/overflow issues.
- [x] RTL/Arabic PASS — switched to Arabic; strip header reads "الكوبونات المتاحة", promo field "الرمز الترويجي" + "أدخل الرمز الترويجي", "أضف قسيمة" (Add Voucher), chips WELCOME5/NEARS10 RTL-mirrored, no overflow. shot 12b. RTL apply works: NEARS10 selected + localized snackbar "لقد حصلت على خصم د.إ. 10". shot 12c. No runtime errors.
- [x] Grocery home content intact after card removal — all rails render (AC-1/AC-6 sweep).
- [x] Manual promo-entry still works with strip present (covered under manual-parity).
- [x] No runtime errors / red screens / overflow at ANY point (get_runtime_errors clean x5).

## VERDICT: PASS
All NEARS-500 ACs demonstrated live on emulator-5556 (Android, dark mode + RTL).
- AC-1/AC-6 PASS, AC-2/AC-3 PASS, AC-5 (apply/swap/toggle, boundary respected) PASS, AC-4 reasoned+test-covered, module-bleed PASS.
- Automated backstop: coupon_section_strip_test.dart 6/6 PASS.
- No order placed / no payment / no persistence (AC-5 hard boundary honored).
- task_bugs: none (no defect in the NEARS-500 change).
- regression_bugs: 1 pre-existing — percentage coupons applied as flat amount (CouponController._processCoupon discountType=='percent' vs API 'percentage'); shared by manual+strip; git-confirmed NEARS-500 did not touch coupon_controller.dart. See bug-percentage-coupon-flat-applied.log.
