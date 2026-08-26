# NEARS-2460 — delta re-QA (fix-cycle 1, retry) — progress log

Device: emulator-5566 (freshly freed, disk 935232KB/~913MB free at acquire — above 800MB floor).
Worktree: /Users/Apple/Projects/nears-NEARS-2460-store21-subscription-expiry
Backend: primary tree Admin (port 8000, shared multi_food_db), VendorApp default baseUrl 10.0.2.2:8000.

## Pre-check (DB, read-only)
- `store_subscriptions` id=1 store_id=21: status=1, mobile_app=1, expiry_date=2031-08-26 (healthy).
- `stores` id=21 "Fast Market": status=1, store_business_model=subscription.
- `stores` id=19 "Eco Market": status=1, store_business_model=commission (no subscription row — expected).
- Seeder diff confirmed present in worktree: NEARS-2537 sets `mobile_app => 1` on BOTH the
  insertGetId path and the self-heal `isStale` update path of `ensureSubscription()`.

## AC1 — store 21 (fastmarket@demo.com) login + Menu reachability
1. Logged in as fastmarket@demo.com / 123456789 on emulator-5566 (VendorApp / Vendor Owner tab).
   `[NET] POST endpoint=/api/v1/auth/vendor/login` -> `http_status=200`. PASS (no 401/no_mobile_app).
2. Landed on Home dashboard (route `/`, MainActivity) past Sign In. PASS.
3. Tapped Menu tab -> all 19 Menu items rendered (`All Items`...`Terms & Condition`), **no**
   "Your Package is Expired" bottom sheet / `Scrim` blocking overlay. PASS.
4. Opened "Reports" (a gated Menu item per the subscription gate) -> opened cleanly
   (Expense Report / Tax Report), no gate. PASS.
5. Opened "My Business Plan" -> shows `Next Billing Date: Aug 26, 2031`, `Mobile App Access`,
   package `QA Single-Store Fixture` — matches the DB row post-fix. PASS.
6. Logs: no `[FAIL]`/`[ERR]` in the app runtime log for the whole login->Menu->Reports->My
   Business Plan flow. Evidence: `store21-menu-no-expiry-gate.png`.

## Regression spot-check — store 19 / vendor 16 (ecomarket@demo.com)
1. Logged out of store 21, logged in as ecomarket@demo.com / 123456789.
   `[NET] POST endpoint=/api/v1/auth/vendor/login` -> `http_status=200`. PASS.
2. Landed on Home dashboard, Menu tab reachable, all 19 items rendered, no gate (expected —
   commission model store, gate doesn't apply). PASS.
3. Logs: clean, no `[FAIL]`/`[ERR]`. Evidence: `store19-menu-regression-check.png`.

## Unrelated finding (regression_bugs, non-blocking)
While on "My Business Plan" -> "Transaction" tab for store 21, hit a pre-existing,
unrelated TypeError: `type 'int' is not a subtype of type 'String?'` in
`SubscriptionTransactionModel.fromJson` (`offset` field declared `String?`, backend
returns int — same class of bug as the already-documented `ItemModel.fromJson` issue,
NEARS-540/NEARS-2261). File untouched by this ticket's diff. Logged as regression_bug,
does not affect AC1 verdict. Evidence: `bug-vendor-subscription-transaction-offset-typeerror.log`.

## Verdict
PASS — AC1 demonstrated live on emulator-5566, no [FAIL]/[ERR], regression guard (store 19)
unaffected.
