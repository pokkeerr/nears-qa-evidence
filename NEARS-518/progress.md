# NEARS-518 QA progress
device: emulator-5554 | branch: fix/NEARS-518-toggle-contrast | worktree HEAD: 6a61a7d2 | light mode only
Token preflight: surface3=#EBE7E7 outlineVariant=#D9D6D6 outline=#767684 mint=#00FF99 navy=#000080 — all match AC

## AC verdicts (observed live, light mode)
- AC1 OFF state: PASS — Dark-Mode toggle: track light grey (#EBE7E7), inner thumb light gray (#D9D6D6) clearly LIGHTER than gray border (#767684); no grey-on-grey blob. Evidence: off-state.png
- AC2 ON state: PASS — Notification toggle (captured in LIGHT theme): track mint (#00FF99), inner thumb NAVY (#000080) strong contrast vs mint, gray border (#767684) STILL PRESENT (not transparent). Evidence: on-state.png
- AC3 border gray both states: PASS — gray ring visible in both OFF (Dark Mode) and ON (Notification). Evidence: off-state.png + on-state.png + settings-full-state1.png
- AC4 both usages consistent: PASS — same _SettingsSwitch on Dark-Mode (OFF) and Notification (ON) rows render identical treatment in one light screen. Evidence: settings-full-state1.png / settings-final-light.png
- Notification toggle confirm-sheet observed (display-only switch, row onTap drives confirm); cancelled with "No" — preference UNCHANGED (still ON). No data mutated.
- Automated backstop: flutter test test/theme/ ALL PASS incl. NEARS-518 switch-outline guard (6/6, ON+OFF pin to colorScheme.outline, light+dark).
- Runtime: no Flutter exceptions/overflows in app log; ui_errors clean.
VERDICT: PASS
