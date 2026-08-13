# NEARS-2003 — live QA evidence (joint fix with NEARS-2001)

Device `emulator-5556` (sdk_gphone16k_arm64, 1344x2920) · light mode only (dark deferred).
Flutter `/Users/Apple/Tools/flutter` 3.41.9 · worktree
`/Users/Apple/Projects/nears-NEARS-2003-zone-index-minus-one` · branch
`feat/NEARS-2003-zone-index-minus-one` @ `5b0ec1ac` · base `feat/userapp-reskin2` @ `d3d03bed`.
Backend: local Laravel `10.2.2:8000` from the app (`127.0.0.1:8000` host, HTTP 200) — real
backend, not a demo host.

## Build identity (two-stage freshness)

Both builds' APK md5 + `lastUpdateTime` were read by the SAME on-device shell invocation that
produced each assertion's `uiautomator dump` (`cap.sh`), so no install can slip between the
build-identity read and the observation it guards.

| Build | APK md5 | installed | app pid |
|---|---|---|---|
| BASE (`d3d03bed` content of the 2 files) | `0b0458c7244586d36de3764f2aa29863` | 2026-08-14 01:12:21 | 17324 |
| FIXED (`5b0ec1ac`) | `332de216a4174393ae65d1121020c2ce` | 2026-08-14 01:25:34 | 19866 |

Base content asserted before building: `_selectedZoneIndex = 0;` present, NEARS-1967 `initState`
reset block count = 1. Fixed content asserted after restore: `_selectedZoneIndex = -1;` count = 2,
NEARS-1967 reset block count = 0. `git status --porcelain` empty before the fixed build and at end
of run.

## AC1 — first arrival at Vendor Info

Reached via Home -> Grocery & Food -> Profile -> Open Vendor -> Vendor Info -> Location Info.

| | zone control | module control |
|---|---|---|
| BASE | `Select Zone` hint = **unselected** | **`Not Available Module`** placeholder |
| FIXED | `Select Zone` hint = **unselected** (unchanged) | **`Select Module` + `Select Module Type`** enabled `NSelect` |

Zone behaviour is identical across builds. The module delta is the INTENDED consequence of dropping
the `initState` reset (which used to null `_moduleList` via `setZoneIndex(-1, canUpdate:false)`);
`getZoneList()` still awaits `getModules(_zoneList![0].id)`, so on the fixed build the list is
populated at load. Observed on device on both builds — not predicted.

Shots: `ac1-PRE-base-zone-unselected.png`, `ac1-PRE-base-module-not-available.png`,
`ac1-POST-fixed-zone-unselected.png`, `ac1-POST-fixed-module-dropdown-enabled.png`.

## AC3 — NEARS-2001 step-back repro

Sequence both builds: Vendor Info -> zone `Main Service Zone` -> module `Grocery & Food` -> fill the
step-1 gate (business name `QA2003`, logo, cover, in-zone marker via
`adb emu geo fix 90.36601818622162 23.81796491735989` = read-only `ST_Centroid` of zone 1, delivery
time) -> `Next` -> Owner Info (step 0.6) -> tap `Vendor Info` tab -> back to step 0.1.

| | zone after step-back | module after step-back |
|---|---|---|
| BASE | **CLEARED** -> `Select Zone` hint | **CLEARED** -> `Not Available Module` |
| FIXED | **`Main Service Zone` survives** | **`Grocery & Food` survives** |

Everything else (business name, images, delivery time `10:13 minute`, address) survived on both
builds — only zone+module were wiped on base. Bug reproduces on base, fixed on HEAD.

Shots: `ac3-PRE-base-zone-CLEARED-after-stepback.png`,
`ac3-PRE-base-module-CLEARED-after-stepback.png`,
`ac3-POST-fixed-zone-SURVIVED-after-stepback.png`,
`ac3-POST-fixed-module-SURVIVED-after-stepback.png`.

Re-pressing `Next` after the step-back passed the step-1 gate again and landed on Owner Info. No
`RangeError` / `Invalid value` / `Null check operator` in the flutter-tag buffer (counts 0/0/0,
against a positive control of 2 `[FAIL]` lines and 132 lines from pid 19866 in the same buffer —
so the instrument was live).

## AC4 — fullscreen map expand (NEARS-1967 path) on the fixed build

`View fullscreen map` -> `Set Your Store Location` (CTA `Set Location`, enabled) -> `Back`.
Zone `Main Service Zone` AND module `Grocery & Food` both preserved, verified in a single dump.
Repeated for a 2nd cycle — preserved again. Shot:
`ac4-fixed-fullscreen-roundtrip-preserved.png`.

## F1 — map picture desync after step-back (separate finding, NOT a regression of this ticket)

Confirmed live on the fixed build. After the step-back the controller data is correct
(zone dropdown `Main Service Zone`, address `House: 10 Av 2, Dhaka 1216, Bangladesh`) but the
re-mounted `SelectLocationViewWidget` builds a fresh `State`: the map shows **no zone polygon, no
location marker, and the camera re-seeded at the default Dhaka centre** (Paikpara area) rather than
the zone centroid the user had set. Nothing re-derives `_polygons` / `_isMarkerVisible` /
`_cameraPosition` from the controller on re-mount.

Not a regression of this change — the base build wiped zone+module entirely, which masked it. Does
not block this ticket. Shot: `f1-fixed-map-after-stepback.png`.

## Regression sweep (bounded)

Blast radius measured by grep: every consumer of `getZoneList` / `setZoneIndex` /
`selectedZoneIndex` lives under `lib/features/auth/`.

1. Store registration wizard, both steps, both directions, 2 fullscreen cycles — clean.
2. Delivery Man / Delivery Partner Registration (adjacent registration wizard, its OWN
   `DeliverymanRegistrationController`, does not use the changed widget) — renders clean, gate
   behaves, no red screen.
3. Registration exit dialog `Are you sure to go back?` -> `Yes` — clean.
4. Profile hub + EARNINGS card — clean.
5. Home / module browse with bottom nav + live order cards — clean.

## Automated backstop

`flutter test` (UserApp, pinned SDK 3.41.9), measured on BOTH sides:

- BASE content: `+3602 ~2 -10`
- FIXED (`5b0ec1ac`): `+3608 ~2 -4`

Exactly 6 tests flipped fail -> pass and **zero flipped pass -> fail**. The 6 are the ticket's own
regression pins. The ticket's 4 changed test files run standalone: **15/15 pass**.

The 4 remaining failures are pre-existing and unrelated —
`test/features/category/category_screen_back_button_test.dart` and
`test/features/coupon/coupon_refresh_failed_row_test.dart`, neither of which contains any reference
to `store_registration` / `select_location_view` / `StoreRegistrationController` (grep count 0).
Run standalone they give an identical `+7 -1` at base content and at fixed HEAD.

## Log scan

`ui_errors emulator-5556` exit **0** (scanned 328 flutter-tag lines of 144619 buffer lines).
Matches, all attributed:
- 2x `[FAIL] framework_error library=image resource service type=_Exception msg="Exception: Could
  not decompress image."` (pids 17324 base / 19866 fixed) — caused by the **synthetic PNG fixture I
  generated** for the logo/cover dropzones, reproduced identically on both builds, and paired with a
  proper `AppLogger.failure` line (logging contract satisfied). Not a defect of this diff.
- 1x `[ERR] msg="error snackbar shown"` (pid 17324, base) — the delivery-time picker's own
  validation snackbar, correctly paired with a log line.

No unhandled exception, no overflow, no GetX error in either build's window.
