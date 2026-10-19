# NEARS-4213 QA progress (head dc9535ff4, cycle 0, device-free)
AC1 PASS - shared report read-only, checksum equal, own SELECTs reproduce counts, R re-derived
AC2 doc half PASS / owner-review clause UNVERIFIABLE (owner review pending)
AC3 PASS - twin apply/verify/rollback, checksums equal to shared
AC4 PASS (reshaped scope) - zone 3 report-only store still exposed (1 of 593)
AC5 PASS - log lines aggregate-only, fault injected at phase addresses aborts cleanly, refusals write zero rows
Regression: unrelated tower zones unchanged, 5 test files 53/53 green, no route diff
