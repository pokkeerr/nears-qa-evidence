# NEARS-4113 QA progress (checkpoint)
tested sha 4a1a0082056b1db607df01cb906898f57fbd17e4 · clone DB multi_food_db_qa4113 · own server php -S 127.0.0.1:8413 from worktree Admin/ (env DB_DATABASE override, SESSION_SECURE_COOKIE=false, OTEL off; worktree .env NOT edited, sha1 unchanged)
- AC1 PASS ac1-ac4-submitted-partial-offline.log (order 91416)
- AC2a PASS ac2a-non-partial-offline.log (order 91420) · AC2b PASS ac2b-ac2c-partial-switch-to-cod.log (91417) · AC2c PASS ac2c-cod-remainder-then-offline-submit-verify.log · AC2d PASS ac2d-replay-and-unauth.log
- AC3 PASS ac3-residual-rows.log (0 / 0)
- AC4 PASS (flow logs above)
- AC5 PASS phpunit 4113 class 9 tests/34 assertions OK; with 4107 filter 172 tests/2039 assertions OK
- extra: long method name ac2-unauth-and-long-method-name.log, contract-check-*.log, be-log-check.log, bug-switched-to-cod-submitted-partial-row-not-cod.log
