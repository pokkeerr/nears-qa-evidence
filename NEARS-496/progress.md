# NEARS-496 QA progress (light mode only; dark deferred)
Device: emulator-5556 (Android 17 / API 37), pkg com.izzes.nears, worktree feat/NEARS-496-remove-fresh-finds, baseUrl http://10.0.2.2:8000, zone 1 (Demo), logged-in.

- AC3 (dead-code grep) PASS: `grep -rn "SpecialOfferView|fresh_finds|Fresh Finds" UserApp/lib UserApp/assets` -> 0 matches. fresh_finds key also removed from en.json+ar.json.
- flutter analyze touched files: No issues found.
- AC1 GROCERY PASS: module home has NO "Fresh Finds" label. Top + mid captured.
- AC2 GROCERY PASS (logged-in junction): ItemThatYouLoveView "Buy It Again" -> VisitAgainView "Visit Again" -> RecommendedStoreView "6 stores near you" flow clean, normal spacing, no double-gap.
- REGRESSION (pre-existing, NOT NEARS-496): RenderFlex overflow 36px at cart_count_view.dart:64 (+/- stepper inside ItemCard). Untouched by diff (last touched NEARS-494). -> regression_bug.
