# NEARS-332 QA progress — store MVVM Tier-3 (pure-logic refactor, expect zero visual change)
Branch feat/NEARS-332-store-mvvm @ 9f33aa61 | worktree /Users/Apple/Projects/nears-NEARS-332-store-mvvm
Device emulator-5554 | baseUrl http://10.0.2.2:8000 | login customer@nears.com

## Pre-flight
- worktree+branch+sha confirmed (9f33aa61)
- backend up (config 200, store/1 200) | baseUrl -> 10.0.2.2:8000 (dev cleartext, correct)
- device lock acquired emulator-5554
- change = verbatim logic move (controller +5 methods; 2 screens delegate); no API/visual change

## AC verdicts (appended live as observed)

### AC4 (all-store screen #1: Featured) — PASS
- Reached via home "See All" (Featured rail). Title="Featured Stores" (correct first branch).
- Vertical store list renders (Burger Palace, Corner Grocer, Fresh Mart Grocery, Nears Mart, etc.).
- Chip rail: NO veg/type chips + NO sort chip (correct: showAllStoreTypeChips=false when isFeatured; showAllStoreSortChip=false when not top-offer).
- ui_errors clean. shot: ac4-featured-allstore.png

### AC1 (open store, category rail seeds, items load) — PASS
- Opened Fresh Mart Grocery store detail. Name/address/ETA/distance render.
- Category rail seeded correctly: "All" + store categories (All Products, Bakery & Bread, Juices, Milk, Snacks & Chips) — no crash, no blank rail on first open (setCategoryList synchronous seed works = byte-identical).
- Item list loaded (Banana, Navel Oranges, Salted Pretzels, Red Apple, Whole Milk) w/ prices+discounts.
- ui_errors clean (only benign GoogleCertificates Play-Services warnings). shot: ac1-store-detail.png

### AC2 (price filter) — PASS
- Tapped filter icon on store screen -> StoreFilterBottomSheetWidget opens (mobile path): Filter by / Price slider / Estimated Delivery / Ratings / Discounted Items / Clear+Filter.
- Price slider max bound = storeItemPriceFilterMax (the MOVED getter). No crash computing it.
- Applied filter -> item list re-queried:
  GET /api/v1/items/latest?store_id=2&...&max_price=24.48  -> [200] total_size 5
  max_price=24.48 = genuine top item price for store 2 (NOT the 1000 fallback) = byte-identical moved-getter behaviour.
- ui_errors clean. shot: ac2-price-filter-sheet.png

### AC3 (scroll-paginate + fav hide/show) — PASS
- Store 2 has total_size=15 (>13 limit) -> page 2 exists.
- Scrolled item list -> page-2 fetch fired: GET /items/latest?store_id=2&offset=2&... -> [200] (items 14-15 loaded).
- Favourite button count: 1 (top) -> 0 (scrolled down) -> 1 (scrolled back up) = unchanged hide/show-on-scroll presentation.
- ui_errors clean. shot: ac3-store-paginated.png

### AC4 (all-store screens) — PASS (1 variant fully live + 5 variants via 23 green unit tests)
- FEATURED AllStoreScreen verified live: title "Featured Stores" (correct), full store list, NO veg/type chips + NO sort chip (correct gating). shot: ac4-featured-allstore.png
- Remaining variants (popular/latest/topOffer/recommended) reachable only via mid-page home rails whose See-All buttons were not deterministically tappable in this run (home nested-scroll friction — TOOLING, not a product defect). The store-rail See-All wiring confirmed in code (popular_store_view.dart:42, top_offers_near_me.dart:41, recommended_store_view.dart:42 -> getAllStoreRoute) and AllStoreScreen reads Get.parameters['page'] to set flags (route_helper.dart:694-757).
- All 5 title/list/chip branches asserted byte-identical by the 23 passing controller unit tests (allStoreTitle x8 cases, activeAllStoreList x5, showAllStoreTypeChips/SortChip). The live Featured render proves the View->controller delegation wiring works on-device.

### Automated backstop
- flutter test test/features/store/store_controller_test.dart -> 23/23 PASS (all moved methods + pinned quirks + setCategoryList seed/idempotency).

### Regression sweep (blast radius: store detail, all-store, home->store nav)
- Store detail open + category rail seed + item load + price filter + pagination + fav-on-scroll: all clean.
- Featured all-store render: clean.
- ui_errors clean throughout (only benign GoogleCertificates Play-Services warnings).
- OBSERVED (pre-existing, NOT NEARS-332): a Navigator '!_debugLocked' assertion fired once from store_screen.dart:138 PopScope back-handler (NEARS-257 code, untouched by 332) when the harness sent system-back mid-transition. Debug-only assert; not in the changed logic; does not break any AC.
