# NEARS-4276 QA [8] cycle 1 (re-QA, full) - tested_sha d2b8921dd
- 11:13 baselines: orders 179/91415; 32 multi_food_db_qa% DBs (identical to cycle 0); no nears-qa-nightly_* worktree; no qa-locks; crontab empty
- AC2 control branch qa/NEARS-4276-ac2-broken-label = d2b8921dd + 5201fc30d (en.json edit_profile -> "Edit Profile QA4276"); temp worktree removed
- 11:14 base run launched: --ref feat/NEARS-4276-maestro-nightly, worktree script copy, real primary Admin/.env
- 11:16 .env guard PASSED on real primary .env: copied tree .env line 152 is a comment naming the shared DB (still present), line 21 DB_DATABASE=<clone>; tree HEAD d2b8921dd
- 11:38 BASE run rc 0 status PASS, 6 rows PASS + control CONTROL OK, 7/7 self_check pass, teardown 9/9 ok; each row gate CLEAN err_fail=0 with 'suppressed N x ... token update' (N=1 per row, 4 in order-tracking w/ 4 app pids); independent logcat grep 0 FAIL/ERR outside the 5 noise entries; independent AC3 reads clean (orders 179/91415, 32 qa DBs identical, 0 nightly trees, no locks, emu gone, cred grep 0 w/ positive control 1)
- 12:01 AC2 run rc 1 status FAIL reason 'a flow failed', sha 5201fc30d; pilot/01-login FAIL (JUnit FAIL, wrapper 'FAIL (a flow failed)', Maestro: assertVisible "Edit Profile" FAILED = 01-login.yaml:14; :13 My Orders COMPLETED); other 5 rows PASS; control CONTROL OK; 7/7 legs pass; teardown 9/9 ok; every row gate CLEAN err_fail=0
- 12:20 BLOCKED run rc 2 status BLOCKED (env file missing), nothing left; suites 335/51/277/89 PASS; AC2 branch + env file deleted; cycle-1 evidence assembled + credential-swept 0
