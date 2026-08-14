# NEARS-2029 — live QA progress log

Device **emulator-5558**, native geometry Physical `1344x2992` @ density `480` (no override active)
= **448 x 997 dp**. Desktop arm driven under an explicit override `wm size 2400x1800` +
`wm density 240` = **1600 x 1200 dp**, reset to native afterwards (`wm size reset` / `wm density reset`,
re-read as Physical 1344x2992 @ 480 with no Override line).
Backend: primary tree `php artisan serve` on `127.0.0.1:8000` (`/api/v1/config` -> 200).
Flutter SDK `/Users/Apple/Tools/flutter/bin/flutter` (3.41.9). Light mode only (dark deferred).

Builds (two-stage freshness):
- PRE-FIX  base `4bb5294f` (detached worktree `nears-NEARS-2029-prefix`) — installed APK md5 `3c37ddf960ac8834f2814baea2327939`
- POST-FIX `0954efe9` (worktree `nears-NEARS-2029-module-cue`) — installed APK md5 `114eb600e08e035cf66611d8f006a593`
- Build-distinguishing value read from the SAME uiautomator dump as each assertion:
  the trigger `content-desc` — `Select Module Type` (pre-fix, impossible post-fix in the
  zone-unselected state) vs `Please select Zone` (post-fix, impossible pre-fix).

## Validity control — method (a): pre-fix build observed first
Cold arrival at Vendor Info, no zone selected, PRE-FIX build:
- trigger node `content-desc="Select Module Type" clickable="true" enabled="true" bounds=[75,880][1269,1024]`
- tapping it OPENED the overlay listing **Food & Restaurant / Grocery & Food / Pharmacy**
  (`Pharmacy` node `clickable=true enabled=true`)
=> the module data IS genuinely present in the zone-unselected state; the post-fix disabled
render cannot be an artefact of an empty list. This is also the repro screenshot the ticket lacked.
Shots: `prefix-02-module-trigger-enabled.png`, `prefix-03-module-overlay-open-nonempty.png`.

## AC results
- **AC1 [ui] PASS** (mobile arm + desktop arm). Post-fix cold arrival:
  trigger `content-desc="Please select Zone" clickable="false"`, label `Select Module` still above
  (`bounds=[87,814][361,868]`). Tap at the live-resolved centre (672,952): no overlay, no module
  items in the dump; `ac1-01` and `ac1-02` are **byte-identical** (md5 `3cdc77f7…`) — the tap changed
  zero pixels. Fill measured `(247,246,245)` vs enabled `(240,237,236)` on white = exactly the
  alpha-0.5 blend. Desktop arm (1600x1200 dp, single-page layout: Vendor Information + General
  Information + TIN + Owner Information + Vendor Name/First name/Last name/Phone):
  `content-desc="Please select Zone" clickable="false" bounds=[345,603][1200,675]`, tap inert.
  Logs clean (`ui_errors` exit 0, 483–495 flutter-tag lines scanned, 0 matches).
- **AC2 [behav] PASS for the guard, with a pre-existing caveat.** Selecting `Single Store QA Zone`
  re-enabled the trigger (`Select Module Type`, `clickable="true"`) and fired a real refetch
  (`13:40:32 [NET] GET /api/v1/module -> 200`), overlay opens and is populated. The list content is
  NOT zone-specific — see `bug-module-zone-param-ignored.log` (backend ignores `?zone_id`, pre-existing,
  outside this diff).
- **AC3 [behav] NOT TESTED live** — NEARS-2058: the seeded `default_location` is outside every zone,
  so the desktop Submit renders disabled on a cold screen. Covered by diff-absence
  (`store_registration_screen.dart` is not in the diff) + `store_registration_desktop_submit_blocks_test.dart`
  (passes; it was hardened this ticket to scope the snackbar finder to `NSnackBar` so the new hint
  copy cannot fake a tap-landed observation).

## Extra checks
- **RTL/Arabic:** hint `الرجاء تحديد المنطقة` right-aligned inside the trigger, no clipping/ellipsis;
  label `حدد الوحدة النمطية` right-aligned above; section title mirrored to `bounds=[943,631][1269,724]`;
  trigger still `clickable="false"`; disabled fill identical `(247,246,245)`. Chevron mirrors position
  and stays a down-caret (correct, excluded from the mirror set). Language restored to English after.
- **`not_available_module` placeholder / NEARS-2057:** after `Use my current location`
  (geo fix 90.3654 23.8177, zone auto-detected as `Main Service Zone`) the widget collapses to
  `content-desc="Not Available Module"` exactly as before — the new hint does NOT leak into that
  branch. NEARS-2057 still reproduces identically; reported as information, not a defect of this change.
