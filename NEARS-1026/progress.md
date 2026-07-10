# NEARS-1026 QA — cycle 0 (2026-07-10)

Build: worktree `/Users/Apple/Projects/nears-NEARS-1026-condition-counts`, branch `feat/NEARS-1026-condition-counts` @ `51910ee3` (base `feat/human-review` @ 7cf8783c).
Backend under test: `php artisan serve` port 8026 FROM THE WORKTREE. Device: emulator-5556 (lock acquired/released). App: UserApp from the worktree, `--dart-define=API_HOST=10.0.2.2:8026`.

## Seeder application (user-approved DB write — recorded)
- Pre-seed: `common_conditions` = 0 rows; `pharmacy_item_details` = 3 rows (all `is_basic=1`, untouched).
- Applied: `NEARS_SEED_ALLOW_DB=multi_food_db php artisan db:seed --class=Nears1026ConditionCountQaSeeder --force` → condition id=1 slug=`nears1026-pain-relief-qa`; +3 pid rows (items 32, 33 → zone 1 via store 7; item 598 → zone 2 via store 53), all `is_basic=0`.
- Post-seed: `pharmacy_item_details` = 6 rows. Transcript: `seeder-apply.log`.
- **Fixture LEFT IN PLACE** (per instruction — regression fixture for future runs). Rollback available: `(new Database\Seeders\Nears1026ConditionCountQaSeeder())->down()`.
- Note: an OpenTelemetry export error printed at artisan shutdown — local OpenObserve (port 5080) not running; environmental, unrelated.

## AC verdicts (live)
| # | AC | Verdict | Evidence |
|---|----|---------|----------|
| 1 | Chip count zone-scoped: z1=2, z2=1, values differ | PASS | `curl-matrix.txt` AC1a/b — zoneId `[1]` → `items_count=2`; `[2]` → `items_count=1`; HTTP 200 both |
| 2 | Chip count == list `total_size`; list unchanged | PASS | `curl-matrix.txt` AC2a/b — z1 `total_size=2` ids `[32,33]`; z2 `total_size=1` ids `[598]` |
| 3 | Fail-closed malformed zoneId | PASS | `garbage` / `[true]` / `{}` / `[[1,2],3]` → all HTTP 200, condition listed, `items_count=0` |
| 4 | Absent zoneId → default-zone counts | PASS | default zone = 2 (is_default=1) → `items_count=1` (== explicit `[2]`); parity: `/categories` absent-header also 200/5 rows via same setZoneIds substitution |
| 5 | Regression `/common-condition/list` | PASS | HTTP 200 `[{"id":1,"name":"NEARS1026 Pain Relief QA",...}]`. Non-default sort path SKIPPED: needs `business_settings` write (`common_condition_default_status` row absent → defaults to 1); DB read-only. Sort code untouched by the diff. |
| 6 | BE-log clean on `/api/v1/common-condition` | PASS | Worktree `laravel.log`: 0 lines mention common-condition; live-serve (`local` env) wrote 0 lines during matrix + device traffic; only `testing.` env lines from phpunit runs present |

## On-device spot-check (both zones reached)
- Zone 1 (guest, Dhaka demo address): pharmacy home renders chip **NEARS1026 Pain Relief QA**; grid below = Paracetamol 500mg + Ibuprofen 400mg (HealthCare Pharmacy) — exactly items {32,33}. Chip tap → `/common-condition/items/1` HTTP 200 refetch. Shot: `pharmacy-home-zone1-chip-and-items.png`.
- Zone 2 (login `customer@nears.com`, saved Abu Dhabi home address): chip renders; grid = Multivitamin Daily (CarePlus Pharmacy Abu Dhabi) only — item {598}; zone-1 items absent. Shot: `pharmacy-home-zone2-chip-and-item.png`.
- App log full-run scan: 0 `[ERR]`; 1 `[FAIL]` = transient `/api/v1/config/get-zone-id` 404 during QA's own GPS geo-fix jump (later calls 200; properly logged w/ correlation_id — not silent, not an AC action, unrelated to this change).
- Note (scope): mobile chip renders the condition NAME only — `CommonConditionModel.itemsCount` is parsed but not rendered on the mobile surface; the corrected count is API-payload-observable (and equals the on-device list size, demonstrated).

## Automated backstop
- Full suite (worktree): `vendor/bin/phpunit --configuration phpunit.xml` → **OK 774/774**, 6935 assertions (1 deprecation + 2 PHPUnit deprecations, pre-existing).
- New tests: `--filter CommonConditionCountZoneScopingTest` → **OK 6/6**, 72 assertions.

## Verdict: PASS
