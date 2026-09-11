# Scenario 7: unrecognized receiver_type

Request: POST /api/v1/customer/message/send  receiver_type=bogus  receiver_id=4
Response: HTTP 403 {"errors":[{"code":"conversation","message":"Not found"}]}  -- NOT a 500/undefined-variable crash.

BE log: [FAIL] conversation messages_store: unrecognized receiver_type
