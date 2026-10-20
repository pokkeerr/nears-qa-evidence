# Maestro nightly (NEARS-4276): FAIL

- reason: a flow failed
- ref: qa/NEARS-4276-ac2-broken-label @ 457e9d70db47c22e88e83c36a933aef39dde5ee0
- serial: emulator-5580 (AVD NEARS_2414_QA), backend port 8276, clone `multi_food_db_qa4276_20261020_094311_32403`
- wall: 1396 s

| flow | verdict | wrapper rc | JUnit | note |
|---|---|---|---|---|
| controls/02-browse-store-wrong-assert.yaml | CONTROL OK | 1 | FAIL | the control failed, as it must |
| pilot/01-login.yaml | FAIL | 1 | FAIL |  |
| pilot/02-browse-store.yaml | FAIL | 1 | PASS |  |
| pilot/03-add-to-cart.yaml | FAIL | 1 | PASS |  |
| pilot/04-checkout.yaml | FAIL | 1 | PASS |  |
| pilot/05-order-tracking.yaml | FAIL | 1 | PASS |  |
| store/store-oos-listed-last.yaml | FAIL | 1 | PASS |  |

## Self-check (AC3)

- clone_config: pass - artisan config:show = multi_food_db_qa4276_20261020_094311_32403
- clone_name: pass - multi_food_db_qa4276_20261020_094311_32403
- marker_restored: pass - item 1 name + translations equal the shared read
- no_cloud_argv: pass - flow controls/02-browse-store-wrong-assert.yaml
- no_cloud_env: pass - no MAESTRO_*KEY/TOKEN variable for flow controls/02-browse-store-wrong-assert.yaml
- request_marker: pass - GET :8276/api/v1/items/details/1 returned the clone's marker
- shared_orders_unchanged: pass - orders COUNT/MAX 179/91415 before and after

## Teardown

- uninstall_app: ok com.izzes.nears.qanightly
- reverse_remove: ok tcp:80
- account_release: ok customer_a
- stop_server: ok pid 81786
- stop_emulator: ok pid 81959
- lock_release: ok emulator-5580
- drop_clone: ok multi_food_db_qa4276_20261020_094311_32403
- delete_env_copy: ok 
- remove_tree: ok /Users/Apple/Projects/nears-qa-nightly_20261020-094306-32403

Known egress: api.copilot.mobile.dev (TLS, about 6 KB per maestro test; accepted, blocking it is NEARS-4277)

nothing is published automatically: screenshots are never scrubbed (maestro-pilot.md §9.6); check them, then run a row's publish line by hand:

    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-094558-88370 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-ac2-x/evidence/01-02-browse-store-wrong-assert
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-094742-91886 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-ac2-x/evidence/02-01-login
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-094903-94686 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-ac2-x/evidence/03-02-browse-store
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-095057-2226 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-ac2-x/evidence/04-03-add-to-cart
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-095252-5888 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-ac2-x/evidence/05-04-checkout
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-095507-10411 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-ac2-x/evidence/06-05-order-tracking
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-095923-20610 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-ac2-x/evidence/07-store-oos-listed-last
