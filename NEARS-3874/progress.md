# NEARS-3874 QA (cycle 0) - progress / evidence index
Backend: /Users/Apple/Projects/nears-NEARS-3874-parcel-module @ 0794251ec on :8113, private DB multi_food_db_qa_bug3874 (marker business_name=QA3874COPY proven via /api/v1/config; push creds blanked on the copy).
Per-request BE excerpts: be-log-excerpt.log. Device: ac6-failed-order-module-message.png + fe-fail-line.log.

AC1 A 203 order_amount/cod_cap (aaaa0001, hdr 10, no pivot); hostile hdr 203 (aaaa0002); slug hdr 203 (aaaa0003) - orders count unchanged
AC1 B 203 (bbbb0001) with hdr 10 given a zone-2 NULL-cap pivot (row 289 inserted on copy)
AC1 C 200 orders.module_id=5 for hdr 10 (91416), absent (91418), module slug (91419)
AC1 D base delivery 5.00 -> 10.00 after surge 5.00 on module 5 (+9.00 surge on module 10 ignored) (91417)
AC2 403 {errors:[{code:module,message}]}: place (dddd0001), prescription (eeee0001), group flag OFF (ffff0002, group envelope code group_gate/reason module_unavailable_in_zone), sub_self_delivery (aaab0001), inactive module w/ pivot (aaab0002), parcel module inactive (aaad0001/2); all_zone_service exempt 200 (aaac0001, order 91421); zone 3 no parcel pivot -> code zone (aaae0001)
AC3 zone-1 store 1 order 200 (91422); phpunit 191 OK
AC4 keys endpoint/store_id/zone_id/module_id/reason/request_id (+ middleware trace_id/correlation_id); hostile text absent
AC6 device: emulator-5570 UserApp shows 'Selected module is not available in this zone.'; Try Again and Back to Home both live; FE [FAIL] correlation_id joins BE request_id
