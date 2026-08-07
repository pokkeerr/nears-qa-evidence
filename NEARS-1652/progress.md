# NEARS-1652 live QA — progress / result log (fix_cycle 0)

Device `emulator-5558` · APK md5 `2116a5c1f527e790e53ee74b6ac506b2` (verified identical
BEFORE and AFTER every observation) · worktree
`/Users/Apple/Projects/nears-NEARS-1652-chat-load-failure-state` @ `5fba433a`
Flutter `/Users/Apple/Tools/flutter/bin/flutter` 3.41.9 · light mode only (dark deferred).

Fault injection: `nears_fault_proxy_1652.py` on port 8791 → `127.0.0.1:8000`, app pointed at it
with `--dart-define=API_HOST=10.0.2.2:8791`. Shared backend never stopped; DB read-only.

## Per-test-point results

| Point | Result | Evidence |
|---|---|---|
| A — AC3 live, conversation list | PASS | `[FAIL] endpoint=/api/v1/customer/message/list http_status=503 type=ApiFailure msg="chat: conversation list fetch failed" correlation_id=9b8dfc5c-…` — exactly 1, path-only, PII-free |
| A — AC3 live, message thread | PASS | `[FAIL] endpoint=/api/v1/customer/message/details http_status=503 type=ApiFailure msg="chat: message thread fetch failed" correlation_id=53796107-…` — no `conversation_id`/`admin_id` in the line |
| B — 401 force-logout, in-scope GET | PASS | token refresh → retry → 401; exactly ONE `[FAIL]` (`api request failed`, checkApi's); guest re-login + nav to initial route; Profile = `Guest User` |
| C — 401 during SEARCH | PASS | exactly ONE `auth/guest/request` in the proxy log; exactly ONE `[FAIL]`; no double logout |
| D — search failure user-visible | PASS | toast `QA fault injection` found in a11y tree + paired `[FAIL] … msg="api request failed"` |
| E — NEARS-1173 pagination retry row | PASS | retry row shown on faulted page 2; Retry re-fired `offset=2` exactly; unfaulted Retry loaded page 2 |
| F — failed refresh keeps data | PASS | faulted `offset=1` refresh over 15 loaded rows → list intact, 1 `[FAIL]` |
| G — success path | PASS | list 200, thread 200 (conv 46 + admin thread), thread pagination, message sent + post-send refresh 200 — all zero `[FAIL]` |
| H — interim no-toast/no-error-state | AS DOCUMENTED | first-load fault renders bare chrome only; not filed |

## PII sweep — all 11 chat `[FAIL]` lines captured this session
0 occurrences of: `conversation_id`, `admin_id`, `vendor_id`, `delivery_man_id`, `?` (query
string), `@`, `token`, `Bearer`, any message body text, any phone/email, `statusText`.
All 11 carry `http_status=` + a UUID `correlation_id=` (except the transport case, where
status/correlation are legitimately null).

## Transport-throw case (measured, not inferred)
Proxy killed → connection refused → **2** `[FAIL]` per fetch: api_client `_send`'s
unconditional `"api request threw"` + the controller's `"chat: conversation list fetch failed"`
(`http_status=null`, no correlation_id, `ApiFailure.transport()` — PII-safe).
Exactly as solution doc §1.3 predicted. **Count is unchanged from base** (base emitted
`_send`'s line + checkApi's line = also 2), so this is not a regression.

## Automated backstop
`flutter test` (UserApp, from the worktree, after `rm -rf .dart_tool build && flutter pub get`):
**`+2948 ~2 -6`** — matches the stated post-change baseline exactly.
All chat suites pass in isolation: `test/features/chat/` + `load_more_error_rows_test.dart`
= **55/55**.
