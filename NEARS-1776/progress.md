# NEARS-1776 — live QA progress log

Cold deep-link into a store route red-screens on a config-load race.

## Builds under test (md5 of the *installed* artifact, verified on-device)

| Build | Worktree / commit | APK md5 | Device | Geometry |
|---|---|---|---|---|
| HEAD (fixed) | `nears-NEARS-1776-deeplink-config-race` @ `c092e66c` | `0d974fd609872637d0ed476a435a6f52` | `emulator-5554` | 1344x2992 @480dpi = 448x997 dp |
| BASE (unfixed) | detached worktree @ `5ab0de66` | `d62648274e31a154778740b38aed43ef` | `emulator-5556` | 1344x2992 @480dpi = 448x997 dp |

Flutter `/Users/Apple/Tools/flutter/bin/flutter` 3.41.9 (pinned). Both APKs `flutter build apk --debug`.
Backend: local `php artisan serve :8000`, app `baseUrl=http://10.0.2.2:8000` (real local backend, not demo).

## Repro recipe (per attempt)

1. `am force-stop com.izzes.nears` (cold process)
2. `run-as com.izzes.nears rm -f app_flutter/cache_response_new_db.sqlite` — **surgical config-cache miss.**
   The config cache is a drift/sqlite DB, NOT SharedPreferences, so deleting it forces the cache-miss
   leg while login (FlutterSecureStorage), address and zone (FlutterSharedPreferences) survive.
   This avoids the `pm clear` validity trap (which wipes login/zone and never reaches StoreScreen).
3. `logcat -c`
4. `am start -a VIEW -c BROWSABLE -p com.izzes.nears -d 'https://6ammart-web.6amtech.com/store/demo-store?id=1&page=store&module=grocery-food'`
5. wait 22 s, raw `screencap` -> red-fraction detector, `logcat -d -s flutter`, `uifind.py list`

## Instrument validity

- **Red detector positive control** = 0.993 on a known red screen; **negative control** = 0.000 on a
  normal store screen. Threshold 0.5.
- **Positive control for reachability**: warm deep-link on both devices rendered StoreScreen
  ("Store Reviews", item rows, prices) — the harness demonstrably reaches the store route.
- Red screen persists (t≈9 s .. t≈30 s stable at 0.993) — it is not transient.

## Findings recorded as they were observed

- **[OBSERVED] BASE red screen captured** — `bug-base-redscreen-null-check-deeplink.png`,
  full-screen `Null check operator used on a null value`. First artifact of this crash in the ticket.
- **[INSTRUMENT / pre-existing defect] The red screen is INVISIBLE to logs-first QA.**
  `main.dart:90` sets `FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterError`,
  replacing the default console dump; Crashlytics collection is `!kDebugMode` = OFF in debug.
  Result: a full-screen framework error produced **0 lines** in `logcat` (all tags) and **0**
  `[FAIL]`/`[ERR]`. Also 0 text nodes in the a11y tree. Detection had to be pixel-based.
- **[ENVIRONMENT / Data DoR gap] `business_settings.prescription_order_status = 0`** on the dev DB,
  so `configModel.prescriptionStatus == false` and the prescription FAB is **unconditionally hidden**
  for every store, pharmacy included. The "pharmacy FAB must still be visible" regression twin is
  therefore NOT demonstrable live without a DB write (forbidden: read-only DB).
- **[INSTRUMENT] concurrency confound** — two devices against one single-threaded
  `php artisan serve` serialise requests and push the crash past a 15 s window, producing
  false "clean/blank" attempts. Runs were redone strictly sequentially.

## Measured result — n=30 per build, sequential, identical harness

| Build | attempts | store route pushed | valid samples | RED screens | rate |
|---|---|---|---|---|---|
| BASE `5ab0de66` (unfixed) | 30 | 30/30 | 30 | **29** | **96.7 %** |
| HEAD `c092e66c` (fixed)   | 30 | 30/30 | 29 (1 still on splash at t+22s) | **29** | **96.7 % / 100 % of valid** |

APK md5 re-verified identical before AND after each 30-attempt run (no artifact swap).

What n buys: against the ticket's field rate of 1-in-7, `(6/7)^30 = 1.0 %` — n=30 would have had a
99 % chance of catching it. But the measured BASE rate is **96.7 %, not 14 %**, because the surgical
cache-miss makes the null window deterministic; at that base rate a single clean run is already
strong evidence, and 30 is overwhelming. The instrument is therefore NOT insensitive — and HEAD's
29/30 is a real, reproduced failure, not an absence of signal.

Per-attempt verdicts: `BASE_results.tsv`, `HEAD_results.tsv` (AC3's session log).

## Causal pin (falsifiable, predicted before measuring)

Predicted: every RED attempt logs `configNull=true`; non-red attempts log `configNull=false`.
Measured: BASE 29 RED / all `configNull=true`; BASE 1 CLEAN / `configNull=false`. HEAD 29 RED /
all `configNull=true`. Prediction held exactly.

Discriminator that rules the FAB OUT as the live thrower: in **58/58** red attempts across both
builds `/api/v1/stores/details` never fired, so `StoreScreen.initState` never ran and its
`floatingActionButton` `Visibility` chain — the only thing NEARS-1776 changes — was never evaluated.
In the one attempt that did render the store screen it fired 4x.

**Live throw site: `UserApp/lib/helper/route_helper.dart` `RouteHelper.getRoute()` lines 1474 / 1479 /
1481** — `configModel!.appMinimumVersionAndroid`, `minimumVersion!`, `configModel!.maintenanceMode!`.
`_storePage()` is `getRoute(_waitForModule(...))`; Dart evaluates the argument first (hence the
`route: waiting for module=` + `checkModuleId` lines DO appear), then `getRoute`'s body null-asserts
config while the fetch is still in flight. `getRoute(` has 37 call sites in that file.

## Regression sweep (HEAD build, light mode)

- Warm deep-link -> `demo-store`: store screen renders ("Store Reviews", item rows). No crash.
- Warm deep-link -> `careplus-pharmacy` (id 42, module pharmacy): renders "CarePlus Pharmacy",
  `configNull=false`, `stores/details/careplus-pharmacy` fired. No crash.
- Scroll down x2 then up on the store screen: no crash, no red (0.000 / 0.003).
- `ui_errors`: "scanned 88 flutter-tag lines of 1121 buffer lines; 0 match(es)", exit 0.
- Prescription FAB: absent everywhere — **expected and NOT attributable to the fix**, because
  `prescription_order_status = 0` globally. The "FAB must still be visible" twin is UNVERIFIABLE here.
- Automated backstop: `flutter test test/features/store/` -> **295/295 pass**, including the
  ticket's own `store_screen_null_config_fab_test.dart` (5/5). Green units, live crash unchanged.
