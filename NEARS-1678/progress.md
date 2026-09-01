# NEARS-1678 QA progress

Device: emulator-5558 (locked, disk 873996KB free at acquisition)
App: UserApp, worktree /Users/Apple/Projects/nears-NEARS-1678-interest-grid-tap-target
Account(s): fresh signups created live (qa.nears1678.tap@example.com, qa.nears1678.tab@example.com) — seeded demo accounts (sophie.davis, robert.taylor) were no longer cold on modules 1/2 (module_ids already [1,2] from prior QA runs against the shared dev DB).

## AC1 [ui] — phone (2-col), 320dp width override (wm density 160 + wm size 320x711)
- Module 1 (Grocery, category set A): cards [20,218]-[155,275] etc. height 56-57px=dp (density 160 = 1:1 px:dp). Width 135dp matches the grooming's predicted cell width exactly.
- Module 2 (Food, category set B): same geometry, height 56-57dp, width 135dp.
- Both >= 44dp floor, matches predicted 56.7dp with margin.
- Logs clean (ui_errors: 0 matches) at measurement time.
- Screenshot: ac1-320dp-interest-grid.png
- Automated backstop widget test (`NEARS-1678 tap target`) independently pins the same >=44dp assertion at 320dp — PASS.

## AC2 [behav] — tab (800dp) + desktop (1400dp) breakpoints
- Tab 800dp: 3-col grid, cell width 247dp, height 79dp. No overflow/clipping (full dump, all labels intact).
- Desktop 1400dp: 4-col grid, cell width 275dp, height 88dp. No overflow/clipping.
- childAspectRatio branches for isTab/isDesktop are byte-identical pre/post diff (confirmed via code read) — measured geometry is a live regression check, not a new-behavior check.
- Screenshots: ac2-tab-800dp-interest-grid.png, ac2-desktop-1400dp-interest-grid.png

## Regression sweep
- Skeleton vs loaded grid geometry: both call the same `_gridDelegate(context)` (confirmed via code read, interest_screen.dart:289-306, called at both the loaded GridView and the skeleton GridView). Live capture of the transient skeleton frame not achievable — local dev backend responds faster than the ~1-8s uiautomator dump latency (documented tooling limit, NEARS-1747). Structural guarantee (single shared function) stands in for the live frame-by-frame observation.
- NEARS-1675 CTA-disable-while-saving: `onPressed: categoryController.isLoading ? null : (...)` untouched by this diff (confirmed via code read). Live capture of the sub-second disabled window also not achievable for the same reason. Automated widget test `NEARS-1675 CTA disabled while saving` (already in the suite, unrelated to this ticket's edit) — PASS, confirms the mechanism still functions.
- Two [FAIL] `update-interest http_status=403` log lines observed during navigation — traced to legitimate empty-interest submission attempts (Laravel `required|array` validator correctly rejecting a 0-selection Save & Continue), each paired with a user-visible "The interest field is required." message and a correctly-emitted [FAIL] log line. NOT a defect (no silent-failure pattern) — expected validation behavior, unrelated to NEARS-1678's diff either way.

## Automated backstop
`flutter test test/features/interest/interest_screen_dls_test.dart` — 9/9 passed, incl. `NEARS-1678 tap target` and `NEARS-1675 CTA disabled while saving`.
