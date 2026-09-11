# Scenario 2: admin first-contact (no receiver_id sent)

Request: POST /api/v1/customer/message/send  receiver_type=admin  (no receiver_id field)
Response: HTTP 200, conversation.receiver_id=0 (sentinel), receiver_type="admin"

DB verify: SELECT id, sender_id, receiver_id, receiver_type FROM conversations WHERE id=71;
  -> 71 | 124 | 0 | admin
