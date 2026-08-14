# NEARS-2027 — QA [8] progress log (live run, 2026-08-14)

Device `emulator-5556` · worktree `/Users/Apple/Projects/nears-NEARS-2027-desktop-submit-return`
branch `feat/NEARS-2027-desktop-submit-return` @ `c260c8c7` · Flutter 3.41.9 (`/Users/Apple/Tools/flutter`)

## Build provenance
| item | value |
|---|---|
| built APK (worktree) md5 | `8e396579cd34ac2e7f2ba6ace6fa830d` |
| on-device `base.apk` md5 | `8e396579cd34ac2e7f2ba6ace6fa830d` (identical) |
| `firstInstallTime` | 2026-08-14 03:57:12 (pre-existing install) |
| `lastUpdateTime` | 2026-08-14 05:57:29 (this run's `install -r`) |
| applicationId | `com.izzes.nears` |
| backend | real local Laravel on `127.0.0.1:8000`; app `baseUrl` = `http://10.0.2.2:8000` |

## Geometry — read from BOTH lines, every observation
`wm size` and `wm density` each print Physical and Override.

| phase | active line | px | density | dp (= px*160/density) | arm |
|---|---|---|---|---|---|
| desktop ACs | **Override** | 2400x1800 | 240 | **1600 x 1200** | desktop (>= 1300) |
| mobile control + regression | **Physical** (override reset) | 1344x2992 | 480 | **448 x 997** | mobile |

`dumpsys window displays` cross-check during the desktop phase: `base=2400x1800 240dpi cur=2400x1800 app=2400x1800`.

## Positive control — the desktop arm really rendered
Discriminators observed BEFORE any submit assertion:
* button label = **`Submit`** (never `Next`) — mobile shows `Next` at 0.1
* a **`Reset`** button renders beside Submit — desktop only
* single-page composition: Vendor Information + General Information + Business TIN + Owner Information + a web footer, all on ONE page (mobile is a 2-tab pager: `Vendor Info` / `Owner Info`)
* the ONLY tap-time proof: both stack traces name `store_registration_screen.dart:3661`, a line that lives **inside** `if (isDesktop) { ... }`

## Per-AC results
| AC | result | when |
|---|---|---|
| AC1 zone unset | **NOT TESTED** (environment-blocked, mechanism below) | — |
| AC1 module unset | **PASS** | 06:14:33 |
| AC2 two-sided control | **PASS** | 06:19:19 |
| AC3 two taps / no RangeError | **PASS** | 06:14:33 + 06:14:44 |
| genuine end-to-end registration | **NOT TESTED** (owner no-DB-write fence) | — |

## AC1 zone-unset — why it is not reachable live in this environment
The desktop Submit button is `onPressed: null` whenever `isDesktop && !inZone`. Observed on a cold
desktop screen: `content-desc="Submit" enabled="false" clickable="false"` while `Reset` was
`enabled="true"` (positive control — the dump does discriminate).

`_inZone` is assigned in exactly one place (`store_registration_controller.dart`, `setLocation`) and
only when a non-null `zoneId` is passed. All six `setLocation` call sites were read:
* cold load (`getZoneList`) passes `zoneList[0].id` and, via `forStoreRegistration: true`, deliberately
  leaves `selectedZoneIndex == -1` — **this is the only state that is zone-unset AND inZone-true**;
* every other call site (map camera idle, address search, zone dropdown) resolves a zone first and
  calls `setZoneIndex(found)`, so zone is set; when no zone is found it passes `zoneId: null`, which
  sets `_inZone = false` and re-disables Submit.

The cold-load state needs the config default location to sit inside `zoneList[0]`. It does not here:
`business_settings.default_location` = `23.788080, 90.355377`, and
`GET /api/v1/zone/check?lat=23.788080&lng=90.355377&zone_id=1` returns **`false`**
(`/api/v1/config/get-zone-id` for the same point returns `Service not available in this area`).
Zone 1's polygon spans lat 23.8036-23.8364; the default is south of it.

Making it reachable would require editing `business_settings.default_location` — a DB write, refused.
The branch is one `else if` above the module branch in the same chain (lines 3657-3659) and carries an
identical `return;`; it is covered by the shipped widget test
`AC1 zone unselected: submit warns and does NOT advance to 0.9` (passing).

## Test-data setup used (no DB writes)
* `adb emu geo fix 90.3654 23.8177` — a point the server confirms is inside zone 1
  (`zone/check?...&zone_id=1` -> `true`), then the in-map "Use my current location" control.
* `adb push` of two generated JPEGs to `/sdcard/Pictures/` for the logo/cover pickers.
* Location runtime permissions granted via `pm grant`.
None of these touch `multi_food_db`.
