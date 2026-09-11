# Scenario 3: delivery_man with owned active order (Robert Taylor user_id=5 -> delivery_man id=2, order 91124 status=handover)

Request: POST /api/v1/customer/message/send  receiver_type=delivery_man  receiver_id=2
Response: HTTP 200, conversation.receiver_id=127, receiver_type="delivery_man"

DB verify: SELECT id, sender_id, receiver_id, receiver_type FROM conversations WHERE id=63;
  -> 63 | 124 | 127 | delivery_man

Note: a conversation already existed between this pair from prior activity, so this
request landed on the "resume" branch inside the no-conversation_id code path (the
authorization check -- owns_active_order_with_delivery_man -- is NOT cached, it is
re-evaluated on every request regardless of whether the conversation row already
exists), so this is still a live, meaningful demonstration of the active-order gate.
Order 91124 (user_id=5, delivery_man_id=2, order_status='handover' -- a non-terminal
status in the allowed set) is the seeded triple used (NEARS-2259 seeder).
