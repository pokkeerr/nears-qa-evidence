# NEARS-1371 — NPasswordStrengthBar — QA evidence

Build: worktree feat/NEARS-1371-npasswordstrengthbar @ c6db8571 (light mode only; dark deferred).
Live surface `new_pass_screen.dart` is OTP/backend-gated (reset flow needs a valid phone+token) → drove the
migrated widget via widgetbook + relied on deterministic goldens per team-lead guidance.

| AC | verdict | evidence | logs |
|----|---------|----------|------|
| 1 render: 4 segs, score 0→4 lights, Weak=red/Fair=orange/Good=navy/Strong=mint+glow, tier label + min-8 hint, maintainSize no-jump | PASS | golden-states-light.png (all 5 states, tier colors + labels confirmed by read); nears_dls tier-color/clamp tests | clean |
| 2 never gates submit — 8-char weak submits | PASS | UserApp verification test "CRITICAL: 8-char all-lowercase NOT blocked" (51/51) | clean |
| 3 RTL (ar) + dark render, no overflow/error | PASS | golden-rtl-weak.png (lit-from-trailing), golden-dark-good.png; nears_dls RTL+dark tests; ar/en i18n keys resolve | clean |
| 4 app boots clean, no NPasswordStrengthBar runtime errors | PASS | widgetbook web compiled+loaded, ZERO exceptions in run log; analyze 0; migration grep-zero (old widget deleted, 1 call site) | clean |

Automated: nears_dls flutter test 141/141; goldens 3/3; UserApp verification 51/51; flutter analyze 0 (package + screen).
Note: the `[ERR] "error snackbar shown"` lines in the verification suite are the deliberate min-8 REJECTION
tests exercising the guarded (AppLogger-paired) error path — expected, not a silent-failure defect.
Live headless CanvasKit render was blank (Flutter web-server lacks cross-origin-isolation headers skwasm needs);
goldens are the authoritative pixel-exact visual proof for this display-only widget.
