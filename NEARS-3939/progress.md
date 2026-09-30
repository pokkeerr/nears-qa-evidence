# NEARS-3939 QA progress (phase 8, fix-cycle 0)

Build 61f53dd99 (worktree fix/NEARS-3939-group-payment-server-total), emulator-5554, pkg com.izzes.nears.nears_nears_3939_group_payment_server_to.
Backend: /Users/Apple/Projects/nears @ bb4fc8927 (Admin byte-identical to base 59f8edffd), port 8139, DB nears_qa_3939 (cross_module_basket id=228 -> 1 on copy only). Logging proxy :8140 -> :8139 (money fields only, payment_token redacted).

- AC1 PASS: group digital #91418/#91419 (group c50abd70-...). Client checkout total 31.88; group/place total_amount 34.28; DB SUM(order_amount) by order_group_id 34.28; PaymentScreen delivery-quote order_amount 34.28 (route amount); gateway intent payment_requests 34.28 attribute=order_group, unpaid. Logs clean (0 [FAIL]/[ERR]).
- AC2 PASS: live normal digital group placement emits 0 'group placed amount fallback' lines; the fallback branch is pinned by group_place_server_amount_test.dart (9/9), which asserts groupId + reason + rid, no body marker, no payment_token.
- AC3 PASS: route amount 34.28 == group total_amount, != either child (28.40 / 5.88).
- AC-REG PASS: single-store digital #91420, client 26.00, place total_ammount 28.4, delivery-quote order_amount 28.4, DB 28.40, intent 28.40, purchase value 28.4. Logs clean.
- Scope 4: group COD #91423/#91424 -> group tracking (track?order_id=91423 + group/details), no payment route, no fallback line.
- Backstop: flutter test test/features/checkout/ test/helper/analytics_service_test.dart -> 957 passed.
