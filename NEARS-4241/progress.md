# NEARS-4241 QA (fix-cycle 0) - backend-only, own servers, throwaway clone multi_food_db_qa4241
Fix server: php -S 127.0.0.1:8741 from worktree @ 0076db3f5 | Base server: 127.0.0.1:8742 from primary tree @ b3315bc2e | both DB_DATABASE=multi_food_db_qa4241 (proved by the clone-only schedule edit changing both servers' output)
AC1 PASS: fix top_rated=[21(4.2 open),19(3.4 open),35(5.0 closed)] vs base [35,21,19]
AC2 PASS: all/nearest/fastest/popular/newly_joined bodies identical fix vs base (host URL keys stripped) - ac2-store-types.txt
AC3 PASS: ties by id (12,13,20 open 4.0; 14,35 closed 5.0), limit=2 walk 7 unique ids no dup/drop - ac3-page-walk.txt
AC4 PASS: all_stores_default_status=0 -> fix == base pure rating then id [14,35,21,12,13,20,19]; flip back to 1 -> open-first again - ac4-default-status-0.txt
AC5 PASS: phpunit 150 tests / 2535 assertions OK; fixture diff only default_top_rated (+one leading open desc) - ac5-*.txt
AC6 PASS: get-data filter=nearby store_type=all: closed store 35 at distance 0 ranks after 12 open stores, identical fix vs base (no change, by design) - ac6-nearby.txt
Sweep: popular/latest/recommended/top-rated/discounted/legacy filter[]=top_rated/with_filters all|popular|newly_joined identical; get-data & get-combined-data & with_filters top_rated changed (intended) - regression-sweep.txt
BE log: 0 production-channel lines during live run.
