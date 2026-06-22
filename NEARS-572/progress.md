# NEARS-572 QA progress checkpoint

Device: emulator-5554 (Android 17, com.izzes.nears, debug build).
Backend: worktree Admin (has NEARS-571 SetRequestId) on :8000, vendor via `composer install`, env+oauth copied from primary (DB read-only). baseUrl NOT edited — worktree already derives `10.0.2.2:8000` for Android dev.

| AC | Verdict | Evidence (live) |
|----|---------|-----------------|
| AC1 outbound unique v4 | PASS | 7 app requests -> 7 distinct strict UUID v4 `X-Request-Id` (tap-proxy capture) |
| AC2 backend echo / read-back | PASS | sent `ae2721b3...` -> echoed identical; app `[FAIL]` carried the echoed id |
| AC3 handled-error join (C1 fix) | PASS | login 401 `[FAIL] correlation_id=ae2721b3...` (NOT null) == backend structured `[FAIL] correlation_id=ae2721b3...` |
| AC3 H1 transport failure | PASS | backend killed -> 14 `[FAIL]` lines, each `http_status=null` yet a valid minted v4 `correlation_id` |
| AC4 Crashlytics key + no PII | PASS | `[FAIL]` console line carries id live; `setCustomKey('correlation_id')` proven by unit backstop; dashboard upload deferred (debug collection off, NEARS-296) |
| AC5/AC6 names + PII-safe | PASS | `X-Request-Id` / `x-request-id` / `correlation_id` exact; id hex+dashes only; only allow-listed fields on `[FAIL]` |
| AC7 full test suite | PASS | `+1452: All tests passed!` (exit 0) |

Regression: clean (200s additive; token-refresh retry mints fresh id; no red-screens).
