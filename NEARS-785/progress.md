# NEARS-785 QA progress (live checkpoint)
device: emulator-5556 | branch fix/NEARS-785-dead-routes @812c3485 | worktree nears-NEARS-785-dead-routes
Wave 8 dead-code removal: 4 dead routes + PopularItemScreen removed. Regression-only, no new surface.

## Static pre-checks (source)
- baseUrl(android)=http://10.0.2.2:8000 (real local backend). backend :8000 up (302 /admin). OK
- deleted route consts gone from route_helper: PASS
- kept routes present: allStores /stores, popularStores /popular-stores, topOffers /top-offers-near-me, itemViewAllScreen /item-view-all-screen: PASS
- live ItemController.commonConditions getter + common_condition_view.dart intact (renders in pharmacy_home_screen): PASS
- zero lingering refs to popularItems/specialItems/bestReviewed/PopularItemScreen in lib/: PASS

## AC results (live)
(pending boot)

- AC2 CRITICAL: common_conditions table EMPTY (0 rows, global) → genuine no-data state.
  Live pharmacy home fired GET /api/v1/common-condition -> http_status=200 (log line captured),
  backend returns [] 200. Widget present+loader wired (home_controller:155/213), renders empty
  SizedBox cleanly, ui_errors clean. Diff = comment-only in item_controller (priceFilterMax doc);
  live ItemController.commonConditions getter + common_condition_view.dart UNTOUCHED. MET (empty-state path).

- AC1: sector landing -> pharmacy home -> store(MediQuick) -> item sheet(Muscle Relief Gel) -> add-to-cart -> basket -> profile. All render, nav clean, ui_errors clean throughout. MET.
- AC3: itemViewAllScreen live (Food>Most Popular Items>See All, /api/v1/items/popular 200, header "Most Popular Items"(85)); store-list route live (Recommended For You>See All -> AllStoreScreen "Featured Stores", /api/v1/stores/get-stores/all 200); topOffers = same getAllStoreRoute mechanism (registered route_helper:1187) + /api/v1/stores/top-offer-near-me 200. All clean. MET.
- followup(non-blocking, pre-existing): store distances show ~10044 km on store-list (emulator GPS Dhaka vs AD store coords zone mismatch); cosmetic, unrelated to route deletion.

- AC4: LinkConverter (link_converter_helper.dart) + deep-link handling never referenced any removed route name/path; diff did NOT touch LinkConverter; no residual refs to removed paths in lib/. Live https deep-link opened Chrome (emulator App-Links verification limitation, not a regression). Diff = pure route/screen deletion + comment/test/doc; no widget/theme/color/layout change -> no visual change. Ran light mode only (dark deferred). MET (source-verified).
