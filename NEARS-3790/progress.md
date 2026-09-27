# NEARS-3790 QA progress (cycle 0) — emulator-5564, build from worktree @26fd004a0
- EN 1.0x: Flash Sale 176x290 (grocery+pharmacy+food), Best Reviewed 176, Most Popular 160, JFY 176, Trending 2-col 202x325, Item View-All 2-col 201x325, Category grid 209x273, Store grid 209x273, Store Recommended 150x240 — top-aligned, lead<=9.7dp, interior ink gaps<=17dp, one trailing gap below price. PASS
- Category storeSlot row: 24-36dp ink gap before name (44dp tap band) — intentional per UX/conductor; noted.
- EN 1.3x: all above sites clean, Flash 176 organic STACKS (badge x=10.7dp start edge, name full width); 209 cells badge beside, name avail 95.7dp.
- Reorder rail 116x190 EN 1.3x: organic badge side-by-side, name collapsed to 0 width, RenderFlex overflowed 7.9px (n_item_card.dart:1226) — FAIL AC5
- Reorder rail 116x190 EN 1.0x: stacked badge, 2nd name line clipped mid-glyph under price — FAIL AC5
- Badge/name widths (hseg.py, navy-pill scan): Flash 176 EN1.0 beside, name avail 78dp; EN1.3 STACKED at start edge x=10.7dp; AR1.0 beside (RTL end edge x=13.3-61), name avail ~101dp; AR1.3 beside, name avail ~95dp. Category/Store 209: EN1.3 name avail 95.7dp; AR1.3 badge at left (end) x=10.3-66.7.
- AR stacked-badge right-edge (start) pixel check: NOT reachable on device — AR label 'عضوي' is short enough that 160-176/209 cells never stack, and the 116 rail's height gate keeps it beside. Covered only by golden n_item_card_rtl.
- Reorder rail AR1.0 + AR1.3: badge beside, name squeezed to ~25-34dp -> 1-char line 'ي', 'Fa...' — FAIL AC5 (no overflow log in AR: label narrower).
- Add control: 114 card/add pairs checked, add button bottom >= 8.0dp above image bottom everywhere — never overlaps badge/name/price.
- Logs: only overflow = n_item_card.dart:1226 Row @ Reorder rail EN1.3x (7.9px). Firebase init [FAIL] lines at launch are env (suffixed package), unrelated.
- Backstop: 13 n_item_card component test files 222/222 pass; NItemCard goldens 14/14 pass (pinned SDK 3.41.9). The 116x190 harness case runs at 1.0x only.

# Cycle 1 delta re-QA — emulator-5564, UserApp built from worktree @72980e95c (qa-run.sh, API_HOST=10.0.2.2:8093), own backend :8093 cwd=nears-NEARS-3790-itemcard-grid-spacing @72980e95c, customer@nears.com (read-only)
- AC5 Reorder "Reorder your usuals" rail 160x260 (6 items; 4 organic):
  - EN1.0: organic badge STACKED above name (pill x10-84dp), names whole (Fresh Organic Tomato 2 lines), unit kept except Tomato (2-line name -> meta dropped per ladder), no overflow. PASS
  - EN1.3: stacked, names whole lines (Orange Juice/1L, Organic/Bananas 2 lines; Tomato 1 line ellipsis), unit dropped on organic cards (expected), no overflow. PASS
  - AR1.0: badge BESIDE, pill x20.7-68.3dp -> name area ~76dp (>=70), names 1-2 whole lines, unit kept. PASS
  - AR1.3: badge STACKED at start edge (pill x82-140dp of 150) — first on-device AR stacked check (cycle 0: unreachable). PASS
- Store "Recommended For You" 150x240:
  - EN1.0 food (Spice Route): Chicago Style Cheese / Deep Dish Pepperoni / Spicy Jalapeno Burger / Thin Crust Margherita = 2 whole name lines + rating row + price, trail 8.3dp. PASS
  - EN1.3: rating dropped, names 2 whole lines, no overflow. PASS
  - AR1.0 food: same four 2-line cards keep 2 lines but DROP the rating row (trail 21dp vs EN 8.3dp). FAIL
  - AR1.3 grocery (Test Store) + food: every 2-line name renders as ONE ellipsized line ("…Fresh Cream", "…Croissants 4", Spicy Jalapeno Burger, Thin Crust Margherita, Chicago Style Cheese, Pepperoni Pizza) + meta/rating dropped + empty band (trail 29dp vs 9dp siblings); EN1.3 same cards = 2 whole lines. FAIL -> bug-ar-1.3x-store-rail-name-truncated-meta-dropped-mid-band.png
- Regression re-sweep: Flash Sale 176x290 (grocery EN1.0/1.3/AR1.0/1.3, food EN1.3/AR1.3), Best Reviewed/Most Popular 176/160x270 (EN1.0/1.3, AR1.3), Store grid 209x273 (EN1.0/1.3, AR1.3), Item View-All 201x325 (EN1.0/1.3): values match cycle 0, no band above name, one trailing gap, no overflow. PASS
- Logs: no NItemCard overflow at any site/scale/locale. One pre-existing overflow: n_appbar.dart:1136 Column 17px at 1.3x on store screen (not in diff) -> bug-store-appbar-overflow-17px-1.3x.log. Login 500 at first attempt = my backend missing oauth keys (env, fixed; correlation_id join app<->laravel.log verified).
- Backstop: packages/nears_dls flutter test 2497 pass / 2 known n_store_card_sentence_case_badges fails.

# Cycle 2 delta re-QA — emulator-5564, UserApp built from worktree @1b1edbbd1 (qa-run.sh, API_HOST=10.0.2.2:8093), own backend :8093 cwd=nears-NEARS-3790-itemcard-grid-spacing @1b1edbbd1, guest then customer@nears.com (read-only)
- New instrument: rt_eval.py — VM-service evaluate over live RenderParagraphs (full-precision h/y/maxLines/didExceedMaxLines); pixels via measure.py/cards.py as before.
- Store rail 150x240 Spice Route (food):
  - EN1.0: 4 two-line cards keep rating: 42+1+19+1+26=89/90, trail 8.3dp. PASS
  - AR1.0: same 4 cards: 2 whole lines, rating DROPPED. name 42 + gap 4 + price 29 = 75/90 -> band 15 + gap 4 = 19.0 == rating 19.0. Exact fit (42+19+29=90) lost to _nameFitSlack 1dp. AR price 29 vs EN 26 (+3.0). Pixel trail 21.3 vs EN 8.3. FAIL (strict: leftover not below rating height) -> bug-ar-1.0x-store-rail-rating-dropped-at-exact-fit.{png,log}
  - AR1.3: 1 whole line (27, ellipsized) + rating back (24) + price 38 = 89/90, gaps 0, trail 9.0dp; 2 lines impossible (54+38=92>90). PASS (cycle-1 29dp band gone)
  - EN1.3: 2 whole lines (54) + price 34, rating dropped, band 1. Chicago Style Cheese (discounted): 1 line + stacked strike (19) + price — whole line, no band. PASS (see followup)
- Store rail 150x240 Test Store (grocery): AR1.0 Fresh Cream 250ml 2 lines + unit + price trail 7.3 PASS; AR1.3 Fresh Cream/Croissants 1 whole line + unit back + price, trail 9.0 PASS; EN1.0/1.3 match (EN1.3 Fresh Cream 2 lines, unit dropped, band 1). PASS
- Reorder 160x260: EN1.3 stacked ORGANIC, whole lines (Orange Juice/Organic Bananas 2 lines; Low Fat Milk/Tomato 1 line), unit dropped on organic; AR1.3 stacked عضوي at start edge, whole lines. No overflow. PASS
- Regression: Flash Sale 176x290 EN1.0 (lead 7.4/2.7, trail 95.3/74.3 = cycle 0) + AR1.3 (Dish Soap, Navel Oranges beside badge 2 lines) PASS; Store grid 209x273 EN1.0 (trail 40.7 = cycle 0) PASS; 2-col item grid 201x325 AR1.3 PASS; Best Reviewed 176x270 EN1.0 bold PASS.
- Bold text (secure font_weight_adjustment=300, fw=w700 confirmed): store rail EN1.0 identical to non-bold (2 lines + rating); EN1.3 Spicy Jalapeno 2 lines ex=true (3rd line ellipsized), no 1-line name except discounted Chicago (strike kept). PASS
- Logs: no NItemCard [FAIL]/[ERR]/overflow. n_appbar.dart:1136 17px @1.3x pre-existing. Env [FAIL]s: Firebase init/FCM (suffixed pkg), GetPosition timeout (mock GPS).
- Backstop: packages/nears_dls test/components/n_item_card*_test.dart 307/307 pass.
