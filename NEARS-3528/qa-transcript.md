# NEARS-3528 — Live QA transcript (Admin panel, HTTP-level)

Backend: `php artisan serve --host=127.0.0.1 --port=8215` from
`/Users/Apple/Projects/nears-NEARS-3528-customrole-horizontal-authz/Admin`
(confirmed listener PID's cwd = this worktree, not another session's backend —
port 8123 was found already bound by a DIFFERENT worktree's `php artisan serve`
before this run started, and was abandoned in favor of 8215).

QA actor (reversible, removed at close): `Admin` id=9, email
`nears3528-qa-Nears3528QA-6aa65794f416e@test.local`, bound to `AdminRole` id=11
(`modules: ["custom_role"]`, i.e. a "legacy grant" actor per
`actingAsNonSuperAdminWithCustomRoleModule()` in
`Admin/tests/Feature/Security/Nears3476CustomRoleControllerTest.php`).
Target "other" role: `AdminRole` id=12 (`modules: ["order"]`).
Superadmin: `admin@admin.com` (id=1, role_id=1).

All requests driven via `curl` with a real logged-in session cookie (session
established through the actual `/login/admin-employee` + `/login/admin` form
flow, custom captcha solved by reading the plaintext `six_captcha` session
value server-side — SESSION_DRIVER=file, encrypt=false in this local dev
config — not a shortcut around authn, just a scripted browser).

## AC1 — non-owner denied (actor role_id=11, target role_id=12)
- GET `/admin/users/custom-role/edit/12` -> HTTP 200, body = `errors.404` view (matches documented convention: `assertOk()` + 404 body, not a redirect)
- POST `/admin/users/custom-role/update/12` (rename attempt) -> HTTP 200, `errors.404` body; DB row 12 unchanged (`name`, `modules` identical pre/post)
- DELETE `/admin/users/custom-role/delete/12` -> HTTP 200, `errors.404` body; DB row 12 still exists post-request

## AC2 — self-edit ALSO denied (actor targeting OWN role_id=11)
- GET `/admin/users/custom-role/edit/11` -> HTTP 200, `errors.404` body
- POST `/admin/users/custom-role/update/11` (self-escalation attempt: rename + add `store`,`settings` modules) -> HTTP 200, `errors.404` body; DB row 11 unchanged (name AND modules identical, still just `["custom_role"]`)
- DELETE `/admin/users/custom-role/delete/11` -> HTTP 200, `errors.404` body; DB row 11 still exists post-request

## AC3 — superadmin protection unaffected
- Superadmin POST `/admin/users/custom-role/update/1` (master role rename attempt) -> HTTP 200, `errors.404` body; DB row 1 (`Master admin`) unchanged
- Superadmin DELETE `/admin/users/custom-role/delete/1` -> HTTP 200, `errors.404` body; DB row 1 still exists
- Non-superadmin GET `/admin/users/custom-role/edit/1` -> HTTP 200, `errors.404` body (role_id==1 protected against non-superadmin too, not just superadmin)
- **Positive control** — superadmin GET `/admin/users/custom-role/edit/12` -> HTTP 200, real edit form (not 404); superadmin POST `/admin/users/custom-role/update/12` (legit rename to `SA-Renamed-OtherRole`, modules `order,store`) -> HTTP 302 redirect to create page (success path); DB row 12 actually updated — proves the fix does not over-block a legitimate superadmin action on a non-reserved role.

## Add/create gap (new AddRequest authorize(), same fix)
- Non-superadmin POST `/admin/users/custom-role/create` (new role attempt) -> HTTP 200, `errors.404` body; `admin_roles` row count unchanged (7 -> 7)
- Superadmin POST `/admin/users/custom-role/create` (new role) -> HTTP 302 redirect (success); new row (id=13, `Nears3528-QA-SA-Create`) persisted — positive control

## getUpdateView (GET edit) spot-check
Exercised directly above for both actor(non-owner id12)/self(id11)/non-superadmin-on-master(id1) — all three return the `errors.404` body via the same `roleCheck()` path, confirming the engineer's flagged shared-path note.

## NEARS-3501 modules[] whitelist regression check
Superadmin POST `/admin/users/custom-role/update/12` with `modules[]=evil_module_not_in_whitelist` -> HTTP 302 back-redirect (Laravel validation-failure redirect, not the success redirect), DB row 12 modules unchanged (`["order","store"]`) — `Rule::in(ALLOWED_MODULES)` still enforced; this fix's `authorize()`/`roleCheck()` change did not touch `rules()`.

## Logs-first check
- `storage/logs/laravel.log`: **zero** entries at all during the live QA HTTP window (12:00:xx-12:03:xx on 2026-09-13) — no `[FAIL]`/`[ERR]`/exception logged for any of the above requests. Pre-existing `testing.ERROR` entries from an earlier phpunit run (channel=`testing`, timestamps 11:42-11:43) are unrelated (different channel, different test fixtures: store lookups, FCM, vendor-register validation) — not part of this ticket's surface, not counted as a regression.
- PHP built-in server log (`/tmp/nears3528_serve.log`): all requests returned in the dotted-progress format with no fatal-error stack traces.

## Automated backstop
`vendor/bin/phpunit --filter Nears3476CustomRoleControllerTest` -> 8/8 pass, 22 assertions.
`vendor/bin/phpunit --filter 'Nears3501CustomRoleModulesWhitelistTest|Nears3527VendorCustomRoleModulesWhitelistTest'` -> 10/10 pass, 31 assertions (regression check, whitelist untouched by this fix).

## Cleanup (DB read-only otherwise — reversible QA row removed at close)
- Deleted `Admin` id=9 (QA actor)
- Deleted `AdminRole` id=11 (QA actor's own legacy-grant role)
- Deleted `AdminRole` id=12 (QA "other role" target, including its superadmin-driven rename — was never real data)
- Deleted `AdminRole` id=13 (QA superadmin create-flow positive control)
- `admin_roles` table confirmed back to its pre-QA baseline: 5 rows (`Master admin`, `QA Role A/B/C/D...`), identical to the state before this run started.
- `php artisan serve` on port 8215 killed (PID cwd re-verified as this worktree before kill).
