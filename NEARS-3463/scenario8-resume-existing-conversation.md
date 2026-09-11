# Scenario 8: existing-conversation resume (conversation_id present)

Request: POST /api/v1/customer/message/send  conversation_id=70  (vendor conversation from scenario 1)
Response: HTTP 200, conversation.id=70, receiver_id=114, receiver_type="vendor" -- unchanged, correct routing preserved.
