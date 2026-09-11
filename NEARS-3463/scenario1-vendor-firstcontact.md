# Scenario 1: vendor first-contact (Robert Taylor, user_id=5, sender_id=124 -> vendor_id=4)

Request: POST /api/v1/customer/message/send  receiver_type=vendor  receiver_id=4 (Vendor.id, NOT UserInfo.id)

Response: HTTP 200
conversation.receiver_id = 114, conversation.receiver_type = "vendor"

DB verify (direct query, not trusting response):
  SELECT id, sender_id, receiver_id, receiver_type FROM conversations WHERE id=70;
  -> 70 | 124 | 114 | vendor

Proof of server-side derivation: client sent receiver_id=4 (the Vendor row's own id);
the PERSISTED conversation.receiver_id is 114 -- the UserInfo row's id, resolved via
UserInfo::where('vendor_id',4) -- NOT the raw client value. AC1 demonstrated live.
