# NEARS-4118 QA progress (tested sha 35c65f0796f8773260d3a1c6273a12978dcd22ea, cycle 0)

Surface: BACKEND HTTP only, device-free (no emulator, no device lock, no DeliveryApp run).
Own server: `php -d pcre.jit=0 artisan serve --no-reload --host=127.0.0.1 --port=8118` from the worktree, DB_DATABASE=multi_food_db_qa4118 (private clone of multi_food_db; the dump only READ it). pid 95053, cwd = worktree, head 35c65f079 (backend-freshness-check.sh 8118 = PASS).
All orders staged through product routes (customer cart/add + order/place + order/offline-payment, Admin panel order/status, add-delivery-man, order/offline-payment verify/deny, store toggle-settings-status, business-settings update-dm / update-order / update-payment-setup, customer wallet add-fund). No DML, no migrate/seed.
Couriers (credentials per users_test_data.md): dm2 david.miller, dm3 carlos.rodriguez (zone 1, vehicle NULL), dm1 ali.hassan (zone 2, vehicle 2), dm4 d@d.d (zone 1, vehicle 2). Real login route /api/v1/auth/delivery-man/login.
Settings changed on the CLONE only (via Admin routes): dm_maximum_orders 2 -> 10 (briefly 1 for the 405 demo), canceled_by_deliveryman 0 -> 1, partial_payment_status NULL -> 1 (method both), order_confirmation_model store <-> deliveryman (left at deliveryman).

Staging recipes that worked (reachable shapes after NEARS-4107):
- customer digital_payment order is placed `failed` + unpaid (order_status failed, method digital_payment); Admin order/status can then move it to pending / confirmed / processing / handover (4107 gates only offline) -> unpaid-digital at every claimable status.
- Admin order/status order_status=failed on a COD order -> failed COD.
- stale assignment: Admin add-delivery-man on a failed/pending digital order (allowed), then customer PUT order/offline-payment flips it to pending + offline row pending while the courier assignment stays -> update-order-status sees an unverified offline order.
- confirmed + offline row `denied`: customer submit -> Admin verify=yes -> Admin verify=no (deny route has no status gate) -> the only reachable "confirmed + unverified offline" shape; re-verify gives the positive control.
- partial: partial_payment=1 with wallet funded via Admin add-fund (< order amount); COD remainder ships confirmed/partially_paid; offline remainder ships `failed` pre-submit.

Order ids per AC: see ac_table in the ticket comment. Files in this folder are named by AC (ac1-*, ac2-*, ac3-*, ac4-*, ac6-*, ac7-*, probe-*, ctl-* = control/admin staging, stage-* = admin staging). Each courier file holds request, HTTP, body and the laravel.log lines for the sent X-Request-Id; tokens redacted.

Live results are summarised in the Jira QA comment and ac5-log-audit.txt (all [WARN] courier order refused lines since server start: key set, one-per-refusal, correlation_id == sent X-Request-Id; zero on every HTTP 200 control).
