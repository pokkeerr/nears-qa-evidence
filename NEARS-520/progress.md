# NEARS-520 QA progress (fix-cycle 0) — device emulator-5556
started: 2026-06-28T12:41:53Z

- 12:53:59 reached ForgetPassScreen (phone variant: +971/Request OTP + OR + email). Login hero captured. logs clean so far.
- 12:57:56 AC1 PASS (full-height, no seam, logs clean)
- 12:57:56 AC3 PASS keyboard-open (gradient fills viewport above docked keyboard, no band) + dismiss re-fill, logs clean
- 13:10:46 AC2 PASS Login+Signup heroes full-height (live); OTP/Verification+Reset light-bg (code-confirmed untouched)
- 13:10:46 RTL/Arabic PASS full-height no seam, mirrored layout, logs clean
- backstop: forget_pass_hero_fill_test 8/8 PASS
- OBSERVATION (not NEARS-520): floating bottom nav not visible/reachable on guest home (zone 2) — possible NEARS-591 glass-nav render/a11y artifact; flagged as regression-candidate
