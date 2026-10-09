# NEARS-4088 QA progress (cycle 0)
Backend: /Users/Apple/Projects/nears-NEARS-4088-offline-payment/Admin @ c5d994daf, port 8188, DB clone multi_food_db_test_nears_4088 (clone vanished once at start, recreated via setup_test_db.sh --clone nears_4088; method 4 re-inserted from multi_food_db copy, business_settings offline_payment_status=1, zone1 offline_payment=1 set on clone)
AC1 PASS (curl): 999/deactivated -> 403 method_id, ar message OK, abc/array/missing -> 403 validator, no rows/order change, precedence 'order' on delivered
AC2 PASS: missing/""/"   "/[x]/null -> 403 transaction_id; ar text OK
AC3 PASS: 200 {payment:success}; payment_info {method_id,method_name,transaction_id}, method_fields 2 fields, order offline_payment/pending
AC4 PASS: 7 malformed variants 200 + offline_payment object; 1 WARN each scoped by X-Request-Id; healthy 0 WARN; no row -> null
AC5 PASS: key sets match docs; method 90 no fields -> [] ; method 91 optional omitted OK
AC7 PASS: 5 unresolvable variants -> 403 method_id, rows/order/user_notifications unchanged, WARN refused order_id+reason only; healthy 200 (+notification positive control); deactivated editable 200; foreign order 403 order
Probe verified: PUT offline-payment-update on verified row -> row verified->pending, proof overwritten, order stays payment_status=paid/processing (desync)
Regression: admin offline list 200, order view healthy 200; PRE-EXISTING admin order-view 500 on payment_info NULL / '"x"' (blade foreach json_decode), unchanged blade
AC6 PASS (device emulator-5554, build c5d994daf, pkg com.izzes.nears.nears_nears_4088_offline_payment): placed order 91804 via app offline Bank Transfer, submit 200, detail shows Seller Payment Info + My Payment Info; edit dialog update 200; method_fields NULL / payment_info [] / method_fields '{bad' -> detail renders, no exception, no [FAIL]; unresolvable stored method (777) edit -> 403, 'Payment Failed' toast, exactly one [FAIL], row untouched, BE [WARN] refused method_missing
Env notes: php -S segfaults rc=139 ~1/min (restarted by loop); socket [FAIL]s at those instants are environmental
