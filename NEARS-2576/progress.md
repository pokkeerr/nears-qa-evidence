# NEARS-2576 QA progress

Device: emulator-5564 (Android), UserApp worktree
`nears-NEARS-2576-order-successful-reskin`, branch `feat/NEARS-2576-order-successful-reskin`,
HEAD 794902529. Backend: primary `Admin/` (`php artisan serve --port=8000`), local
`multi_food_db`, read-only.

## Headline finding (governs AC2–AC6 verdicts)
`order_successful_screen` is reachable via live app navigation on mobile **only** through a
completed digital-payment gateway round trip (`order_service.dart` `paymentRedirect()` /
`_redirection()`), which requires the closed-source `Admin/Modules/Gateways` add-on. That module
is physically absent from this repo/environment (standing, documented constraint — see
`CLAUDE.md` "nwidart modules"). Confirmed live: two real digital-payment orders (91141, 91142)
both dead-ended at `{baseUrl}/payment-mobile` with a raw `gateways_default_204` JSON response —
the webview never reaches `/payment-success` or `/payment-fail`/`-cancel`, so neither
`order_successful_screen` (paid) nor `digital_payment_failed_screen` (full-screen) is ever
entered for a genuine unsettled/failed digital order. COD/wallet/offline checkout on mobile
routes straight to Track Order (NEARS-517), never to this screen either.
**Precedented:** NEARS-403 QA hit the identical wall on this exact screen and recorded
`PASS(code)` / "unreachable live" for its analogous success/failure surfaces.

## Per-AC status
- AC1 (skeleton) — code+test verified; live entry blocked (see above).
- AC2 (NErrorRetry + retry recovery) — code+test verified; live entry blocked.
- AC3 (failure dress, 3 buttons incl. Retry Payment) — code+test verified; live entry blocked.
- AC4 (Retry Payment routes to digital_payment_failed_screen) — code+test verified (route-push
  assertion); the DESTINATION screen's own recovery mechanics (Switch to COD / Cancel Order) were
  exercised LIVE and worked cleanly (see DB evidence log) — only the exact tap-from-
  order_successful hop is unreachable live.
- AC5/AC6 (success dress unchanged, group prefix) — code+test verified; live entry blocked.
- F2 (cancelled order excludes Retry Payment) — **live DB precondition reproduced** (order 91142:
  order_status=canceled, payment_method=digital_payment, payment_status=unpaid) — proves the
  scenario is real, not hypothetical. FE gate verified via code + the ticket's own widget test
  (asserts button absent AND `getPaymentFailedDetails` never called).
- F1 (recovered retry re-runs group fetch) — code+test verified; live entry blocked.

## Automated backstop
`flutter test test/features/checkout/order_successful_screen_test.dart` — 7/7 passing, one
testWidgets per AC/finding (F1, F2 explicitly named and asserted). `flutter analyze` on the
touched file — no issues.

## Live regression sweep (checkout → payment webview → recovery)
Signed in (qa.singlestore@nears.com, zone 3), added items from the zone-3 fixture store (id 59,
digital_payment=1 zone), full checkout twice with Paypal selected, drove the payment webview,
backed out through `PaymentScreen` → `PaymentFailedDialog`, exercised both "Switch to Cash On
Delivery" (order 91141) and "Cancel Order" (order 91142). `ui_errors` clean (0 matches) across
the whole session. No red-screens, no overflow, no unexpected `[ERR]`/`[FAIL]`.

## Evidence files
- `gateway-broken-204-response.png` — the dead-end webview response.
- `checkout-payment-method-picker.png`, `checkout-cod-only-zone2.png`,
  `zone3-fixture-store.png`, `payment-processing-placeholder.png` — flow screenshots.
- `live-db-evidence.log` — read-only SELECTs proving both order states.
- `flutter-test-output.log` — full widget-test run.
