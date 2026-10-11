# NEARS-4134 QA (cycle 0) - progress / evidence index

Backend (branch): /Users/Apple/Projects/nears-NEARS-4134-profile-login-remember-token @ e1d4835b5 (port 8134)
Backend (base, RED arm): /Users/Apple/Projects/nears-NEARS-4134-qabase @ 9af6f635e (port 8135, detached scratch worktree)
Same private clone for both: multi_food_db_qa4134 (dump of multi_food_db_test, 6 pending migrations applied). Same fixture, same requests, same walker.
DML grant used on the clone only: INSERT (Nears4120 seeder via its NEARS_SEED_ALLOW_DB override, employee_roles + vendor_employees rows by plain INSERT, conversation/message/user_info rows via real send endpoints), UPDATE (login_remember_token on vendor 2 and the QA employee; auth_token/passport via real login endpoints). No DELETE, no DDL beyond the worktree migrations.
Token values never printed or stored in evidence: lengths and sha8 only (all 60 chars). Files: keypaths_base_*.json, keypaths_branch_*.json (flattened key paths, [] = list element), keypath_diff.txt, qa_harness.py.

Fixture: owner vendor 2 (ahmed.khan@demo.com, store 2 live), QA employee 18 (store 2), customer 6, delivery man 1; conversations 223 (customer<->vendor), 224 (dm<->vendor), plus vendor-initiated rows.
