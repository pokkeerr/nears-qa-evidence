# NEARS-3799 QA [8] cycle 0 — emulator-5560, UserApp debug from worktree @ 9c9cefc05
AC1 EN/LTR flat menuRow — PASS (ac1-en-ltr-menurow.png)
AC2 AR/RTL mirror — PASS (ac2-ar-rtl-menurow.png, ac2-ar-rtl-instore-search.png)
AC3 text scale 1.0/1.3 — PASS (ac-textscale-1.3x-ltr.png); struck-price truncation task_bug (non-breaking)
AC4 food default list / non-food grid / toggle holds — PASS
AC5 Store-entry skeleton = list — PASS (ac-skeleton-store-entry-food.png)
AC6 id-only skeleton grid -> list once; non-food no change — PASS (contact sheets)
AC7 non-food regression — PASS (ac-nonfood-*)
AC8 description empty — PASS (automated)
AC9 HTML description — PASS (automated)
AC10 closed/unavailable — FAIL (chip truncated 'CLOS...', add not disabled) bug-menurow-closed-*
AC11 Customizable tag + single open — PASS
AC12 add -> stepper, live count — PASS (pre-existing cart-parse exception, layout-independent)
AC13 favourite persists — PASS
AC14 analytics — UNVERIFIABLE for add_to_cart (pre-existing throw); select_item/view_item/wishlist PASS
AC15 AC-LOG — PASS
AC16 DLS catalog/widgetbook/goldens — PASS

# cycle 2 (delta) — emulator-5560, UserApp debug from worktree @ 0425f002b, backend :8379 own (cwd worktree @ 0425f002b); device clock set 10:30 (+04) via cmd alarm set-time so store 5 items are schedule-closed
AC10 closed/unavailable — PASS: TB1 chip 'CLOSED'/'مغلق' full + centred, clear of heart at 1.0x LTR, 1.3x LTR, 1.3x RTL (c2-ac10-closed-en-1.0x.png, c2-ac3-closed-struck-1.3x-ltr.png, c2-ac2-rtl-ar-1.3x-closed-and-discount.png); TB2 closed rows expose no add node (store list + in-store search), '+' tap -> 0 cart/add (app+BE), opens item sheet; open item add POST cart/add 200 + stepper; grid of same store + non-food grid keep enabled add on CLOSED cards (intended); heart on closed item toggles (wish-list add/remove 200, DB 0->1->0)
AC3 text scale — PASS: TB3 struck '21.62 AED' + '7% OFF' pill full at 1.3x (c2-ac3-open-discount-struck-1.3x-ltr.png); struck '14.99 AED' full 1.0x/1.3x
AC2 RTL — PASS (c2-ac2-rtl-ar-1.3x-closed-and-discount.png)
AC7 non-food store 2 — PASS unchanged 2-col grid
AC14 analytics add_to_cart — UNVERIFIABLE: open item 125 (no add-ons) added; response carries whole shared cart -> NEARS-3808 Item.fromJson crash before _logAddToCart. add_to_wishlist/favourite_removed observed.
Regression candidates: compact NItemCard Table semantics assert (bug-compact-table-semantics-assert.log); AR discount pill hardcoded 'OFF' (item_card.dart:253, NEARS-1403).
Cleanup: cart row 948 (item 125) removed via customer API DELETE cart/remove-item (200), cart back to 9 rows; wishlist item 22 back to 0.
