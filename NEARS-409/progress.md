# NEARS-409 QA progress (live, checkpointed)

Device: emulator-5554 (Android) | App pkg com.izzes.nears | baseUrl http://10.0.2.2:8000 | branch feat/NEARS-409-see-all-grids-reskin @7fab4356 | zone 2 (Abu Dhabi), customer@nears.com

Automated backstop: flutter test test/features/item test/features/store test/common/widgets/dls -> ALL PASSED (108 tests).

## Observations

- item_view_all_screen (Most Popular Items, food, zone2): NearsAppBar navy + white back arrow + white cart icon (no badge=empty cart, correct); DLS search pill; title "Most Popular Items" + muted "(75)"; sort+filter icon buttons in white surface cards (navy glyphs). Screenshot 01. [light]
- item_view_all sort: A to Z sheet -> "Sort by" apply -> grid reorders (BBQ Burger first); API filter=["a_to_z"]. PASS
- item_view_all filter: rating sheet -> 4+ Rating -> apply -> count 75->50; API rating_count=4. PASS
- item_view_all infinite-scroll: deep scroll -> API offset=2&limit=25 fired (page 2 loaded). dispose fix did not regress. PASS
- item_view_all search: type "burger" + submit -> API search=burger, grid filters to burgers. PASS
- item_view_all empty state: search "zzqnonexistent" -> "(0)" + NearsEmptyState (search_off navy disc + "No items found"). Screenshot 03. PASS
- item_view_all clear (x): tap clear -> search param dropped, list reloads (50). PASS
- item_view_all back/dispose: 4x enter->scroll->back cycles + Dart MCP runtime errors -> NO "ScrollController used after disposed"/exceptions. dispose fix PASS.

== all_store_screen (Best Stores Nearby, food/popular route, zone2) ==
- [CRITICAL cycle-1 fix] Veg-filter glyph: WHITE & clearly visible top-right of navy NearsAppBar (was navy-on-navy invisible). Screenshot 04. PASS
- Veg-filter functional: tap -> popup (All/Veg/Non-Veg) opens (screenshot 05) -> select Veg -> API /stores/popular?type=veg fired, list re-filtered. PASS
- NearsAppBar: navy, white back arrow, white centered title "Best Stores Nearby", NO cart icon (correct parity). PASS
- Chip rail All/Veg/Non-Veg (NearsFilterChip) + NearsSectionHeader + StoreCompactCard rows (Closed badge on closed store) render. PASS
- all_store pull-to-refresh: firm pull -> /stores/popular re-fetched (preserved type filter). PASS
- veg-filter ABSENT on featured/recommended: Recommended See-All -> "Featured Stores" route -> NearsAppBar with back+title only, NO veg glyph, NO cart, NO chip rail. Screenshot 06. PASS (conditional showVegFilter correct)
- all_store loading shimmer: store rows arrived too fast to capture shimmer reliably on warm backend; _StoreRowShimmer present in code, not regressed.

== AC#3 collateral veg-filter surfaces ==
- store_item_search_screen (food store, Spice Route): *** REGRESSION (task_bug) *** header is a WHITE DLS app bar (store_item_search_screen.dart:57,67 color=cardColor; back arrow navy & visible). VegFilterWidget passes fromAppBar:true -> glyph now WHITE (255,255,255) == INVISIBLE on the white header (pixel-sampled glyph region [1215-1275]x[219-279] all (255,255,255); header bg also white). Still FUNCTIONAL (tap opens All/Veg/Non-Veg popup). PRE-fix (7fab4356^) glyph was unconditionally NearsColors.navy -> VISIBLE navy-on-white. The fromAppBar:true flag (already present pre-commit, line 131) now over-whitens it. Screenshots 08/08b/08c. AC#3 NOT MET on this surface.
  -> ROOT: fromAppBar conflates "in an app bar" with "on a navy surface"; store_item_search uses a WHITE app bar.
- category_item_screen: appbar backgroundColor = _navy (category_item_screen.dart:113) -> white glyph CORRECT (white-on-navy, identical render proven live on all_store). Mobile UI path is desktop/deep-link only; verified by source + identical widget path. OK.
- inline (non-app-bar, fromAppBar:false=navy) veg filter: ONLY live call site is dead-commented (store_screen.dart:1342). No live light-surface inline veg filter exists -> sub-case has no live surface; navy default path unchanged in code.

== AC#2 popular_item_screen (DEAD ROUTE) ==
- Not reachable via live UI (no nav entry) nor simple deep link (manifest deep-link gated to host 6ammart-web.6amtech.com, flutter_deeplinking_enabled=false; routes are in-app GetX named only). Verified by CODE: scaffoldKey now on Scaffold (popular_item_screen.dart:117), endDrawer:MenuDrawer (174) owned by that key -> endDrawer can open (cycle-1 fix correct). NearsAppBar(showBack, title, cart + veg fromAppBar:true) -> navy bar, white back/title/cart, white veg glyph correct on navy. Relying on code + green automated suite per task instruction.

== AC#6 RTL/Arabic ==
- all_store (light): veg glyph mirrored to top-LEFT (logical end), back arrow to top-RIGHT, chip rail + section header + rows flip RTL, white glyph visible on navy. Screenshot 09. PASS
== AC#7 Dark mode ==
- all_store (dark+RTL): navy bar stays navy, WHITE veg glyph + white back arrow legible on navy; chips + mint store-name text legible. Screenshot 10. PASS
- item_view_all (dark): screen legible; navy appbar white back+cart; sort/filter white cards legible; item grid legible. Search input: typed "burger" -> text VISIBLE/legible (NEARS-429 did NOT reproduce on this field/state). Screenshot 11. PASS (NEARS-429 not observed)

== store_item_search regression — SCOPE confirmed ==
- DARK mode: header bg = dark navy (26,26,140); white veg glyph (255,255,255) -> VISIBLE (white-on-navy). Screenshot 12. So the regression is LIGHT-MODE-SPECIFIC: light header (cardColor=white #FFFFFF) + always-white glyph = invisible; dark header (cardColor dark) = visible.
- Correct fix should be theme-aware (e.g. primaryColor, as the back arrow uses) instead of hardcoded textOnNavy, OR not pass fromAppBar:true on this white-header screen.

== Automated backstop ==
- flutter test test/features/item test/features/store test/common/widgets/dls -> ALL PASSED (108 tests / earlier run reported +108).
