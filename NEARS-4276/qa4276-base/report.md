# Maestro nightly (NEARS-4276): BLOCKED

- reason: the copied .env still names the shared DB
- ref: feat/human-qa-uiux @ ec800c90faef929e5938eb9fb3f42bff70d92bea
- serial: None (AVD None), backend port None, clone `multi_food_db_qa4276_20261020_091618_20198`
- wall: 7 s

| flow | verdict | wrapper rc | JUnit | note |
|---|---|---|---|---|

## Self-check (AC3)

- clone_name: pass - multi_food_db_qa4276_20261020_091618_20198
- shared_orders_unchanged: pass - orders COUNT/MAX 179/91415 before and after

## Teardown

- drop_clone: ok multi_food_db_qa4276_20261020_091618_20198
- remove_tree: ok /Users/Apple/Projects/nears-qa-nightly_20261020-091614-20198

Known egress: api.copilot.mobile.dev (TLS, about 6 KB per maestro test; accepted, blocking it is NEARS-4277)

nothing is published automatically: screenshots are never scrubbed (maestro-pilot.md §9.6); check them, then run a row's publish line by hand:

