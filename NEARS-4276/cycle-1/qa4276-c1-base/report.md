# Maestro nightly (NEARS-4276): PASS

- reason: every flow passed, the control failed, every self-check leg passed
- ref: feat/NEARS-4276-maestro-nightly @ d2b8921dd0ca8f1e2df5604468d675f5b891cc7d
- serial: emulator-5580 (AVD NEARS_2414_QA), backend port 8276, clone `multi_food_db_qa4276_20261020_111338_16063`
- wall: 1417 s

| flow | verdict | wrapper rc | JUnit | note |
|---|---|---|---|---|
| controls/02-browse-store-wrong-assert.yaml | CONTROL OK | 1 | FAIL | the control failed, as it must |
| pilot/01-login.yaml | PASS | 0 | PASS |  |
| pilot/02-browse-store.yaml | PASS | 0 | PASS |  |
| pilot/03-add-to-cart.yaml | PASS | 0 | PASS |  |
| pilot/04-checkout.yaml | PASS | 0 | PASS |  |
| pilot/05-order-tracking.yaml | PASS | 0 | PASS |  |
| store/store-oos-listed-last.yaml | PASS | 0 | PASS |  |

## Self-check (AC3)

- clone_config: pass - artisan config:show = multi_food_db_qa4276_20261020_111338_16063
- clone_name: pass - multi_food_db_qa4276_20261020_111338_16063
- marker_restored: pass - item 1 name + translations equal the shared read
- no_cloud_argv: pass - flow controls/02-browse-store-wrong-assert.yaml
- no_cloud_env: pass - no MAESTRO_*KEY/TOKEN variable for flow controls/02-browse-store-wrong-assert.yaml
- request_marker: pass - GET :8276/api/v1/items/details/1 returned the clone's marker
- shared_orders_unchanged: pass - orders COUNT/MAX 179/91415 before and after

## Teardown

- uninstall_app: ok com.izzes.nears.qanightly
- reverse_remove: ok tcp:80
- account_release: ok customer_a
- stop_server: ok pid 65152
- stop_emulator: ok pid 65898
- lock_release: ok emulator-5580
- drop_clone: ok multi_food_db_qa4276_20261020_111338_16063
- delete_env_copy: ok 
- remove_tree: ok /Users/Apple/Projects/nears-qa-nightly_20261020-111333-16063

Known egress: api.copilot.mobile.dev (TLS, about 6 KB per maestro test; accepted, blocking it is NEARS-4277)

nothing is published automatically: screenshots are never scrubbed (maestro-pilot.md §9.6); check them, then run a row's publish line by hand:

    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-111620-72278 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-c1-base/evidence/01-02-browse-store-wrong-assert
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-111807-75224 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-c1-base/evidence/02-01-login
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-111912-77350 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-c1-base/evidence/03-02-browse-store
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-112106-84516 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-c1-base/evidence/04-03-add-to-cart
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-112257-88505 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-c1-base/evidence/05-04-checkout
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-112518-99328 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-c1-base/evidence/06-05-order-tracking
    bash /Users/Apple/Projects/nears/scripts/qa-evidence-publish.sh NEARS-4276/maestro/20261020-113009-11105 "<verdict line>" --evidence-dir /Users/Apple/.nears/qa-nightly/qa4276-c1-base/evidence/07-store-oos-listed-last
