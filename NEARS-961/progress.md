# NEARS-961 QA — FINAL: Cannot-Reproduce / Already-Fixed (grid-card scope) = PASS
Device: emulator-5560 | built from worktree fix/NEARS-961-grid-card-1px-overflow @6dae327a (clean, no code changed)
font_scale=1.0 default | light-first | Detection: Dart VM get_runtime_errors (Flutter.Error) + visual yellow banner
(FlutterError.onError->Crashlytics at main.dart:89 suppresses overflow from logcat, so ui_errors/logcat are blind to it)

FLOW: login(customer@nears.com) -> Profile -> Logout -> Yes -> guest home -> Abu Dhabi zone2 -> module home.

AC1 grid-card overflow during logout->guest-home @DEFAULT scale -> NOT REPRODUCED (Already-Fixed/CNR). MET.
  get_runtime_errors CLEAN after each grid re-render:
   - guest-home sector landing (store+offer cards)  CLEAN  01/02
   - module-home item grid                           CLEAN  03
   - module-home "15 stores near you" store grid     CLEAN  04
   - store-page item grid                            CLEAN  05
  Grid cards also CLEAN at 1.3 scale (07, no banner on Buy-It-Again cards).
AC2 grid cards render identical / no crop, light+dark -> MET (06 dark clean; 01-05 light clean).
AC3 flutter/dart analyze no new issues -> MET (scoped analyze "No issues found!"; zero-diff branch; overflow is
    runtime-only, not statically detectable).

FINDINGS (do NOT gate 961's grid-card verdict):
  R1 [DEFAULT scale] 1px bottom RenderFlex overflow on sign_in_screen.dart:221 Column (sign-in branding+form stack).
     Matches ticket phrase "1px RenderFlex bottom overflow" EXACTLY but on the SIGN-IN screen, not a grid card;
     trigger = opening sign-in (login), not logout->guest-home. Contradicts in-code comment (line 210-218) that
     claims Flexible(FlexFit.loose) removed "~1px RenderFlex overflow". Present on current development too.
     => Strong candidate for what the original reporter actually saw (mis-attributed to "grid-card"). Log: bug-signin-branding-1px-overflow.log
  R2 [1.3 scale only] app-bar 'Deliver To' location Column overflow 4.0px (home_screen.dart:238-390).  Shot 07.
  R3 [1.3 scale only] promo BannerView Column overflow 44px (banner_view.dart), "QA Single-Store Campaign A" wraps. Shot 07.
     R2/R3 = large-font a11y regressions on NON-grid widgets. Log: bug-fontscale-1.3-nongrid-overflows.log

DRIFT: worktree nears-NEARS-961-... removed mid-run by a concurrent session; primary advanced 6dae327a->ae2a3be9
       (identical sign_in/grid code). Live QA ran against the 6dae327a build = ticket target.
Device reset: font_scale=1.0, theme=light on exit.
