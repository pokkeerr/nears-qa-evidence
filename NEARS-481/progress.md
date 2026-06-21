# NEARS-481 QA progress checkpoint

Device: emulator-5556 | Build: UserApp worktree (feat/NEARS-481-category-landing-sections, dirty fix)
Backend: worktree Admin on :8001 (reskin-tip + NEARS-475 active_stores_count) — app host repointed to :8001 (TEMP, revert before exit)

## Observed
- [PASS] AC-3 multi-store (zone1/grocery): Daily Essentials ABSENT across full feed scroll; store rails (Popular, Stores, Newly joined, Top Rated, Fresh Finds) render. shot 01-zone1-grocery-multistore-rails.png
- App language switched EN; running guest (customer endpoints 500 for guest, expected).
- /api/v1/module on :8001 returns active_stores_count: zone3/mod4=1, zone2/mod2=5, zone2/mod3=5, zone1 all>=6.
- [PASS] AC-2 food (zone2/mod2): backend popular+latest return store47 (closed) +49,50,51,52; home store rail "New on Nears" shows only open stores (Spice Route/Noodle/Golden Wok/Mediterranean); Grill House(47) only in main "Restaurants" all-stores list (5 near you) w/ Closed badge = allowed (no over-reach). Daily Essentials HIDDEN (multi-store). shots 06-11.
- [PASS] AC-2 pharmacy (zone2/mod3): backend returns CarePlus(53,closed)+55,56,57,58; New on Nears rail (isolated, shot 15) shows Family Health/MediQuick (open), CarePlus ABSENT (count 0 across rail scroll); CarePlus only in main "Stores" list. Daily Essentials HIDDEN. shots 12-15.
- Pre-existing (regression candidate, NOT this change): /api/v1/cashback/list 500 -> "type 'Null' is not a subtype of FutureOr<List<CashBackModel>>" in HomeService.getCashBackOfferList; surfaces "Something went wrong" toast on guest module home. Also customer/* endpoints 500 in guest mode.
- [PASS] AC-1 (zone3/mod4 single-store): ALL store rail headers ABSENT (Popular/Best/Featured/New on Nears/Top offers/Visit Again/Newly joined/Top Rated/Stores-in-Tower all 0); single-store hero + "Shop NEARS-257 Fixture Store" fast-path present (NEARS-253 OK); clean feed, no orphan header / no whitespace residue. shots 16-18. Confirmed light, dark (17), RTL+dark (18).
- [PASS] AC-3 multi-store HIDDEN: live zone1/zone2 food/zone2 pharmacy. AC-3 single-store VISIBLE: requires a TOWER address (YourTowerView line 65 gates on towerName != null); no zone-3 tower address seeded + guest cannot add one + DB read-only -> covered by widget test your_tower_view_test.dart (single-store+tower -> Daily Essentials findsOneWidget). Test-covered, documented.
- Automated backstop: 22 NEARS-481 widget tests PASS (popular_store_view_closed_filter, recommended_store_view, your_tower_view, module_controller_single_store, available_stores_filter).
- RTL+dark food rail (shot 20): New on Nears shows open stores (Spice Route/Noodle NEW badges), closed Grill House only in main Restaurants list w/ "مغلق" badge. No overflow/stray padding.
- No runtime errors across full session (get_runtime_errors clean repeatedly).
