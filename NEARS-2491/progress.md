# NEARS-2491 QA progress

Device: emulator-5566 (Android, light mode only). App: UserApp, worktree
`nears-NEARS-2491-clearshareddata-header-reset`, commit aa3f3fe3. Backend:
primary-tree `php artisan serve` on :8000 (pid 96814), reached via 10.0.2.2:8000.

- AC1 (invalidation POST carries valid Authorization, no stale moduleId/zone):
  MET. Unit test `clear_shared_data_header_reset_test.dart` captures the exact
  `headers` Map passed to `ApiClient.postData` for the real
  `AuthRepository.clearSharedData()` code path — Authorization ==
  `Bearer old-account-bearer`, no `moduleId` key. Live: logcat
  `endpoint=/api/v1/customer/cm-firebase-token http_status=200` immediately
  post-logout (account had Pharmacy module + zone 2 active). True wire-level
  packet capture NOT available in this sandbox (no root -> tcpdump permission
  denied; no mitmproxy/Charles installed) — noted as a gap, code-level capture
  used as the best-available proxy since Dart's http.Client sends exactly the
  Map passed to `postData(headers:)`.
- AC2 (guestLogin POST carries neither stale moduleId/zone nor departing
  bearer): MET. Same unit test's 2nd case proves the header-reset
  (`updateHeader`) runs before BOTH the invalidation POST and guestLogin's
  POST — guestLogin() takes no headers override so it inherits the already-
  reset `_mainHeaders` (no bearer, no moduleId). Live: logcat
  `endpoint=/api/v1/auth/guest/request http_status=200` right after the
  invalidation call.
- AC3 (invalidation POST still 2xx, not 401): MET. Live logcat status=200.
  Backend laravel.log has a history of `[FAIL] OAuthServerException` at this
  exact endpoint at other timestamps (evidence the failure class this fix
  targets is real) but NONE at this session's timestamp (17:41:47-48 UTC+4).
- AC2-static (no crash, subsequent guest browse zone-less/module-less): MET.
  Zero `[FAIL]`/`[ERR]`/exception lines in the full session logcat. Post-
  logout Profile == "Guest User"; post-logout Home == "Select Your Location"
  (address cleared) + un-scoped module tiles (no "Good evening, James"
  bleed-through).
- Regression sweep (non-default module/zone login -> logout -> fresh
  login/guest browse): MET. Logged in james.wilson@demo.com, zone_id=2 (Abu
  Dhabi, non-default), Pharmacy module selected. Logout clean, no crash.
  Guest browse of Grocery & Food module: all 200s (one expected 404 on
  `get-zone-id` — no address set post-logout, not a regression). Fresh
  re-login: 200, Profile correctly shows "James Wilson" again.
- Automated backstop: `flutter test test/features/auth/` — 358/358 PASS.
  Full `flutter test` run in background for broader regression sweep.

Evidence: `docs/qa-evidence/NEARS-2491/logout-and-relogin-net-log.txt` (scoped
logcat NET excerpt), `docs/qa-evidence/NEARS-2491/ac5-fresh-relogin-profile.png`.

Verdict: PASS.
