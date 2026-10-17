NEARS-4194 QA progress (HEAD d9350622d, fix_cycle 0). Own server :8194 from this worktree, clone multi_food_db_qa4194 (dropped), shared multi_food_db untouched (shared-db-before/after.txt).
AC1 PASS contract+doc | AC2 PASS | AC3 PASS | AC4 PASS | AC5 PASS (low note: free_delivery[]=1 / "1," accepted as ON) | AC6 PASS | AC7 PASS | AC8 PASS | AC9 PASS
AC10 PASS (no migration; cold p95 <=1.09x, warm p95 <=+2.9%) | AC11 PASS documented | AC12 FAIL (M9 cuisine predicate survives; M26 M27 M29 M32 survive) | AC13 PASS engine-level | AC14 PASS | AC15 PASS | AC16 PASS
Files: live-*.log (curl-level assertion transcripts), resilience-*.txt, killswitch-off-summary.txt, perf-*.json/txt, mutation-table.txt, phpunit-*.log, sort-regression-base-vs-head.txt, stampede-6-parallel-cold.txt, shared-db-*.txt
