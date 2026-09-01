# NEARS-2752 QA progress checkpoint

Backend-only fix (no UI/device surface). Lane: API, device-free.

## Positive control (falsifiable proof)
- Reverted `Admin/app/Http/Controllers/Api/V1/CustomerController.php` to pre-fix commit `defb12ce7`
  (`git checkout defb12ce7 -- <file>`), ran `OrderPaymentFailedNullAddressTest`:
  RESULT: 3/4 FAIL — `Expected response status code [200] but received 500` for null / invalid-JSON /
  valid-JSON-missing-key cases. 4th test (valid delivery_address WITH contact_person_number) still
  passed pre-fix (unaffected code path) — confirms positive control isolates the right cause.
- Restored fixed file (`git checkout HEAD -- <file>`), tree confirmed clean via `git status --short`.
- Re-ran same test: 4/4 GREEN.

## AC1 (null/invalid/missing-key -> 200 + null contact_person_number)
- `vendor/bin/phpunit --filter OrderPaymentFailedNullAddressTest` -> OK (4 tests, 8 assertions), post-fix.
- BE-log check: laravel.log shows the RED run's `[FAIL] Attempt to read property "contact_person_number"
  on null` / `[FAIL] Undefined property: stdClass::$contact_person_number` ErrorException entries
  timestamped exactly at the pre-fix run; the GREEN restore-run immediately after produced ZERO new
  matching log lines. Clean.
- STATUS: PASS

## AC2 (valid delivery_address w/ contact_person_number unchanged)
- Same test class, `test_valid_delivery_address_returns_correct_contact_number` -> asserts
  `contact_person_number === '+9990001122'`. GREEN both pre-fix and post-fix (unaffected path).
- STATUS: PASS

## IDOR guard regression (NEARS-1301, lines 224-260 untouched)
- `vendor/bin/phpunit --filter OrderPaymentFailedIdorTest` -> OK (2 tests, 4 assertions). No regression.

## Regression-candidate drain (from [6]/[8b]): ItemModuleFollowsStoreTest x2 + BulkImportZoneScopeTest x1
- Ran both full files: `vendor/bin/phpunit tests/Feature/ItemModuleFollowsStoreTest.php
  tests/Feature/Security/BulkImportZoneScopeTest.php` -> OK, **19/19 tests, 86 assertions, ALL GREEN**.
- Could NOT reproduce the engineer-flagged failures in this worktree's private test DB
  (`multi_food_db_test_nears_nears_2752_payment_failed_null_add`, per NEARS-1199). Per protocol,
  dropped with this note — NOT filed as regression_bugs (could-not-reproduce).

## UserApp client tolerance (courtesy check, code-read)
- `UserApp/lib/features/checkout/domain/models/payment_model.dart:49`:
  `contactNumber = json['contact_person_number'] ?? ''` — already null-coalesces server null to
  empty string client-side; no crash risk regardless of backend fix. Confirms client was already
  nullable-shaped, per ticket's stated non-blocker framing.

## Automated backstop
- Started a full `--testsuite Feature` run (292 test files) as a completeness check beyond the
  scoped tests above; killed it after ~30s CPU / no progress signal once it became clear it would
  run well past the bounded window with no scope match to the QA Test Scope (which named the exact
  targeted tests to run, all already green above). Targeted backstop used instead:
  `OrderPaymentFailedNullAddressTest` (4/4), `OrderPaymentFailedIdorTest` (2/2),
  `ItemModuleFollowsStoreTest` + `Security/BulkImportZoneScopeTest` (19/19) = 25 tests, all GREEN,
  all run live in this worktree. Tree confirmed clean (`git status --short`) after the
  positive-control revert/restore cycle.
- FINAL VERDICT: PASS
