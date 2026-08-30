# NEARS-2636 QA progress

Device: emulator-5556, worktree nears-NEARS-2636-payinwevview-override, package com.izzes.nears.nears_nears_2636_payinwevview_override

## AC1 (default build -> PaymentScreen) -- PASS
- No --dart-define. `flutter run -d emulator-5556` via scripts/qa-run.sh.
- Reach: switched delivery address to "Demo Zone -- Dhaka" (customer_addresses.id=46, zone_id=1,
  digital_payment=1) -- default Abu Dhabi address's cart store (zone_id=2, digital_payment=0)
  never surfaces "Pay Via Online" (NEARS-2635 zone-scoped checkDigitalPaymentActive gotcha,
  already documented in userapp-navigation-guide.md). Switching address surfaced a pending
  order #91146's PaymentIncompleteBottomSheet automatically -> "Pay Now" -> PaymentMethodBottomSheet
  showed Paypal/Razor pay ("Pay Via Online"). Selected Paypal -> Proceed.
- Result: InAppBrowserActivity opened (gateway sandbox 204 "information not found" JSON --
  expected, no live Paypal gateway configured on dev backend, unrelated to this ticket).
  Closed browser (system back) -> landed on Flutter MainActivity, AppBar title == "Payment"
  (payment_screen.dart's NAppBar) -- confirms PaymentScreen, NOT PaymentWebViewScreen.
- Logs: grepped qa-run-default.log for [FAIL]/[ERR]/Exception -- only pre-existing unrelated
  Facebook GraphResponse (deleted FB app in SDK config) + GoogleCertificatesRslt warnings.
  Clean re: this flow.
- Evidence: docs/qa-evidence/NEARS-2636/ac1-default-build-paymentscreen.png

## AC2 (override build -- PAY_IN_WEBVIEW=true -> PaymentWebViewScreen) -- PASS
- `flutter run -d emulator-5556 --dart-define=PAY_IN_WEBVIEW=true` (NEARS_PKG_SUFFIX env var set
  to match the same per-worktree package as AC1's install: com.izzes.nears.
  nears_nears_2636_payinwevview_override -- session/login preserved across the two builds).
- Reach: same order #91146 payment-incomplete flow -> Pay Now -> Paypal -> Proceed.
- Result: `adb shell dumpsys activity activities | grep ResumedActivity` stayed on
  MainActivity (Flutter) throughout -- no separate InAppBrowserActivity this time (confirms
  PaymentWebViewScreen embeds flutter_inappwebview as a WIDGET, not a launched native browser
  Activity, unlike PaymentScreen's flow). AppBar showed ONLY a "Back" node, empty title --
  matches payment_webview_screen.dart's `NAppBar(title: '', ...)` exactly, and matches NEARS-2623
  QA's documented distinguishing signal. Same gateway sandbox 204 JSON rendered inside the
  embedded webview (Chrome "Pretty-print" viewer) -- gateway-not-configured, expected/unrelated.
- Logs: 0 [FAIL]/[ERR] lines (excl. pre-existing Facebook GraphResponse noise) across the whole
  override-build session.
- Evidence: docs/qa-evidence/NEARS-2636/ac2-override-build-paymentwebviewscreen.png

## AC3 (exit-dialog + retry/connectivity sanity, override build) -- PASS (exit-dialog); retry/
## connectivity UI not re-exercised this session (see note)
- Single back-press on the live PaymentWebViewScreen (reached via normal navigation, not
  constructed directly) fired the GuardedExitDialog immediately: "Are you agree with this order
  fail?" / "Cancel Order" / "Switch to Cash On Delivery" -- exact NEARS-2623 fix, working live.
  Tapped "Cancel Order" -> cleanly navigated back to Home, no crash, no [FAIL]/[ERR].
- Evidence: docs/qa-evidence/NEARS-2636/ac3-exit-dialog-live.png
- Retry/connectivity-error UI (NEARS-2579): attempted a second live pass (fresh zone-1 checkout,
  Spice Route Kitchen / Double Bacon Burger) to reach PaymentWebViewScreen again with network
  disabled, but got stuck in a pre-existing multi-store-cart UI quirk (a stale "Proceed to
  Checkout" tap position after the basket list re-rendered around live pending-order status
  tiles) unrelated to this ticket's diff. Not pursued further per the QA scope's own framing
  ("light sanity pass, not new coverage -- the underlying logic is already unit-tested and green,
  13/13"). The exit-dialog demonstration above already proves the KEY claim this AC exists to
  verify (PaymentWebViewScreen's interactive logic still functions once actually reachable via
  normal navigation) -- retry/connectivity UI is the same already-shipped NEARS-2579 file, not
  touched by this ticket's diff, and is covered by the existing green unit suite.

## Automated backstop
`flutter test test/features/payment/payment_webview_exit_dialog_routing_test.dart` -- 3/3 passing
(matches engineer's build-time run).

## Regression / AC4 (default build no new bug)
Default-build session (AC1) ran clean end-to-end: login, home, wallet, checkout, payment method
sheet, PaymentScreen resolution -- 0 [FAIL]/[ERR] from the const-flag mechanism itself.
