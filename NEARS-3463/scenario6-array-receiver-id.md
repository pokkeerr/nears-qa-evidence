# Scenario 6: receiver_type=vendor / delivery_man with receiver_id sent as an ARRAY
# (?receiver_id[]=N style) -- this is exactly the bug fix-cycle 1 (commit 48b3050bf) closed:
# Vendor::find() on an array dispatches to findMany(), returning a truthy empty Collection
# that used to slip past the `!$vendor` guard and null-deref at ->stores (uncaught \Error, 500).

## vendor branch
Request: receiver_type=vendor  receiver_id[]=4
Response: HTTP 403 {"errors":[{"code":"conversation","message":"Not found"}]}  -- NOT a 500.
BE log: [FAIL] conversation messages_store: non-scalar receiver_id for vendor lookup

## delivery_man branch
Request: receiver_type=delivery_man  receiver_id[]=2
Response: HTTP 403 {"errors":[{"code":"conversation","message":"Not found"}]}  -- NOT a 500.
BE log: [FAIL] conversation messages_store: non-scalar receiver_id for delivery_man lookup

messages.MAX(id) unchanged across both calls -- no message row persisted for either.
