# NEARS-4114 QA progress (phase 8)

Tested sha 41764e6b33806571ea9f817554dbe2cd0fbf666f (branch fix/NEARS-4114-preapproval-token-scope), base 8966ac24d. Own server 127.0.0.1:8414 from the worktree Admin dir, DB multi_food_db_qa4114 (copy of multi_food_db_test_nears4114). Backend freshness guard: PASS.

- AC1 PASS live: ac1-pending-token-sweep.log, ac1b-allowlist-and-log.log (101 refused auth-003 / 4 allowed, money counts identical, [FAIL] vendor.account_suspended joined by X-Request-Id).
- AC2 test-level only (no product route can create a model-none store0 vendor!=1 employee): Nears4114PreApprovalTokenScopeTest (owner+employee, 44 tests green).
- AC3 PASS live: ac3-business-plan-commission.log, ac3b-free-trial-pending-commission.log, ac3c-ac4a-post-approval.log (admin approval via Admin panel Approve button + update-application route).
- AC4 (a),(c) live: ac4a-approved-vendor-sweep.log (104 routes x2 approved tokens, 0 auth-003), ac3c log. (b) test-level (live unreachable without raw DML: see ac4b log).
- AC5: phpunit 252 tests / 4295 assertions green (4105 + 4103 + 4086 + 4114 classes, one run); live: free_trial hold + activation after admin approval in ac3b/ac3c.

Tokens and passwords are redacted; hashes in the logs are row digests, not secrets.
