# NEARS-4053 mutation log

Fix under test: `_isFirstTime = true;` inside `PricingSummaryController.resetOrderTax()`
(`UserApp/lib/features/checkout/controllers/pricing_summary_controller.dart`).
Test files: `UserApp/test/features/checkout/checkout_reset_rearms_order_tax_test.dart` (15 tests, all green on the fixed tree) and, for M16,
`UserApp/test/features/checkout/checkout_screen_widget_test.dart` group `NEARS-4053` (1 new test; whole file 9 tests green).

Method: scratch COPY of `UserApp` + `packages` (never the live worktree), pristine controller restored before each mutation,
mutation applied by script, the unified diff of pristine vs mutated printed (the "proved-landed" column), then the test run once
per invocation through `mem-guard.py`. "RED" lists the failing test names (short form).

Base (unfixed tree) run of the final 15-test file (= M1 on the final file): 6 RED / 9 green. RED: reset-alone re-arm,
Place Order held, Total carries tax + no "tax components missing" line, zero-tax next entry re-fetches, failure-after-success
second entry, and the no-notify pin (its precondition `isFirstTime == true` fails on base). On the unfixed base the Total test
logged `[FAIL] ... checkout: cod cap verdict not scheduled (tax components missing)` and the Total read 20.0 instead of 22.0.

M3-M13 ran against the 14-test file before the zero-tax test (added to kill M15) existed. M1, M2 (cycle-1 re-runs), M15 and M16 ran against the final files.
The cycle-1 review edits (F3 stronger Total test, F4 test replaced) kept the file at 15 tests; M1 and M2 were re-run on that final file.
M14: the number is unused. The original log has no M14 row and no record of its content survives (scratch deleted), so it is treated as NOT RUN; numbering was not changed. The zero-tax test is RED on M1/M2/M7 by construction (no re-arm at all).

| # | Mutation (what changed) | Proved landed (diff hunk) | Result |
|---|---|---|---|
| M1 | delete the re-arm line from `resetOrderTax` | `-    _isFirstTime = true; // NEARS-4053` at resetOrderTax | RED (final file): re-arm test, Place Order held, Total/COD verdict, zero-tax next entry, failure-after-success, no-notify pin (6) |
| M2 | re-arm only in `onClose` (after `resetOrderTax()`), not in the reset | `-` line in resetOrderTax and `+    _isFirstTime = true;` after `resetOrderTax();` in onClose | RED (final 15-test file, cycle-1 re-run): 6 RED / 9 green, same set as M1 (re-arm, Place Order held, Total/COD verdict, zero-tax next entry, failing second entry, no-notify pin). Tests drive the initCall path = `resetOrderTax`, never `onClose` |
| M3 | re-arm unconditionally at the top of `triggerOrderTaxIfNeeded` | `+    _isFirstTime = true;` as first statement of triggerOrderTaxIfNeeded | RED: "control: without re-arm the second trigger does not dispatch", "updateFirstTime()+reset+trigger twice = ONE call", characterisation "reply between reset and first trigger" |
| M4 | success branch never flips `_isFirstTime` false | `-        _isFirstTime = false;` under `statusCode == 200` | RED: 8 tests (re-arm, settling release, detector control, once-per-entry, rearmOrderTaxForBasketChange, 2 characterisation) |
| M5 | failure branch flips `_isFirstTime` false | `+        _isFirstTime = false;` after `_orderTaxAttempts++` | RED: "non-200 keeps latch armed, 3 attempts, one paired [FAIL]", "failing second entry stays armed" |
| M6 | drop `_orderTaxInFlight = false` from `resetOrderTax` | `-    _orderTaxInFlight = false;` | RED: the two characterisation tests that dispatch a second entry while the first entry's reply is held (in-order, out-of-order) |
| M7 | re-arm only in `rearmOrderTaxForBasketChange` | identical diff to M1 (base already re-arms there) | RED, same set as M1. M7 == M1 by construction on this tree |
| M8 | add `_orderTaxEpoch++` to `resetOrderTax` (the TL's epoch question, not a bug) | `+    _orderTaxEpoch++;` after the re-arm | RED: the 3 CHARACTERISATION tests (see below); every other test stays green. Not part of the fix |
| M9 | `update(['checkout_pricing'])` inside `resetOrderTax` | `+    update(['checkout_pricing']);` | RED: "re-arms without notifying listeners" (`addListenerId('checkout_pricing')`) |
| M10 | `_isFirstTime = false;` in the reset (inverse) | `-/+` on the re-arm line | RED: 13 of 15 |
| M11 | drop `_resetCodVerdict()` from `resetOrderTax` | `-    _resetCodVerdict();` | SURVIVES the new file (the line is pre-existing, not this ticket's). KILLED by the pre-existing `checkout_cod_full_amount_verdict_test.dart` "resetOrderTax drops the verdict and the captures" (run: 41 pass, 1 RED) |
| M12 | `_isFirstTime = _orderTaxAttempts == 0;` | line replaced | SURVIVOR, equivalent: `_orderTaxAttempts = 0;` runs 4 statements above in the same method, so the condition is always true |
| M13 | `if (!_orderTaxInFlight) _isFirstTime = true;` | line replaced | SURVIVOR, equivalent: `_orderTaxInFlight = false;` runs on the line above in the same method, so the condition is always true |
| M15 | success branch flips the latch only when the tax is non-zero | `-/+` on the `_isFirstTime = false` line | RED: "a zero-tax success settles Place Order and the next entry still re-fetches" (test added to kill it; first version of the file did not) |
| M16 | delete `Get.find<PricingSummaryController>().resetOrderTax();` from `CheckoutScreen.initCall` (scratch copy of `checkout_screen.dart`) | `-    Get.find<PricingSummaryController>().resetOrderTax();` at checkout_screen.dart:233 (hunk `@@ -230,7 +230,6 @@`, diff pristine vs mutated printed) | RED: `checkout_screen_widget_test.dart` "NEARS-4053 ... a latch left false by an earlier success is armed again and getOrderTax dispatches exactly once" fails at `expect(pricing.isFirstTime, isTrue)` (screen mounted, latch still false). Restored copy byte-identical to the worktree file (`diff -q`); the test is GREEN on the fixed tree (1 pass; file 9 pass). Killed by the new widget test; the 15 direct-call tests alone did not kill it |

## M8 detail (answer to the TL epoch question)

On the fixed build (no epoch bump) the characterisation tests pin: (a) a stale reply landing between the new entry's reset and its
first trigger flips the latch so the new entry never fetches (1 call), (b) in-order replies settle the new entry early with the old
tax, (c) out-of-order replies leave the old entry's tax as the final value. With M8 (`_orderTaxEpoch++` in `resetOrderTax`) all three
become correct (2 calls; still settling after the stale reply; final tax = the new entry's). Side effect probed in scratch: the
dropped stale reply's `finally` clears `_orderTaxInFlight` while the new fetch is in flight, so a rebuild then dispatches ONE extra
get-Tax (3 calls total, final state still correct). That is the same trade-off `rearmOrderTaxForBasketChange` already accepts.

Total test (F3): on M1 it still fails, at the `total == 22.0` assertion (20.0 on base) before reaching the new COD assertions, so the quote-amount and no-"not scheduled" assertions are exercised only on the fixed tree (green).

Scratch copies deleted after the runs.
