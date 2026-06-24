# NEARS-495 QA progress (live checkpoint)
- backend: worktree :8001 (has get_offer_products + has_offers) — primary :8000 LACKS it, do not use
- device: emulator-5556 (locked)
- test data: OFFERS store 3 Organic Paradise (zone1,mod1,10 disc items); store 2 Fresh Mart (7); NO-OFFERS store 15 Sk General Store (zone2,mod1,0 items)
- backend spot-checks: scope OK, no-leak OK, no-offers OK, zone-less empty(no 500) OK, has_offers True/False correct, status=0 ->0
- backend tests: 10/10 PASS
- BE-log: clean (no offers errors; pre-existing unrelated ERROR lines only)

## Live (emulator-5556, zone 400 Abu Dhabi, nearest store=3168 Dama baqala)
- AC1 PASS: Offers tile FIRST in rail, local_offer glyph, DLS styling (ac1 shot)
- AC2 PASS: tap Offers -> grid = store 3168 ONLY (4 items, all discounted), no leak; backend mirror confirms store_ids=[3168]
- AC4 seen: discount badges 18% OFF / 3% OFF + strike-through prices render in offers grid
- offers call: /categories/items/offers?limit=10&offset=1&type=all (no store_id param -> backend nearest-resolves; multi-store zone, singleStoreId null)
- ANALYTICS FINDING: offers_rail_selected fired ONCE but with EMPTY params {} (no store_id) in multi-store zone (singleStoreId null). store_id only sourced from singleStoreId (single-store fast-path). low-sev analytics gap.
- Firebase Analytics DISABLED in build (Missing google_app_id) -> observed via internal AnalyticsService console line "📊 analytics:"

## Full results
- index-math regression PASS: Bakery->cat13, Dairy->cat6, Fruits&Veg->cat3, Snacks->cat12 (all exact, no off-by-one); rail data idx0=cat13 confirmed
- AC2 cross-store PASS (live): Abu Dhabi zone400 -> store 3168 items [47315,47318,47323,47325]; Demo zone1 -> store 1 (Nears Mart) items [40,97,102,104]; disjoint, single-store each
- AC3: backend has_offers:False for store15 + widget test "tile ABSENT when no offers" pass; not live-inducible (no reachable nearest no-offers store, read-only) -> backend+test-backed
- AC4 PASS (visual): 18%/3% OFF badges + strike-through prices in offers grid (ac2-ac4 shot)
- AC5 demonstrated: location switch re-resolves store + re-evaluates tile presence
- analytics: fires ONCE per Offers tap, NOT on category tap, NOT on rebuild; params {} (no store_id) in multi-store zone -> FINDING (low)
- silent-failure gate PASS: offers fetch fail -> [FAIL] endpoint=/api/v1/categories/items/offers correlationId present, PII-safe; NOT silent
- error state: grid stuck on shimmer on transport failure (shared with regular category grid -> pre-existing, regression-lane)
- endless-scroll: not live-inducible (no store >10 disc items); test-backed (pagination test pass)
- RTL: translations correct (العروض); live Arabic toggle not reachable via driver (nav-guide gap, followup)
- regression PASS: normal browse, sub-cat chips, add-to-cart (/cart/add hit), no overflow/red-screen/[FAIL]
- backend tests 10/10 PASS; widget tests 12/12 PASS
