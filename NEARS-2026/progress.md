# NEARS-2026 — live QA log (phase [8], QA cycle 0, build fix_cycle 1)

Device `emulator-5556` (sdk_gphone16k_arm64, 1344x2992 px @ density 480 = **448 x 997 dp**;
`wm size`/`wm density` reported **Physical only, no override active**).
Worktree `/Users/Apple/Projects/nears-NEARS-2026-map-state-restore`, branch
`fix/NEARS-2026-map-state-restore` (product diff uncommitted, present in the tree at build time).
Backend `http://127.0.0.1:8000` (app `baseUrl` -> `http://10.0.2.2:8000`), `/api/v1/config` = 200.

## Build freshness (two-stage + the swap window)
| Check | Value |
|---|---|
| `firstInstallTime` | `2026-08-14 09:16:00` |
| `lastUpdateTime`   | `2026-08-14 09:16:00` — **equal ⇒ no earlier install survives; stale APK ruled out** |
| installed `base.apk` md5 (before first AC observation) | `f565a0f57c54f599d43618d3de27a31a` |
| worktree `build/app/outputs/flutter-apk/app-debug.apk` md5 | `f565a0f57c54f599d43618d3de27a31a` (built 09:15 from this worktree) |
| installed md5 re-read after the last AC observation (09:46) | `f565a0f57c54f599d43618d3de27a31a` — unchanged |
| app pid continuity | pid **15225** from launch to end, `ETIME 30:56` — an install-over would have killed it ⇒ **swap window closed** |
| NEARS-1952 in-dump string channel | **not available** — this diff adds no new user-visible string (stated, not overclaimed) |

AC4 asserts ABSENCE, so it is the AC a stale pre-fix build could have false-PASSED. The
install-time equality + pid continuity close that specifically.

## Environment facts measured (not assumed)
* Seeded `default_location` = `{lat 23.788080, lng 90.355377}`. `SELECT ... ST_Contains(coordinates, POINT(90.355377 23.788080)) ... HAVING contains_default=1`
  over all `status=1` zones returns **zero rows** — NEARS-2058 confirmed, the cold camera is out of zone.
* Zone 1 "Main Service Zone" envelope `lat 23.8036–23.8364`, `lng 90.3359–90.3983` (Mirpur, Dhaka).
* Emulator GPS pinned to `90.366 23.818` (inside zone 1) so the app reaches Home.

## Timeline
1. 09:16 fresh install (uninstall first, so the install times match). Language/onboarding/permissions.
2. 09:20 **AC4 #1** cold entry to Vendor Registration, map scrolled into view **via swipes at x=30, outside the map's x-range 78..1266** so the map is never panned. `ac4-cold-entry-*`.
   * A first attempt scrolled at x=672 (over the map); that pan set `_hasUserInteractedWithMap` and raised the out-of-zone banner. Discarded and re-entered clean — the clean dump has **no** banner while still carrying the sibling map-stack nodes ("Location Search here", "Use my current location") as the required-positive control.
3. Zone dropdown -> "Main Service Zone": polygon drawn + camera fitted to zone bounds (`step-zone-selected-*`) — Q7 first half, `_setPolygon` unchanged.
4. Map tap inside the zone -> address `R962+7QX, Dhaka, Bangladesh`, centre marker visible.
5. Module -> "Grocery & Food". Name/logo/cover/delivery-time filled to satisfy the step gate.
6. **Pre-departure comparator** `predeparture-*` (map fully inside the ScrollView viewport at `[78,920][1266,1964]`).
7. 09:39 `Next` -> **Owner Info** (0.6). Then tab **Vendor Info** -> step back (0.1) = the re-mount.
8. **AC1/AC2/AC3** `ac1-ac2-ac3-after-stepback-*` at map bounds `[78,1109][1266,2153]`.
9. NEARS-2057 non-retrigger: module dropdown opened and listed options; zone dropdown value intact.
10. AC3 metric probe + its two-way validity control (below).
11. Q7 pan-out-of-zone, out-of-zone banner + disabled Next, Q8 fullscreen expand/back.
12. **AC4 #2** — left the screen and re-entered fresh AFTER a zone had been selected in the same app session. `ac4-fresh-reentry-*`.

## Measurements (instrument validated in both directions before use)

### Polygon — mean "paper" RGB of the map background
Predicted fill: DLS navy `#000080` at `alpha .2` over Google's white paper (242) = **(194,194,220), B-R = +26**.

| Frame | mean paper RGB | B-R | reading |
|---|---|---|---|
| pre-departure, sample box INSIDE the polygon | (197.0, 197.3, 223.2) | **+26.2** | positive control — matches prediction |
| pre-departure, sample box OUTSIDE the polygon | (223.4, 244.3, 231.7) | +8.3 | negative control |
| **AC4 #1 cold entry**, whole frame | (240.1, 241.0, 241.3) | **+1.2** | **no polygon** |
| **AC4 #2 fresh re-entry**, whole frame | (240.1, 241.0, 241.3) | **+1.2** | **no polygon** |
| **AC1 after step-back**, whole frame | (196.7, 195.3, 221.2) | **+24.5** | **polygon present** |

### Marker overlay — red-pixel mass in the centred 120x120 px box (= 40x40 dp asset x DPR 3)

| Frame | red px in centre box | red px elsewhere (detector live?) | reading |
|---|---|---|---|
| AC4 #1 cold entry | **0** | 8529 (red POI pins) | no marker |
| zone selected, before the map tap | **0** | 2696 | no marker |
| pre-departure | 2996 | 5701 | marker |
| **AC1/2 after step-back** | **2977** | 3544 | **marker, same mass (-0.6%)** |
| AC4 #2 fresh re-entry | **0** | 8795 | no marker |

Corroborating state channel: a 120x120 px node at `[612,1571][732,1691]` (exactly the map centre for
map bounds `[78,1109][1266,2153]`) is present in the post-step-back uiautomator dump and **absent**
from the fresh-re-entry dump taken at the identical framing — `grep -c '612,1571'` = **1** vs **0**.

### Camera centre (AC3) — reverse-geocode probe
`GoogleMap.onTap` writes the tapped LatLng to `restaurantLocation` and reverse-geocodes it into the
address field, so tapping the exact map centre reports the camera centre as an address.

| Step | action | address |
|---|---|---|
| measurement | tap map centre (672,1631) on the restored map | `R962+7QX, Dhaka, Bangladesh` — **identical to the pre-departure value** |
| control A | tap OFF-centre (922,1881) | `R953+GFG, House- 50 Road No. 3, Dhaka, Bangladesh` — **changed** ⇒ probe is live |
| control B | tap the NEW centre (672,1631) | `R953+GFG, …` — unchanged ⇒ "centre tap == camera centre" holds generally |

`R962+7QX` is a plus code with 3 characters after the `+` ⇒ agreement within a few metres. The
config default is ~3.4 km away and resolves to an entirely different code, so the probe discriminates.

## Logs
* `ui_errors` **exit 0** ("scanned 30 flutter-tag lines of 16089 buffer lines; 0 match(es)") — scanned, clean, non-zero scan count as the validity control. Buffer window `09:39:01 -> 09:46`, i.e. it covers the step-forward, the re-mount, the restore and every probe.
* Whole-session run log (961 lines, 09:16 -> 09:46): exactly **one** `[ERR]` —
  `[ERR] msg="error snackbar shown"`, the delivery-time validation snackbar, paired with its
  `AppLogger.error` (`custom_snackbar.dart:30`). Correctly logged, not silent, not a defect.
* Zero `[FAIL]`, zero unhandled exceptions, zero `RenderFlex`/overflow across the session.
* BE `laravel.log` **not opened** — no AC here is `[api]`-tagged (NEARS-566 default-OFF).
