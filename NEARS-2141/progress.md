# NEARS-2141 QA progress — fix-cycle 1 delta re-QA

Device: emulator-5558, com.izzes.nears, build 82aa2481, English, light mode only.

## AC1 (task-bug fix, [ui]): collapsed 320dp/1.3x status text visible with nonzero width
- MET. Render-tree evidence: label Flexible flex=2 (max 63.8dp, painted 63.8x29 "Your…"),
  status Flexible flex=3 (max 95.7dp, painted 95.7x29 "Confirm…") — exact 2:3 split,
  both nonzero, matches code's 2:3 flex ratio comment.
- Screenshot: fix-collapsed-320dp-1.3x-status-visible.png — "Confirm…" clearly legible,
  navy/primary-colored bold text, no invisible sliver.
- logs: clean (0 [FAIL]/framework_error hits, positive control confirmed pipe alive)

## AC2: zero overflow at 320dp/1.3x, collapsed AND expanded (all 13 rows)
- MET on fresh cold boot at target dimensions (canonical repro method): collapsed clean,
  expanded scrolled top-to-bottom (all 13 orders) clean, across app background/foreground.
- NOTE: one transient overflow (31px/41px, line 85:28 outer Row — icon+"+N more" circle,
  NOT the header Row this ticket touches) was observed exactly once, during a LIVE `wm size`
  override applied while the app was already running mid-session (a resize-animation
  transient, not steady state). Not reproduced across 4 subsequent attempts incl. cold boot
  at the same target dimensions. Filed as a non-blocking followups[] observation, not a
  task_bug — unreproducible on the canonical boot-time test method the AC targets.

## AC3 (sanity): standard scale / 100%, no regression
- MET via render tree: status "Confirmed" 80.2x22dp painted inside 178dp max (comfortable
  margin, no ellipsis triggered); label "Your Order is " 102.4x22dp inside 118.7dp max
  (fits). No visual truncation regression.

## Automated backstop (independent re-run)
flutter test test/features/dashboard/running_order_status_overflow_test.dart -> 9/9 passed.
