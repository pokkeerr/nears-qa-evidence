# NEARS-3949 QA progress (cycle 0) — emulator-5660, build 7adc1abb5, backend :8103 nears_qa_3949
- AC-TEST PASS: 90/90 (row widget + latch + store_controller tests).
- AC-LOG: [FAIL] endpoint=/api/v1/stores/details/ http_status=403 msg="checkout: group store out of zone store_id=3168" correlation_id=79d35d2c-..., c3cf380f-..., f8598d3e-... (once per address switch); no 'store detail unresolved' line.
- AC1 FAIL: at address 60 store 3168 403 out_of_zone -> fee line renders RESOLVED "Dama baqala 0.00 AED, —" (no reason, no Edit Cart). Root: admin_free_delivery=free_delivery_to_all_store maps the -1 null-store sentinel to 0 -> unresolved=false.
- AC5 FAIL: Total resolved (17.00 AED); with store 13 leading, Place Order ENABLED at address 60 (bug-out-of-zone-place-enabled-lead13-mobile.png).
- AC-ADDR (request level) PASS: switch 60->45 re-fetches 3168 (200), line ETA "—" -> "30-40 min", Place enabled, stayed in checkout.
- AC4 (request level) PASS: coupon apply re-ran the group pipeline at the same address; no /stores/details/3168 request, no second [FAIL].
- Mixed basket: address switch to 60 -> group/validate out_of_coverage_area -> returned to Cart with 3851 card (Host A unreachable for logged-in mixed).

# Cycle 1 (HEAD 05aac208f, emulator-5660 = freshly booted Pixel_10_Pro AVD)
- AC-TEST PASS 96/96.
- Override ON (seed free_delivery_to_all_store): addr 60 -> Host B row "Dama baqala, This store doesn't deliver to your area, Edit Cart", no Retry; Delivery Fees "—"; Total "—"; Place disabled — 3168 lead AND 13 lead. Edit Cart -> Cart. [FAIL] once per switch (fe0cc3e6, a6a31afd).
- AC3 Host B: EN 320dp x1.3 Edit Cart 44dp, end edge 855 == amount end 855, reason wraps between words; AR default + 320x1.3 Edit Cart start 105 == amount start 105, 44dp. Wide EN + AR captured.
- Private-copy writes (nears_qa_3949 only): UPDATE business_settings SET value='0' WHERE id=120 (admin_free_delivery_status) -> config status False; UPDATE stores SET active=0/1 WHERE id=13 (x2 cycles) -> /stores/details/13 404 store_temporarily_closed; all restored (120=1, store 13 active=1), copy cache cleared with DB_DATABASE prefix.
- Override OFF: addr 60 row out_of_zone (no Retry), Fresh fee 1.00, Total unresolved, Place disabled (13 lead and 3168 lead).
- AC2 OFF: store 13 404 -> "حدث خطأ ما" + "أعد المحاولة" + Edit Cart; Retry re-requested /stores/details/13 (200) -> resolved, Place enabled at 45.
- AC4 live: at addr 60 with 13 transient + 3168 out_of_zone, Retry -> only /stores/details/13 re-requested, 0 requests for 3168, row kept.
- Host A unreachable: place_order_controller.dart:991-995 (NEARS-3851 AC9) returns to Cart for guest and logged-in mixed.
