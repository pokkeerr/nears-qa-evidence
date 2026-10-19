# NEARS-4185 QA progress (checkpoint log)
- tested_sha b9d427767a86af813ac50e1488af252a2ab0d3a5; twin multi_food_db_qa4185 (10 pending migrations applied, shared DB untouched, 271 migrations rows); own server php -S :8185 from worktree public (DB_DATABASE pinned, ps eww proves); freshness-check PASS.
- Device emulator-5558, pkg com.izzes.nears.nears_nears_4185_eta_display built by qa-run.sh from this worktree, API_HOST=10.0.2.2:8185.
- AC6 api: PASS (matrix in ac6 output; computed=created+max at all 5 states incl. picked_up no tightening; self-delivery no courier same; legacy source created+30; NULL source legacy parse 40 then picked_up+15; none null; computed NULL window null; HTTP 200, key present, forbidden eta_* substrings absent in track, running-orders, details raw bodies).
- Security probes: cust B -> 404 Not found; guest own-token -> 404 Not found; guest no/wrong token -> 401 (middleware, stricter).
- AC1: store card (24-26 besideLogo pill), store page header 16-18 min, item sheet pill 16-18 min, cart BK8 rows (mixed 16-18 / 18-20), checkout hero 'Arriving in 16-18 min', checkout mixed per-store lines: PASS (shots ac1-*). Single-store mobile cart has no ETA row by design (desktop only).
- AC4: single (38-40 @ addr60) and group (38-40 / 54-56 @ addr60) == curl stores/details at addr60 (38-40, 54-56): PASS; placed group orders computed 38-40/54-56 stored. Floor DEFERRED.
- AC3: gate tests 24 pass; grep predicate \bdeliveryTime\b only model mirrors; Fastest chip on Grocery, app order == server order (29/30 compared): PASS.
- AC5 countdown boundary sampler 107 samples: transitions at :00 of each minute 4->3->2->1->'Arriving any minute' at 20:05:00 never later than promise: PASS.
- Pre-existing: a11y tree dies on /search results (NEARS-3783 Table semantics assert) - known.
- AC2 PASS (closed store page/item sheet no pill; hidden-walking: cart/checkout line/hero collapse+map kept/confirm sheet row+divider omitted/wishlist no pill, legacy 30-40 min never surfaces; positive control open 16-18 on the same screens).
- AC5 PASS: pending/confirmed/processing/handover/picked_up with courier (91416) and without (self-delivery 91417): rail 'By HH:MM' == tracking sheet 'Latest arrival by HH:MM'; any-minute at promise; Running late at promise+5 exactly (sampler2: flips 20:33:00 for promise 20:28); null -> no block; delivered/cancelled none; UX-4185-1 fold 'By 20:41 · 1 Item · 19.11 AED' verified live.
- AC d: UNVERIFIABLE on device (no list surface reachable without an address; logout clears address -> 'Service not available in this area'); widget tests cover.
- Backend phpunit (private clone via phpunit-isolated.sh): --filter 'OrderEstimatedDeliveryAt|Eta' 825 tests OK (1 skipped), OrderEstimatedDeliveryAt 32 OK.
- Flutter: gate tests 24 pass; 14 ETA suites 302 pass.
- Base-vs-HEAD comparison of pre-existing reds: BLOCKED, mem-guard refused (swap 6.03 GB > 6.0 cap) on every attempt for ~50 min.

## Delta QA cycle 1 (AC d probe) - 2026-10-19 evening, emulator-5558
- tested_sha 192cf449e1348da1bdcdd5efe102856d4bbe2083 (UserApp lib identical to b9d427767; only the nav guide differs). APK reused (adb install -r of the b9d4277 debug APK, API_HOST=10.0.2.2:8185 baked in; no lib file newer than the APK); no rebuild because mem-guard refuses (swap 7.9 GB > 6 GB cap).
- Twin multi_food_db_qa4185 recreated: read-only dump (--set-gtid-purged=OFF), 10 pending migrations applied with DB_DATABASE pinned (281 rows), NEARS_SEED_ALLOW_DB Nears4184EtaQaFixtureSeeder, php -S :8185 from the worktree (freshness PASS 192cf449e).
- AC d: UNVERIFIABLE on device. Reached no-address + cached-module state four ways; no store list ever rendered. See d-* files.
  - real logout (identity-scoped cache removed by design NEARS-2250 -> cached module absent for the new guest id): Home = 'Service not available in this area'; Categories = 403 'Something went wrong'; Basket = 'Choose a module first'.
  - cold start, no address (guest, cached module present via zone_ids=null splash-clear path AND via key delete): splash -> cold_start_completed destination=pick_location -> pick map. Splash post-frame clear observed (user_address key gone).
  - cold start logged-in with no address key: address/list -> autoSelectMostRecent -> home WITH address (state not reachable).
  - deep link (adb VIEW nears-web.izzes.ae/?module=food-restaurant and /popular-stores?...): 'deep link converted, matched=false' (WEB_HOSTED_URL empty in this build -> link null), cold: app parked on splash 'Loading...' forever (setDeeplink(uri) set, splash skips routing); warm: ignored.
  - in-app initial?module=food-restaurant with NO address (offline AccessLocation -> NoInternet -> Try Again -> Get.offAllNamed(getInitialRoute()) with seeded cached module): byPuss gate bypassed (route: initial route module=food-restaurant hasAddress=false) -> checkModuleId no-location path -> module match found=false -> [FAIL] ModuleNotFoundFailure + dialog 'Module is not available' -> Ok -> AccessLocation screen. get-stores/all returned 200 (80 stores without zone) but no list renders: the module never resolves without a zone.
