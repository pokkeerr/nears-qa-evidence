# NEARS-410 QA progress (live, fix-cycle 1 verify)

Build: feat/NEARS-410-survivor-batch-a-reskin @ e4efea0b
Device: emulator-5554 (Android), backend http://127.0.0.1:8000 (HTTP 200)
Started: 2026-06-16

## Code-level pre-checks (done)
- onRemove param on NearsFilterChip is additive/backward-compat (defaults null). VERIFIED.
- Desktop history path: ListView.separated, NearsFilterChip with onTap=run-search + onRemove=removeHistory(index). VERIFIED in src (lines 514-537).
- Mobile history path: Wrap of NearsFilterChip, onTap only, NO onRemove. VERIFIED (lines 540-568).
- Clear-all via NearsSectionHeader.onAction=clearSearchHistory(). VERIFIED.
- removeHistory writes local prefs only (saveSearchHistory). No DB mutation. VERIFIED.
- Favourite: nullable _tabController + null-safe dispose. surface1 track, mint selected, tapMin. VERIFIED.
- Flash sale timer chain: Timer.periodic(1s)->update()->GetBuilder->FlashSaleTimerView(duration). VERIFIED untouched.
- Flash sale header/cards: NearsSurfaceCard(elevated), no Border.all. VERIFIED.
- Active flash sales in DB: ids 1/2/3 (modules 1/2/3), 6 items each, window 06-05..06-20. AVAILABLE.
- baseUrl -> local backend (10.0.2.2 / 127.0.0.1:8000), not demo. VERIFIED.
- enableCrossStoreSearch = false -> cross-store entry card on search will NOT render live; code-verify only.

## Live AC results
(appended as observed)

## LIVE observed (Android emulator-5554)
- AUTOMATED: flutter test search/favourite/dls/flash_sale/category = 130 PASS.
- Boot: no runtime errors. App logged in (zone shown).
- AC2 mobile search history: "Pizza" chip = NearsFilterChip pill, NO trailing 'x'. Tap -> ran search (results state, Item/Stores tabs). Clear All header action present. PASS. [01,02]
- AC4 search tokens: suggested-items grid tiles = NearsSurfaceCard (white, no hard border, soft shadow). "Suggestions" section header present. PASS (live mobile). [01]
- AC3 NearsFilterChip backward-compat: category sub-category chips (All/Juices/Soft Drinks/Seafood) render unchanged pills, mint-selected + hairline unselected, NO stray 'x'. PASS. [04]
- AC6 categories: navy bar, rail labels render (mint selected / muted unselected), rail->grid selection works (Bakery->Beverages updated grid), sub-cat chip "Juices" filters grid, drill-down to item detail works (NEARS-409 untouched). No errors. PASS. [03,04,05,06]

## Web/desktop boot attempts (AC1 desktop search-history)
- flutter run -d web-server :8765 -> Playwright sees only 8710B bootstrap; DDC modules need Dart Debug ext (headless Playwright lacks it). App did not render. [web-00,web-01]
- flutter run -d chrome :8766 (headless) -> app runs in flutter-spawned browser, but Playwright fresh context only gets bootstrap; empty semantics. [web-02]
- Fallback: building static `flutter build web --profile` bundle to serve self-contained for Playwright.

## Flash sale (details screen reached via grocery home -> Flash Sale header -> See All)
- AC8 CRITICAL countdown ticks LIVE: PASS. Timer sec decremented across reads (35->26->roll to next min) ~5s apart. Timer.periodic chain live on details screen. [09]
- AC8 header card: NearsSurfaceCard (white, no border, ambient shadow), navy "Flash Sale" title (PublicSans), mint "Limited Time Offer" badge w/ navy bolt+text, navy TimerWidget cells + Days/Hours/mins/sec labels. PASS. [09]
- AC8 product cards = NearsSurfaceCard (no border, ambient shadow), mint discount tag, navy Organic tag, navy price, strike price, mint + button. PASS token re-theme. [09]
- *** TASK BUG (breaks_ac): RenderFlex overflow 8.0px bottom on FlashProductCardWidget Column (flash_product_card_widget.dart:90). Yellow/black overflow stripe clips the "Sold X/Y" stock-overlay text on EVERY flash product card. Confirmed via Flutter runtime error + visible stripe in [09]. Cause: NEARS-410 token pass upsized unit text 10->13px + strike price 10->15px (DoR 2H) without enlarging the fixed card height (mainAxisExtent 240 mobile / inner Column 100px box). DoR 2H pre-warned "verify card height is sufficient". ***

## Reachability findings (pre-existing, NOT introduced by NEARS-410)
- FavouriteScreen route /favourite: getFavouriteScreen() defined but NEVER called anywhere; no menu/drawer/nav entry. Orphaned 6amMart-base route. AC7 cannot be demonstrated live in this build (and web not bootable). Dispose fix + tab-pill tokens code-verified; 130 tests green. -> regression_bug.
- FlashSaleDetailsScreen IS reachable (grocery home Flash Sale header/See All) -> AC8 demonstrated live. (getFlashSaleDetailsScreen called from FlashSaleViewWidget.)
- enableCrossStoreSearch=false -> cross-store entry card on search + cross-store screen not reachable live; AC5 code-verified only.

## Dark mode (AC10)
- Settings + Search + grocery product grid legible in dark; mint toggles/price/discount tags clear; navy surfaces + white text. [10,12,13]
- Mobile "Pizza" history chip dark: navy pill, white text, legible, no 'x'. [12]
- Suggested-tile label text slightly soft on dark navyContainer (NearsText labelMd textBody) — borderline, falls under known NEARS-429 (record, not fail). Search FIELD text legible (no 429 repro on field, per DoR). 

## Web/desktop FINAL (AC1)
- UserApp has NO web/ platform dir (not web-configured): `flutter build web` bails ("not configured for the web"); `flutter run -d chrome/web-server` only runs in its own spawned browser via DDC, not drivable by external Playwright; stale build/web (Jun 9, different branch) is not this code. Scaffolding web (`flutter create . --platforms web`) would mutate the worktree (forbidden for QA). => desktop/web layout NOT bootable for QA in this build. AC1 (desktop per-chip remove) CODE-VERIFIED per DoR fallback.
