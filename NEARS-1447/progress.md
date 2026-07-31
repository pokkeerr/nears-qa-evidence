# NEARS-1447 QA progress (delta re-QA, fix cycle 2, re-scoped)

Build: worktree feat/NEARS-1447-fcm-token-logout-race · DeliveryApp · emulator-5556 · locale ar (RTL)
Fix confirmed in code: auth_repository.clearSharedData() no longer POSTs update-fcm-token (line 140 comment); updateToken() (login) still POSTs with fcm_token.

- AC1 [behav] logout fires ZERO update-fcm-token: PASS
  - 4 logout cycles: 0 update-fcm-token POSTs on any logout (FE [NET] log). laravel.log: 0 update-fcm-token lines, no 403 on endpoint.
- AC2 [behav] logout completes, lands sign-in, no toast, no crash, session cleared: PASS
  - All 4 logouts landed on sign-in ("أهلاً بعودتك"). No crash. One-time /profile poll [FAIL] on logout1 only (properly logged, no toast) — non-blocking, pre-existing race.
- AC3 [behav] login re-registers fcm token 200: PASS
  - 3 fresh logins + boot re-reg = 4 update-fcm-token POSTs, all http_status=200.

Evidence: signin-after-logout.png, login-succeeded-dashboard.png, bug-logout-profile-poll-throw.log
