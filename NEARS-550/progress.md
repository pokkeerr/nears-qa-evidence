# NEARS-550 QA progress — guest cashback [] hardening

Device: emulator-5556 | branch feat/NEARS-550-guest-cashback-500 @ 236f42cb | base 0c2caecf
Build: freshly built from worktree (app-debug.apk, directory=nears-NEARS-550-guest-cashback-500/UserApp)
Fix cycle: 0 (first QA) | light mode (dark deferred)

- AC1 (guest device) PASS — logged out -> Guest User; Home + Food + Grocery modules load; NO "Something went wrong" toast; no crash; no runtime errors. Logs: guest path has NO /api/v1/cashback/list call (NEARS-633 isLoggedIn gate). Evidence ac1-guest-home.png, ac1-guest-grocery.png
- AC2 (service []-not-throw) PASS — 10/10 unit cases green (401/500/null/non-list/happy at repo+service). Live proof: guest home no crash. Evidence: test run + ac1 shots
- AC3 (curl guest 401) PASS — with Accept: 401 Unauthenticated (matches DoR); without Accept: 302 redirect; never 500 in either. Evidence ac3-guest-curl.log
- AC4 (authed regression) PASS (empty-parity) — authed user, Food+Grocery home load, /api/v1/cashback/list -> [200] empty (no offers seeded), no FAB (expected, data-unverifiable for "sees offers"), no crash, no runtime errors. Evidence ac4-authed-home.png, ac4-authed-grocery-cashback200.png
- Security qa_point — 401->refresh->logout path is api_client._send (NEARS-65), UPSTREAM of repo getList; repo []-hardening cannot bypass it; diff touches only home_repository.dart. Best-effort code-path verify + guest-401 curl.
- Automated backstop: flutter test (worktree UserApp) = 1658/1658 passed.

Verdict: PASS
