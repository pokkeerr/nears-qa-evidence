# NEARS-1892 — device-free QA determination (independent verification)

QA independently re-derived the device-free predicate rather than accepting the
conductor's framing at face value. Findings:

1. **`AppLogger.failure`'s debug console `[FAIL]` line** (`UserApp/lib/helper/app_logger.dart:74-85`)
   only reads `e.runtimeType` (always the string `ApiFailure` for both
   `ApiFailure()` and `ApiFailure.transport()` — Dart's `runtimeType` does not
   vary by named constructor) and `e.transportKind` (null on both the old and
   new sentinel calls in this diff — neither call site passes a kind argument).
   The `.transport` bool field is **never read** by this line. Confirmed live
   by running the touched test files: every `[FAIL]` line printed during the
   run reads `type=ApiFailure` with no `kind=` suffix, identical to what the
   pre-fix `.transport()` sentinel would have produced (see
   `regression-test-run.log`).

2. **Crashlytics non-fatal payload.** `main.dart:82-83` sets
   `FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(!kDebugMode)`
   — collection is OFF on every debug-mode device/emulator run, which is the
   only mode QA drives. So even though `ApiFailure.toString()` *does* branch on
   `.transport` (`app_logger.dart:384-390`) and that string could reach a
   release-mode Crashlytics dashboard, it never reaches the debug-mode QA
   session because collection is disabled there.

3. **No debug-only diagnostic screen** exposes the raw `ApiFailure` object or
   its `.toString()` anywhere in `UserApp/lib` — grepped for
   debug-panel/log-viewer/diagnostic-screen patterns, none found reading this
   sentinel.

4. **Screen/state behavior is untouched.** `_couponListError` /
   `_userInfoLoadFailed` are set to `true` on a null result regardless of which
   `ApiFailure` sentinel is logged — the classification object never feeds any
   widget-visible state. Confirmed by `coupon_refresh_failed_row_test.dart` and
   `refer_and_earn_screen_render_test.dart` passing unchanged (same widget
   assertions, same NearsErrorRetry visibility).

**Conclusion:** genuinely device-free. The only observable difference from this
change is an internal object field (`ApiFailure.transport`, and its
`.toString()`) that is unit-test-inspectable but not reachable through any
console line, Crashlytics debug-mode upload, or on-screen state in a normal QA
device session. Verified via live `flutter test` execution (not just re-trusting
the conductor's/engineer's report) — see `regression-test-run.log` (55/55 green,
executed by QA in this pass).

## Minor drift noted (non-blocking)

AC5's exact wording ("api_client.dart's own generic `[FAIL] ... msg="api request
failed"` line") does not match the actual reason strings in
`UserApp/lib/api/api_client.dart` — they are `'api request threw'` (transport
throw path, ~line 815) and `'unhandled api response'` (non-2xx handled path,
~line 1241); no site uses the literal string `"api request failed"`. The
underlying claim the AC is checking — that `api_client.dart` is untouched by
this diff and still logs its own independent `[FAIL]` line separate from the
controller's — is TRUE (confirmed: `git diff feat/userapp-reskin2 --
UserApp/lib/api/api_client.dart` is empty). This is a QA Test Scope wording
drift, not a code defect.
