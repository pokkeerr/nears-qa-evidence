# NEARS-518 QA progress — switch track-outline (mint ON ring) fix
Device: emulator-5554 (Android) | Build: worktree feat/NEARS-518-toggle-active-border @a0d18c4b | UserApp, backend http://10.0.2.2:8000 (200)

| AC | Verdict | Evidence |
|----|---------|----------|
| 1 OFF border unchanged (grey) | PASS | 04-light-notif-off.png (both rows grey ring), 01-light-off-and-on.png |
| 2 ON border removed (no grey/dark ring over mint) | PASS | 01 (light notif ON clean mint), 02-dark-darkmode-on.png (dark ON clean mint), 05-light-notif-on-settled.png |
| 3 All DLS-toggle screens consistent | PASS | dark-mode + notification rows both consistent across all shots |
| 4 Both light AND dark verified | PASS | light 01/04/05, dark 02/03 |
| 5 No one-off overrides (theme-level only) | PASS | code: _SettingsSwitch sets thumb/track colors but NO trackOutlineColor; inherits SwitchThemeData |
Carry-overs: transition no grey-ring flash = 06-light-transition-no-grey-ring.png; dark OFF sky-blue ring reads inactive (pre-existing) = 03; Cupertino switches (cart cutlery/profile) unaffected (separate widget, immune to SwitchThemeData).
Automated: flutter test = 1210 passed (incl. 6 new nears_theme_switch_outline_test).
