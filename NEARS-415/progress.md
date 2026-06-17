# NEARS-415 QA progress — strip PII from api_client debug logs (UserApp)

Device: emulator-5554 | branch feat/NEARS-415-strip-pii-logs @ 0496ba5e | baseUrl http://10.0.2.2:8000 (real local backend, /api/v1/config -> HTTP 200)
Build: debug APK (com.izzes.nears), launched fresh via flutter run.

## Per-AC verdicts (observed live)

- **AC L3 (response body — main vector): PASS.** Boot fired many authenticated GETs
  (/config, /banners, /module, /stores, and post-login /customer/info x2,
  /customer/address/list). EACH emitted ONLY `====> API Response: [200] <uri>`.
  NO full response body, NO customer name/email/phone/street/lat-lng in any log line.
  Saved-addresses screen rendered 2 saved spots — data flows to UI, never to logs.

- **AC L1 (request body via LOGIN POST): PASS.** Signed in customer@nears.com / 123456789.
  `====> API Response: [200] /api/v1/auth/login` — login succeeded. NO `API Body:` line
  before the POST (request body phone/password never logged). `API Call: <uri>` line
  present via dart:developer log() (VM Logging stream). Authorization header redaction:
  source-pin proves `Header: ${_redactHeaders(...)}` is wired and truncates Bearer to
  first-14+"..."; the live VM-service capture truncates the header tail at ~128 chars
  (capture-channel limit), so the redacted-tail isn't directly visible — BUT a scan for
  `Bearer <20+ char token>` across logcat + VM log returns ZERO, confirming no full token leaks.

- **AC3 (no PII anywhere): PASS.** Whole-session scan: 0 `API Body:` lines (logcat AND VM),
  0 full Bearer tokens, 0 f_name/l_name/latitude/longitude/"address": tokens on flutter tag.

- **AC4 (functional intact): PASS.** Login succeeded (200), /customer/info loaded (200 x2),
  saved-addresses list loaded (200) and rendered 2 addresses. No runtime errors
  (Dart MCP get_runtime_errors: "No runtime errors found"), no flutter error signatures (ui_errors empty).

- **AC5 (release-gate reasoning): PASS by inspection.** All 3 surviving log lines are inside
  `if (kDebugMode)` blocks; the 3 PII body-log lines were DELETED outright (not just gated),
  so a release build emits nothing from these sites regardless. No release build required.

- **AC6 (automated backstop): PASS.** Source-pin test +6/6 green; flutter analyze api_client.dart 0 issues.

## Verification counts
API Body in logcat: 0 | API Body in VM log: 0 | full Bearer tokens anywhere: 0 | customer PII tokens on flutter tag: 0

VERDICT: PASS
