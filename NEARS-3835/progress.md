# NEARS-3835 [8] QA progress (fix_cycle 0)
- AC1 PASS — validate valid:true 3/3 pass; place 200 order_ids 91419/91420/91421; orders.module_id = store module (1/2/3); order_details each own-store (ac1-*.txt)
- AC2 PASS — mixed group 3f88ac9a… module_id NULL; live non-mixed (12+13, header 2) group 78dda53c… module_id=1 store-derived (ac2-nonmixed-place.txt) + test (c)
- AC3 PASS — pharmacy detached: validate 55 pass:false module_unavailable_in_zone, 12/51 pass:true; place 403 group_gate, counts 184/17/196 unchanged; flag OFF -> empty_cart for 51/55, no module_unavailable_in_zone; fixture restored
- AC4 PASS — all 3 children order_note 'QA3835 group note'
- AC5 PASS — mixed validate/place 0 mismatch lines; non-mixed foreign-header validate+place 2 mismatch lines each; single-store place with smuggled body field still logs
- AC-LOG PASS — WARN line keys: endpoint, store_id, module_id, zone_id, reason, request_id (+trace_id, correlation_id)
- AC-REG PASS — GroupOrderPlacementTest (unmodified) 8/8; flag-OFF live validate 12+13 valid:true, 0 log lines
- AC-TEST PASS — 111 tests / 595 assertions OK
- REG sweep clean — single-store place 200 (order 91436); group/details 200
