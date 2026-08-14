# NEARS-1984 — QA evidence log

Device `emulator-5558` · **physical** density 480 (dpr 3.0), **no override active** ·
`wm size` physical 1344x2992 px = 448x997.33 dp · Android build `com.izzes.nears` 3.8.0
Worktree `/Users/Apple/Projects/nears-NEARS-1984-current-location-tap-target` @ `230148ba`
Flutter `/Users/Apple/Tools/flutter/bin/flutter` 3.41.9 · light mode only (dark deferred)

Build freshness: installed APK md5 `bcf2341454627af9a5195af4197a2924` (pre) →
`7e552a5707b3a8352330c80afaf39c6e` (post, `lastUpdateTime=2026-08-14 11:37:23`, inside this
run's window; `firstInstallTime` 2026-08-12). Same md5 re-read after the last observation.
Device pid `26453` continuous throughout and identical to the `I/flutter (26453)` tag on this
run's own `flutter run` log, host pid 76928.

Reference frame: the `Google Map` TextureView = the widget's `Stack`, bounds
`[78,1488][1266,2532]` = 396.00 x **348.00 dp** (the exact stack height the widget test pins).
Stack top = y 1488 px. All "stack-rel" figures below are `(px - 1488) / 3`.

## AC1 — bounds >= 44 dp on both axes, X unchanged at 45

Two independent `uiautomator dump`s (byte-identical results), each carrying the required
in-dump positive control:

| node | bounds (px) | size px | size dp |
|---|---|---|---|
| `Use my current location` | `[1131,1758][1266,1890]` | 135 x 132 | **45.00 x 44.00** |
| `View fullscreen map` (positive control) | `[1131,1617][1266,1749]` | 135 x 132 | 45.00 x 44.00 |

Before (ticket, `emulator-5562`): 135 x 90 px = **45 x 30 dp**. After: **45 x 44 dp** —
Y 30 -> 44 (+14), **X exactly 45, neither wider nor narrower**. PASS.

Predicted before measuring: 135 x 132 px. Observed: 135 x 132 px.

## AC2 — no overlap with the expand box; both independently addressable

- expand band, stack-rel: `(1617-1488)/3 = 43.00` .. `(1749-1488)/3 = **87.00**`
- this control, stack-rel: `(1758-1488)/3 = **90.00**` .. `(1890-1488)/3 = **134.00**`
- gap `1758 - 1749 = 9 px = **3.00 dp**` — positive, so no overlap.

From the neighbour's side: tapping the **centre of the expand control** (1198, 1683 =
stack-rel y 65.0) with the device GPS parked at Abu Dhabi opened the **fullscreen map**
(`Set Your Store Location`, 448x867.67 dp `Google Map`, `Set Location` CTA, Zoom in/out) and
the address did **not** become Abu Dhabi — i.e. the *expand* action fired, not
current-location. Wrong-action collision ruled out. PASS.

## AC3 — two-sided boundary taps (2 dp inside / 2 dp outside all four edges)

Discriminator: `adb emu geo fix <lng> <lat>` to a distinct far-apart point before each probe,
then read the address `EditText` + the zone dropdown. "Fired" = address became the geocode of
the **new** GPS point. A tap that misses the control still lands on the `GoogleMap`, which
reacts (marker move / zone clear) — so the negative asserted is specifically **"the
current-location action did not run"**, not "nothing happened".

| # | edge | tap px | stack-rel | geo fix | observed | verdict |
|---|---|---|---|---|---|---|
| 1 | **inside TOP** (neighbour side) | (1198,1764) | y 92.0 | Abu Dhabi | address -> `CCXF+XX Abu Dhabi - United Arab Emirates`, zone -> `Abu Dhabi Zone` | **FIRED** |
| 2 | outside TOP (in the 3 dp gap) | (1198,1752) | y 88.0 | Dubai | address cleared, zone -> `Select Zone` (map reacted) | not fired |
| 3 | **inside BOTTOM** (the new 14 dp) | (1198,1884) | y 132.0 | Dhaka | address -> `House: 10 Av 2, Dhaka 1216, Bangladesh`, zone -> `Main Service Zone` | **FIRED** |
| 4 | outside BOTTOM | (1198,1896) | y 136.0 | Dubai | address cleared, zone -> `Select Zone` (map reacted) | not fired |
| 5 | inside LEFT | (1137,1803) | x left+2 | Abu Dhabi | address -> `CCXF+XX Abu Dhabi …` | **FIRED** |
| 6 | outside LEFT | (1125,1803) | x left-2 | Dhaka | address cleared + banner `Please place the marker inside the zones.` (map reacted) | not fired |
| 7 | inside RIGHT (transparent 15 dp margin) | (1260,1803) | x right-2 | Dubai | address -> `34XX+XX Dubai - United Arab Emirates`, zone -> `Single Store QA Zone` | **FIRED** |
| 8 | outside RIGHT | (1272,1803) | x right+2 | Dhaka | address **unchanged** (still Dubai), zone unchanged, no banner | not fired |

Probe 8 lands **beyond the map's right edge** (TextureView right = 1266 px), on the map
container's border / page background — nothing under it reacts at all. Because that is the one
"nothing happened" negative, it carries a **validity control**: with the *same* Dhaka geo fix
still set, an immediate repeat of probe 3 fired and produced the Dhaka address, proving the
instrument was live at probe 8's moment. PASS, all eight sides.

## AC4 — existing current-location behaviour intact

Probe 1 above is the demonstration: from the out-of-zone cold state (`get-zone-id http_status=404`,
`get-zone-id: no zone / out of zone — prompting location picker`, `Please place the marker inside
the zones.` banner) the tap produced `geocode-api 200` -> `get-zone-id 200` -> `zone/check 200` ->
`location: inZone=true`, the banner cleared, the address populated and the zone auto-selected.
Reproduced four independent times (probes 1, 3, 5, 7) against three different GPS points. PASS.

## Regression sweep (bounded)

1. **Visual no-drift** — pixel-measured off the screenshot, not eyeballed. White circle at
   x `1131..1220` (30.0 dp) and y `1758..1847`, stack-rel **90.0 .. 119.7 dp**, centre y
   **105 dp**. Unchanged. An `alignment: center` slip would have put it at 97..127 — the
   measurement discriminates. Instrument validated by the expand circle reading a clean
   30.0 dp at its own pinned midline (stack-rel y 65).
2. **`!fromView` fullscreen arm** — `Use my current location` = `[1164,2087][1344,2222]` =
   **60.00 x 45.00 dp**, unchanged. Clear of the zoom card: its bottom 2222 px vs `Zoom in`
   top 2375 px = 153 px = **51 dp**. Tapping it still fires (geocode-api / zone/check /
   `inZone=true`); `Set Location` stays `enabled=true`.
3. **Map still pannable** — swipe (400,2200)->(400,1850) in the free band moved the camera
   (address `34XX+XX Dubai` -> `34WX+XX Dubai`). The 14 dp below the circle now swallowing
   pan is the expected, documented trade (same one NEARS-1952 made) — not filed.
4. **Zone survives the expand -> Back round trip** (NEARS-1967 still holding).
5. **RTL** — `Positioned(right:)` is physical, not directional, so the control does not mirror
   under Arabic. Pre-existing and shared with NEARS-1952; recorded by construction, not
   re-demonstrated live, and not a regression of this ticket.
6. **NEARS-2057** (module dropdown after map-driven auto-detect) not attributed here.

## Logs

`ui_errors` -> `scanned 423 flutter-tag lines of 155200 buffer lines; 0 match(es)`, **exit 0**
(a real validity count, not an empty-output vacuum). Direct grep of this run's own log for
`[FAIL]`/`[ERR]` bound to pid `26453`: none. No `EXCEPTION CAUGHT` / `RenderFlex` / overflow.
BE `laravel.log` deliberately **not** opened — no `[api]`-tagged AC (NEARS-566 default-OFF).

## Automated backstop

`/Users/Apple/Tools/flutter/bin/flutter test test/features/auth/select_location_fullscreen_control_a11y_test.dart`
-> **+10 All tests passed**, with all six NEARS-1984 cases reported by name.

## Not tested

True end-to-end vendor-registration **Submit** — would POST a registration row. Read-only
DB rule; recorded NOT TESTED, as on NEARS-1967 / NEARS-2027 / NEARS-2026.
