# NEARS-3856 QA [8] progress (cycle 0)

Backend: /Users/Apple/Projects/nears-NEARS-3856-backend-logging/Admin (own `php artisan serve --no-reload`, :8356) @ 7a8d37825, DB `multi_food_db_qa3856` (private copy, dropped after the run). Freshness check: PASS.

- AC-TEST PASS: Nears3856BackendLoggingGapsTest 40/40 (816 assertions).
- AC-REG PASS: Nears3835GroupCrossModuleTest 12/12, Nears3830ModuleFromStoreTest 13/13, Group|Cart|Nears383|GroupPayment|OrderPaymentFailed|BuyNowOrderIdempotencyTest 352/352. Orders count 179 before and after the live run, so no order was placed.
- AC1 PASS: at LOG_LEVEL=warning, R1/R2/R4/R5/R6/R8/R10/R11/R12 each wrote their line (grep by X-Request-Id UUID; payment-mobile also by endpoint+timestamp). At LOG_LEVEL=error, R16 wrote the [FAIL] and dropped the [WARN]; R17 wrote nothing.
- AC2 PASS: keys in the 18 captured lines are all on the allow-list (plus trace_id/correlation_id from middleware). Zero hits for the guest contact values, lat/lng, guest_id, token or message.
- AC3 PASS (phpunit only): the registration-mail and notify-dispatch cases write [ERR] and return 200. Not forced live because that needs a successful order, which sends a real FCM push.
- AC4 PASS: R4 (flag OFF) wrote the base [WARN]. R14 (flag ON, warning level) wrote no mismatch WARN. R15 (flag ON, info level) wrote [INFO] with the same keys.
- B1 PASS: R5/R16 wrote `endpoint":"api/v1/customer/order/place"`.
- Positive control PASS: R3 cart add returned 200 and wrote no log line.
- Row 4 drop PASS: R9 group/validate returned 200 and wrote no `group order rejected` line (only the existing producer cause line).
