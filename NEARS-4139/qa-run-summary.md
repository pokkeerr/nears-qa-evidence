# NEARS-4139 QA run summary

Arms: BASE = detached worktree at 69abec1ed (own composer install + passport keys), `php artisan serve` 127.0.0.1:8140; FIXED = worktree fix/NEARS-4139-tempproduct-zonescope-label @ eef0bd61e, `php artisan serve` 127.0.0.1:8139. Both read the SAME private clone `multi_food_db_qa4139` (DB_DATABASE set in each tree's Admin/.env; DB identity proved by the seeded admins logging in: they exist only in the clone). backend-freshness-check: PASS for both ports (own worktrees, cwd + sha printed). The host PHP 8.2.34 segfaulted the php -S child several times (SIGSEGV in a shutdown function, both arms, no ticket-code involvement); a supervise loop restarted artisan serve and every probe was retried only on connection errors.

Clone: DROP/CREATE of multi_food_db_qa4139 only; dump imported with the GTID_PURGED lines (24-25) stripped from the stream (the file itself untouched). Seeder blob a3cd50916c19c115182d439ebd3c6b408087e91a verified before the run. product_approval = '1' verified on the clone. Login credentials of fixture vendors 91116/91123/91127 were reset on the clone only (their original hashes were unknown).

## phpunit from the fixed worktree (NOT the full suite)
- Nears4139TempProductZoneScopeTest: OK 18 tests / 68 assertions
- Nears4130ZoneScopeStoreSubscriptionTest: OK 10 / 78
- Nears4139TempProductZoneScopeQaFixtureSeederTest: OK 31 / 1279
- Nears4130ZoneScopeSubscriptionQaFixtureSeederTest: OK 37 / 1022
- AdminRouteSmokeTest: OK 3 / 9

## Mutations (scratch worktree at the tip, never the live worktree; each mutation proven landed by git diff; control unmutated 18/18 + 10/10 first)
- M1 remove the new case: Nears4139 RED 11/18, Nears4130 RED 2/10 (test_every_zonescope_applier_has_a_label + test_tempproduct_applies_zonescope_and_is_labelled)
- M2 lowercase label tempProduct: Nears4139 RED 11/18, Nears4130 RED 3/10 (adds the exact-case label test)
- M5 revert both findOrFail to find: Nears4139 RED 3/18 (delete, repeated delete, remove-image), Nears4130 GREEN 10/10
