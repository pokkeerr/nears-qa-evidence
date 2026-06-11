# NEARS-333 QA progress (live demonstration log)

Build: worktree /Users/Apple/Projects/nears-NEARS-333-search-mvvm @ 280051d9
Device: emulator-5554 (Android, flutter run from worktree/UserApp)
Backend: http://10.0.2.2:8000 (config 200), php artisan serve up
Automated backstop: search_controller_test 28/28 green; full UserApp suite 679 green.

| AC | result | evidence | when |
|----|--------|----------|------|
| AC4 start-match bold+TitleCase + case-insensitive | PASS | shot suggest_br.png: lowercase "br" → "Br"occoli/"Br"own Bread/"Br"eakfast bold+capitalized; Banana/Bagels/Bell Peppers (no "br") plain | live |
| AC4 clear query → plain rows | PASS (logic: matched:false when empty) | confirmed in tree + unit pin +27 | live/test |
| AC4 mid-string bold+RAW (not title-cased) | PASS | shot suggest_ana.png: "ana" → "B"+bold"ana"+"na", slice stays lowercase; Mango/Tomato/Cola plain | live |
| AC1 price-max mobile (_openFilterSheet) | PASS | "Milk" search → 5 results, backend max price 9.46 (Low Fat Milk); filter sheet slider item-derived (0%→100% drag, 9 divisions), NOT 1000 default | live + backend xcheck |
| AC1 price-max desktop (FilterWidget) | PASS (same getter; phone build is mobile layout) | identical searchItemPriceFilterMax call in _actionSearch else; unit pins +16-21 | test/structural |
| AC2 store mode → max 1000 (isStore guard) | PASS | Stores tab filter sheet: NO Price slider rendered (isStore gating); getter !isStore short-circuit → 1000; unit pin +19 | live + test |
| AC3 empty results → max 1000 | PASS | "zzqxnoresults" → "No item available"; filter sheet Price slider renders continuous 1000-div track (vs coarse 9-tick for Milk); unit pin +18 | live + test |
| AC5 existing flows unchanged | PASS | submit search OK; item↔store tab toggle OK; history chips record+rerun+clear-all OK; popular categories tap loads results; suggestions rail OK; leading/trailing icons present | live |
| AC5 cross-store / voice entry | n/a-gated/PASS | cross-store gated OFF (enableCrossStoreSearch=false, pre-existing config); voice mic icon present in field (unchanged by this refactor) | live/config |

Final: NO runtime errors / overflows in app log across full session. Verdict: PASS.
