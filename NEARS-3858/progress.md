# NEARS-3858 QA [8] progress — fix_cycle 0 — device-free (DB + CLI + API), 0 screenshots

Worktree HEAD ef7dc87db (feat/NEARS-3858-mixed-basket-seeder). Copy: multi_food_db_qa3858 (fresh dump 15:45, CHECKSUM TABLE == shared).
Backend: /Users/Apple/Projects/nears-NEARS-3858-mixed-basket-seeder @ ef7dc87db (pid 22203, :8158, --no-reload, DB_DATABASE=multi_food_db_qa3858; stopped after QA)

| AC | status | evidence |
|----|--------|----------|
| AC7 (i) shared+allow-listed | PASS | REFUSED: connected database is "multi_food_db"… rc=1; shared fixture rows 0, all tables + cache checksum unchanged |
| AC7 (ii) unlisted multi_food_db_test | PASS | REFUSED: … only multi_food_db_qa3858 is allowed by default … (currently NULL) rc=1; 0 fixture rows |
| AC7 (iii) non-local host | PASS | DB_HOST=db.nears.invalid and DB_HOST=127.0.0.2 (not aliased on lo0), both with DB_DATABASE=qa3858 -> REFUSED: database host is … rc=1; copy unchanged; phpunit case (h) green |
| AC3 run1/run2 | PASS | +3 vendors +3 stores +21 schedule +6 items +2 pharmacy details +1 surge; run2 diff empty incl. CHECKSUM TABLE |
| AC1 | PASS | stores 91158/91159/91160 zone 1, modules 1/2/3, status 1 active 1, module_zone pivot 1 each; API details 200 open=1; get-stores/all per moduleId lists each |
| AC2 | PASS | pid row is_prescription_required=1 for 91157; tinker requiresPrescription() true (91157) / false (91156 OTC, 91152); API item details is_prescription_required 1 / 0 |
| AC4 | PASS | max details rows per fixture item = 1 |
| AC5 | PASS | surge id 1 (1,[1],7.00 active); 0 active zone-1 surges w/ module 2; after 3830 seeder: still exactly 1 (1,1) row (3830 adopted id 1) |
| AC6 | PASS | digit_after_decimal_point=2; business_settings sha256 + CHECKSUM TABLE unchanged pre/run1/run2 |
| AC8 | PASS | §21 matches 36/36 seeded values; isolated-copy-only; customer@nears.com + addr 46 (in zone 1 only). Non-AC doc defect filed: cache:clear unprefixed |
| AC-REG | PASS | grep: 0 update/delete/truncate/upsert/down/raw-write; pre-existing rows on copy == shared (6 tables); shared DB before==after |
| AC-TEST | PASS | 3858 suite 12/12 (82 assertions); 3830 suite 5/5 (18) |
| vendor pw insert-only | PASS | sentinel hash survives rerun; original hash restored, verifies 123456789 |

## Delta re-QA cycle 1 @ 243da9248 (FIR-1)
| AC8 (re-verify) | PASS | §21 diff = 10 command lines only; dump line has --single-transaction --set-gtid-purged=OFF; Run cache:clear prefixed; Clean-up prefixed; bash -n OK; flags accepted |
| C1 | PASS | probe in qa3858.cache (91->92); §21 line cleared qa3858.cache 92->0 (probe gone); multi_food_db.cache 91 rows, CHECKSUM 2661995565 unchanged; probe never present in shared |
