# Maestro nightly (NEARS-4276): FAIL

- reason: a flow failed
- ref: feat/human-qa-uiux @ ec800c90faef929e5938eb9fb3f42bff70d92bea
- serial: emulator-5580 (AVD NEARS_2414_QA), backend port 8276, clone `multi_food_db_qa4276_20261020_091749_22522`
- wall: 1439 s

| flow | verdict | wrapper rc | JUnit | note |
|---|---|---|---|---|
| controls/02-browse-store-wrong-assert.yaml | CONTROL OK | 1 | FAIL | the control failed, as it must |
| pilot/01-login.yaml | FAIL | 1 | PASS |  |
| pilot/02-browse-store.yaml | FAIL | 1 | PASS |  |
| pilot/03-add-to-cart.yaml | FAIL | 1 | PASS |  |
| pilot/04-checkout.yaml | FAIL | 1 | PASS |  |
| pilot/05-order-tracking.yaml | FAIL | 1 | PASS |  |
| store/store-oos-listed-last.yaml | FAIL | 1 | PASS |  |

## Self-check (AC3)

- clone_config: pass - artisan config:show = multi_food_db_qa4276_20261020_091749_22522
- clone_name: pass - multi_food_db_qa4276_20261020_091749_22522
- marker_restored: pass - item 1 name + translations equal the shared read
- no_cloud_argv: pass - flow controls/02-browse-store-wrong-assert.yaml
- no_cloud_env: pass - no MAESTRO_*KEY/TOKEN variable for flow controls/02-browse-store-wrong-assert.yaml
- request_marker: pass - GET :8276/api/v1/items/details/1 returned the clone's marker
- shared_orders_unchanged: pass - orders COUNT/MAX 179/91415 before and after

## Teardown

- uninstall_app: ok com.izzes.nears.qanightly
- reverse_remove: ok tcp:80
- account_release: ok customer_a
- stop_server: ok pid 71652
- stop_emulator: ok pid 71830
- lock_release: ok emulator-5580
- drop_clone: ok multi_food_db_qa4276_20261020_091749_22522
- delete_env_copy: ok 
- remove_tree: ok /Users/Apple/Projects/nears-qa-nightly_20261020-091745-22522

Known egress: api.copilot.mobile.dev (TLS, about 6 KB per maestro test; accepted, blocking it is NEARS-4277)

nothing is published automatically: screenshots are never scrubbed (maestro-pilot.md §9.6); check them, then run a row's publish line by hand:

    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-092036-78385 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-base-x/evidence/01-02-browse-store-wrong-assert
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-092220-81957 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-base-x/evidence/02-01-login
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-092323-84208 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-base-x/evidence/03-02-browse-store
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-092509-87851 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-base-x/evidence/04-03-add-to-cart
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-092709-94511 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-base-x/evidence/05-04-checkout
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-092925-98906 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-base-x/evidence/06-05-order-tracking
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-093421-11184 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-base-x/evidence/07-store-oos-listed-last
