# NEARS-3836 QA [8] cycle 0 — API-level live QA

Backend: /Users/Apple/Projects/nears-NEARS-3836-coupon-mixed-basket/Admin/public @ 20aba532b (php artisan serve :8736 --no-reload, DB_DATABASE=nears3836_qa private copy, LOG_LEVEL=info, MAIL_MAILER=log)
DB proof: copy-only business_settings.business_name='Nears QA3836 COPY' returned by GET /api/v1/config.
Copy prep: cross_module_basket=1, push_notification_service_file_content=NULL, mail_config.status=0, user 6 cm_firebase_token=NULL, store 51/55 schedule 00:00-23:59, coupons QA36* inserted. Log shows "FCM config missing - no project_id" on every place (no real push).

Files: <name>.json = response body (payment_token redacted), <name>.rid = X-Request-Id, *-db.txt = SELECT on the copy, *-log.txt = laravel.log grep by request id.

| AC | Verdict | Evidence |
|---|---|---|
| AC1 positive | PASS | ac1-validate/ac1-place: 12 (mod1) coupon_applied true 5.00, 51 (mod2) false 0; DB 51 coupon_discount_amount 0.00, coupon_code NULL; QA36FIX uses 0 -> 0 (validate) -> 1 (place) |
| AC1 negative | PASS | ac1neg-validate: both stores pass:false reason coupon; ac1neg-place 403 group_gate/coupon; orders 181/groups 16/uses 0 unchanged; WARN module_not_in_basket |
| AC2 | PASS | ac2-l1: validate +0, place 12+13+51 200 uses 0->1; replay 403 "Coupon usage limit over" uses stays 1; ac2-l1b (51,12,13) 200 uses 0->1; fixed budget shared: 12=5.00, 13=0.00 |
| AC2 percent (security ask) | PASS | pct-place: 12=1.20, 13=2.67, 51=0; discount_total 3.87; uses 0->1 |
| AC2 history | PASS | l2: place1 uses 1, validate2 valid, place2 uses 2, validate3 limit_exceeded |
| AC2 V1 | PASS | off-v1-place (flag OFF, 12+13, limit-2) uses +2; group stamp set NULL in copy; flag ON v1-validate -> 12 rejected "Coupon usage limit over" (counted 2, not 1) |
| AC2 first_order (f) | PASS | fo-place stores[51,12], limit = prior+1: 51 placed first, 12 discounted 5.00 |
| AC3 | PASS | per-store coupon_applied + coupon_discount_amount on validate stores[] and place orders[]; top coupon{code,applied_store_ids,discount_total}; nocoupon-validate keys = base |
| AC-LOG | PASS | 21 group-coupon lines over 27 request ids: 14 INFO module_mismatch, 3 WARN module_not_in_basket, 4 WARN limit_exceeded; call-site keys exactly coupon_id,group_id,reason,request_id; group_id null on validate; no code/amount/user |
| AC-REG | PASS | flag-OFF validate keys base; flag-OFF group place keys base, uses +2 per child; flag-OFF single place uses +1 code stamped; flag-ON same-module group keys base uses +2; /coupon/apply ON==OFF byte-identical |
| Security spoof | PASS | sec-single-wrongmod 403 coupon Not found (no skip); sec-single-uses +1; sec-group-uses +2, base keys |
| No moduleId header | PASS | nohdr-validate 200 with breakdown (no 403 group_order) |
| Rollback probe | PASS | rollback-place 12+53: 403 store_closed, orders/groups/uses unchanged |
| AC-TEST | PASS | phpunit filter suite 153 tests / 723 assertions OK; Nears3836 13/13 (a)-(j) |
