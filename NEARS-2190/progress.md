# NEARS-2190 QA progress

Device: emulator-5556 (Android). Build: worktree
/Users/Apple/Projects/nears-NEARS-2190-payment-back-debuglocked, branch
fix/NEARS-2190-payment-back-debuglocked. Fix cycle: 1.

## AC1 — back press shows exit dialog, no crash
- Entry path tried: **Wallet Add Fund** (Profile > My Wallet > Add Fund > Razor
  pay > Add Fund -> PaymentScreen w/ addFundUrl set).
- Hardware back press -> FundPaymentDialogWidget ("Do you want to cancel this
  add fund?") appeared, no crash, no [FAIL]/AndroidRuntime FATAL in logcat,
  app pid unchanged. Screenshot: ac1-fundpaymentdialog-appears-on-back.png
- Checkout (order) entry path: UNREACHABLE in this env — business_settings
  razor_pay/paypal/stripe all status=0 (COD-only checkout sheet, verified via
  read-only DB query). Screenshot: checkout-cod-only-config-limitation.png
- Subscription entry path: UNREACHABLE — no store with
  store_business_model='subscription' in seed data.
- So only 1 of 3 entry paths was live-reachable; PaymentBackGuard wiring is
  identical for all three (_exitApp() branch only changes the DIALOG
  constructed, not the guard), so this is real but partial coverage.

## AC2 — rapid repeat back-press: FAIL (real defect found)
- Single back-press, clean each time: exit dialog appears within 1s. 2/2 trials.
- RAPID DOUBLE back-press (`adb shell input keyevent KEYCODE_BACK` x2,
  ~100-190ms apart): exit dialog does NOT appear for 40+ seconds (confirmed
  idle-poll, spinner still actively re-rendering so frames ARE pumping) --
  reproduced 3/3 trials. A THIRD back-press then reveals the dialog
  immediately. No crash/exception/AndroidRuntime FATAL in logs at any point;
  app pid never changes -- this is a STALL/WEDGE, not a crash.
- PaymentBackGuard's OWN latch logic is proven correct in
  payment_back_guard_test.dart (synchronous fake scheduler) -- the defect is
  in the interaction between the real WidgetsBinding.addPostFrameCallback
  and Android's back-gesture dispatch under rapid repeat presses, which the
  unit tests (fake scheduler) cannot see. See bug-rapid-back-wedge.png
  (screenshot taken mid-wedge, ~20s after the double back-press, still on
  the bare "Processing payment" spinner with no dialog).
- This directly violates AC2 ("does not wedge navigation").

## Barrier-dismiss + repeat back-press (regression point, most important per ticket)
- PASS. Barrier-tap-dismissed the dialog (tap in the grey scrim, well
  outside the card -- NOT the a11y "Dismiss" node, whose reported bounds are
  full-screen and land on the card per NEARS-1802's documented trap).
  Screenshot: regression-barrier-dismiss-state.png
- Pressed back again (single) -> dialog reappeared instantly. Confirms the
  reset-on-settle latch works; NOT the one-shot-wedge failure mode the ticket
  worried about.

## Dialog action button
- "Cancel Add Fund" tapped -> navigated back to Wallet screen correctly, no
  crash, no wallet balance mutated (cancel path only).

## NAppBar back arrow (direct tap, deliberately unguarded)
- Tapped the appbar back arrow directly (not hardware back) from the bare
  PaymentScreen (spinner) state -> dialog appeared immediately, same as
  pre-fix behavior. Works correctly, unaffected by the guard.

## AC3 — no new silent failure path
- Confirmed: guard is a pure UI-thread no-op guard, no new error/catch path
  introduced. flutter test on the touched dir (test/features/payment/, 24
  tests) all green.

## Automated backstop
- `flutter test test/features/payment/` -- 24/24 pass (includes the new
  payment_back_guard_test.dart, 3/3 pass).
