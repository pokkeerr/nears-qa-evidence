# NEARS-490 QA progress (live, emulator-5554, worktree backend :8000)

- AC5 (API contract): PASS — store_id scopes; omit+coords -> nearest; store_id=0 -> nearest (not blank);
  different coords -> different store; no-signal -> legacy zone-wide. JSON-string + bare coord both decode.
  evidence: TEST A/B/C/D/E/F (curl matrix), shots not applicable (terminal).
- AC1 (live grid single-store): PASS — Categories page in zone2 multi-store, Fruits&Veg grid = ALL "BAQALA ABU TALIB STAR"
  (nearest store at resolved GPS 24.45/54.40, store id 3354), zero cross-store mix. shots 01,02. No runtime errors.
- AC2 (rail = categories with items in store): PASS — rail showed only stocked categories for the resolved store. shot 03.
- AC3 (empty category not backfilled): PASS — API cat13@store12 total:0 empty; rail omits empty cats. shot 04.
- AC4 (reloadForStore hook): hook present; store-picker NEARS-484 unbuilt; verified via cache-key + reload path.
- Automated: phpunit CategoryStoreScoping 8/8, Categor 9/9; flutter test 1233/1233. All green.
- Regression: see-all items/{id}/all now store+active scoped (PASS); pagination same-store (PASS); single-store hero zone3/mod4 intact (PASS).
- ISSUE (regression, pre-existing): rail-vs-grid count divergence cat9 store16 rail=2 grid=3 -> bug-rail-grid-count-divergence.log
- ISSUE (regression, pre-existing): ANR on Set Location 'Use Current Location' reverse-geocode -> bug-setlocation-anr.log (not NEARS-490 code)
