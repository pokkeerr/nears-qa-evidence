# NEARS-400 — Item Detail (PILOT) — QA progress checkpoint
Device: emulator-5554 (Android) · QA SHA 76e6aefd (build 3912b8a6 + fix cycle 1)
Backend: http://10.0.2.2:8000 (local, HTTP 200) · queue:work running
Login: customer@nears.com / 123456789

## AC checkpoints (appended live as observed)

### AC1 Composition — PASS (02-item-detail-light.png)
- Hero square rounded card, ~20px margins, ambient shadow: PASS
- Decorative grab handle top (gray pill): PASS
- Rounded sticky footer: PASS
### AC2 Carousel — indicator "1/4" navy pill present (4 images); tap-to-gallery pending
### AC4 Title/price — name-left, price+pill right; price NAVY (light), strike 17, In Stock soft-mint pill: PASS (TOK-1 light)
### AC5 Description — always-open label+paragraph, no accordion chevron: PASS (Read more pending)
### AC6 CTA add_to_cart state — "Add To Cart | 14 د.إ" mint pill: PASS
### AC7 Qty stepper mint +/-: PASS visual
### AC9 Parity — ORGANIC badge, ETA pill, FBT rail present: PASS
### A3 DiscountTag "17.0% OFF" top-start, clipped in card: PASS

### AC2 Carousel — multi-slide swipe works (1/4→2/4), per-slide a11y updates: PASS (03)
### AC3 Gallery — NearsAppBar "Product Images", navy@0.85 nav circles + white chevrons 44dp, open/close/reopen x3 NO crash, reopens on first image (C1/C2 fix): PASS (04/05/06). Pinch-zoom gesture no crash. Images broken-placeholder (seeded URLs unreachable=data condition, gallery graceful → also covers I1).
### AC7 Variant state — Size accordion, NearsFilterChip (64g selected mint, others white+hairline); select 250g → CTA price 70→210, chip toggles: PASS (07/08)
### AC5 Description — always-open label+paragraph, no chevron (long-desc Read-more test pending on item 94)
### Note: indicator showed "2/1" briefly on single-image variant item (stale imageSliderIndex from prior item) — verify

### AC6 CTA states:
- add_to_cart "| price" suffix: PASS (02,07)
- update_in_cart "| price" suffix: PASS (11) — CTA flipped after add
- cross-store reset ConfirmationDialog ("Start a new basket?"): PASS (10)
- snackbar "Item added to cart" + View Cart: PASS (11)
- cart badge incremented to 1 (shake wired via ValueNotifier): PASS (11)
### AC7 qty stepper: increase 1→2 → CTA price 210→420; decrease 2→1 → 210: PASS bounds
### REGRESSION BUG (pre-existing, NOT NEARS-400): slide indicator shows "2/1" on single-image item after navigating from a multi-image item (swiped). Root: getItemDetails() resets _item but not _imageSliderIndex (confirmed absent at base c258ae0d). Cosmetic. per-slide a11y Semantics is correct ("1/1").

### AC5 Description Read more — item 96 (320-char desc): collapsed shows 3-line trim + "Read more" underlined link; tap → full text expands ("Show less" at end): PASS (15/16)
### AC9 Parity (item 96 ref shot): rating bar "5.0 (3)", ORGANIC badge, ETA pill, FBT rail, valid hero image: PASS (15)

### AC8 Share — tapping Share opens OS share sheet; text = "Fresh Organic Tomato https://6ammart-web.6amtech.com/item-details/...?id=96&...": PASS (17). NOTE: Share is WIRED (not the no-op stub FU-1 described — appears folded in / completed). Button present (webHostedUrl non-empty=demo host default). URL contains product URL+id. No PII.

### AC6 CTA out_of_stock — item 61534 (QA OOS Fixture, zone1, stock gate ON): CTA "Out of Stock" disabled style (pale mint, legible), NO price suffix; OOS pill error-tint right-aligned in price column; price still navy; tapping CTA = no-op (no add, no dialog): PASS (24)

### AC10 Dark mode — item detail (Croissants): scaffold navy-deep, cards navyContainer, PRICE = SKY #8FB4FF (NOT mint) TOK-1 PASS, grab handle WHITE, mint reserved for CTA/stepper/badges, description label mint (DLS-consistent): PASS (30). Gallery dark: NearsAppBar navy, navy@0.85 nav circles white chevrons (31). onNavy skeleton = code-confirmed (live capture blocked by unreachable seeded image URLs → placeholder, not loading).
### D2 ACCEPTED DIVERGENCE confirmed: Substitution Preferences (5 options) present in CART (27), NOT on item-detail. Capability preserved in correct location.

### AC10 RTL/Arabic — item detail (Rice 5kg): overlay trio mirrored (cart/fav/share LEFT, back-chevron RIGHT), title+store RIGHT-aligned, price column LEFT, price "12 د.إ" currency LTR-preserved, In Stock pill "في الأوراق المالية" mint, Description "وصف" RIGHT-aligned, DiscountTag "18% OFF" top-RIGHT (=logical-START in RTL): PASS (33). SF-7 RESOLVED in fix cycle: call site sets inLeft=(Directionality==ltr) so tag is logical-start in both directions.
### AC3 RTL gallery — NearsAppBar mirrored (title right, icons left), nav circle chevron mirrored (mirrorForRtl working): PASS (34)

### AC10 Loading skeleton (F1) — captured LIVE with network off (40b-loading-skeleton.png): branded NearsSkeleton shimmer = grab-handle bar + square hero block + title row(name+price) + 3 desc lines + pinned action bar (stepper+CTA pill). NOT a spinner. Semantics announces "Loading...": PASS
### SF-8 confirmed (KNOWN/ACCEPTED pre-existing, NOT NEARS-400): item load FAILURE → screen stays in shimmer indefinitely, no NearsErrorRetry, no auto-retry on reconnect (ItemController has no error flag — confirmed in code). Fresh re-navigation with network recovers. Reported as regression_bug (does not affect verdict).
### Regression sweep:
- item_bottom_sheet / category grid quick-add: kept QuantityButton stepper (common/widgets/quantity_button.dart) works inline, add-to-cart + snackbar fire, cross-store guard fires (SF-6 kept class is live): PASS (37)
- item_bottom_sheet routes to same restyled getItemImagesRoute gallery (code line 188) — shared gallery inherits chrome
- Desktop/web DetailsWebViewWidget: code-confirmed local QuantityButton steppers (L306/320/428/442) + addToCart intact + SF-5 web price uses _priceColor (L363). NOT booted live (gated by ResponsiveHelper.isDesktop; phone target). 
- I1 imagesFullUrl unreachable → item detail + gallery render w/ placeholder, no crash: PASS (seeded URLs unreachable throughout)
