# NEARS-1628 — QA [8] progress checkpoint

Worktree `/Users/Apple/Projects/nears-NEARS-1628-wallet-bonus-loading` @ `5390fbe1`
Device `emulator-5558` · app pid 16629 · APK md5 `689ffcd8bd86737f7f37f6371aac499b` (unchanged start→end)
Flutter `/Users/Apple/Tools/flutter/bin/flutter` 3.41.9 · light mode only (dark deferred)
Backend `127.0.0.1:8000` via QA fault proxy on `10.0.2.2:8091` (`--dart-define=API_HOST`)

## Build freshness (two-stage, per observation)
- Stage 1 (pre-filter): installed-artifact md5 before/after every AC observation — constant `689ffcd8…`.
- Stage 2 (verdict): live-isolate source of `wallet_controller.dart` read over the Dart VM service —
  marker present=True, `else` branch=True, sentinel probe=False (instrument comes out two ways).
  Re-run before AC2, before AC1b, and at teardown. All FRESH.

## Per-AC results
| AC | Result | Evidence |
|---|---|---|
| AC1 (unit still holds) | PASS | 17/17 in the two wallet test files, 0 failures; includes `a failed bonus fetch leaves no bottom skeleton` (asserts `NSkeleton findsNothing` + `isLoading isFalse`) and a positive control asserting `findsOneWidget` |
| AC1b (live no-regression, bonus 500) | PASS | `11-fault-snackbar-caught.png`, `10-fault-snackbar.png`, `measure-skeleton-fault.log`, `measure-snackbar-fault.log`, `measure-isloading-fault.log`, `fault-proxy-wallet-traffic.log` |
| AC2 (success path unaffected) | PARTIAL — 3 of 5 clauses PASS, 2 NOT TESTED (data gap) | `06-wallet-success-settled.png`, `07-addfund-dialog.png`, `measure-skeleton-success.log`, `measure-isloading-success.log` |

## Regression sweep
| Check | Result | Evidence |
|---|---|---|
| Initial-load bottom skeleton appears then clears | PASS | `measure-isloading-success.log` — 300 valid samples, `isLoading` false→**true**→false |
| Wallet filter re-fetch | PASS | `measure-skeleton-filter.log` — 12→0 skeletons, list 4→2, `isLoading=false` |
| Add-Fund button not stuck | PASS | `07-addfund-dialog.png` + live `isLoading=false` |
| Pagination load-more | NOT TESTED (unreachable) | live `canLoadMore=false`; 4 rows for this user, 6 in the whole DB, page size 10 |
| Loyalty Points / Home smoke | PASS | `12-loyalty-points.png`, `13-home-smoke.png` |

## Logs
Scoped to my own pid 16629 (NOT the raw `ui_errors` buffer). 338 flutter-tag lines scanned.
5 `[FAIL]` lines total, all `endpoint=/api/v1/customer/wallet/bonuses http_status=500` — the
injected faults, one per fault navigation, matching `fault-proxy-wallet-traffic.log`. Zero
unexpected `[ERR]`, zero exceptions, zero RenderFlex overflows.

## Test gate
Full suite `+3222 ~2 -6` on a cleared `.dart_tool`/`build`. Composition matches baseline exactly:
`coupon_controller_test` x3, `dls_golden_test` x2, `category_screen_back_button_test` x1
(`gate-test-failures.log`). No golden moved.
