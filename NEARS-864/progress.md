# NEARS-864 QA progress (fix-cycle 0)
- AC1 (PRIMARY): FAIL — debug APK built (exit 0) + installed on emulator-5554 + launched → FATAL crash, backend never reached.
  Cause: network_security_config.xml nested <domain-config> inside <debug-overrides> → XmlConfigSource$ParserException "Nested domain-config not allowed in debug-overrides" (line #8). Deterministic (crash-loops).
- AC2: met via merged-manifest inspection (aapt2) of built app-debug.apk — no usesCleartextTraffic, has networkSecurityConfig.
- AC3: intended scope correct (exactly 10.0.2.2 + 127.0.0.1, base cleartext=false) per packaged xml decode — but file never loads (AC1 crash).
- Finding NEARS-864-nsc-ip-literal-dart-policy: not refuted; superseded by launch-crash blocker; dart:io layer never reached.
- VERDICT: FAIL. Jira comment posted (id 12146). Evidence gallery published.

## Cycle-1 (fix @ e67e90a1) — RE-QA
- Rebuilt debug APK from worktree @ e67e90a1. NSC restructured: main src = base-config false only; src/debug overlay = base false + TOP-LEVEL domain-config (10.0.2.2, 127.0.0.1). No debug-overrides.
- AC2/AC3 re-confirmed on new packaged config (aapt2): no usesCleartextTraffic; base false + top-level domain-config scoping exactly the two loopback hosts.
- Blocker RESOLVED: app launches, no XmlConfigSource$ParserException / Nested domain-config, Application instantiates.
- Env note: worktree lacked google-services.json (gitignored) → AnalyticsService threw 'No Firebase App' aborting di.init() → stuck on splash. Copied primary-tree google-services.json (project nears-1d39b) into worktree as env bootstrap (gitignored, won't dirty tree). Rebuilt.
- AC1 PASS (live): [NET] GET /api/v1/config -> http_status=200 over cleartext to 10.0.2.2:8000. NONE of the dart:io signatures (Insecure HTTP / Invalid domain / CLEARTEXT not permitted). App advanced past splash to login screen.
- Finding NEARS-864-nested-domain-config-in-debug-overrides: RESOLVED.
- Finding NEARS-864-nsc-ip-literal-dart-policy: REFUTED (cleartext IP-literal request succeeded 200; dart:io did not reject).
- Regression: app boots + config loads + reaches login. Network stack intact.
- VERDICT cycle-1: PASS.
