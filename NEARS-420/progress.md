# NEARS-420 QA progress (live, emulator-5554)

- Build: feat/NEARS-420-signin-overflow @7b911775, UserApp on emulator-5554
  (tested at density 600 = ~358dp small phone for the sharp keyboard-compression case; restored to 480)
- Backend: http://127.0.0.1:8000 config 200 (real local, not demo)
- analyze (sign_in_screen.dart): PASS — No issues found (1.7s)
- test (sign_in_hero_overflow_test.dart): PASS — 11/11 (9 shape-replica + dismiss + source-pin)

## AC live observations (all on the navy sign-in hero)
- AC1 keyboard-open no overflow (small viewport): PASS — mInputShown=true; ui_errors log clean; Dart MCP runtime errors none; wordmark "Nears"+tagline+form+guest+terms all reachable; hero scrolls.
- AC2 keyboard-dismiss re-center: PASS — wordmark back at [75,752], tagline [75,962], guest [75,2497], terms [818,2696] = identical to closed baseline; no jump/blank gap; clean.
- AC3 BC-1 unbounded guard: PASS — no "incoming height unbounded" exception on build or any keyboard transition (Flexible stays bounded by retained IntrinsicHeight).
- AC4 landscape + keyboard: PASS — mInputShown=true, scrolls, lower content reachable, zero overflow.
- AC5 dark mode + RTL/Arabic: PASS — navy hero + mint accents render in dark; Arabic mirrors (Language pill top-LEFT, Back top-RIGHT vs LTR); field icons RTL-aligned; guest+terms reachable; zero sign-in overflow either direction. Restored EN+light.
- AC6 analyze + automated backstop: PASS.

## Regression sweep (bounded)
- sign_up_screen: PASS — renders ("Join the Elite", phone field, Sign Up, terms); no overflow.
- forget_pass_screen: PASS — renders ("Forgot Your Password", phone field, Request OTP); no overflow.

## regression_bug (pre-existing, NOT this change — does NOT affect verdict)
- Home banner carousel RenderFlex overflow 10px (LTR) / 12px (RTL) on bottom
  @ UserApp/lib/features/home/widgets/views/banner_view.dart:248 (Column).
  Last touched by NEARS-397 (home reskin) commit 2e0ea8ed, NOT NEARS-420.
  Fires because the guest home stays mounted under the pushed sign-in route.
  Independent of the sign-in hero.

## Verdict: PASS
