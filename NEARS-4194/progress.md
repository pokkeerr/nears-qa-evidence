NEARS-4194 QA progress (HEAD d9350622d, fix_cycle 0). Own server :8194 from this worktree, clone multi_food_db_qa4194 (dropped), shared multi_food_db untouched (shared-db-before/after.txt).
AC1 PASS contract+doc | AC2 PASS | AC3 PASS | AC4 PASS | AC5 PASS (low note: free_delivery[]=1 / "1," accepted as ON) | AC6 PASS | AC7 PASS | AC8 PASS | AC9 PASS
AC10 PASS (no migration; cold p95 <=1.09x, warm p95 <=+2.9%) | AC11 PASS documented | AC12 FAIL (M9 cuisine predicate survives; M26 M27 M29 M32 survive) | AC13 PASS engine-level | AC14 PASS | AC15 PASS | AC16 PASS
Files: live-*.log (curl-level assertion transcripts), resilience-*.txt, killswitch-off-summary.txt, perf-*.json/txt, mutation-table.txt, phpunit-*.log, sort-regression-base-vs-head.txt, stampede-6-parallel-cold.txt, shared-db-*.txt

== fix_cycle 2 delta re-QA, HEAD 6fa4537d6 (verified) ==
Backend: /Users/Apple/Projects/nears-NEARS-4194-dynamic-filters-backend @ 6fa4537d6 (own server :8194, clone multi_food_db_qa4194 DROPPED, shared multi_food_db unchanged: shared-db-before/after-cycle2.txt)
AC12 PASS: 59/59 mutants KILLED, 0 survivors (mutation-table-cycle2.txt); M9 M26 M27 M29 M32 now RED; delta mutants D1-D9d killed
AC1 PASS: api-shapes.md:1331 matches live; 11-key set + filters keys {applied,counts_omitted,items,sort} unchanged (cycle2/live-contract.log 95/0, live-toggle-grammar-cycle2.log 35/0)
AC5 PASS: free_delivery[]=1 / "1," now OFF, scalar 1 ON; multi/CSV==array unchanged (cycle2/live-counts.log 157/0, live-grammar.log 48/0)
Regression: filter suite 198 tests / 1169 assertions green (phpunit-filter-suite-cycle2.log). Other ACs reused from cycle 0.
