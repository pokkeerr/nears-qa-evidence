# NEARS-515 QA progress — UserApp basket appbar icon removal
device: emulator-5556 | build: feat/NEARS-515-remove-basket-appbar-icon @95e526ce

## AC verdicts (live)
- AC-1 (Basket appbar, NO basket icon, fromNav=true): PASS — 01-basket-appbar-fromnav-light.png — title "Basket" centered, no back arrow (bottom-tab), clean trailing edge, no gap/remnant.
- AC-3 (bottom-nav basket tab clickable + badge): PASS (partial) — basket tab opened Basket page; mint badge "1" visible — 03-home-basket-entry.png / 01-*.png.
- No runtime errors on Basket page (ui_errors clean).
- AC-1 fromNav=false (pushed from store, back arrow shown): PASS — 01b-basket-appbar-fromstore-backbtn.png — back arrow left, title "Basket" centered, NO basket icon trailing, no gap.
- AC-2 (Checkout appbar, NO basket icon, centered title): PASS — guest 02-checkout-appbar-guest.png + populated 02b-checkout-appbar-populated-light.png — title "Checkout" centered, no trailing icon/remnant, no phantom right padding. No runtime errors.
- AC-5 (Basket->Checkout nav, back returns to Basket cleanly): PASS — 05-back-checkout-to-basket.png — back pops Checkout, lands on Basket, appbar intact, no errors.
- AC-3 (functional cart entries intact + clickable, removal scoped): PASS — 03b-home-appbar-cart.png shows Home appbar cart icon + bottom-nav basket badge "1"; Home cart icon tap -> opens Basket (03c-home-cart-opens-basket.png); bottom-nav Basket tab -> opens Basket (earlier). Removal scoped to dead glyphs only.
- AC-4 dark mode: PASS — Basket 04a-basket-appbar-dark.png + Checkout 04b-checkout-appbar-dark.png — both appbars navy, titles centered, NO basket icon, no gap/remnant. No errors.
- AC-4 RTL/Arabic: PASS — Basket 04c-basket-appbar-rtl-arabic.png ("سلة التسوق" centered, no icon, trailing edge mirrors clean) + Checkout 04d-checkout-appbar-rtl-arabic.png ("الدفع" centered, no icon). RTL layout mirrors correctly. No errors.

## Regression sweep
- REG cart badge add/remove: PASS — qty 1->2->1 (reg-badge-qty2.png), bottom-nav basket badge present, no errors. State restored to 1.
- REG appbar title centering (objective): appbar title node bounds [567,194][777,275] => x-center 672 = exact screen midpoint (1344/2). Title mathematically centered, no gap after icon removal.
- REG empty vs populated appbar: CustomAppBar/NearsAppBar built unconditionally, independent of cart count; empty-state Checkout appbar captured identical (02-checkout-appbar-guest.png). Verified-by-construction + guest empty-state shot.
- No runtime errors across all flows (ui_errors clean throughout).
