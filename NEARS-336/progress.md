# NEARS-336 QA — Tier-4 minor-leaks cleanup (FINAL UserApp MVVM module)

**Device:** emulator-5554 (Android 17 / API 37) · **Branch:** feat/NEARS-336-tier4-cleanup (b113ef99)
**Backend:** http://10.0.2.2:8000 (local, baseUrl derived correctly) · queue:work running · session authenticated.
**Verdict: PASS** (pins-primary + live render clean; live drive-through of moved surfaces blocked by pre-existing a11y cluster).

## Automated backstop — PRIMARY safety net for this byte-identical refactor
- `flutter test` (UserApp): **779 passed / 0 failed** (719 baseline + **60 new Tier-4 pins**) — GREEN. Re-run by conductor, confirmed `+779: All tests passed!`.
- The 60 pins directly assert byte-identity of every one of the 15 moved computations: #2 validation order + UpdateUserModel; #3 the exact offline-payment payload map; #4 maxCod loop; #5 remaining math; #6 cart→payload; #7/#8 pagination max-page math; #9 date-grouping; #10/#11 recent-active + sender-resolve; #12 percentages; #13 canReviews + the pinned 100ms quirk; #14 interest count; #15 selectModuleById.

## Live demonstrations
- App boots, authenticates, and renders on the 336 branch against the real local backend — food-module Home + store list (The Grill House, Burger Palace, Pizza Heaven…) + the live "Order #152 Pending" banner all render. Shots `00-home.png`, `01-food-home-render-clean.png`.
- Flutter **widget tree intact** (read via Dart VM service / DTD) — the app renders correctly.
- **logcat scan: ZERO flutter exceptions/errors from the 336 build** (excluding the known pre-existing address log-noise NEARS-342).

## Live label-driven drive — BLOCKED by pre-existing a11y cluster (NOT caused by 336)
- `ui_list` / raw `uiautomator dump` return an **empty semantics tree** on the food-Home surface. Root cause confirmed via Dart VM `get_runtime_errors`: the **NEARS-339** framework assertion `'!semantics.parentDataDirty': is not true` (rendering/object.dart:5493, "Exception caught by scheduler library" — caught, non-fatal). This is the documented food-home semantics crash that blinds label-driven QA.
- Compounded by **NEARS-340**: this seeded account has a running order (#152), which swaps the bottom-nav Row→SizedBox, so the Profile/Wallet/Loyalty/Notifications/Interest tabs are unreachable by label OR coordinate.
- Both defects are pre-existing, already ticketed, and untouched by NEARS-336. Same blocker class that gated NEARS-334's live QA. The moved surfaces are therefore **pin-covered** (the 60 pins are the byte-identity proof) rather than live-driven.

## Triage
- **task_bugs:** none (byte-identical; suite green; no new runtime error from 336).
- **regression_bugs:** none new — the only runtime error observed is NEARS-339 (already ticketed); nav block is NEARS-340 (already ticketed); address log-noise is NEARS-342.
