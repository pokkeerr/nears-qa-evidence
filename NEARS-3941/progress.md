# NEARS-3941 baseline-red (pre-fix) measurements

Base dc6f17be3, UserApp on emulator-5558 (1080x2400 px), private DB nears_qa_3941, backend :8121 (worktree cwd @ dc6f17be3).
Geometry: 320dp = `wm density 540`, 360dp = `wm density 480`; font via `settings put system font_scale`. Sticky Total row = `checkout_screen.dart:1090:47` on base (ticket says :1082).
Overflow px = FIRST-layout `[FAIL] framework_error` line for a fresh checkout entry (Flutter dedups later relayouts, so a tax flag arriving after first layout is NOT re-logged; see tax-incl row).
Node bounds are device px from uiautomator dumps (per-glyph nodes exist for the price). Positive control in every dump: `Total Amount` / `Place Order` nodes present.

| Variant | Total | Sticky-row overflow | Notes |
|---|---|---|---|
| EN 320dp x1.3, non-tax, 2-digit | 47.64 | **23 px** | exactly the ticket's number; file 16 |
| EN 320dp x1.3, non-tax, 3-digit | 112.25 | **41 px** | digits 619..950 px on-screen, ` AED` node starts 950, runs past 1080 (clipped); label ends 619 = first digit starts 619 (gap 0); file 08 |
| EN 320dp x1.3, non-tax, 4-digit | 1190.84 | **59 px** | digits end 1011 (still on-screen, at the 1013 content edge), ` AED` fully off-screen; file 11 |
| EN 320dp x1.3, TAX-INCLUDED (`system_tax_setups.is_included=1`), 3-digit | 106.90 | log says 41 (first layout, pre-tax); rendered ~145 (41 + Vat text 350px/3.375=104) | **DIGITS CLIP**: only `1`,`0` of `106.90` on-screen ([969..1080]); `6 . 9 0 AED` nodes have bounds [0,0][0,0]. files 09/10 |
| EN 320dp x1.3, Due Payment (partial), 4-digit | 1180.84 | 59 (first layout) ~57 after label swap | body row `bottom_section.dart:399:77` due_payment Row overflows 66 px; file 12 |
| EN 320dp x1.0 | 112.25 | none | label 68..491, digits 603..858, AED to 1013 (fits exactly); file 06 |
| EN 360dp x1.0 | 112.25 | none | file 07 |
| EN 360dp x1.3, 2-digit | 47.64 | none | file 17 |
| AR 320dp x1.3, 3-digit | 119.08 | none | label 552..1013, currency 68..203; file 14 |
| AR 320dp x1.3, 4-digit | 1190.84 | **13 px** | all glyphs on-screen; label right edge 1056; label left edge 595 == first digit edge 595 (gap 0); file 13 |

Per-digit growth 18 logical px (61 device px) at 320dp/1.3x.

## AC3 labels (320dp x1.3; files 03 EN, 15 AR)
EN: `Choose Payme…` (payment_section title, storeId==null path), `Cash on…`, `Apply coupon or prom…`, `Delivery Partner …` all ellipsized, NONE has a framework_error.
AR: only `الدفع عند الا…` (cash-on-delivery) ellipsized; title, coupon, tips render whole. No framework_error for any of the four.

## Other overflows seen on the same screen (not the Total row)
- `delivery_section.dart:566:17` address card Row: EN 320/1.3 125 px, EN 320/1.0 77 px, EN 360/1.0 37 px, EN 360/1.3 85 px, AR 320/1.3 87 px
- `checkout_screen_shimmer_view.dart:53:11` (NEARS-3873, ignored)
- `payment_method_bottom_sheet.dart:904:27` 27 px (wallet partial `remaining_bill` row, 4-digit)
- `bottom_section.dart:399:77` 66 px (due_payment body row, partial pay, 4-digit)
- `nears_dls n_item_card.dart:1964:19` RenderConstraintsTransformBox 19 px bottom (AR 320/1.3 cart/suggested item card; basket screen)

## Delta re-QA fix-cycle 2 (qa_sha 8b2c042cc, emulator-5558, wm size 1080x2400, prefix fix2-)
Backend: /Users/Apple/Projects/nears-NEARS-3941-checkout-total-row @ 8b2c042cc (backend-freshness-check 8121 PASS; DB nears_qa_3941). Full per-cell table: fix2-measurements.md.
- Cell 1 EN 320dp/1.3x non-tax 1190.84: label 'Total'/'Amount' whole words, price 1190.84 AED whole; price span 586->536 px (x0.915), label slot 318->368 px, bar 580->459 px. PASS
- Cell 2 EN 320dp/1.3x tax-incl 3d 113.41 + 4d 1134.13: '(Vat/Tax Incl.)' unbroken. PASS
- Cell 3 EN 320dp/1.3x Due Payment 4d 1180.84: 'Due'/'Payment' whole (ink 350 px of 368 slot). PASS
- Cell 4 AR 320dp/1.3x non-tax 4d 1190.84: 'المبلغ'/'الإجمالي' whole, label flush right, price LTR left, real device Arabic font. PASS
- Cell 5 AR 320dp/1.3x tax-incl 3d/4d: wraps between words only; widest token 'المضافة/الضريبة' ink 292 px vs slot 377 (4d); 3d widest line 410 px vs slot 438. PASS
- Cell 6 AR 320dp/1.3x Due Payment 4d 1180.84: 'الدفع'/'المستحق' whole. PASS
- Cell 7 non-regression: 3-digit EN/AR at 320/360 x 1.0/1.3, 4-digit at 320/1.0, 360/1.0, 360/1.3: price span, label slot and bar height byte-identical to first post-fix run (price scale 1.0). PASS
- Sticky-row overflow lines: 0 in every cell and 0 in the whole session log. Other overflow lines are pre-existing non-sticky: checkout_screen_shimmer_view.dart:53 (NEARS-3873), n_item_card.dart:1964, bottom_section.dart:399, payment_method_bottom_sheet.dart:885/904.
- flutter test test/features/checkout/checkout_sticky_total_row_overflow_test.dart: 164 passed.
