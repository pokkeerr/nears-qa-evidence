# NEARS-602 QA progress (fix-cycle 0)
Device: emulator-5556 | Build: worktree feat/NEARS-602-store-offers-chips (base feat/userapp-reskin @48d4d1e5)
Data: zone 2 (Abu Dhabi). Offers store candidates: Fresh supermarket (id13, 8 disc), Veggie Market (id18, 8 disc). No-offers store: only id59 NEARS-257 Fixture (zone 3). Max disc/store=8 (<10) -> AC4 page-2 unreachable via data.
Offers fetch limit=10.

## AC verdicts (append as observed)
- AC1 PASS: Fresh supermarket detail. Chip strip [All][Offers][General Items][Cheese][Juices] + All Products row (toggle+filter funnel) above grid; pinned on scroll (hero collapsed to navy appbar, strip stuck). Shots AC1-store-detail-chips-top.png, AC1-pinned-after-scroll.png. logs clean.
- AC6 PASS (same view): no NEARS-483 offers banner carousel anywhere on store page.
- AC2 (unselected) PASS: Offers chip mint fill + tag icon + navy "Offers" text (promotional unselected). Shot AC1-store-detail-chips-top.png.
- AC2 (selected) PASS: tap Offers -> navy fill + mint tag icon + white text; "All" went white; grid = discounted-only (every card %OFF + strikethrough). Sub-chip row appeared. Analytics: offers_chip_tapped {store_id:13} PII-safe. Shot AC2-offers-selected.png. logs clean.
- AC3 PASS: sub-chip row = store 13 offer cats [Cheese][Cleaning Supplies][General Items][Juices][Soft Drinks] (matches DB). Tap Cleaning Supplies -> mint-selected; grid = exactly 2 items All Purpose Cleaner(12%) + Dish Soap(16%), store-scoped Fresh supermarket only. Analytics: store_offer_category_tapped {category_id:101, store_id:13} PII-safe. Shot AC3-subchip-cleaning.png. logs clean.
- ANALYTICS PASS: both offers_chip_tapped + store_offer_category_tapped observed via '📊 analytics:' flutter log, ID-only (store_id/category_id), no PII. (Native FA disabled: 'Missing google_app_id' — DebugView N/A, app-log channel used.)
- AC4 PASS (data-limited live, proven API+auto): bare Offers view = 8 discounted-only items, no full-price bleed; single page (8<limit10) so live FE page-2 UNREACHABLE - stated. API probe (limit=5): page2 offset=2 -> 3 items all discounted (7/15/16%), 0 bleed. Shots AC4-bare-offers-top/bottom.png + AC4-page2-api-probe.log. Automated test 10/10 backstops guard. logs clean.
- AC4-toggle-hygiene PASS: Offers->Cheese(normal cat): sub-row collapses, Offers reverts mint-unselected, grid=full Cheese cat incl full-price Cream Cheese (no sticky filter). Re-Offers: sub-row back, discounted-only, Cream Cheese ABSENT (no stale grid). ->All: sub-row collapses, reset. Shots AC5toggle-A-normalcat.png, AC5toggle-C-all-reset.png. logs clean.
- AC8 PASS: filter funnel opens StoreFilterBottomSheetWidget (Filter by: Discounted Items toggle, Estimated Delivery, Price, Ratings, Clear/Apply). Applied Discounted Items -> grid filters, chip strip intact, independent of Offers chip. Shots AC8-filter-sheet.png, AC8-filter-applied.png. logs clean.
- AC5 PASS (live+API): switched GPS to zone 3 (Single Store QA Zone), opened NEARS-257 Fixture Store (0 discounted items). Chip strip = [All][QA Staples] only -> NO Offers chip, no sub-chip row, no empty row, no crash; all items full-price. API offer_categories store59 -> total_size:0, categories:[]. Shot AC5-no-offers-store.png. logs clean.

## Regression sweep (zone 2, Fresh supermarket)
- REG add-to-cart discounted item PASS: tapped Add To Cart on Mozzarella 200g (9% OFF) -> qty stepper [- 1 +] appeared, item added, no error. Shot REG-addtocart-discounted.png.
- REG store header/hero PASS: immersive hero (name/NEW/2-3 hours) renders correctly, unaffected by relocated chip strip.
- REG normal browsing PASS: All view shows mixed full+discounted items; category chips (Cheese etc) work; list/grid toggle + filter intact.
- REG header expand 98->144dp PASS: Offers toggled on/off many times (expand/collapse) -> no overflow, no exception (ui_errors + get_runtime_errors clean all run).

## Automated backstop
- flutter test store_offers_chip_test.dart (worktree): 10/10 PASS. Covers AC2/AC3/AC4(THE PIN page-2 no-bleed)/AC4-R4/AC5/toggle-reset/analytics + NearsFilterChip promo states + local_offer glyph.
- Full suite (1576) green = engineer claim; not independently re-run (targeted 10/10 + live QA suffice).

## Regression bugs (verdict-neutral, pre-existing)
- cart_count_view.dart:64 RenderFlex overflow 36px (qty stepper in narrow recommended-rail card, after add-to-cart). NOT in NEARS-602 diff. bug-cartcount-overflow.log.

## VERDICT: PASS
