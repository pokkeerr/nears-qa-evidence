# NEARS-2484 QA progress (fix-cycle 1)

- AC1 [ui] reference-only: met=true (cited NEARS-2455 evidence log, not re-demonstrated per instructions)
- AC2 [ui] zero overflow / scroll-reachable / nothing clipped, logged-in: met=true — ac2-loggedin-natural-viewport.png + wm-size-forced 1344x1600 and 1344x2100 trials, zero RenderFlex/[FAIL] in any trial (LTR+RTL)
- AC3 [behav] every tile tappable+reachable via scroll, guest+logged-in: met=false, breaks_ac=true — scroll-position-reset defect (bug-profile-scroll-position-reset.log), reproduced at 2 independent viewport heights, zero interaction/zero log line
- Regression sweep (bounded to this screen): clean
- Automated: flutter test test/features/profile/profile_screen_scroll_overflow_test.dart -> 3/3 passed
- Verdict: FAIL
- Evidence gallery: https://github.com/pokkeerr/nears-qa-evidence/tree/main/NEARS-2484
- Jira comment posted: yes
- Device: emulator-5558, released clean, wm size reset to native, language pref reverted en

## Delta re-QA (fix-cycle 2, commit 848fa20d, worktree nears-NEARS-2484-profile-scroll-overflow, device emulator-5556, 2026-08-25)

Fix: removed dead `key: UniqueKey()` on ProfileScreen's Scaffold (was forcing a full
subtree remount -> discarded SingleChildScrollView's scroll state on every
GetBuilder<ProfileController> rebuild) + added `PageStorageKey('profile_account_settings_scroll')`
on the SingleChildScrollView as defense-in-depth.

- AC3 re-demo, 1344x1600: scrolled to bottom (Logout + "Version 3.8 - Built for Speed"
  visible), idled 8s zero-interaction, re-dumped -> Logout + Version STILL present
  (previously reset by t=5.2s). Evidence: ac3-redemo-1344x1600-t0-scrolled.png/.xml,
  ac3-redemo-1344x1600-t8-idle.png/.xml. met=true.
- AC3 re-demo, 1344x2100: same methodology, same result -> scroll position preserved
  after 8s idle. Evidence: ac3-redemo-1344x2100-t0-scrolled.png/.xml,
  ac3-redemo-1344x2100-t8-idle.png/.xml. met=true.
- Every settings tile confirmed tappable+reachable, logged-in (qa.singlestore@nears.com):
  Dark Mode (tap registers, immediately toggled back per light-mode-only policy —
  rendering not inspected), Notification (opens disable-confirm bottom sheet, dismissed),
  Change Password (navigates to update_profile_screen, Back returns to same scroll
  offset), My Address (navigates to Saved Addresses), Coupons (navigates to coupon list),
  Talk to Nears! (navigates to Conversation List), Help & Support (navigates to contact
  screen), Logout (opens confirm dialog at re-verified bounds, first pass cancelled via
  No, second pass confirmed via Yes -> "Logout Successful"), Version footer visible.
- Guest state (post-logout, natural viewport, no scroll needed): Guest User header,
  Login CTA, Dark Mode / Coupons / Talk to Nears! / Help & Support / Version all present
  and reachable (Notification/Change Password/My Address/Logout correctly absent —
  gated by isLoggedIn, matches profile_screen.dart). Guest tap on Coupons correctly
  routes to an auth-gated "please login" prompt (expected, not a defect).
- Regression sweep (bounded to this screen): avatar/header render clean at both
  viewports and at native size; no new RenderFlex/overflow/exception; runtime log
  (`get_runtime_errors` equivalent via flutter run console) clean throughout — zero
  [ERR]/[FAIL]/exception lines across the whole sequence. Dark-mode toggle rendering
  itself was NOT visually verified (dark mode deferred per light-first policy) — only
  that the tile remains tappable.
- Automated backstop: `flutter test test/features/profile/profile_screen_scroll_overflow_test.dart`
  -> 3/3 passed (incl. the new NEARS-2511 regression test
  "ProfileScreen rebuilding in place ... does not reset the settings scroll position").
- Verdict: PASS
- Evidence gallery: https://github.com/pokkeerr/nears-qa-evidence/tree/main/NEARS-2484
- Jira comment posted: yes (on NEARS-2511)
- Device: emulator-5556, released clean, wm size reset to native
