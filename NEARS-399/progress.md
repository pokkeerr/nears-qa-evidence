# NEARS-399 QA progress (live checkpoint)

Device: emulator-5554 (Android 17 / API 37)
Branch: feat/NEARS-399-store-detail @ f98697bc
Backend: http://10.0.2.2:8000 (local, HTTP 200)

## Automated backstop
- flutter analyze: 8 info-only lints, 0 warnings/errors; none in NEARS-399 scope files. CLEAN.
- flutter test: +882 all passed, exit 0. GREEN (matches expected 882).

## AC verdicts (appended live)

### Live observations (Test Store, zone 2, light mode)
- HERO (store_hero_light.png): navy gradient hero; mint-ring logo; rating pill 5.0(5) mint star; distance 6453km pill; tower "Marina Heights"; address; "Delivered in 1-15 min" mint pill; back+search+share+favourite(mint heart) glass buttons present. Name is focal point. PASS H1-H17.
- SKELETON (sk_3.png) KEY: NearsSkeleton-based — navy hero block w/ navyGlass shimmer shapes (logo circle, name, pills), chip-row of 5 skeleton pills, 2-col card-grid skeleton. Navy gradient MATCHES live hero gradient => NO gradient flash/jump. NOT legacy gray shimmer, NOT spinner. PASS C12.
- CATEGORY TABS: All(mint fill, navy text=active), Bakery & Bread, Snacks & Chips, General Items, Organic. PASS C7 render.
- FILTER ICON: filter_list present in "All Products" section header row (right of view toggle). PASS C5 position.
- BOTTOM CART BAR: white bar + mint View Cart (navy text), 56 د.إ / 2 Item. PASS C14.
- RECOMMENDED rail + "See All" (mint) present. PASS C4.

### FILTER SHEET (filter_sheet_light.png)
- Opens from filter_list in section header (C5->C6). Three-tier hierarchy: "Filter by" > Estimated Delivery/Price/Ratings > chips. ETA chips REAL labels: "Under 15 min"/"15–30 min"/"30+ min" (NOT raw keys). Discounted Items chip, Price slider, Ratings stars. Clear Filter (navy outline) + Filter/Apply (mint, navy text).
- Apply re-queries: Discounted Items -> grid showed "Breakfast Cereal 6% OFF" w/ strikethrough (was absent before). PASS.
- Clear resets: Clear + Apply -> full set (Carrots/Croissants/Low Fat Milk) returned, discounted-only item gone. PASS.

### CATEGORY TABS (category_bakery_active.png)
- Tapping "Bakery & Bread" -> active chip mint fill + navy text; "All" deactivated; grid switched to bakery items only (Croissants). setCategoryIndex re-paginates. PASS.

### SEARCH-WITHIN-STORE (search_in_store_empty.png) — TASK BUG FOUND
- Back arrow (navy) mirrors RTL; NearsInput "Search item in store..."; chips ETA/Price/Organic/Brand; branded empty "No item available" illustration (not blank). 
- *** BUG: "BOTTOM OVERFLOWED BY 8.0 PIXELS" debug stripe under the search input. Runtime error: RenderFlex overflow in NearsInput Column (nears_input.dart:147), constrained to h<=40 by the search app-bar but NearsInput needs 48px. ***
- ROOT CAUSE: NEARS-399 (481e547d) swapped the old isDense TextField (fit 40px) for NearsInput (48px) inside the unchanged 60px PreferredSize app-bar (store_item_search_screen.dart:51-105). breaks_ac: search NearsInput renders broken. TASK BUG.

### CLOSED STORE (store_closed_hero.png, store_closed_items.png)
- Organic Shop closed-now: hero "Closed Now" pill present, DIM navy/charcoal (NOT mint), beside mint "Delivered in 2-3 hours" pill. Rating="NEW" (unrated, never "0.0 (0)") -> also verifies hero-meta NEW AC. Store fully BROWSABLE (rail, tabs, grid all interactive). Collapsed pinned bar (back+name) confirmed on scroll. PASS C closed-browsable + H8 NEW.
- NOTE: scope said pill "red"; actual pill is dim charcoal — recon H14 doesn't pin red (red CLOSED badge belongs to item-card NotAvailableWidget for UNAVAILABLE items, inherited 397, not the hero pill). Closed store has in-stock items so cards render normal (correct). No grayscale item reachable in seed (store closed != item unavailable). Verified via source/recon. Not a bug.
- Hero meta: tower "Marina Heights", placeholder seed address suppressed on this store. PASS H10/H11.

### DARK MODE (store_hero_dark.png, skdark_3.png, filter_sheet_dark.png)
- Hero dark: navy gradient (theme-driven), mint-ring logo, mint-star rating pill, distance, tower, mint delivered-in pill, all action buttons. Body dark navy. Item cards adapt (dark surface, white text, mint price/add, mint Organic badge=dark-safe). PASS.
- Skeleton dark: navyGlass shimmer on dark navy body, hero gradient matches dark hero -> no jump. PASS.
- Filter sheet dark: navyContainer dark sheet, mint headings, ETA real labels, mint slider/buttons, three-tier hierarchy. PASS dark-mode sheet.

### RTL (Arabic) (store_hero_rtl.png, search_rtl.png) — tested with dark mode active (covers both)
- Hero fully MIRRORED: logo+name on right, action buttons left, back arrow on right. Rating/distance/tower/address/delivered-in pills mirror. Recommended rail "موصى به لك" right, "رؤية الكل" left. Category chips flow R->L ("الجميع"=All mint active). View toggle + filter icon mirror to left. Bottom cart "عرض العربة" left. PASS RTL.
- Search RTL: back arrow MIRRORED (top-right), NearsInput RTL, chips R->L (ETA/Price/Organic/Brand AR), branded empty "لا يوجد عنصر متاح". PASS S1/S3 RTL.
- *** SAME 8px overflow stripe reproduces in RTL (and dark) -> NearsInput overflow is locale/theme-independent. Confirms task bug. ***

### REGRESSION SWEEP
- Shared DLS edits by 399 are ADDITIVE only: NearsInput +onSubmitted/+textInputAction (optional, no default change); NearsIcon +5 glyph mappings (near_me/apartment/share/filter_list/description). No existing call site regressed.
- Inherited 397 item cards render unchanged in store grid/list/recommended (verified across light/dark/RTL).
- No runtime errors anywhere EXCEPT the single NearsInput overflow on search screen (reproduces light+dark+RTL).
- Automated: analyze CLEAN (info-only), test +882 GREEN, +1 new store_details_shimmer_test.

### VERDICT: FAIL (1 task bug: search-screen NearsInput 8px overflow, breaks_ac search-NearsInput)
