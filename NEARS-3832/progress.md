# NEARS-3832 [8] QA progress (fix_cycle 0, device-free backend ticket)

Backend: /Users/Apple/Projects/nears-NEARS-3832-cancel-restock @ 9b58065bf (own `php artisan serve` :8132, backend-freshness-check PASS)
DB backup: /Users/Apple/nears-db-backups/multi_food_db_pre_NEARS-3832_qa_20260929023331.sql

| AC | Status | Evidence | Logs |
|---|---|---|---|
| AC1 customer, credit | PASS | order 91408 module_id=2 (food, stock=false), store 1 grocery, item 40 x2: 96 -> 94 at place -> 96 after cancel | clean |
| AC1 customer, no credit | PASS | order 91409 module_id=1 (grocery, stock=true), store 39 food, item 389 x1: 80 -> 80 -> 80 after cancel | clean |
| AC1 admin, credit | PASS | order 91411 module_id=2, item 40 x3: 96 -> 93 -> 96 via POST /admin/order/status (302, toastr success, canceled_by=admin) | clean |
| AC1 admin, no credit | PASS | order 91412 module_id=1, item 389 x2: 80 -> 80 -> 80 via admin status | clean |
| AC2 | PASS | group 30ba64b6 (91413 store 1 grocery item 40 x4, 91414 store 39 food item 389 x1): cancel 91413 -> item 40 92 -> 96; 91414 still pending, detail updated_at unchanged, item 389 80 | clean |
| AC-LOG | PASS | phpunit (e) restock_target_missing + (e2) module_config_missing: exact allow-list key sets, cancel 200; live normal cancels emitted 0 restock warnings | clean |
| AC-REG | PASS | order 91410 module 1 == store module, item 40 x1: 96 -> 95 -> 96; re-cancel 409, stock stays 96 (also re-cancel 91408 409) | clean (409 path has no Log:: line, pre-existing) |
| AC-TEST | PASS | phpunit 13/13, 71 assertions | n/a |

Stock net zero: item 40 96 -> 96, item 389 80 -> 80, item 16 0 (not touched).
