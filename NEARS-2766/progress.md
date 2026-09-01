# NEARS-2766 — QA delta re-QA (fix-cycle 1) progress log

Reviewed commit: d3263af67 (code-reviewer PASSED)
Device: emulator-5554, UserApp built from worktree at d3263af67.

## Correction vs fix-cycle 0 assumption

fix-cycle 0's repro apparently used a screen reachable via Home -> location chip ->
"Set From Map", which is actually `pick_map_screen.dart` — a DIFFERENT screen with its
own separate, still-unguarded synchronous zoom in/out `animateCamera` calls (lines
~510-519, ~542-550). That screen is NOT touched by NEARS-2766's fix and was NOT
re-tested here (out of this ticket's file scope — `select_location_view_widget.dart`
only). Logged as a drift/regression-candidate below, not a NEARS-2766 blocker.

`SelectLocationViewWidget(fromView:false)` (the file this ticket actually touched) is
ONLY reachable via:
Store/Vendor Registration -> Vendor Info tab -> scroll to "Location Info" -> select a
zone -> "View fullscreen map". Confirmed this is the same `!widget.fromView` zoom
in/out block at lines 649-693 that d3263af67 fixed.

## AC2 — live repro re-verify

- Confirmed correct screen reached (AppBar "Set Your Store Location", Zoom in/Zoom out
  visible) at bounds Zoom in [1203,2441], Zoom out [1203,2576].
- Minimal 2-tap repro: 1x zoom-in tap + immediate hardware back -> **clean**, no
  StateError, app pid unchanged (3512).
- 12-cycle rapid tap+back loop (alternating zoom in/out, immediate back each time,
  re-entering via "View fullscreen map" every cycle) -> **zero StateError / zero FATAL
  EXCEPTION** across the full logcat capture (`grep -c` = 0 hits for
  StateError/animateCamera on disposed/FATAL EXCEPTION/[FAIL]/[ERR]).
- App process survived throughout (same pid), screen remained responsive and returned
  to the embedded Location Info tab correctly after each back-nav.
- Functional regression check: a normal (non-racing) zoom-in then zoom-out tap on the
  fullscreen map produced no error either.
- Verdict: AC2 **met**.

## AC1 (static) — re-confirmed

Diff (56f5dafa2 -> d3263af67) moves the `try` to wrap from
`await _mapController?.getZoomLevel()` through the `animateCamera` call in both
zoom-in and zoom-out `onTap` handlers. The sibling `_setPolygon` guarded path (line
~790-800, NEARS-2517 precedent) is untouched and intact. AC1 **met**.

## AC3 — flutter analyze

`~/Tools/flutter/bin/flutter analyze lib/features/auth/widgets/select_location_view_widget.dart`
-> "No issues found!". AC3 **met**.

## Automated backstop

`flutter test test/features/auth/select_location_map_restores_on_remount_test.dart`
-> 19/19 passed.

## Verdict: PASS
