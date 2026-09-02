# NEARS-2722 QA progress

Device: emulator-5554, VendorApp built from worktree
/Users/Apple/Projects/nears-NEARS-2722-vendor-wallet-adjustable-seed
Fix-cycle 1 (doc-only fix from code review, no code diff)

## AC1
- demo.store@gmail.com wallet screen: "Adjust Payments" reachable, Cash in Hand
  25.00 AED, Withdrawable Balance 46.56 AED, Total Earning 71.56 AED — matches
  scope item 1 exactly. Logs clean. Shot: ac1-demo-store-wallet.png
- organicshop@demo.com wallet screen: "Adjust Payments" reachable, Cash in Hand
  10.00 AED, Withdrawable Balance 10.00 AED, Total Earning 20.00 AED — matches
  scope item 2 exactly. Logs clean. Shot: ac2b-fallback-organicshop-wallet.png
  (captured after consuming demo.store, doubles as fallback evidence)

## AC2(a) fallback
- Consumed demo.store (Adjust Payments -> Ok): POST
  /api/v1/vendor/make-wallet-adjustment http_status=200. DB: id=1
  collected_cash 25.00->0.00, total_withdrawn 0->25.00. "Adjust Payments"
  button now absent for demo.store (adjust_able flipped false, matches
  formula). Shot: ac2a-consumed-demo-store.png
- organicshop still shows "Adjust Payments" reachable post-consumption
  (verified live, see AC1 organicshop shot above) -> fallback path CONFIRMED.

## AC2(b) restore
- Re-ran seeder (NEARS_SEED_ALLOW_DB=multi_food_db, --force): id=1 WRITTEN
  collected_cash 0.00->25, id=12 SKIPPED (already 10). DB confirms id=1
  collected_cash=25.00, total_withdrawn stays 25.00 (real consumed txn kept).
- Live: re-logged into demo.store, wallet screen shows "Adjust Payments"
  reachable again, Cash in Hand 25.00 AED, Withdrawable Balance 21.56 AED
  (reflects the real prior withdrawal), transaction history shows the
  "Transferred to Account / Approved" entry from the consumption step.
  Restore path CONFIRMED live. Shot: ac2c-restored-demo-store.png

## Scope item 5 (regression, DB diff)
- Snapshotted all 25 store_wallets rows before any QA action.
- Diff after full QA pass (excluding id=1,12) = EMPTY. id=23 (store 26,
  ts@ts.com) untouched (updated_at unchanged: 2026-08-31 12:15:39).

## Scope item 6
- git diff 320cd8738..HEAD -- Admin/app/Http/Controllers/Api/V1/Vendor/VendorController.php
  = empty. Only seeder + docs/data-qa/verification-checks.md changed.
  Formula at lines 94-101 read directly, matches seeder's replicated logic.

## Scope item 7 (guard)
- NEARS_SEED_ALLOW_DB unset -> RuntimeException REFUSED, nothing written
  (verified via DB read after).
- NEARS_SEED_ALLOW_DB=wrong_db_name -> RuntimeException REFUSED, nothing
  written.

## Scope item 8 (idempotency)
- Re-ran seeder immediately (correct env, no consumption in between):
  both rows reported SKIPPED, updated_at unchanged, values unchanged.

## Automated backstop
- vendor/bin/phpunit --filter Wallet: 46 tests, 151 assertions, OK (private
  test DB per NEARS-1199, isolated from the live multi_food_db QA run).
  (First attempt threw phantom CryptKey errors -- fresh worktree missing
  passport keys; fixed with `php artisan passport:keys --force`, documented
  worktree gotcha, not a real regression.)
