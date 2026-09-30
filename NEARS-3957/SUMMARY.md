# NEARS-3957 live QA - group payment child-state gate (Backend, device-free, all ACs [api])

Code under test: worktree /Users/Apple/Projects/nears-NEARS-3957-group-payment-child-gate @ af83db583 (branch fix/NEARS-3957-group-payment-child-gate).
Backend: php artisan serve --no-reload on 127.0.0.1:8957 from that worktree's Admin/ (freshness check: PASS, cwd @ af83db583),
DB_DATABASE=multi_food_db_test_qa3957 (private clone of the test twin; shared multi_food_db never written: orders max id 91415, order_groups 15, business_settings id 228 = 0 before and after).
Groups were placed through the real API (POST /api/v1/customer/order/group/place as customer 6); state flips (failed/digital_payment, COD/partial rows, payment_requests rows for pre-fix fan-out) were private-DB SQL, as GroupPaymentTest does.
Gateway: stripe; only the 302 Location header was asserted (on-host /payment/stripe/pay?payment_id=...), never followed; no FCM/SMS/gateway call.

| Scenario | Result | Evidence file |
|---|---|---|
| S0 eligible group: 302 + exactly 1 payment_requests row, amount 13.00 = 4.00+9.00 | PASS | S0-S1.log |
| S1 token replay after success hook: 403 order-state, payment_requests count unchanged (1), children unchanged | PASS | S0-S1.log |
| S2 cancelled child: 403, count 0, callback NOT overwritten (still original) | PASS | S2-S4.log |
| S3 COD-switched child (cash_on_delivery): 403, count 0, child unchanged | PASS | S2-S4.log |
| S3b partial_payment child, unpaid order_payments row = cash_on_delivery: 403, count 0 | PASS | S2-S4.log |
| S3b-control same shape, remainder row digital_payment: 302, amount 11.00 (4-2 wallet + 9) | PASS | S2-S4.log |
| S4 delivered / processing / handover / picked_up child: 403 each, count 0, unchanged | PASS | S2-S4.log |
| S5 pre-fix paid row, delivered+COD+already-paid children + eligible sibling: only sibling confirmed; Log::error order_group_place_partial child_order_state / child_cash_selected / child_already_paid (ids only); replay idempotent | PASS | S5.log |
| S5b pre-fix paid row, processing/handover/picked_up children: unchanged, sibling confirmed | PASS | S5b-S6.log |
| S6 order_group_failed (twice): only pending-unpaid-digital sibling -> failed/stripe; COD pending, paid pending, COD-switched failed children unchanged | PASS | S5b-S6.log |
| S7 group:reconcile-stranded-payments: baseline 0; ineligible-only leftovers 0 (no partial log re-emitted); genuinely stranded 1 -> confirmed/paid, re-run 0; mixed (COD + eligible) 1, COD child untouched | PASS | S7.log |
| S8 X-Request-Id (uuid) on S2 request echoed in response and on the `[WARN] group payment rejected` log line; keys code,correlation_id,endpoint,group_id,http_status,order_id,reason,request_id; no token/PII | PASS | S8.log, laravel-log-excerpt.log |
| S9 live re-entry after REAL PUT customer/order/cancel: 403, still 1 row | PASS | S9-S11.log |
| S10 live re-entry after REAL PUT customer/order/payment-method (COD): 403; success fan-out on the earlier session leaves COD child pending/unpaid/cash_on_delivery, sibling confirmed; Log::error child_cash_selected | PASS | S9-S11.log |
| S11 token usable for retry after FAILED attempt: 302, 2nd row | PASS | S9-S11.log |
| Automated: Nears3957GroupPaymentChildGateTest + GroupPaymentTest 50 tests / 294 assertions OK; + Nears3902/Nears3856/PaymentTokenBinding/OrderPaymentFailedIdor/DeadControllerMethodGuard 91 tests / 1866 assertions OK | PASS | phpunit.log |

Notes: (1) a non-UUID X-Request-Id is not echoed by SetRequestId (server mints its own UUID); correlation was demonstrated with a UUID. (2) `correlation_id` appears on every `group payment rejected` line including pre-existing reasons (logging pipeline processor), not introduced by this change. (3) the laravel.log is shared with other sessions' phpunit runs (`testing.` channel lines) - the excerpt keeps only this run's `production.` lines.
