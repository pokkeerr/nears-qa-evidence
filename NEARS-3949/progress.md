# NEARS-3949 QA progress (cycle 0) — emulator-5660, build 7adc1abb5, backend :8103 nears_qa_3949
- AC-TEST PASS: 90/90 (row widget + latch + store_controller tests).
- AC-LOG: [FAIL] endpoint=/api/v1/stores/details/ http_status=403 msg="checkout: group store out of zone store_id=3168" correlation_id=79d35d2c-..., c3cf380f-..., f8598d3e-... (once per address switch); no 'store detail unresolved' line.
- AC1 FAIL: at address 60 store 3168 403 out_of_zone -> fee line renders RESOLVED "Dama baqala 0.00 AED, —" (no reason, no Edit Cart). Root: admin_free_delivery=free_delivery_to_all_store maps the -1 null-store sentinel to 0 -> unresolved=false.
- AC5 FAIL: Total resolved (17.00 AED); with store 13 leading, Place Order ENABLED at address 60 (bug-out-of-zone-place-enabled-lead13-mobile.png).
- AC-ADDR (request level) PASS: switch 60->45 re-fetches 3168 (200), line ETA "—" -> "30-40 min", Place enabled, stayed in checkout.
- AC4 (request level) PASS: coupon apply re-ran the group pipeline at the same address; no /stores/details/3168 request, no second [FAIL].
- Mixed basket: address switch to 60 -> group/validate out_of_coverage_area -> returned to Cart with 3851 card (Host A unreachable for logged-in mixed).
