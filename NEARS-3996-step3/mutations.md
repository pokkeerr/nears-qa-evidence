# NEARS-3996 step 3 QA - independent mutation pass (scratch copy, sha 7103c127)

Own list written BEFORE reading the engineer (124) / independent (84) logs; round 3 re-formulated the classes the independent pass had found (tab-sync value, retry capture, fire-and-forget delegates, reset ordering, extra operand) to verify the fix-cycle assertions myself.
Method: scratch copy (UserApp + packages, excl build/.dart_tool/ios/android/public) in the session scratchpad, own `flutter pub get --offline`, one mutation at a time; each proved LANDED by `diff -U0 live scratch` non-empty (diffs in mutation_diffs.txt) and each restore proved by `cmp live scratch`; tier 1 = owner_test, characterization, wiring, scan (stop at first red), tier 2 (only for tier-1 survivors) = 13 pre-existing nets; every run via mem-guard, cap 6 GB, one file per invocation; unmutated control green in scratch first.

| id | mutation | result | first killer | landed | restored (cmp) |
|---|---|---|---|---|---|
| Z1 | getOfferCategories: zoneId -> null | KILLED | store_offers_owner | True | True |
| D1 | getOfferCategories: moduleId -> null | KILLED | store_offers_owner | True | True |
| Z2 | selectOfferCategory: zoneId -> null | KILLED | store_offers_owner | True | True |
| D2 | selectOfferCategory: moduleId -> null | KILLED | store_offers_owner | True | True |
| Z3 | getOfferCategoryItemListPaginated: zoneId -> null | KILLED | store_offers_owner | True | True |
| D3 | getOfferCategoryItemListPaginated: moduleId -> null | KILLED | store_offers_owner | True | True |
| Z4 | selectAllOffers: zoneId -> null | KILLED | store_offers_owner | True | True |
| D4 | selectAllOffers: moduleId -> null | KILLED | store_offers_owner | True | True |
| Z5 | getStoreOfferItemListPaginated: zoneId -> null | KILLED | store_offers_owner | True | True |
| D5 | getStoreOfferItemListPaginated: moduleId -> null | KILLED | store_offers_owner | True | True |
| A1 | getOfferCategories: drop the reset-to-null | KILLED | store_offers_owner | True | True |
| A2 | getOfferCategories: drop the reset notify | KILLED | store_offers_owner | True | True |
| A3 | getOfferCategories: failure collapses to null not [] | KILLED | store_offers_owner | True | True |
| A4 | getOfferCategories: drop answer notify | KILLED | store_offers_owner | True | True |
| A5 | getOfferCategories: request uses store id not the arg | KILLED | store_offers_owner | True | True |
| B1 | selectOfferCategory: guard || -> && | KILLED | store_offers_owner | True | True |
| B2 | selectOfferCategory: drop selected flag | KILLED | store_offers_owner | True | True |
| B3 | selectOfferCategory: drop category id write | KILLED | store_offers_owner | True | True |
| B4 | selectOfferCategory: tab index off by one | KILLED | store_offers_owner | True | True |
| B5 | selectOfferCategory: tab sync skips index 0 (tabIndex > 0) | KILLED | store_offers_owner | True | True |
| B6 | selectOfferCategory: drop analytics | KILLED | store_offers_owner | True | True |
| B7 | selectOfferCategory: drop session bump | KILLED | store_offers_owner | True | True |
| B8 | selectOfferCategory: retry target swapped to selectAllOffers | KILLED | store_offers_owner | True | True |
| B9 | selectOfferCategory: drop retry arming | KILLED | store_offers_owner | True | True |
| B10 | selectOfferCategory: drop reset notify | KILLED | store_offers_owner | True | True |
| B11 | selectOfferCategory: drop failed-flag clear | KILLED | store_offers_owner | True | True |
| B12 | selectOfferCategory: first page requested as page 2 | KILLED | store_offers_owner | True | True |
| B13 | selectOfferCategory: first-page failure leaves failed=false | KILLED | store_offers_owner | True | True |
| B14 | selectOfferCategory: drop answer notify | KILLED | store_offers_owner | True | True |
| B15 | selectOfferCategory: model null clear dropped | KILLED | store_offers_owner | True | True |
| C1 | cat pager: guard || -> && | KILLED | store_offers_owner | True | True |
| C2 | cat pager: guard returns false | KILLED | store_offers_owner | True | True |
| C3 | cat pager: always asks page 1 | KILLED | store_offers_owner | True | True |
| C4 | cat pager: drop items ??= [] | KILLED | store_offers_owner | True | True |
| C5 | cat pager: drop totalSize copy | KILLED | store_offers_owner | True | True |
| C6 | cat pager: drop dedupe | KILLED | store_offers_owner | True | True |
| C7 | cat pager: return true always | KILLED | store_offers_owner | True | True |
| C8 | cat pager: drop model-null guard | KILLED | store_offers_owner | True | True |
| C9 | cat pager: items! instead of ?? [] | KILLED | store_offers_owner | True | True |
| C10 | cat pager: drop offset copy | KILLED | store_offers_owner | True | True |
| P1 | offers pager: drop items ??= [] | KILLED | store_offers_owner | True | True |
| P2 | offers pager: drop totalSize copy | KILLED | store_offers_owner | True | True |
| P3 | offers pager: drop dedupe | KILLED | store_offers_owner | True | True |
| P4 | offers pager: return true always | KILLED | store_offers_owner | True | True |
| P5 | offers pager: drop model-null guard | KILLED | store_offers_owner | True | True |
| P6 | offers pager: drop offset copy | KILLED | store_offers_owner | True | True |
| P7 | offers pager: items! instead of ?? [] | KILLED | store_offers_owner | True | True |
| P8 | offers pager: drop !selected clause | KILLED | store_offers_owner | True | True |
| P9 | offers pager: id guard flipped (== null) | KILLED | store_offers_owner | True | True |
| P10 | offers pager: guard returns false | KILLED | store_offers_owner | True | True |
| P11 | offers pager: always asks page 1 | KILLED | store_offers_owner | True | True |
| P12 | offers pager: store null guard dropped | KILLED | store_offers_owner | True | True |
| S1 | selectAllOffers: guard flipped | KILLED | store_offers_owner | True | True |
| S2 | selectAllOffers: drop selected flag | KILLED | store_offers_owner | True | True |
| S3 | selectAllOffers: drop id reset to null | KILLED | store_offers_owner | True | True |
| S4 | selectAllOffers: drop analytics | KILLED | store_offers_owner | True | True |
| S5 | selectAllOffers: drop session bump | KILLED | store_offers_owner | True | True |
| S6 | selectAllOffers: drop retry arming | KILLED | store_offers_owner | True | True |
| S7 | selectAllOffers: retry target swapped | KILLED | store_offers_owner | True | True |
| S8 | selectAllOffers: drop model null clear | KILLED | store_offers_owner | True | True |
| S9 | selectAllOffers: drop failed-flag clear | KILLED | store_offers_owner | True | True |
| S10 | selectAllOffers: drop reset notify | KILLED | store_offers_owner | True | True |
| S11 | selectAllOffers: first page requested as 2 | KILLED | store_offers_owner | True | True |
| S12 | selectAllOffers: first-page branch flipped | KILLED | store_offers_owner | True | True |
| S13 | selectAllOffers: drop answer notify | KILLED | store_offers_owner | True | True |
| S14 | selectAllOffers: failure sets failed=false | KILLED | store_offers_owner | True | True |
| N1 | chip analytics: store_id null | KILLED | store_offers_owner | True | True |
| N2 | chip analytics: unregistered guard removed | KILLED | store_offers_owner | True | True |
| N3 | cat analytics: unregistered guard removed | KILLED | store_offers_family_characterization_baseline | True | True |
| N4 | cat analytics: store_id 0 when unresolved | KILLED | store_offers_owner | True | True |
| N5 | cat analytics: wrong event name | KILLED | store_offers_owner | True | True |
| N6 | cat analytics: category_id param dropped | KILLED | store_offers_owner | True | True |
| K1 | clearSelection: drop flag clear | KILLED | store_offers_owner | True | True |
| K2 | clearSelection: drop id clear | KILLED | store_offers_owner | True | True |
| G1 | hasOfferCategories ignores emptiness | KILLED | store_offers_owner | True | True |
| T1 | port: store getter null | KILLED | store_offers_family_characterization_baseline | True | True |
| T2 | port: categoryList getter null | KILLED | store_offers_family_characterization_baseline | True | True |
| T3 | port: categoryIndex setter no-op | KILLED | store_offers_family_characterization_baseline | True | True |
| T4 | port: storeItemModel getter null | KILLED | store_offers_family_characterization_baseline | True | True |
| T5 | port: storeItemModel setter no-op | KILLED | store_offers_family_characterization_baseline | True | True |
| T6 | port: storeItemsFailed setter inverted | KILLED | store_offers_family_characterization_baseline | True | True |
| T7 | port: session getter 0 | KILLED | store_offers_family_characterization_baseline | True | True |
| T8 | port: session setter no-op | KILLED | store_offers_family_characterization_baseline | True | True |
| T9 | port: retry setter no-op | KILLED | store_offers_family_characterization_baseline | True | True |
| T10 | port: dedupe no-op | KILLED | store_offers_family_characterization_baseline | True | True |
| T11 | port: notify no-op | KILLED | store_offers_family_characterization_baseline | True | True |
| T12 | port: notify carries an id | KILLED | store_offers_family_characterization_baseline | True | True |
| T13 | port: store getter captured at construction | SURVIVOR | - | True | True |
| F1 | facade: selectOfferCategory passes null | KILLED | store_offers_family_characterization_baseline | True | True |
| F2 | facade: cat pager routed to offers pager | KILLED | store_offers_family_characterization_baseline | True | True |
| F3 | facade: offers pager routed to cat pager | KILLED | store_offers_family_characterization_baseline | True | True |
| F4 | facade: selectAllOffers routed to selectOfferCategory(0) | KILLED | store_offers_family_characterization_baseline | True | True |
| F5 | facade: getOfferCategories passes null | KILLED | store_offers_family_characterization_baseline | True | True |
| F6 | facade: isOfferCategorySelected const false | KILLED | store_offers_family_characterization_baseline | True | True |
| F7 | facade: offerCategoryId const null | KILLED | store_offers_family_characterization_baseline | True | True |
| F8 | facade: hasOfferCategories ignores emptiness | KILLED | store_offers_family_characterization_baseline | True | True |
| F9 | facade: storeCatalogIsFiltered ignores offers | KILLED | store_offers_family_characterization_baseline | True | True |
| F10 | facade: getStoreDetails does not clear offers selection | KILLED | store_offers_family_characterization_baseline | True | True |
| F11 | facade: setCategoryIndex does not clear offers selection | KILLED | store_offers_family_characterization_baseline | True | True |
| F12 | facade: offerCategoryList getter null | KILLED | store_offers_family_characterization_baseline | True | True |
| T13b | port: store getter captured at construction (real capture) | COMPILE_GUARD | store_offers_owner | True | True |
| T14 | port: notify refreshes no ids (update([])) | KILLED | store_offers_family_characterization_baseline | True | True |
| X1 | PD-14 inverse: getOfferCategories gains a store guard (would FIX the pinned defect) | KILLED | store_offers_owner | True | True |
| X2 | PD-15 inverse: cat pager gains a session guard (would FIX the pinned defect) | SURVIVOR | - | True | True |
| X3 | PD-15 inverse: offers pager gains a selection guard (would FIX the pinned defect) | KILLED | store_offers_family_characterization_baseline | True | True |
| X4 | selectOfferCategory: analytics fired after the reset notify | KILLED | store_offers_owner | True | True |
| X5 | selectAllOffers: reset notify before the retry is armed | KILLED | store_offers_owner | True | True |
| X11 | selectOfferCategory: null category list guard dropped | KILLED | store_offers_owner | True | True |
| X14 | facade: owner re-created on every access (not one shared owner) | KILLED | store_offers_family_characterization_baseline | True | True |
| X18a | cat pager: dedupe runs before the append | KILLED | store_offers_owner | True | True |
| X18b | offers pager: dedupe runs before the append | KILLED | store_offers_owner | True | True |
| C11 | cat pager: drop final notify | KILLED | store_offers_owner | True | True |
| P13 | offers pager: drop final notify | KILLED | store_offers_owner | True | True |
| C12 | cat pager: store-null guard dropped | KILLED | store_offers_owner | True | True |
| X20 | selectAllOffers: store id sent as 0 | KILLED | store_offers_owner | True | True |
| T13d | port: store captured at construction and read from the capture (real capture) | KILLED | store_offers_family_characterization_baseline | True | True |
| Y1 | tab sync writes the category id, not the list position | KILLED | store_offers_owner | True | True |
| Y2 | selectOfferCategory retry closure reads the live offer id | KILLED | store_offers_owner | True | True |
| Y3 | facade selectOfferCategory fire-and-forget | KILLED | store_offers_facade_wiring | True | True |
| Y4 | facade selectAllOffers fire-and-forget | KILLED | store_offers_facade_wiring | True | True |
| Y5 | facade getOfferCategories fire-and-forget | KILLED | store_offers_family_characterization_baseline | True | True |
| Y6 | facade cat pager returns true without awaiting | KILLED | store_offers_family_characterization_baseline | True | True |
| Y7 | facade offers pager returns true without awaiting | KILLED | store_offers_family_characterization_baseline | True | True |
| Y8 | setCategoryIndex: clearSelection after the final notify | KILLED | store_offers_facade_wiring | True | True |
| Y9 | setCategoryIndex: clearSelection after the reload, before the notify | KILLED | store_offers_facade_wiring | True | True |
| Y10 | storeCatalogIsFiltered gains an extra operand | KILLED | store_offers_facade_wiring | True | True |
| Y11 | storeCatalogIsFiltered reads the sub-category id instead of the flag | KILLED | store_offers_family_characterization_baseline | True | True |
| Y12 | facade selectOfferCategory wrapped in async/await (one extra microtask hop) | SURVIVOR | - | True | True |
| Y13 | owner notify fires twice per update() | KILLED | store_offers_owner | True | True |
| Y14 | getOfferCategories resets to [] (hidden) instead of null (shimmer) | KILLED | store_offers_owner | True | True |
| Y15 | hasOfferCategories needs more than one card | KILLED | store_offers_family_characterization_baseline | True | True |
| Y16 | chip analytics: guard inverted | KILLED | store_offers_owner | True | True |
| Y17 | category analytics: guard inverted | KILLED | store_offers_owner | True | True |
| Y18 | owner dedupe shim is a no-op | KILLED | store_offers_owner | True | True |
| Y19 | owner session shim setter no-op | KILLED | store_offers_owner | True | True |
| Y20 | owner retry shim setter no-op | KILLED | store_offers_owner | True | True |

Totals: 136 mutants. KILLED 132, SURVIVOR 3, COMPILE_GUARD 1

## Survivors / guards

- **T13** - EQUIVALENT: the added `_cap` field is written but never read; the `store` getter is unchanged (derivation, my mutant did not capture anything). The real capture is T13d (KILLED).
- **Y12** - EQUIVALENT for every user-observable behaviour: `async => await` only adds one microtask hop before the Future completes (same state, same notifies, same wire). The solution doc claim "same microtask timing" is therefore not test-pinned (followup, Low).
- **X2** - REAL (unpinned): adds a null-id guard to the sub-category pager write-back. Observable: at tip a stale sub-category page 2 lands in the CATALOG list after a normal tab tap cleared the selection (probe: list [100..103] -> [100..103,32,33], 1 notify); with the guard it does not. No test in 17 files observes it. The pinned PD-15 cases (sub-chip -> sub-chip, both pagers) do not cover this sibling.
- **T13b** - COMPILE GUARD: `_cap` undefined (invalid mutant, rejected by the compiler; counted separately).
