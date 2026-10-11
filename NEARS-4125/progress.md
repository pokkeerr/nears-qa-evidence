# NEARS-4125 QA progress (fix_cycle 0)
AC1 PASS fixed 12/12 runs (A/B x N=2/5 x3), base RED (A: 6/6, B: N=2 2/3, N=5 3/3)
AC2 PASS fixed 12/12 (N=2 bal50, N=5 bal100, shared + own session), base both-succeed
AC3 PASS UI + curl, renew + shift, toasts, redirect subscriberDetail
AC4 PASS doc/catalog/index/out-of-scope/S4 row, 12 file:line spot-checks
AC5 PASS positive control 24 refused lines joined by X-Request-Id, 0 on successes
AC6 PASS 74/74 fixed, base 18 RED / 10 green
See qa-run-record.txt, bug-*.log
