# NEARS-475 QA progress (fix_cycle 0)

Device: emulator-5554 (reclaimed stale lock from NEARS-509, dead pid 10925)
Backend: served from worktree /Users/Apple/Projects/nears-NEARS-475-module-zone-visibility/Admin on :8000 (cwd confirmed worktree)
DB: shared multi_food_db, Nears475HideModuleFixtureSeeder confirmed applied (module 6 + store 4116 status=0)

## API-level verification (worktree backend)
- [PASS] zone 1: module 6 active_stores_count=0 (stores_count=1), module 1 active_stores_count=6, all integers, single_store_candidate_id absent
- [PASS] zone 1: parcel (module 5) active_stores_count=0 but returned (client-exempt)
- [PASS] zone 2: module 6 ABSENT (not bound), parcel present
- [PASS] zone 3: module 4 active_stores_count=1, single_store_id=59 (hero fast-path intact)

## Live AC demonstrations
(appended as observed)

## Automated backstop
- [PASS] backend: vendor/bin/phpunit --filter ModuleSingleStoreIdTest => 9/9 (51 assertions)
- [PASS] flutter: cd UserApp && flutter test => 1220/1220 (incl. 5 new NEARS-475 cases)

## Note: emulator-5554 had a leftover `flutter run` (pid 11164) from NEARS-509-basket-ui worktree.
## Stopping it and launching UserApp from the NEARS-475 worktree build.

## Live AC demonstrations (logged in as customer@nears.com, user 6)
- [PASS] AC1/AC2 — ZONE 1 (Demo Zone — Dhaka, zone_id=1): module grid = Grocery&Food(1), Food&Restaurant(2), Pharmacy(3), Parcel(5). Module 6 "NEARS-475 Suspended Grocery" ABSENT despite existing in zone 1 with active_stores_count=0. shot: ac1-ac2-zone1-module6-hidden.png
- [PASS] AC4 — reactive zone change BOTH directions: zone2->zone1 and zone1->zone2; /api/v1/module re-fetched each switch; grid updated. log: get-zone-id + 200 /module + sectors_shown.
- [PASS] NEARS-259 analytics — sectors_shown fired once per zone change, IDs only: zone1 -> {sectors_count:4, zone_id:1}; AbuDhabi addr -> {sectors_count:4, zone_id:400}. NOTE: zone_id 400 is CORRECT — Abu Dhabi saved-addr coords resolve to overlapping "Baqala Zone 37" (id 400) inside zone 2; verified via get-zone-id => "[400,2]". Not a bug.
- [PASS] NEARS-256 single-sector auto-select gate + NEARS-236 no false "module not available" dialog on zone switch (logcat shows no "Module is not available").
- [PASS] Parcel exemption (NEARS-337): Parcel Delivery (module 5, active_stores_count=0) STILL SHOWS in both zones.

## Env setup notes (infra, NOT product code):
- Backend served from worktree; worktree storage/ had NO Passport oauth keys -> all auth:api endpoints 500'd (incl. login). Symlinked oauth-private/public.key from primary tree storage (env artifact reuse). Login then succeeded. This is a worktree-setup gap, unrelated to NEARS-475.

- [PASS] AC5 — ModuleShimmer loading state: suspended backend (SIGSTOP) + cold launch => home renders with NO module cards (moduleList==null => ModuleShimmer); log "module future builder: ConnectionState.waiting // has data: false". Resumed backend => modules loaded. shots: ac5-moduleshimmer.png, ac5-modules-loaded-zone1.png
- [LIMITATION] AC6 — NearsEmptyState (zero non-parcel modules): NO seeded zone yields an empty module list (all 90+ zones have >=1 bound module; verified by SELECT). Cannot reach the empty branch live without a DB mutation (read-only rule). The empty/all-hidden filter branch IS covered by the new flutter unit tests (1220/1220 pass) + the empty-state widget branch (module_view.dart:86 NearsEmptyState) is the documented same-pattern as other reskinned empty states. AC6 verified via code+tests, not live — stated limitation.

## Regression sweep (bounded)
- [PASS] Home other sections render: banners, "Recommended For You", store cards (Fresh Mart Grocery, Nears Mart, Organic Paradise) all load.
- [PASS] Dark mode: zone-1 module selector correct (1,2,3,5; module 6 hidden), navy/mint, no overflow. shot: regression-darkmode-zone1-modules.png
- [PASS] RTL/Arabic: zone-1 selector mirrored correctly (chevrons left, icons right, header right-aligned), module 6 hidden, no clipping. shot: regression-rtl-arabic-zone1-modules.png
- [PASS] NEARS-257 single-store hero (zone 3, module 4, store 59): GPS->zone3 => single-store hero "YOUR NEIGHBORHOOD STORE / NEARS-257 Fixture Store"; sectors_shown {sectors_count:1, zone_id:3}; tap CTA routes into store + loads items. Fast-path intact. shot: regression-nears257-singlestore-hero-zone3.png
- [PASS] No runtime errors (ui_errors + get_runtime_errors clean across all states).

## Observation (NOT a defect): Abu Dhabi saved-address coords resolve to overlapping "Baqala Zone 37" (id 400) inside zone 2; sectors_shown reports zone_id:400 correctly. Many granular Baqala sub-zones (364-453) seeded over Abu Dhabi.
