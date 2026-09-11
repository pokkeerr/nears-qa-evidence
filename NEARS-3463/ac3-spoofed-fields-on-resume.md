# AC3 direct demonstration: client-supplied receiver_id/receiver_type mismatching the
# actual resolved recipient is NOT silently trusted, for BOTH fields.

Request: POST /api/v1/customer/message/send
  conversation_id=70          (the REAL conversation: vendor, receiver_id=114)
  receiver_type=delivery_man  (SPOOFED -- attacker-supplied, does not match reality)
  receiver_id=999999          (SPOOFED -- attacker-supplied, does not match reality)

Response: HTTP 200, conversation.receiver_id=114, conversation.receiver_type="vendor"
  -- both spoofed fields IGNORED entirely; the server re-derives receiver_id/receiver_type
  from the conversation's own resolved recipient (conversation->receiver_id -> UserInfo ->
  ->vendor_id/->deliveryman_id/->admin_id), never from request input, on the resume path.

DB verify: SELECT id, sender_id, receiver_id, receiver_type FROM conversations WHERE id=70;
  -> 70 | 124 | 114 | vendor   (unchanged from scenario 1 -- confirms no mutation via spoof)
