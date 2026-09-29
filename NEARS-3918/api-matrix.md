# NEARS-3918 API matrix (AFTER only; before = proven at unit level)
Backend: /Users/Apple/Projects/nears-NEARS-3918-order-attachment @ b9f091120, port 8180, DB multi_food_db_qa_bug3918 (private copy). Host in URLs is APP_URL (http://localhost).

## Customer GET /api/v1/customer/order/details?order_id=N (user 6) -- all HTTP 200, X-Request-Id echoed
91157  raw [{"img":"2026-08-30-6a9441cd38f58.webp","storage":"public"}] -> ["http://localhost/storage/order/2026-08-30-6a9441cd38f58.webp"]  (rid 36fe9d7b-28dd-40f0-b796-53d671f1472f)
991001 raw null      -> []   (rid 407372e3-e366-4b7c-9965-9528ff825295)
991002 raw ["2026-08-30-6a9441cd38f58.webp"] (legacy list) -> 1 real URL (rid e38385b0-9dc7-470c-80d9-e7b35627e63b)
991003 raw {not-json -> []   (rid 9bcb1a74-a90a-4df5-9b4a-27c7d136aee7); no WARN on THIS endpoint: controller pre-decodes to null before the accessor
991004 raw 2 entries -> 2 real URLs (rid db1ae22f-3963-4f62-b759-c4baed674d8f)
991005 raw ""        -> []   (rid 0ba50d1a-8497-49e8-beaa-7e14e22a7052)
Customer B (emily.johnson) requesting 91157 / 991021 -> 404 "No query results for model [App\Models\Order]" (no URLs leaked)
Ordinary orders with order_details (91403, 91399) -> 200, array of detail rows (no order-level attachment key); 91405 parcel no attachment -> [].
File fetch: GET /storage/order/2026-08-30-6a9441cd38f58.webp -> 200 image/webp 8752 bytes.

## Lists (no row errors)
customer order/list rid 861a8747-b897-47c5-a36c-5d7af04b3fac: 200, 80 orders; 91157/991002 -> 1 URL, 991004 -> 2 URLs, 991001/991003/991005 -> []; exactly ONE `[WARN] order attachment unparsable {order_id:991003, reason:malformed_json}` (+ ambient trace_id/correlation_id) for that request.
customer running-orders rid d6bd308f-...: 200, 54 orders; 991021 pending + 991022 -> 1 URL; 991023 (malformed), 991024 (null), 91403 -> [].
NOTE: rows whose file is not on disk (91366, 91364, 91129, 91365) get Helpers::get_full_url's placeholder img2.jpg (existing helper file_exists behaviour), not a decode error.

## Vendor (vendor 40, store 42; header vendorType: owner)
current-orders / all-orders: 200; 991021/991022/991025/91157/991002 -> 1 URL, 991004 -> 2, 991001/991003/991005/991023/991024 -> [].
vendor/order?order_id=991021: 200, URL present. vendor/order-details: 200.

## Delivery man (token param)
dm2 (zone 1) latest-orders: 200; 991026 confirmed unassigned Rx -> real URL; 991027 malformed -> []; 991028 null -> [] (SEC: unassigned Rx orders visible to any zone DM -- existing behaviour).
dm2 current-orders / order?order_id=991025: 200, real URL. dm5 current-orders / order?order_id=991022: 200, real URL.
dm order?order_id=<someone else's> -> 204 No Content (scoped).
dm order-details?order_id=991025 -> 200 [] (details rows only).

## Logs
laravel.log since start of run: 0 lines matching "Undefined array key" / "[FAIL]" / production.ERROR|CRITICAL. 19 distinct (request,order) WARN lines, max 1 repeat per request+order, only for orders 991003/991023/991027 (the malformed fixtures).
