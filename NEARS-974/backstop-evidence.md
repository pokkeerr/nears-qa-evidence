# NEARS-974 QA backstop evidence — remove orphaned `transaction_dashboard()`

Worktree: `/Users/Apple/Projects/nears-NEARS-974-orphaned-method`
Branch: `fix/NEARS-974-remove-orphaned-transaction-dashboard`
Mode: tests-backstop (live admin-UI click-through parked — read-only-DB QA envelope, same standing reason as NEARS-972/967/965).

## AC1 — method is gone (grep 0 hits)
```
$ grep -rn "transaction_dashboard" Admin/       # (git history excepted)
(no output — grep exit 1 = clean)
$ grep -rn "transaction_dashboard" app/ routes/ resources/   # from Admin/
(no output — grep exit 1 = clean)
```
Diff confirms the exact orphaned method (was lines 150-155) removed; it rendered the same
`admin-views.dashboard-{module_type}` view the live `dashboard()` serves.

## AC2 — main dashboard resolves, app boots clean, no new orphan
```
$ php artisan config:clear   -> INFO Configuration cache cleared successfully.  (exit 0)
$ php artisan route:clear    -> INFO Route cache cleared successfully.           (exit 0)
$ php artisan route:list --json   (exit 0, no stderr, NO reflection / "method does not exist")

admin.dashboard  GET|HEAD  admin  -> App\Http\Controllers\Admin\DashboardController@dashboard   [PRESENT]
admin.transactions.dashboard   -> count 0   (already removed by NEARS-972)
routes whose action references transaction_dashboard -> count 0   (no new orphan)
```

## AC3 — sibling dashboard actions intact
```
$ grep -n "public function ..." Admin/app/Http/Controllers/Admin/DashboardController.php
 30: public function user_dashboard(Request $request)
150: public function dispatch_dashboard(Request $request)
214: public function dashboard(Request $request)
623: public function dashboard_data($request)          # shared helper
     public function transaction_dashboard(...)         # GONE
```

## AC4 — full suite green, no new failures
```
$ vendor/bin/phpunit --configuration phpunit.xml
PHPUnit 11.5.55 — PHP 8.5.6
.......... 749 / 749 (100%)
Time: 01:09.279, Memory: 263.00 MB
OK, but there were issues!
Tests: 749, Assertions: 6782, Deprecations: 1, PHPUnit Deprecations: 2.   (exit 0)
```
Deprecations (1 + 2 PHPUnit) are pre-existing/environment (PHP 8.5 on a Laravel-11-era suite),
not introduced by this 6-line deletion. Zero failures, zero errors.

## Cleanup
phpunit-dirtied `config/system-addons.php` + `resources/lang/en/messages.php` reverted via
`git checkout --`; final `git status` shows only `DashboardController.php` modified.

VERDICT: PASS (4/4 ACs met).
