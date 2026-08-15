# NEARS-1483 (Option C-prime) — QA progress checkpoint
Branch fix/NEARS-1483-live-surface-error-logging @ 20a077bb (base e6c135e8)
Device emulator-5558 | PRE apk md5 a639a4a0... | POST apk md5 9dafc34a...

TASK1  isForMainFrame == TRUE (1 WARN line on PRE)      -> task1-isformainframe.log
AC-C1  PASS  1 [FAIL], PII-clean                        -> ac-c1-transport-failure.log
AC-C2  PASS  PRE 0 lines / POST 1 [FAIL] http_status=502-> ac-c2-http-502.log
AC-C3  PASS  sub-resource 502 + refused -> 0 [FAIL]     -> ac-c3-subresource-control.log
AC-C4  PASS (wallet field) + unit seam for order/subs   -> ac-c4-entrypoint-labels.log
REGRESSION  clean, real Razorpay load, no UI change     -> regression-and-ui.log
PRE-EXISTING bug (regression lane)                      -> bug-payment-back-navigator-assert.log
AUTOMATED  flutter test (UserApp, worktree) = 3953 passed, 2 skipped, 0 failed (exit 0)
           gate test payment_webview_failure_gate_test.dart = 8/8 passed
