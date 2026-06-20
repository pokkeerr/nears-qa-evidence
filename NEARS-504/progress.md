# NEARS-504 QA — live results (emulator-5556, build b746508b @ feat/NEARS-504-viewcart-floating)

Backend: live local php artisan serve :8000 (crashed mid-run, restarted). Zone 2 Abu Dhabi.
Logged in: customer@nears.com (guest cart-add returns 403 → had to log in).
Driving: TalkBack semantics (focus + double-tap) required — this build's NearsPrimaryButton
(GestureDetector) does not respond to raw adb taps.

## Verdict: FAIL — universal 2px bottom overflow on the restyled cart bar.

| AC | Result | Evidence |
|----|--------|----------|
| AC-1 no overlap on Search | PARTIAL/FAIL | bar floats ABOVE navy nav (no overlap, distinct layers) BUT shows "BOTTOM OVERFLOWED BY 2.0 PIXELS" + clipped "N item" subtext. ac1-search-cartbar-above-nav-OVERFLOW.png |
| AC-2 glassy style | FAIL | 2px overflow; "N item" subtext clipped; bar not a clean glass pill. ac2-cartbar-nav-closeup.png |
| AC-3 other render sites + empty hidden | FAIL (bar) / PASS (empty) | Store Detail + Store Item Search both overflow 2px. Empty-cart → bar hidden on Search, Store Detail, Basket (PASS). ac3-* shots. |

## Additional checks
- Dark mode: price text = sky #8FB4FF (CORRECT, not navy/mint); mint CTA OK; BUT 2px overflow present. ac-darkmode-cartbar-price-sky-OVERFLOW.png
- Cart count/price update correctly on add/remove (regression clean).
- Automated: flutter test bottom_cart_widget_test.dart = 4 PASS (does NOT catch the device overflow).

## THE BUG
"BOTTOM OVERFLOWED BY 2.0 PIXELS" on BottomCartWidget — all 3 render sites, light+dark.
Content Column (price + "N item" subtext) doesn't fit the fixed 64dp content height with internal
vertical padding. "N item" subtext is clipped. bug-cartbar-bottom-overflow-2px.{png,log}
