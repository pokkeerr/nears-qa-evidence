# NEARS-3803 QA progress (cycle 0)
- AC1 PASS live: place/prescription 403 order_time; group/place 403 group_gate store_closed group_placed=false; group/validate 200 valid=false store_closed; counts unchanged
- AC2 PASS phpunit (test_e validate pass:true; GroupOrderPlacementTest Ac1 positive placement) — live positive skipped (would INSERT, rolled back, on multi_food_db)
- AC3 PASS live positive control store 35 (active=1, schedule-closed) 403 identical body, 0 log lines; phpunit test_f assertExactJson + 0 WARN
- AC4 PASS phpunit 18/18, 80 assertions
- AC5 PASS live: exactly one WARN event per rid, keys trace_id/correlation_id/endpoint/http_status/code/reason/store_id/request_id only
- AC6 PASS live d_future_schedule 403 order_time + phpunit test_d
