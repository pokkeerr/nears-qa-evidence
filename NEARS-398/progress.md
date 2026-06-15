# NEARS-398 QA progress (live checkpoint)

Device: emulator-5554 (Android) | Branch: feat/NEARS-398-home-tower @ d8b5cf29
Backend: http://10.0.2.2:8000 (live local) | DB: multi_food_db read-only

## Automated backstop
- flutter analyze: 8 info-level lints, ALL pre-existing in untouched files (item_widget, cart, voice_search, analytics_service). ZERO in 398-touched widgets. => clean for this ticket.
- flutter test: All tests passed! (00:12 +879) => 879 green, matches expected.

## Seeded states discovered (read-only)
- Single-store zone = zone 3 "Single Store QA Zone": 1 module (id4 QA Single-Store Grocery), 1 store (id59 NEARS-257 Fixture Store, OPEN 24/7, rating NULL, ETA 30-40min).
- Tower addresses: addr47 user409 (qa.singlestore@nears.com) "Tower A" zone3 single-store; addr45 user6 (customer@nears.com) "Marina Heights" zone2 multi-store.
- Active flash sales: modules 1/2/3 (grocery/food/pharmacy), window 2026-06-05..06-20 ACTIVE NOW. Note: zone3 store is module4 -> flash-sale may self-hide in tower; renders on grocery/shop marketplace.

## Live AC verdicts (appended as observed)

### Marketplace (zone2 multi-store, grocery module) — LIVE
- Flash-sale on grocery MARKETPLACE home: VERIFIED mounted+live. Widget tree shows FlashSaleViewWidget x2, FlashSaleCard x2, FlashSaleTimerView x2, TimerWidget x8 (live countdown), RecommendedStoreView x2. API /api/v1/flash-sales [200] returns module1 "Flash Deals — Grocery" w/ populated active_products (Banana stock77/sold4 ...). Zero runtime errors. Discount tags (navy pill, white text), Organic tags (mint pill), strike+discounted price, mint "+" add (CartCountView w/ qty stepper), mint See-All all rendered. (CAP-D1..D5, flash-sale-on-marketplace = PASS)
- Marketplace home (397) visually intact: navy appbar, mint CTAs/See-All, store cards w/ CLOSED badge + FREE DELIVERY mint badge + ETA mint badge. No reskin bleed. NearsBadge x70 / NearsSurfaceCard x60 in tree (DLS wrappers in use).
- Brand rules on marketplace: navy front-door, mint=action (See All / + / Shop Now / FREE DELIVERY / ETA), navy-text-on-mint CTA, no white-on-mint observed. PASS.

### Single-store zone 3 / Tower A (user 409 qa.singlestore) — LIVE
- HERO RENDERS restyled: navy->deep-navy gradient surface, mint-ringed logo, white "YOUR NEIGHBORHOOD STORE" eyebrow + white "NEARS-257 Fixture Store" name, mint ETA badge "30-40 MIN" (bolt). NO rating badge (store rating NULL -> avgRating>0 false, correctly hidden CAP-A4). NO CLOSED badge (open 24/7). Mint CTA "Shop NEARS-257 Fixture Store ->" navy-text-on-mint (CAP-A5 open=Shop{store}). (CAP-A1/A4/A5 = PASS)
- Suppression matrix SINGLE-STORE arm: NO "Stores in Tower A" rail (CAP-B2 suppressed), Daily Essentials chips Milk/Water/Bread/Eggs STILL SHOW (CAP-B4 PASS), NO "Popular in Tower A" (CAP-C3 shell-suppressed). No bottom collapse/jump observed. (PASS)
- Hero analytics store_auto_opened: fires w/ PII-safe params {store_id:59, module_id, zone_id} (IDs only). C1 one-per-zone: pull-to-refresh re-ran full fan-out (stores/details/59 + popular+latest+get-stores) yet store_auto_opened did NOT re-fire (count 0) -> sentinel suppresses per-rebuild/refresh. PASS. (Tab remount Home->Cat->Home re-fires once = legit new impression, not a rebuild.)
- CAP-E2 pull-to-refresh: re-runs fan-out incl re-resolve zone + refetch hero store (details/59). PASS.
- No runtime errors (Dart MCP get_runtime_errors clean) across single-store home.

### Hero tap + chips + store-resolution (single-store) — LIVE
- CAP-B4 chip tap: "Milk" -> search pre-filled "Milk" -> "1 results found" QA Whole Milk 1L (NEARS-257 store). One-shot search shortcut. PASS.
- CAP-A5/A6 hero CTA tap: single_store_hero_tapped fired {store_id:59,module_id:4,zone_id:3} (PII-safe); store opened to NEARS-257 Fixture Store page (module set). PASS.
- CAP-A2 read-only resolution: view_store fired ONLY after tap-through to store screen (16:55:14), NOT during hero render -> hero's fetchStoreForHero is non-side-effecting. PASS.

### Dark mode + RTL/Arabic (single-store hero) — LIVE
- DARK MODE: navy hero STAYS navy (distinct from dark page bg), white hero text legible, mint CTA legible (navy-on-mint), ETA mint badge legible, chips/cards flip to dark navyContainer, greeting+See-All mint legible. PASS.
- RTL/ARABIC (tested simultaneously w/ dark): layout fully mirrored (logo right, text right-aligned), hero CTA arrow MIRRORED (points left, mirrorForRtl), Daily-Essentials chips localized (حليب/ماء/خبز/بيض) + mint "+" on logical side, bottom nav mirrored. BIDI: "تسوّق من NEARS-257 Fixture Store" — Arabic prefix + Latin store name, store name NOT reversed. PASS.

### Multi-store + tower (Marina Heights, user6) — LIVE
- Suppression matrix MULTI-STORE arm: NO single-store hero (CAP-A1 self-hidden); "Stores in Marina Heights" tower store rail SHOWS (CAP-B3); Daily-Essentials chips SHOW (CAP-B4 both modes); "Popular in Marina Heights" rail SHOWS (CAP-C4, NOT shell-suppressed since multi-store). PASS.
- BADGE NEUTRALITY (brand rule 2): "IN YOUR BUILDING" = NEUTRAL GREY (info), "POPULAR" = NEUTRAL GREY (info) — NOT mint. ETA badges ("1-15 MIN"/"2-3 HOURS") = mint (speed). Mint correctly reserved for speed/CTA only. PASS (C4 neutral-badges + B3 in_your_building neutral).
- Open/closed semantics: "Closed Now" in red on Organic Shop card. PASS.
- Note: tower rails+chips render on the MODULE home (showMobileModule=false), gated OFF on the cross-module landing (showMobileModule=true) — consistent w/ home_screen.dart slivers 686-724. isSingleStoreZone shell gate on PopularInTowerView (line 715) intact.

### Non-tower self-hide (Dhaka, user6) + final sweeps — LIVE
- Non-tower address (Demo Zone Dhaka, no tower_name): ALL tower content absent (Stores-in/Popular-in/Daily-Essentials/In-your-building/hero counts = 0). Every tower view self-hides to SizedBox.shrink. PASS (CAP-B1/C1).
- Flash-sale add-to-cart (CAP-D4): item detail of flash-discounted Rice 5kg shows strike orig (15) -> discounted (12); Increase/Decrease qty steppers + Add To Cart functional (triggered standard cross-store new-basket guard, dismissed, no DB mutation). PASS.
- No RenderFlex/overflow/FlutterError/RangeError/Null-check exceptions across entire session (Dart MCP get_runtime_errors clean x3; logcat clean). 
- INHERIT-397 cards (ItemWidget/item_view/NearsStoreCard/NearsItemCard) NOT touched by 398 diff. PASS (no re-restyle regression).
- Desktop/responsive: ResponsiveHelper isMobile/isTab/isDesktop structure preserved; only spacing values migrated Dimensions.* -> NearsTokens.* (intended foundation migration) + reformatting. Not a desktop logic regression. Mobile path is what was live-tested.
- 397 marketplace home visually intact across all addresses; flash-sale shared widget renders on grocery marketplace home (widget tree: FlashSaleViewWidget/FlashSaleCard/TimerWidget x8 live).
