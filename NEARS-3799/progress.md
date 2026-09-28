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
