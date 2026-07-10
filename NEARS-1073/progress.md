# NEARS-1073 QA progress — banner-store force-unwrap fail-soft fix

Build: feat/NEARS-1073-banner-store-unwrap @ 5d490a2b (worktree)
Device: emulator-5554 (Android 17 / API 37), UserApp com.izzes.nears, local backend 10.0.2.2:8000
Surface: module_view featured banner carousel (isFeatured:true). Zone 2 (Abu Dhabi) — open featured store banners = stores 12/13/14.
Verdict: PASS.

## Backstop
- Unit tests: 7/7 PASS (banner_store_tap_null_address_test.dart 4 + module_banner_store_failsoft_test.dart 3). [WARN] IDs-only confirmed (store=222 zone=7 module=2).

## Live states (all taps by resolved node bounds — no hardcoded targets)
- [x] State 3 (valid in-zone, zone-2 addr): PASS. Tapped centered featured banner (Fresh local, store 12). Route=/store/fresh-local?id=12&page=module&module=1 (correct grocery module refine), view_store{store_id:12}, 0 errors, NO warn (in-zone refine succeeded). Evidence s3-01/s3-02.
- [x] State 2 (zone-mismatch = reported "store zone NOT covered by saved address", old "Bad state: No element"): PASS. Crafted addr zone_ids=[2] (carousel loads) + zone_data=[{id:400}] (no id=2) + lat/long 0,0 so syncZoneData preserves craft. Tapped centered banner (Online market, store 14, zone 2). [WARN] msg="banner-store module refine skipped: store=14 zone=2 module=1" (IDs-only, no PII), /stores/details/14 200, view_store{store_id:14}, store OPENED, 0 crash. Evidence s2-01/s2-02/s2-warn-log.log.
- [x] State 1 (no/null address): covered. Pure null-address re-routes to location picker at boot (route_helper.dart:1519) → no tappable banner. Null zone_data renders unserviceable empty home (no carousel). Neither presents a tappable banner on-device; both are the unit-test domain (primary AC test "null/absent saved address ... does NOT crash and STILL opens the store" PASS). No crash observed booting the null-zone_data state. Evidence s1-01/s1-null-zonedata-noncrash.log.
- [x] Regression: non-featured module-home promo banner (isFeatured:false, untouched path). Tapped store banner -> /store/fresh-supermarket?id=13&page=banner&module=grocery-food (page=banner, NO module switch, NO banner-store warn), view_store{store_id:13}, 0 crash. Campaign banner also routed normally (/basic-campaign).

## Sweep
- Full-session logcat defect scan (Null check / Bad state / E/flutter / Unhandled / RenderFlex overflow): 0 hits.
- Device state restored to original (zone-1 Home).
