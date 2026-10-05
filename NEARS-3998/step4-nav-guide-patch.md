# Nav-guide patch candidates (NEARS-3998 step 4 QA, 2026-10-05, emulator-5554). NOT applied: docs/apps/userapp/userapp-navigation-guide.md has a foreign dirty copy in the primary tree. Conductor/steward to merge.

## Pick-map: reaching an OUT-OF-ZONE position (no GPS needed) and the CTA labels (verified NEARS-3998 s4 QA)
- `adb emu geo fix` could not move the fused provider on this run (cached `last location` stayed on the Abu Dhabi Zone centroid 24.449998,54.424998; toggling `cmd location set-location-enabled false/true` then a new fix still gave `getCurrentLocation resolved via fallback rung=activeAddress`). The pick-map FAB `Use my current location` therefore always returns that centroid: use it as the deterministic "back IN zone" action.
- OUT-OF-ZONE by drag (label-driven, no coordinates stored): tap `Zoom out` x4, then 4 swipes of (0.22W,0.635H)->(0.74W,0.435H) over the map (W,H from `adb shell wm size`, 1344x2992 here) with ~1.5 s between; the 4th idle returns 404. Pick-map then shows two nodes `Service not available in this area` (the info line enabled=true clickable=false, and the Confirm button enabled=false). IN-zone again: `Use my current location`.
- The CTA label on the access-location/pick-map is `Confirm Location` (not `Pick Location`); the address-search suggestions for out-of-zone places render `... , Not available yet` with enabled=false, so search can never SET an out-of-zone location (drag is the only way, via updatePosition -> getZone).
- State probe: `uiautomator dump` -> per node `enabled=`; `Confirm Location | enabled=false` while in zone and not loading is the signature of PD-S4-1 (see below).

## Login suggestion sheet (dashboard, guest) (NEARS-3998 s4 QA)
- Shows ~3 s after the dashboard mounts, ONCE per fresh install (`suggestLogin` pref is cleared by `pm clear`, disabled once the sheet is dismissed). Labels: `Login/Sign Up`, `Continue as guest`, `Scrim`. `Login/Sign Up` opens the normal Sign In screen (same as Profile -> `Log in/ Sign up`); its `syncZoneData` call (login_suggestion_bottomsheet.dart:367) is inside the SOCIAL (Google/Facebook/Apple) success handler only, so it is not reachable with email login on an emulator.
- It covers the home (a11y shows only the sheet nodes), so dismiss with `Continue as guest` before any home interaction or pull-to-refresh.

## Home address chip (NEARS-3998 s4 QA)
- Guest: the chip (label = the geocoded address, contains `United Arab Emirates`) opens the pick-map. Logged in: it opens the `Set Location` sheet, rows `Select address: Home, <address text>` (for customer@nears.com on the scratch copy: `Marina Heights`, `Demo Zone — Dhaka`, `FC2G+22 Abu Dhabi ...`, 3 Dhaka rows), plus `Use Current Location` / `Set From Map`. Selecting a saved address runs setLocation/_prepareZoneData: 1 get-zone-id request + 2 `short-TTL coord cache` reuse lines on both builds.
- customer@nears.com shows an `Your payment was Incomplete` dialog (order #91404) after the home loads: `Close` only (never Pay Now / Cancel Order).

## Offline path (NEARS-3998 s4 QA)
- `adb shell cmd connectivity airplane-mode enable` then pull-to-refresh on home -> syncZoneData -> `[FAIL] LocationNoInternetAbort "location: syncZoneData aborted — no internet"` (+ one socket `[FAIL]` per other home endpoint) and the `NoInternetScreen` (`Oops!`, `No internet connection`, `Try Again`). `airplane-mode disable` then `Try Again` returns to home.

## Request counting / failure injection without touching the backend (NEARS-3998 s4 QA)
- A 60-line logging reverse proxy (listen :8235 -> own backend :8234; app built with `--dart-define API_HOST=10.0.2.2:8235`) gives per-request lines (ts, path, status) and window markers (`GET /__mark?name=...`); a mode file switches `get-zone-id` to an injected 500, a per-request delay, or a delay of only the 200 answers (stale-response test). `php artisan serve` prints no request paths, so the proxy is the attributable channel for wire counts. Window markers in logcat: `adb shell "log -p i -t QAWALK <tag>"` (quote it: an unquoted `|` is parsed by the device shell).
- Never start `adb logcat` without `-T 1` for a run capture: it replays the whole ring buffer and old markers with the same tag double-count.
