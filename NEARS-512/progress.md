# NEARS-512 QA progress (live, append-as-observed)
Build: worktree feat/NEARS-512-checkout-cleanup @ c8dca855 | device emulator-5556 | backend 127.0.0.1:8000 (200)

## Automated backstop
`flutter test test/features/checkout test/features/cart` -> All tests passed! (100 tests). Includes new tests:
- deliveryman_tips_section_no_save_checkbox_test.dart (AC-4: save-tip checkbox gone, chips remain)
- checkout_controller_test.dart (order_type forced delivery)

## AC-2 part 2 (Cart still has Substitution) — PASS
Cart screen shows "Substitution Preferences" card + radio options (Remove/I'll wait/Please cancel/Call me ASAP). Cart has 3 items. Evidence: ac2-cart-substitution-present.png
ETA banner "Arriving in ~20 mins" also visible on Cart.

## Checkout top — observed (AC-2/AC-3/AC-5 partial) — PASS
Order top->down: ETA banner "Arriving in 1-15 min" (STAYS, AC-5) -> map -> Review Items -> Delivery Address (name/contact/address fields render, NOT hidden, AC-3). NO Substitution Preferences card (AC-2 part1). NO delivery-type/order-type picker (no Home Delivery/Take Away selector) anywhere visible (AC-3). Evidence: ac3-checkout-top-eta-delivery-no-picker.png

## AC-4 (tips, no save checkbox) — PASS (visual + tree)
"Delivery Partner Tips" section: header + info icon + quick-amount chips (Custom, Not now, 15, 10, 20, 40, Most Tipped). NO "save this tip for next time" checkbox between chips and Payment Method. Tree find "save this tip"/"Save this tip for next time" -> empty. Promo code field above intact. Evidence: ac4-tips-section-no-save-checkbox.png

## AC-4/AC-5 functional (tip reflects in total) — PASS
Tapped "20" tip chip -> chip highlights mint, Order Summary "Delivery Partner Tips (+) 20", Total Amount 22-2+20 = 40. Still NO save-tip checkbox after selection. Evidence: ac5-tip-selected-reflects-in-total.png

## AC-4 (Custom option opens amount input, no checkbox) — PASS
Tapped "Custom" chip -> chip row collapses into editable amount field "0.0" + X to revert (custom amount input opens). NO save-tip checkbox in custom mode. Tree find "save this tip" -> empty. Order summary tip back to (+) 0, Total 20. Evidence: ac4-custom-tip-input-no-checkbox.png

## AC-3 (delivery section + instruction render, no picker, no gap) — PASS
Flow renders unconditionally: Delivery Address -> "Add More Delivery Instruction" (DeliveryInstructionView, NOT hidden) -> Preference Time (Instant) -> Available Coupons/Promo -> Delivery Partner Tips. NO order-type/delivery-type picker anywhere. No orphaned whitespace where picker was removed (Delivery Address flows straight into Delivery Instruction). Evidence: ac3-delivery-instruction-renders-no-gap.png
order_type=delivery verified at code level (initCheckoutData forces _orderType='delivery'; both placeOrder payload sites drop take_away arm) + unit tests green. NOT placed (verified at validation boundary only).

## Clean post-removal checkout (UX review) — captured
checkout-post-removal-clean-top.png (ETA banner -> map -> Review Items -> Delivery Address; no Substitution card, no order-type picker).
Runtime: ui_errors clean; run-log no overflow/exception (only benign Google Play cert warn + Firebase-disabled notice, neither in scope).

## Regression sweep — PASS
- Dark mode: Dark Mode toggle already ON; ALL checkout shots above are dark-mode render -> clean, no orphaned gaps. (regression-checkout already dark)
- RTL/Arabic: switched Language->عربى. Cart still shows "تفضيلات الاستبدال" (Substitution) + radios + ETA "يصل خلال ~20 دقيقة". Checkout RTL: ETA banner present, Delivery Address + fields mirror correctly, NO Substitution card, NO order-type picker, tips chips render, NO save-tip checkbox (find "حفظ"->empty), Order Summary intact, no orphaned whitespace. Evidence: regression-cart-substitution-arabic-rtl.png, regression-checkout-arabic-rtl-top.png, regression-checkout-arabic-rtl-tips.png
- Tip submission path intact (chip select -> total updates; custom opens input). No place-order performed.
