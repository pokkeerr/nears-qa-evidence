# NEARS-485 — Cross-store search (UserApp) — QA progress

Device: emulator-5556 (Android 16 / API 37) · worktree feat/NEARS-485-cross-store-search · light mode · Zone 1 (Demo) / Module 1 (Grocery) · backend http://10.0.2.2:8000

| AC / check | result | evidence |
|---|---|---|
| AC1 cross-store ≥2 stores | PASS | `Cola 1.5L`→3 Cola stores + fuzzy; `Sparkling Water`→4 distinct stores. ac1-cross-store-results-english.png / ac2-grid-mode-store-names.png |
| AC2 store name (grid + list) | PASS | grid + list both show source store on each card. ac2-grid-mode-store-names.png, ac2-list-mode-store-names.png |
| AC3 tap → that store's item | PASS | Tower Mart Cola (4 AED) vs Nears Mart Cola (16 AED), each own sheet. ac3-towermart-cola-detail-sheet.png, ac3-nearsmart-cola-detail-sheet.png |
| AC4 zero-match NoDataScreen | PASS | "No item available" branded empty state. ac4-zero-match-nodatascreen.png |
| Analytics multi-store post-result | PASS | `search {search_term: Sparkling Water, result_count: 4, store_count_returned: 4}`. analytics-search-event.log |
| Analytics zero-match still fires 0/0 | PASS | `search {..., result_count: 0, store_count_returned: 0}` NOT suppressed. analytics-search-event.log |
| Analytics once-per-query post-result | PASS | 1 event per submitted query, no per-keystroke; voice path code-verified (same call-site) |
| REG NEARS-507 stores-tab gate | PASS | Zone1 Grocery=6 ≤10 → no Item/Stores TabBar, items only |
| REG module scoping | PASS | all result stores (1,2,3,36,37,38) module 1 grocery; no pharmacy/food bleed |
| REG grouped flag OFF (NEARS-208) | PASS | no "available at N stores" comparison UI |
| REG inStore guard | PASS | in-store product cards carry NO store-attribution line. reg-instore-no-attribution.png |
| REG RTL/Arabic alignment | PASS | store-name line aligns to start (right) grid+list. reg-rtl-arabic-grid.png, reg-rtl-arabic-list.png |
| Automated backstop | PASS | search_controller_test + search_result_widget_test = 42 pass; analytics_service_test = 8 pass |
| Runtime errors | clean | get_runtime_errors = none across home/search/store/sheet flows |
