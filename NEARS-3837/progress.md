# NEARS-3837 QA progress (fix-cycle 0)

- AC1 PASS — flag ON: 403 prescription_required on new-row + re-add, user + guest; carts unchanged; WARN line logged per rejection. logs: clean (expected WARN only)
- AC-LOG PASS — WARN context keys exactly endpoint,status,code,item_id + shared trace_id/correlation_id; no user/guest id; correlation join proven (3837a1b2-…)
- Extra scope PASS — ar message exact; active=0 store -> prescription_required; 404/store_closed/out_of_zone/cart_item_limit unchanged
- AC-REG PASS — flag ON non-Rx 200, ItemCampaign 200; flag OFF Rx add 200 row written, response == base (0 non-env diffs), re-add increments, guest add 200
- AC2 PASS — flag OFF Rx cart, place w/o attachment -> 403 code prescription, no order
- AC3 PASS — prescription/place flag ON -> order 91416 prescription_order=1, 0 details, carts untouched
- AC-TEST PASS — 69 tests / 328 assertions OK (1 PHPUnit deprecation, pre-existing)
- AC-DOC PASS — api-shapes.md + cross-module-basket.md §S10 match code
