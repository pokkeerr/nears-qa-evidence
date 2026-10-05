# NEARS-3996 step 4 QA - independent mutation pass (scratch copy, tip cf67afd23)

Own list written BEFORE reading the engineer/independent logs (script c3996s4_muts.py, 162 + 3 re-formulations). Method: scratch copy of UserApp + packages (excl. build/.dart_tool/ios/android/public) under the session scratchpad with its own `flutter pub get --offline`; unmutated control green in scratch first; one mutation at a time applied from the LIVE tip file; each proved LANDED by a non-empty `diff -U0 live scratch` hunk (mutation_diffs.txt) and each restore proved by `cmp live scratch`; tier 1 = owner_test, characterization, facade wiring, source scan, independent pass (stop at first red, one file per invocation via mem-guard, cap 6 GB, pinned SDK 3.41.9); tier 2 (survivors only) = 10 pre-existing nets.

**Totals: 165 mutant rows; 159 KILLED, 5 SURVIVED (all EQUIVALENT, 0 REAL), 1 compile-guard (own syntax slip, re-formulated). Effective fresh mutants = 164. All 165 landed=True, all restored (cmp)=True.**

| id | mutation | result | first killer | landed | restored (cmp) | classification |
|---|---|---|---|---|---|---|
| F1 | open-first reads facade getter not owner field | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F2 | open-first null check via facade getter | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F3 | nearestStoreId reads facade getter | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F4 | nearestStoreId scans null list | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F5 | recommended-item reload no longer nulls the model | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F6 | recommended-item reload clears whole zone | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F7 | setPopularFromHomeAll writes latest | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F8 | setLatestFromHomeAll writes popular | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F9 | setPopularFromHomeAll no notify | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F10 | setLatestFromHomeAll no notify | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F11 | clearZoneStores skips owner reset | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F12 | clearZoneStores keeps recommended list | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F13 | clearZoneStores keeps visitAgain list | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F14 | clearZoneStores keeps recommended failed flag | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F15 | clearZoneStores no notify | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F16 | activeAllStoreList featured -> latest | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F17 | activeAllStoreList popular -> latest | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F18 | activeAllStoreList latest -> popular | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F19 | activeAllStoreList popular via facade getter | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F20 | activeAllStoreListFailed featured -> latest | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F21 | activeAllStoreListFailed popular -> featured | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F22 | activeAllStoreListFailed latest -> popular | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| F23 | activeAllStoreListFailed featured via facade getter | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| N1 | clearStoreModel writes empty model | KILLED | store_discovery_owner_test.dart | True | True |  |
| N2 | replacePopular aliases the argument | KILLED | store_discovery_owner_test.dart | True | True |  |
| N3 | replaceLatest aliases the argument | KILLED | store_discovery_owner_test.dart | True | True |  |
| N4 | replacePopular reverses | KILLED | store_discovery_owner_test.dart | True | True |  |
| N5 | replaceLatest skips first | KILLED | store_discovery_owner_test.dart | True | True |  |
| N6 | replacePopular fills latest | KILLED | store_discovery_owner_test.dart | True | True |  |
| N7 | clearForZone keeps popular | KILLED | store_discovery_owner_test.dart | True | True |  |
| N8 | clearForZone keeps latest | KILLED | store_discovery_owner_test.dart | True | True |  |
| N9 | clearForZone keeps featured | KILLED | store_discovery_owner_test.dart | True | True |  |
| N10 | clearForZone keeps storeModel | KILLED | store_discovery_owner_test.dart | True | True |  |
| N11 | clearForZone keeps storeLoadFailed | KILLED | store_discovery_owner_test.dart | True | True |  |
| N12 | clearForZone keeps popular failed | KILLED | store_discovery_owner_test.dart | True | True |  |
| N13 | clearForZone keeps latest failed | KILLED | store_discovery_owner_test.dart | True | True |  |
| N14 | clearForZone keeps featured failed | KILLED | store_discovery_owner_test.dart | True | True |  |
| N15 | clearForZone sets storeLoadFailed true | KILLED | store_discovery_owner_test.dart | True | True |  |
| N16 | clearForZone bumps session id | KILLED | store_discovery_owner_test.dart | True | True |  |
| N17 | clearForZone resets the session id | KILLED | store_discovery_owner_test.dart | True | True |  |
| P1 | shim _filterType constant all | KILLED | store_discovery_owner_test.dart | True | True |  |
| P2 | shim _storeType reads filterType | KILLED | store_discovery_owner_test.dart | True | True |  |
| P3 | shim _storeType setter no-op | KILLED | store_discovery_owner_test.dart | True | True |  |
| P4 | shim _type setter writes storeType | KILLED | store_discovery_owner_test.dart | True | True |  |
| P5 | shim hasDeliveryOrigin negated | KILLED | store_discovery_owner_test.dart | True | True |  |
| P6 | shim update no notify | KILLED | store_discovery_owner_test.dart | True | True |  |
| P7 | facade port filterType reads _storeType | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| P8 | facade port storeType reads _filterType | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| P9 | facade port storeType setter writes _filterType | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| P10 | facade port type setter no-op | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| P11 | facade port hasDeliveryOrigin always true | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| P12 | facade port notify dropped | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| P13 | facade port notify carries an id | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| D1 | getStoreList delegate source fixed local | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| D2 | getStoreList delegate drops emptyOnClientFailure | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| D3 | getStoreList delegate drops onListSettled | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| D4 | getStoreList default source client | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| D5 | getStoreList default emptyOnClientFailure true | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| D6 | getPopularStoreList default dataSource client | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| D7 | getPopularStoreList default fromRecall true | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| D8 | getPopularStoreList delegate -> latest | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| D9 | getLatestStoreList delegate -> popular | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| D10 | getFeaturedStoreList delegate fixed local | KILLED | store_discovery_extraction_source_scan_test.dart | True | True |  |
| D11 | getLatestStoreList delegate drops fromRecall | KILLED | store_discovery_extraction_source_scan_test.dart | True | True |  |
| D12 | getPopularStoreList delegate drops notify | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| G1 | getter storeModel -> null | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| G2 | getter storeLoadFailed -> popular failed | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| G3 | getter popular failed -> latest failed | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| G4 | getter latest failed -> featured failed | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| G5 | getter featured failed -> popular failed | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| G6 | getter session id constant 0 | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| G7 | getter popular -> latest list | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| G8 | getter latest -> featured list | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| G9 | getter featured -> popular list | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| S1 | nearest fallback && -> || | KILLED | store_discovery_owner_test.dart | True | True |  |
| S2 | nearest fallback to fastest | KILLED | store_discovery_owner_test.dart | True | True |  |
| S3 | nearest fallback only for page 1 sentinel (drops write) | KILLED | store_discovery_owner_test.dart | True | True |  |
| S4 | reload keeps model | KILLED | store_discovery_owner_test.dart | True | True |  |
| S5 | reload keeps failed flag | KILLED | store_discovery_owner_test.dart | True | True |  |
| S6 | session bump by 2 | KILLED | store_discovery_owner_test.dart | True | True |  |
| S7 | session bump dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| S8 | reload notify dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| S9 | local branch for offset<=1 only matters at 0 (offset==1 -> offset<2) | SURVIVED | - | True | True | EQUIVALENT: every caller passes offset >= 1 (getStoreList(1,..) from home/chips and pagination offsets >= 2); `offset == 1` and `offset < 2` partition the reachable domain identically |
| S10 | local call source client | KILLED | store_discovery_owner_test.dart | True | True |  |
| S11 | local call swaps filter and store type | KILLED | store_discovery_owner_test.dart | True | True |  |
| S12 | local settle callback dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| S13 | recursion asks next offset | KILLED | store_discovery_owner_test.dart | True | True |  |
| S14 | recursion drops emptyOnClientFailure | KILLED | store_discovery_owner_test.dart | True | True |  |
| S15 | recursion drops onListSettled | KILLED | store_discovery_owner_test.dart | True | True |  |
| S16 | recursion reload true | KILLED | store_discovery_owner_test.dart | True | True |  |
| S17 | client call source local | KILLED | store_discovery_owner_test.dart | True | True |  |
| S18 | client call passes storeType first | KILLED | store_discovery_owner_test.dart | True | True |  |
| S19 | synthetic-empty guard drops emptyOnClientFailure | KILLED | store_discovery_owner_test.dart | True | True |  |
| S20 | synthetic-empty guard _storeModel != null | KILLED | store_discovery_owner_test.dart | True | True |  |
| S21 | synthetic-empty guard offset >= 1 | KILLED | store_discovery_family_characterization_baseline_test.dart | True | True |  |
| S22 | synthetic model offset 2 | KILLED | store_discovery_owner_test.dart | True | True |  |
| S23 | synthetic model total 1 | KILLED | store_discovery_owner_test.dart | True | True |  |
| S24 | synthetic branch flag false | KILLED | store_discovery_owner_test.dart | True | True |  |
| S25 | synthetic branch no notify | KILLED | store_discovery_owner_test.dart | True | True |  |
| S26 | client settle only offset>1 | KILLED | store_discovery_owner_test.dart | True | True |  |
| S27 | client settle callback dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| S28 | return always true | KILLED | store_discovery_owner_test.dart | True | True |  |
| S29 | return inverted | KILLED | store_discovery_owner_test.dart | True | True |  |
| R1 | prepare page1 flag not cleared | KILLED | store_discovery_owner_test.dart | True | True |  |
| R2 | prepare page>1 totalSize not copied | KILLED | store_discovery_owner_test.dart | True | True |  |
| R3 | prepare page>1 offset not copied | KILLED | store_discovery_owner_test.dart | True | True |  |
| R4 | prepare page>1 prepends | KILLED | store_discovery_owner_test.dart | True | True |  |
| R5 | prepare analytics dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| R6 | prepare notify dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| R7 | prepare page1 keeps old model | KILLED | store_discovery_owner_test.dart | True | True |  |
| A1 | analytics registered guard inverted | KILLED | store_discovery_owner_test.dart | True | True |  |
| A2 | analytics preview test inverted | KILLED | store_discovery_owner_test.dart | True | True |  |
| A3 | analytics position zero based | KILLED | store_discovery_owner_test.dart | True | True |  |
| A4 | analytics withPopular = total | COMPILE-GUARD | store_discovery_owner_test.dart | True | True | COMPILE-GUARD (my own mutation broke syntax: replaced the first `withPopular` inside `withPopularItemsCount`); re-formulated as A4b, KILLED |
| A5 | analytics list id changed | KILLED | store_discovery_owner_test.dart | True | True |  |
| A6 | analytics count counts raw (incl null) entries | SURVIVED | - | True | True | EQUIVALENT: StoreModel.stores is `List<Store>?` (non-null elements by type, parser adds only Store.fromJson), so `.whereType<Store>()` never drops an element and `stores.length` == raw length |
| U1 | popular type write dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| U2 | popular reload keeps list | KILLED | store_discovery_owner_test.dart | True | True |  |
| U3 | popular reload keeps failed | KILLED | store_discovery_owner_test.dart | True | True |  |
| U4 | popular notify inverted | KILLED | store_discovery_owner_test.dart | True | True |  |
| U5 | popular fetch guard drops reload | SURVIVED | - | True | True | EQUIVALENT: `if (reload) _popularStoreList = null;` executes synchronously (no await) right before the guard, so `_popularStoreList == null` is already true whenever `reload` is; the `|| reload` operand is redundant |
| U6 | popular fetch guard drops fromRecall | KILLED | store_discovery_owner_test.dart | True | True |  |
| U7 | popular local call source client | KILLED | store_discovery_owner_test.dart | True | True |  |
| U8 | popular local call type fixed | KILLED | store_discovery_owner_test.dart | True | True |  |
| U9 | popular local assign dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| U10 | popular local update dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| U11 | popular recursion notify true | KILLED | store_discovery_owner_test.dart | True | True |  |
| U12 | popular recursion fromRecall false | KILLED | store_discovery_owner_test.dart | True | True |  |
| U13 | popular recursion type fixed | KILLED | store_discovery_owner_test.dart | True | True |  |
| U14 | popular client success keeps failed | KILLED | store_discovery_owner_test.dart | True | True |  |
| U15 | popular failure guard inverted | KILLED | store_discovery_owner_test.dart | True | True |  |
| U16 | popular failure flag false | KILLED | store_discovery_owner_test.dart | True | True |  |
| U17 | popular client update dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| U18 | popular client call source local | KILLED | store_discovery_owner_test.dart | True | True |  |
| L1 | latest type write dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| L2 | latest reload keeps list | KILLED | store_discovery_owner_test.dart | True | True |  |
| L3 | latest reload keeps failed | KILLED | store_discovery_owner_test.dart | True | True |  |
| L4 | latest notify inverted | KILLED | store_discovery_owner_test.dart | True | True |  |
| L5 | latest fetch guard drops fromRecall | KILLED | store_discovery_owner_test.dart | True | True |  |
| L6 | latest fetch guard drops reload | SURVIVED | - | True | True | EQUIVALENT: identical argument for the latest list (`_latestStoreList = null` on reload, same synchronous prefix) |
| L7 | latest local update dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| L8 | latest recursion notify true | KILLED | store_discovery_owner_test.dart | True | True |  |
| L9 | latest recursion fromRecall false | KILLED | store_discovery_owner_test.dart | True | True |  |
| L10 | latest client success keeps failed | KILLED | store_discovery_owner_test.dart | True | True |  |
| L11 | latest failure guard inverted | KILLED | store_discovery_owner_test.dart | True | True |  |
| L12 | latest failure flag false | KILLED | store_discovery_owner_test.dart | True | True |  |
| L13 | latest client update dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| L14 | latest local call type fixed | KILLED | store_discovery_owner_test.dart | True | True |  |
| L15 | latest local assign to popular | KILLED | store_discovery_owner_test.dart | True | True |  |
| H1 | featured local keeps stale failed flag | KILLED | store_discovery_owner_test.dart | True | True |  |
| H2 | featured local source follows client | KILLED | store_discovery_owner_test.dart | True | True |  |
| H3 | featured local prepare dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| H4 | featured local recursion dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| H5 | featured failure guard && -> || | KILLED | store_discovery_owner_test.dart | True | True |  |
| H6 | featured failure flag false | KILLED | store_discovery_owner_test.dart | True | True |  |
| H7 | featured client prepare dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| H8 | featured prepare drops flag clear | KILLED | store_discovery_owner_test.dart | True | True |  |
| H9 | featured prepare drops zone check | KILLED | store_discovery_owner_test.dart | True | True |  |
| H10 | featured prepare drops module check | KILLED | store_discovery_owner_test.dart | True | True |  |
| H11 | featured prepare notify dropped | KILLED | store_discovery_owner_test.dart | True | True |  |
| H12 | featured prepare ignores module list | KILLED | store_discovery_owner_test.dart | True | True |  |
| H13 | featured client failure guard checks popular list | KILLED | store_discovery_owner_test.dart | True | True |  |
| S9b | local branch guard offset==1 -> offset<=1 | SURVIVED | - | True | True | EQUIVALENT: same domain argument as S9 (offset >= 1), `<= 1` == `== 1` for offset >= 1 |
| S9c | local branch guard offset==1 -> offset>=1 (offset 0 would go local) | KILLED | store_discovery_owner_test.dart | True | True |  |
| A4b | analytics withPopularItemsCount = total (re-formulated A4; first A4 broke syntax) | KILLED | store_discovery_owner_test.dart | True | True |  |
