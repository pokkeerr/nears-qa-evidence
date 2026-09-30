# NEARS-3939 QA progress (phase 8, fix-cycle 0)

Build 61f53dd99 (worktree fix/NEARS-3939-group-payment-server-total), emulator-5554, pkg com.izzes.nears.nears_nears_3939_group_payment_server_to.
Backend: /Users/Apple/Projects/nears @ bb4fc8927 (Admin byte-identical to base 59f8edffd), port 8139, DB nears_qa_3939 (cross_module_basket id=228 -> 1 on copy only). Logging proxy :8140 -> :8139 (money fields only, payment_token redacted).

- AC1 PASS: group digital #91418/#91419 (group c50abd70-...). Client checkout total 31.88; group/place total_amount 34.28; DB SUM(order_amount) by order_group_id 34.28; PaymentScreen delivery-quote order_amount 34.28 (route amount); gateway intent payment_requests 34.28 attribute=order_group, unpaid. Logs clean (0 [FAIL]/[ERR]).
- AC2 PASS: live normal digital group placement emits 0 'group placed amount fallback' lines; the fallback branch is pinned by group_place_server_amount_test.dart (9/9), which asserts groupId + reason + rid, no body marker, no payment_token.
- AC3 PASS: route amount 34.28 == group total_amount, != either child (28.40 / 5.88).
- AC-REG PASS: single-store digital #91420, client 26.00, place total_ammount 28.4, delivery-quote order_amount 28.4, DB 28.40, intent 28.40, purchase value 28.4. Logs clean.
- Scope 4: group COD #91423/#91424 -> group tracking (track?order_id=91423 + group/details), no payment route, no fallback line.
- Backstop: flutter test test/features/checkout/ test/helper/analytics_service_test.dart -> 957 passed.

# Fix-cycle 1 (delta re-QA on REBASED bytes d5d2c1793, base bb4fc8927)
Build: qa-run.sh --root <worktree> --dart-define API_HOST=10.0.2.2:8140, emulator-5554, fresh install 19:18:40 (pkg absent before); local app-debug.apk sha256 9125738699860d50 == on-device base.apk; worktree clean at d5d2c1793.
Backend: /Users/Apple/Projects/nears @ bb4fc8927, :8139 (freshness PASS), DB nears_qa_3939 proven via /config cross_module_basket=true (shared bs228=0). Proxy :8140 -> :8139.
- AC1 PASS: group digital #91427/#91428 (group 19a138bd-...). Client confirm-sheet total 31.88; group/place total_amount 34.28; DB SUM(order_amount) 34.28 (28.40+5.88); PaymentScreen delivery-quote order_amount 34.28; payment_requests 34.28 attribute=order_group is_paid=0. Logs clean, 0 fallback lines.
- AC-REG PASS: single-store digital #91429: place total_ammount 28.4; delivery-quote 28.4; DB 28.40; payment_requests 28.40 attribute=order; purchase value 28.4. Client total also 28.40 this run (non-divergent). Logs clean.
- Smoke (3933-touched single-store place path, Instant slot): placement 200 -> payment route, 0 [FAIL]/[ERR].
- AC2: group_place_server_amount_test.dart 9/9 on rebased tree; live 0 fallback lines. AC3 reused + re-observed (34.28 != 28.40/5.88).
- Backstop: flutter test test/features/checkout/ test/helper/analytics_service_test.dart -> 980 passed (957 + NEARS-3933's added tests).
- Regression candidate (pre-existing, not in diff): payment_failed_dialog Cancel Order cancels only the first child of a group -> bug-group-cancel-partial.log.
