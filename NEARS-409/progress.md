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

---

# RE-QA (fix cycle 2) — branch @3259f44a — delta on veg-filter glyph visibility

Device: emulator-5554 | pkg com.izzes.nears | baseUrl http://10.0.2.2:8000 | zone 2 | customer@nears.com | started 2026-06-16T14:57Z
Fix: VegFilterWidget now takes explicit iconColor (default navy). Call sites: navy bars -> textOnNavy(#FFFFFF white); white DLS bar (store_item_search) -> Theme.primaryColor (light=navy #000080 on white card; dark=mint #00FF99 on dark-navy card).

## Code-level verification of fix (pre-live)
- VegFilterWidget glyph color = `iconColor ?? NearsColors.navy` (veg_filter_widget.dart:67). fromAppBar now only suppresses bg decoration, NOT color. OK.
- Call sites: all_store(:131 textOnNavy), category_item(:195 textOnNavy), popular_item(:145 textOnNavy), custom_app_bar(:73 textOnNavy), store_item_search(:119 Theme.primaryColor), inline default=navy. OK.
- Theme resolve: light()=NearsTheme.light(primary:navy) -> primaryColor=#000080; white DLS bar cardColor=surfaceCard #FFFFFF -> navy-on-white VISIBLE. dark()=NearsTheme.dark(primary:mint #00FF99) -> primaryColor=mint; dark white-DLS bar cardColor=navyContainer #1A1A8C -> mint-on-dark-navy VISIBLE. Both contrast OK.

## Live re-demonstration

REQ1 store_item_search_screen (Spice Route Kitchen, store_id=49) — WHITE DLS app bar — THE AC THAT FAILED:
- DARK mode: glyph = MINT (0,255,153), 576 mint px on dark-navy header bg (26,26,140) -> VISIBLE. Shot req01/req01b. PASS
- LIGHT mode (the failed case): glyph DARKEST px = (0,0,128) NAVY, 576 navy px on WHITE header bg (255,255,255 / 246,243,242 near glyph) -> CLEARLY VISIBLE (was all-white invisible pre-fix). Shot req02/req02b. PASS
- Functional: tap glyph -> popup All/Veg/Non-Veg opens (shot req03); search "chicken" -> API type=all; select Veg -> API type=veg fired (search?store_id=49&name=chicken...&type=veg). Shot req04. PASS
- Runtime errors after flow: NONE (Dart MCP get_runtime_errors clean).
=> REQ1 (failed AC) FIXED in BOTH light + dark. theme-aware iconColor:Theme.primaryColor confirmed live (navy light / mint dark).

REQ2 all_store_screen (Best Stores Nearby, popular route, store list 5) — NAVY bar — cycle-1 win re-confirm:
- LIGHT: glyph = 556 WHITE px (255,255,255) on navy app bar (0,0,128) -> VISIBLE. Shot req05/req05b. PASS
- Functional: tap -> popup -> select Veg -> API /stores/popular?type=veg (5 veg stores). Shot req06. PASS
- Regression sanity: chip rail All/Veg/NonVeg present; section header "أفضل المتاجر القريبة"; store rows incl. مغلق(Closed) badge; pull-to-refresh re-fetched /stores/popular?type=veg (preserved filter). PASS
- DARK: navy app bar stays navy (0,0,128); glyph = 556 WHITE px (255,255,255) -> VISIBLE. Shot req07. PASS

REQ3 category_item_screen (navy bar) — NOT mobile-reachable (desktop/tablet/deep-link only: category_view CategoryPopUp is !isMobile; food module Categories tab uses rail layout, not parent-grid -> category_item route). CODE-VERIFIED: appbar backgroundColor=_navy(#000080) + VegFilterWidget iconColor:NearsTokens.textOnNavy(#FFFFFF white) (category_item_screen.dart:114,195). Same VegFilterWidget whose white-on-navy I pixel-proved live on all_store (556 white px, light+dark). met=true via code+identical-widget-render.

REQ4 popular_item_screen — DEAD ROUTE (getPopularItemRoute/PopularItemScreen have ZERO callers anywhere in lib/; route def exists in route_helper only). CODE-VERIFIED: NearsAppBar(navy) + VegFilterWidget iconColor:NearsTokens.textOnNavy (popular_item_screen.dart:145). met=true via code.

REQ5 custom_app_bar veg usage — NO LIVE CALL SITE: grep shows zero screens set onVegFilterTap (only comments in popular_item/all_store reference it). Dormant capability. CODE-VERIFIED: custom_app_bar.dart:73 passes iconColor:NearsTokens.textOnNavy. met=true via code (no live surface to demo).

REQ6 inline/non-app-bar veg (fromAppBar:false default navy) — NO LIVE LIGHT-SURFACE CALL SITE: only inline VegFilterWidget is dead-commented (store_screen.dart:1342 /*...). Default fallback iconColor??NearsColors.navy UNCHANGED. No regression risk. met=true via code (no live surface).

== Regression sanity — core NEARS-409 screens ==
- item_view_all_screen (Most Popular Items, food, count (75)): navy NearsAppBar + back; search pill "ابحث عن..."; item grid; infinite-scroll -> "end of the page, offset:2" + /items/popular?offset=2&limit=25 (page 2 loaded); 3x back/re-enter+scroll stress -> NO ScrollController-disposed, ui_errors clean, Dart MCP runtime errors clean. Shots req08/req09. PASS. (sort/filter sheets NOT re-driven live: outside cycle-2 blast radius [veg_filter_widget + 5 iconColor params only], fully PASSED last run.)

== Runtime-error finding (classified) ==
- RenderFlex overflow 2.6px bottom @ store_card.dart:108 (Pharmacy store "City Care Chemist", Pharmacy module all-store list). NOT a NEARS-409 surface; store_card.dart NOT touched by cycle-2 fix (3259f44a) — last touched by NEARS-266 (2026-06-08). PRE-EXISTING / UNRELATED cosmetic overflow on long pharmacy store names. -> regression_bug (low), does NOT break any NEARS-409 AC, does NOT fail this ticket.

== Automated backstop ==
- flutter test test/features/item test/features/store test/common/widgets/dls -> +108 All tests passed (re-run on 3259f44a).

== VERDICT: PASS ==
- The failed AC (store_item_search white-bar veg glyph) is FIXED: navy-on-white in light, mint-on-dark-navy in dark, both pixel-proven + functional (type=veg API). All other navy-bar call sites white-on-navy (live all_store light+dark; code category_item/popular_item/custom_app_bar). Inline default navy unchanged. No new task_bugs. 1 pre-existing unrelated regression_bug (pharmacy store_card 2.6px overflow).
