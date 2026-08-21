# NEARS-2019 QA progress checkpoint

Worktree: /Users/Apple/Projects/nears-NEARS-2019-money-rounding
Branch: fix/NEARS-2019-persisted-money-rounding
Backend under test: primary tree `Admin/` on 127.0.0.1:8000 (pid 28927), per
nav-guide-userapp (worktree Admin/ has no vendor/, no oauth keys — never serve QA from it).

## Pre-flight
- baseUrl (UserApp/lib/util/app_constants.dart): 10.0.2.2:8000 (Android emulator dev host) — OK, real local backend, not demo/placeholder.
- Backend up: php artisan serve pid 28927, cwd /Users/Apple/Projects/nears/Admin — OK.
- business_settings id=95 (digit_after_decimal_point) = 2 in multi_food_db — confirmed via read-only SELECT.
- Fixture confirmed live: item id 97 "Rice 5kg" price 15.03 status=1; store id 1 "Nears Mart" zone_id=1 status=1.

## AC3 [behav] — Admin/tests/Feature/ConfigContractTest.php --filter ConfigContractTest
RUN. Result: Tests: 6, Assertions: 151, Failures: 1 (test_decimal_precision_is_two_not_whole_dirhams,
"Failed asserting that 0 is identical to 2"). Matches conductor's pre-measured expected shape exactly.
Evidence: docs/qa-evidence/NEARS-2019/ac3-phpunit.log
STATUS: met.

## AC2 [api] — GET /api/v1/config, partial
RUN (no device needed for this half). curl -i http://127.0.0.1:8000/api/v1/config -H "zoneId: [1]":
X-Request-Id: 491b011e-c7c8-485c-b395-48782c52da35; body has "digit_after_decimal_point":2 — fresh,
not stale/serving 0.
Evidence: docs/qa-evidence/NEARS-2019/ac2-config-endpoint.log
STATUS (config-publish half): met. STATUS (order_amount<->laravel.log DB-persistence correlation half): BLOCKED — needs a live UserApp checkout, no device available (see below).

## AC1 [behav] — non-integral order persistence via UserApp checkout
NOT RUN — blocked on device pool (below). No screen was driven, no order was placed.
STATUS: unverified (BLOCKED, not FAIL — no attempt was faked).

## Regression sweep (bounded, admin/vendor web panels — no device needed)
- Admin panel /admin/order/list/all (order list, 59 orders): renders 2-decimal amounts
  (e.g. "9.00", "1.50" — a genuine non-integral existing order), 0 NaN/ErrorException/Whoops in HTML.
- Admin panel /admin/report/store-wise-report (store-summary report): renders 2-decimal amounts
  (e.g. "13.76", "399.00"), 0 NaN/ErrorException/Whoops in HTML.
- Vendor panel /vendor-panel/order/list/all (demo.store@gmail.com): renders 2-decimal amounts
  (e.g. "29.00"), 0 NaN/ErrorException/Whoops in HTML.
STATUS: clean.

## Device pool — BLOCKED
All 3 Android QA-pool devices (emulator-5554/5556/5558) held by OTHER LIVE sessions for the
entire bounded wait window (~10+ min, 5 polls at 60-120s spacing, plus intervening investigative
work): emulator-5554 -> NEARS-2379 (anchor pid 50695, alive), emulator-5556 -> NEARS-2376 (anchor
pid 50695, alive), emulator-5558 -> NEARS-2130 (anchor pid 10132, alive, lock held since
2026-08-19T14:34:18Z — 3+ days, but the anchor process IS live, so not reclaimable as stale).
No iOS simulator booted either (xcrun simctl list devices booted -> none). This ticket's device
pool is Android-only per the spawn prompt, so iOS was not substituted in.
Verdict driver: AC1 cannot be demonstrated without a device -> whole run is BLOCKED, not FAIL.
