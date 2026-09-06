# NEARS-3086 QA evidence

Backend-only, no-UI, no-device-surface ticket. All evidence is command output /
log excerpts (no screenshots — there is nothing to render).

Worktree: `/Users/Apple/Projects/nears-NEARS-3086-lslib-v2-cleanup`
Commit under test: `8c0d6dc670cf0fd83f6a12a73b501b3a9bbb0bcb`
Base: `feat/userapp-reskin2@c6c42d1ac9d9acacf5f2278473fa8a9ec1cc0a62`

## AC1 — files/dirs removed
```
$ ls routes/api/v2
ls: routes/api/v2: No such file or directory
$ ls app/Http/Controllers/Api/V2
ls: app/Http/Controllers/Api/V2: No such file or directory
$ ls routes/api        -> only v1/
$ ls app/Http/Controllers/Api  -> only V1/
```

## AC2 — route:list + live 404
```
$ php artisan route:list | grep -i ls-lib
(no output, exit 1)

$ php artisan serve --host=127.0.0.1 --port=8123 &
INFO  Server running on [http://127.0.0.1:8123].

$ curl -s -o /dev/null -w "HTTP_STATUS:%{http_code}\n" -X POST http://127.0.0.1:8123/api/v2/ls-lib-update
HTTP_STATUS:404
(body: branded "Error 404 | Nears" page)
```

## AC3 — grep LsLibController|Api\V2
```
$ grep -rn 'LsLibController\|Api\\V2' app routes Modules
(no output, exit 1 — 0 hits)
```
Paths searched: `Admin/app`, `Admin/routes`, `Admin/Modules`.

## AC4 — RouteServiceProvider no longer references routes/api/v2/api.php
```
$ grep -n 'v2/api.php\|api/v2' app/Providers/RouteServiceProvider.php
(no output)
```
`RouteServiceProvider.txt` diff (base..HEAD) shows the corresponding 6-line
removal (see AC6 diff-stat) — confirmed by direct read, no `api/v2` mention
remains in either file.

## AC5 — grep v2-api
```
$ grep -rn 'v2-api' . (excluding vendor/node_modules/.git)
app/Providers/RouteServiceProvider.php:227:        // (a cap of N served N/2); outside it (firebase-topic; also v2-api, removed NEARS-3086)
```
Only the historical comment remains; no live `RateLimiter::for('v2-api'` / `throttle:v2-api`.

## AC6 — diff-stat vs base
```
$ git diff --stat c6c42d1ac9d9acacf5f2278473fa8a9ec1cc0a62..HEAD
 Admin/app/Http/Controllers/Api/V2/LsLibController.php    | 16 ---------
 Admin/app/Providers/RouteServiceProvider.php             | 16 ++-------
 Admin/app/Providers/RouteServiceProvider.txt              |  6 ----
 Admin/routes/api/v2/api.php                               |  9 -----
 Admin/tests/Feature/Security/ThrottleBucketIsolationTest.php | 38 ++------------------
 Admin/tests/Feature/Security/V2RouteThrottleTest.php      | 41 ----------------------
 docs/backend/route-inventory.md                           |  4 +--
 nears-reference.md                                        |  2 +-
 8 files changed, 8 insertions(+), 124 deletions(-)
```
Identical with no path restriction — confirms nothing outside this list changed.
`Admin/routes/api/v1` diff: empty. `Admin/installation/activate_install_routes.txt`
and `activate_update_routes.txt`: present on disk, zero diff.
(Ticket text says "9 total" files; actual is 8 — the listed set matches
exactly, treating "9" as a minor miscount in the ticket, not a scope gap.)

## AC7 — route:cache pre-existing bug / route:list clean
```
$ php artisan route:cache   (on HEAD)
LogicException: Unable to prepare route [admin/business-settings/app-settings]
for serialization. Another route has already been assigned name
[admin.business-settings.app-settings].
  at vendor/laravel/framework/.../AbstractRouteCollection.php:257

$ php artisan route:cache   (on a scratch worktree pinned to base commit
  c6c42d1ac9d9acacf5f2278473fa8a9ec1cc0a62, passport keys generated fresh)
IDENTICAL LogicException, same route names, same file/line.
```
Confirmed pre-existing, not caused by this diff.
```
$ php artisan route:clear && php artisan route:list
... Showing [1495] routes
exit 0, no new errors
```
AC7 fallback clause satisfied.

## AC8 — docs updated
```
nears-reference.md:489
| API v2 routes | None — the only route (`api/v2/ls-lib-update`) was a
6amMart licence-library stub, removed in NEARS-3086. |

docs/backend/route-inventory.md:15
- Routes include web, admin, vendor, install, update and API (api/v1) endpoints.
```
Old "API v2 routes" row / "api/v1, api/v2" mention confirmed gone (diff-read
both files in full).

## Regression sweep

### ThrottleBucketIsolationTest (8 methods)
```
OK (8 tests, 516 assertions)
```

### Full Admin/tests/Feature/Security directory — HEAD (run twice)
```
OK (552 tests, 3288 assertions)
```
Note: contrary to the ticket's framing ("expect 1 PRE-EXISTING unrelated
failure"), the full directory run is FULLY GREEN on HEAD, both times. See
regression-candidate #1 below for the explanation (order-dependent test
pollution, exposed only when the deleted v2 test files are still present).

### Full Admin/tests/Feature/Security directory — BASE commit (scratch
worktree, passport keys generated, private test DB
`multi_food_db_test_nears3086_base_check`, run twice)
```
There was 1 failure:
1) Tests\Feature\Security\RegistrationNonceTest::test_registration_nonce_survives_the_full_register_save_chain
Failed asserting that 401 is identical to 200.
Tests: 555, Assertions: 3414, Failures: 1.
```
555 tests on base vs 552 on HEAD — the 3-test delta matches the deleted
`V2RouteThrottleTest.php` (3 methods removed as part of this diff).

(First base attempt before generating `php artisan passport:keys --force` in
the scratch worktree threw 78 unrelated `LogicException: Invalid key
supplied` / 500s from missing OAuth keys — an artifact of the scratch
worktree setup, not a real base-commit defect; discarded once keys were
generated and the run above is the corrected one.)

### RoutePresenceGuardTest / presence-baseline.json
```
OK (4 tests, 176 assertions)
```
No `ls-lib` reference in `tests/presence-baseline.json`.

### php -l on changed .php files
```
No syntax errors detected in Admin/app/Providers/RouteServiceProvider.php
No syntax errors detected in Admin/tests/Feature/Security/ThrottleBucketIsolationTest.php
```
(The other two changed `.php` files, `LsLibController.php` and
`V2RouteThrottleTest.php`, are deleted — nothing to lint; their removal is
itself AC1's evidence.)

## Regression-candidate confirmation

**1. RegistrationNonceTest failure** — CONFIRMED to reproduce on the base
commit (both `--filter`-scoped and full-directory runs, twice each). Root
cause is order-dependent test-isolation pollution: the base commit still has
the (now-deleted) `V2RouteThrottleTest.php` in the discovered test set, which
shifts execution order enough to leak state into `RegistrationNonceTest`.
On HEAD (this diff), the full Security suite runs green including this test,
twice. So: real pre-existing bug, confirmed on base, NOT currently manifesting
on HEAD — filed as a regression bug for the PO/backlog (test-isolation issue,
not something this diff needs to fix), not a blocker for this ticket.

**2. route:cache duplicate-route-name LogicException** — CONFIRMED identical
on the base commit (scratch worktree, passport keys generated). Pre-existing,
unrelated to this diff. `route:list` (this ticket's actual AC7 fallback) runs
clean with 0 errors.
