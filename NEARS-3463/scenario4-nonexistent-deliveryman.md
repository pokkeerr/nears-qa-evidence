# Scenario 4: delivery_man receiver_id that resolves to no real rider

Request: POST /api/v1/customer/message/send  receiver_type=delivery_man  receiver_id=999999
Response: HTTP 403  {"errors":[{"code":"conversation","message":"Not found"}]}

DB verify: messages.MAX(id) unchanged (125 before and after) -- no message row persisted.

BE log (Admin/storage/logs/laravel.log), grep -F "[FAIL]" | grep -F "delivery man unresolved":
[2026-09-11 14:24:25] production.ERROR: [FAIL] conversation messages_store: delivery man
unresolved for receiver_id lookup {"trace_id":"8b7121d9cb1e91cfc9dc7cf55ddadbd4",
"correlation_id":"f751a562-264d-450f-8a8c-480233a65a36","endpoint":"customer/message/store",
"receiver_id":"999999"}
