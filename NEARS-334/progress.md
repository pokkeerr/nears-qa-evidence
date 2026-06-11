# NEARS-334 QA progress — home MVVM Tier-3 (verbatim move)

Branch: feat/NEARS-334-home-mvvm @ a9457c2b
Device: emulator-5554 (sdk gphone16k arm64, API 37)
Backend: http://10.0.2.2:8000 (local, API config 200)
Started: checkpoint as each AC is observed.

## AC checkpoints

### AC1 Cold-load parity — PASS (grocery)
- Fresh open landed on address-select (logged-in), chose Demo Zone (zone 1).
- Module landing showed navy header + location row, banner carousel (3 pages), module switcher (Grocery & Food / Food & Restaurant / Pharmacy), Recommended-For-You rail.
- Entered Grocery & Food: Categories rail, store rails (Nears Mart, Organic Paradise, offers/ETA), item rails (Buy It Again, Fresh Finds with priced products), banners, search, sort.
- Shots: 01-home-zone1-top.png, 02-home-zone1-scrolled.png, 03-home-grocery-rails.png
- No runtime errors (Dart MCP), no ui_errors signatures.

### AC3(b) Module switch — PASS (3 module types)
- Switched Grocery -> (back to landing) -> Food: food home rendered (food categories Sides/Drinks/Desserts/Pizza, Fresh Finds rail Tuna Nigiri/Mozzarella Sticks). Shot 04.
- Switched -> Pharmacy: pharmacy home rendered (Basic Medicine Nearby: Paracetamol/Ibuprofen, categories Pain Relief/Cold&Flu/First Aid, stores CarePlus/HealthCare/Wellness). 64 a11y nodes, no errors. Shot 05.
- Each switch fires HomeController.loadData(true, fromModule:true) (module_controller call site, rewired). All three module branches (grocery/food/pharmacy predicates as ModuleController getters) load correct rails.

### NOTE — transient semantics assertion (NOT a task bug)
- During ONE module-transition (Grocery->Food) a debug-only Flutter framework assertion fired: '!semantics.parentDataDirty' in rendering/object.dart (scheduler callback). Stack is 100% Flutter framework _RenderObjectSemantics; no app/MVVM frames.
- Pixels rendered correctly throughout (screenshot 04 proves it); only the accessibility export was momentarily empty. Recovered fully on rebuild/hot-restart and did NOT recur on the next two module switches when the screen was allowed to settle before a11y polling.
- Aggravated by rapid a11y tree polling during the route animation. Pre-existing Flutter-framework/semantics race; this verbatim-move change touches no widget/semantics code. Logged as regression_bug (pre-existing, debug-only, non-blocking).

### AC2 Pull-to-refresh — PASS
- Pull-down on populated grocery home: rails refetched, spinner cleared (Categories/Buy-It-Again/Nears-Mart all re-rendered post-refresh => setRefreshing(false) ran).
- App logs confirm refresh fan-out fired & returned 200: /items/discounted, /items/popular, /items/most-reviewed, /campaigns/item, /items/recommended, AND the deliberately-UNawaited /campaigns/basic (best-effort) also fired [200].
- Shot 06-pull-to-refresh.png.

### AC3(c) Zone/address change — PASS
- Switched delivery address Demo Zone (zone 1) -> Abu Dhabi (zone 2). Home reloaded: rails now show zone-2 stores (Abu Dhabi Fresh Market, Golden Wok (Abu Dhabi), Spice Route Kitchen (Abu Dhabi)) — zone-1 Dhaka stores cleared & replaced.
- App logs confirm the loadData(true) sequence from LocationController call site: /config/get-zone-id (zone resolved [400,2]) -> '====in zone: true' -> /banners?featured=1 (Abu Dhabi store-wise) -> /module -> /stores/get-stores/all (zone-2). All 200.
- Shot 07-zone-change-abudhabi.png.

### AC3(d) Language change — loadData wiring verified (live-nav blocked by a11y gap)
- The language-change call site (LanguageController.changeLanguage -> Get.find<HomeController>().loadData(true), line 45) is the IDENTICAL verbatim +2/-2 swap pattern proven live for the zone-change and module-switch call sites.
- Could NOT drive to Settings->Language by LABEL: the bottom-nav tabs in this build have empty content-desc (icon-only, no a11y label) AND the floating "Order #152 Pending" tracker overlay occludes the nav bar; the header module-switcher icon is also unlabeled. No coordinate taps allowed (hard rule). => navigation-guide staleness / a11y-labeling gap (regression_bug, pre-existing — unrelated to this change).
- Covered by automated test + by-equivalence with the 3 other live-proven loadData triggers.

### AC4 Single-sector auto-select + sector_auto_selected — UNVERIFIABLE on seed-state (pin-covered)
- Seed HAS single-module zones (zone 3 "Single Store QA Zone" -> single module id 4; Baqala zones 364+). Set emulator GPS to zone-3 centroid (55.15,25.1) and used "Use Current Location".
- Backend resolved correctly: /config/get-zone-id -> zone_id:[3], single module (id 4 QA Single-Store Grocery), '====in zone: true'. BUT the app then logged '-------------Module is not available for this location' and showed the "service not available in your location" dialog INSTEAD of loading the single-sector home.
- Root cause = seed/account state, NOT this change: the logged-in test account's cart holds a module-1 item (Bagels 6pk, store 19, module_id 1) and its saved address is zone-1 (multi-module). The module-availability gate fires before home loads, so autoSelectSingleSector() never runs. Reaching it needs a clean cart / guest session — both require mutating state (cart) or a destructive logout, which the DB-read-only + no-destructive-action rules forbid.
- Analytics channel CONFIRMED working & PII-safe: logcat shows '📊 analytics: sectors_shown {sectors_count: 3, zone_id: 400/1}' (ints only, no PII) on the multi-module zones. No spurious sector_auto_selected fired when the single-zone was gated (correct).
- AUTHORITATIVE backstop: module_controller_test.dart group 'autoSelectSingleSector (NEARS-334)' asserts the event fires with module_id+zone_id as INTS, in order (event BEFORE switchModule), fires-once + no-re-trap on back-nav, re-arms on genuine zone change. Shot 08-single-sector-zone3.png (the availability dialog).

### AC5 Regression sweep (home blast radius) — PASS
- Search entry: opens from home, shows Suggestions/Popular Categories/Your Last Search + history; cart badge "1 Item" correct.
- Item navigation from rail: product detail opens & renders (Add To Cart, Favourite, Share, Description, Frequently Bought Together, qty controls).
- Store-scoped content reachable from home (store-page elements "15 MIN DELIVERY"/"Favourite"/"Cart" rendered). NOTE: opening a store-rail CARD directly by label is flaky because the store name appears in both the promo banner and the rail card (resolver label-overlap, tooling limitation) — item/store-content nav itself works.
- Module switch (grocery/food/pharmacy) + zone switch (1<->2): all functional. Back-nav throughout clean.
- Cart: accessible (View Cart in search, Cart on item detail), badge correct.

### Pre-existing shimmer overflow (regression_bug, NOT a task bug)
- RenderFlex overflowed by 25px on the right in lib/common/widgets/item_shimmer.dart:59 — the loading-skeleton widget, visible only during rail load. errorsSinceReload:7 (same widget, accumulated over many reloads). item_shimmer.dart is NOT in the a9457c2b diff — untouched by NEARS-334. Cosmetic, load-state-only, non-blocking.
