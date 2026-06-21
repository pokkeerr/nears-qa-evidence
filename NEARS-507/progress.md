# NEARS-507 QA progress (live checkpoint)

Device: emulator-5554 · Backend: worktree Admin on :8000 (StoreLogic NEARS-507 fix live, cwd-verified)
Build under test: worktree feat/NEARS-507-search-stores-tab (working-tree changes)

## Backend API proof (pre-UI)
- AC2 zone-scope: search "market" mod=1 zone=[2] -> 8 stores ALL zone=2; zone=[1] -> 1 store zone=1. No cross-zone leak. PASS
- Fail-closed: zoneId="2" (scalar) -> 0 rows; zoneId="[]" -> 0 rows. PASS

## Live UI ACs
- AC1 (zone2 grocery, 13>10): search "market" -> 2-tab layout (Item Tab1of2 / Stores Tab2of2). Stores tab = full-width STORE rows (Eco Market, Fast Market, Fresh supermarket, Online market, Vegan Market, Veggie Market) w/ ETA badges, NOT item cards. CLOSED state shown (Abu Dhabi Fresh Market = CLOSED, addr "Al Wahda Mall, Abu Dhabi"). Switch back to Item tab reloads item context (chips return). PASS
- AC2 (UI cross-check): every store on zone2 Stores tab is a zone-2 grocery store; no zone-1 store (Corner Grocer/Nears Mart/etc) appears. + API proof above. PASS
- AC3: Stores tab has NO category-chips row and NO "Explore by Category" block; Item tab HAS chips (Fresh Fruits/Fresh Vegetables/Fruits&Vegetables/General Items) + item grid. PASS
- Items tab regression: "fresh"/"milk" return item cards w/ price, Add To Cart, discount badges across zone-2 stores. Clean.
- ui_errors: clean (no GetX/overflow/exception) through AC1-3.
- AC4 (zone2 Pharmacy, 5 stores <=10): search "vitamin" -> items render (Multivitamin/Vitamin C/D3 from zone-2 pharmacies) w/ NO TabBar, NO 1-tab strip, NO 48dp gap, NO divider artifact (screenshot-verified: heading->chips->grid flows clean). PASS
- AC4 (zone1 Grocery, 6 stores <=10): search "rice" -> "Rice 5kg" NEARS MART item, chips present, NO TabBar. PASS (2nd data point)
- AC5 (zone2 Grocery, 13>10): Stores tab present (2-tab layout). PASS
- Regression empty-store-state: zone2 grocery search "zzqqxnostore" -> Stores tab "No store available" no-data screen, no crash. Clean.
- Regression home store lists zone-correct: zone2 home = Abu Dhabi Fresh Market/Organic Shop/Test Store; zone1 home = Fresh Mart Grocery/Nears Mart/Organic Paradise. get_combined_data shared method intact. Clean.
- Regression grid/list toggle: present top-right of results row (screenshot-verified), unchanged. Clean.
