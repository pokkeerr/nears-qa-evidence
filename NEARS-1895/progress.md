# NEARS-1895 QA progress

Device: emulator-5558 (spare AVD NEARS_2411_QA booted fresh, pool was at effective_capacity=0).
Backend: primary tree Admin/ (php artisan serve :8000), reached via 10.0.2.2:8000.
Login: customer@nears.com / 123456789 (zone 1).

## AC1/AC2 — met-state row conveys meaning, unmistakable as price pair
- Repro config: stores.id=4 Burger Palace (minimum_order=8.00), items.id=16 Classic
  Cheeseburger (price=8.99), added Size=Large (+2.50) x2 -> subtotal 22.98 AED.
- Cart row renders: "Minimum order met (22.98 AED / 8.00 AED)" — EN.
- ui_errors: clean (0 matches).
- Screenshot: ac1-ac2-min-order-met-en.png, compared element-by-element against the
  original misread reference docs/qa-evidence/NEARS-1590/bug-cart-base-price-9-vs-8.png
  (bare "14 AED / 8 AED", no label) — new row unambiguously labelled.
- PASS.

## Regression — not-met branch + multi-store
- Added Pizza Heaven (store 5, min 10.00) Garlic Bread (4.99) qty 1.
- Basket shows BOTH sections correctly: Burger Palace "Minimum order met (...)",
  Pizza Heaven "Minimum order amount not reached" + "Add 5.01 AED more to reach minimum"
  (copy unchanged from pre-fix).
- ui_errors: clean.
- Screenshot: regression-multistore-met-notmet-en.png.
- PASS / clean regression.

## AC3 — EN+AR keys, RTL amounts stay LTR
- Switched language to Arabic (Settings > Language > عربى > تحديث).
- Row renders: "تم الوصول إلى الحد الأدنى للطلب (⁦د.إ. 22.98⁩ / ⁦د.إ. 8.00⁩)" — amounts
  isolate-wrapped (LRI/PDI marks visible in dump), digits read left-to-right, not mirrored.
- Not-met branch also renders correctly in AR, unchanged.
- ui_errors: clean.
- Screenshot: ac3-min-order-met-ar-rtl.png.
- PASS.

## Narrow-width overflow check (AR, ~320dp via wm size 960x2130)
- This ticket's row: full text intact in a11y tree, NO RenderFlex overflow logged against
  cart_screen.dart. Flexible wrap works as intended.
- FOUND (pre-existing, unrelated): RenderFlex overflow by 40px in a SIBLING widget,
  cart_item_widget.dart:410 (the variations/addons toggle Row) — NOT touched by this
  ticket's diff. Filed as regression_bugs (non-blocking).
- Screenshot: ac3-narrow-320dp-ar-no-overflow.png.
- Log: bug-cart-item-widget-variations-row-overflow-narrow-ar.log.
- wm size reset after capture.

## Automated backstop
- `flutter test test/features/cart/cart_screen_min_order_met_label_test.dart` -> 2/2 pass.
- `flutter test test/features/cart/` (full dir) -> 192/192 pass, no regressions.

## Verdict: PASS
