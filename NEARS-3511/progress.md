# NEARS-3511 QA progress checkpoint

Device-free ticket (backend DB seeder + SQL fixture). No device lock protocol used.

## AC1 [behav] Live demo on isolated/local DB — PASS
Approach (a): created throwaway MySQL schema `nears_qa_nears3511_throwaway` (created via
`CREATE DATABASE`, dropped via `DROP DATABASE` at teardown — never touched shared `multi_food_db`).
- Loaded `email_templates` table structure via `mysqldump --no-data` (read-only) from `multi_food_db`.
- Loaded PRE-patch fixture data (`git show c9cc64d4d:Admin/database/partial/email_tempaltes.sql`) — 30 rows, 29 stale "6amMart" (matches ticket's stated repro exactly).
- Ran `php artisan db:seed --class=NearsMailBrandCleanupByValueSeeder --force` with `DB_DATABASE` env override pointed at the throwaway schema (never touched worktree `.env`).
  - Run 1: "29 row(s) updated across 3 old-value variants." — post-run: 0 stale 6amMart rows, 30 canonical Nears rows.
  - Run 2 (idempotency): "0 row(s) updated" — counts unchanged (0 stale, 30 canonical).
  - Run 3 (admin-customised-row guard, ad hoc extra check): manually set id=1's copyright_text to a non-matching custom string, re-ran seeder — 0 rows updated, custom text on id=1 preserved untouched, id=24 (NEARS-3326's row) also untouched.
- Confirmed shared `multi_food_db.email_templates` untouched throughout (still 29 stale rows post-run, as expected — Tier C apply is explicitly out of scope for this build).
- Throwaway schema dropped at teardown.

## AC2 [behav] Source read — PASS
- `grep -c "6amMart" Admin/database/partial/email_tempaltes.sql` = 0.
- `grep -c "© 2023 Nears. All rights reserved."` = 30 (29 fixed by this ticket + id 24 already fixed by NEARS-3326).
- id=24's row line is byte-identical before (`git show c9cc64d4d...`) vs after (HEAD) — diff empty.
- id=21 and id=28 (the two non-canonical old-value variants) confirmed rewritten to the canonical string in the fixture, all other fields byte-identical.

## Regression sweep
- `git diff c9cc64d4d..HEAD -- Admin/database/seeders/NearsMailBrandCleanupSeeder.php` — empty (NEARS-3326's seeder untouched).
- `git diff --stat c9cc64d4d..HEAD` — exactly 3 files changed (seeder, sql fixture, new test) — no other diffs.
- `business_settings` diff — empty (untouched by this ticket, matches scope).
- `grep -rn "EmailTemplate::" Admin/app/` + `grep -i cache` cross-check — no `Cache::` wraps any `email_templates`/`EmailTemplate` read site; engineer's "uncached" claim confirmed.
- `vendor/bin/phpunit --filter Nears3511MailBrandCleanupByValueSeederTest` — 4/4 tests, 6 assertions, green (uses isolated per-worktree test DB per NEARS-1199, not the shared DB).
- Full `vendor/bin/phpunit --configuration phpunit.xml` — see final envelope for result.
