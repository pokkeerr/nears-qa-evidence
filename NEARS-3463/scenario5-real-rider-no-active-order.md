# Scenario 5: delivery_man resolves to a real rider (Carlos Rodriguez, id=3) but customer
# (Robert Taylor, user_id=5) only has TERMINAL orders with him (91125 refund_requested,
# 91127 returned) -- no active order.

Request: POST /api/v1/customer/message/send  receiver_type=delivery_man  receiver_id=3
Response: HTTP 403  {"errors":[{"code":"conversation","message":"Not found"}]}

diff against scenario 4's saved response body: BYTE-IDENTICAL (verified with `diff`, exit 0).
This confirms the no-enumeration-oracle guarantee live: an attacker cannot distinguish
"rider does not exist" from "rider exists but you have no active order with them" by
response shape.

DB verify: messages.MAX(id) unchanged (125) -- no message row persisted for this request either.
