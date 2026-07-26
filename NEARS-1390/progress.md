# NEARS-1390 — NSnackBar/toast migration — Live QA evidence

Device: emulator-5560 (Android) · build: worktree feat/NEARS-1390-nsnackbar (uncommitted working tree) · backend: local :8000 · light mode.

| AC | Verdict | Evidence | Logs |
|----|---------|----------|------|
| 1 Success snackbar (navy + check_circle mint) | PASS | ac1-ac5a-success-referralcopy-default.png ("Referral Code Copied"); ac4-success-favstore-home-default.png; ac4-success-logout-menu-default.png | clean (no [ERR] on success) |
| 2 Error snackbar (navy + multiply_circle_fill) | PASS | ac2-ac5b-error-getx-notloggedin.png; ac2-ac5a-error-loginfail-default.png ("User credential does not match") | 1 [ERR] "error snackbar shown" per error toast |
| 3 navyDeep #00003C fill (not grey #334257) | PASS | verified on both success + error pills; token navyDeep=0xFF00003C | n/a |
| 4 >=5 distinct screens/flows | PASS | store(guest-fav), refer&earn(copy), menu(logout), login(fail), home(fav store) | clean |
| 5a default ScaffoldMessenger path | PASS | referral-copy / logout / login-fail / fav-store (all default path) | clean |
| 5b GetX path (borderRadius50 floating) | PASS | ac2-ac5b-error-getx-notloggedin.png (guest not-logged-in) | 1 [ERR] paired |
| 6 NEARS-568 log pairing intact | PASS | error toast -> exactly 1 [ERR]; success (isError:false) -> 0 [ERR]; diff shows log block byte-identical | verified |
| 7 NEARS-1225 cold-start guard | PASS(code+boot) | custom_snackbar.dart:52-55 null-context guard; app cold-started clean, no crash | clean |
| 8 Regression sweep | PASS | 10+ screens navigated, zero new snackbar/runtime errors; automated 34 tests green | only pre-existing sign_in 1px overflow (unrelated) |
| 9 RTL/Arabic | best-effort | code: NElement `direction` RTL override; nears_dls direction unit tests pass; not shown live (locale-switch nav flaky) | n/a |
| 10 Desktop margin width*0.7 @>=1300 | best-effort | code: n_snackbar.dart _desktopBreakpoint 1300 / factor 0.7; widgetbook knob; unit-covered; not reachable on phone | n/a |

Automated: nears_dls n_snackbar_test 16 passed; UserApp custom_snackbar_dls_test + api_client_transport_signal_test 18 passed. Total 34 green.
Widgetbook: n_snackbar_stories.dart renders 4 statuses (info/success/warning/error).
Diff confirms parity-preserving: CustomToast(isError) -> NSnackBar(status) in both paths; ScaffoldMessenger branch -> NSnackBar.show() (endToStart/elev0/transparent/floating/2s); NEARS-568 log block unchanged.

VERDICT: PASS
