# NEARS-1483 — Phase [8] live QA record

- **Verdict: FAIL**
- Device `emulator-5558` (lock acquired via `qa_lock_guard`, pid 76513, kind `anchor`)
- Build under test: `fix/NEARS-1483-payment-webview-error-state` @ `8f2eb548`, debug APK
  (142,108,867 bytes), installed 16:02:13 — `adb install -r` returned `Success`, and
  `lastUpdateTime` advanced `14:51:18 → 16:02:13`, so the tested bytes are this branch's.
- Account: `emily.johnson@demo.com` (Emily Johnson), zone 1, wallet 25 AED (unchanged by QA).
- Backend: local `php artisan serve` :8000, `baseUrl = http://10.0.2.2:8000` (real, not demo).

## Headline finding

`PaymentWebViewScreen` — the only widget this ticket changed — **is never constructed at
runtime**. `route_helper.dart:840` builds it only when `AppConstants.payInWevView` is true;
that is `static const bool payInWevView = false`, identical at base `fa3a77ca` and at HEAD
(this ticket touched neither `app_constants.dart` nor `route_helper.dart`). Every payment
entry point — checkout, wallet, subscription — funnels through that single `GetPage`, so the
proof covers all three at once. The live surface is `PaymentScreen` + `MyInAppBrowser` in
`payment_screen.dart`, which still has no `onReceivedError`/`onReceivedHttpError`, no
`NErrorRetry` and no `_loadErrorKind`. AC1/AC2/AC3 are therefore not observable on the app.

## Per-AC

| AC | Result | Falsifier available? | Evidence |
|---|---|---|---|
| AC1 branded error state | **NOT MET** | yes, and it fired | Real main-frame failure (`net::ERR_EMPTY_RESPONSE`) rendered Android's platform error page; no branded state, no Retry |
| AC2a Retry re-attempts | **NOT MET** | n/a — CTA never rendered | overlay never appears |
| AC2b `back` → dialog identity | **NOT MET** (blocked twice) | yes | overlay CTA absent; and the changed `_exitApp` gate would pick `PaymentFailedDialog` on the wallet path because `plugin_payment_gateways=false` |
| AC3 PII-safe `AppLogger.failure` | **NOT MET at runtime** | yes | 0 Flutter log lines during a real failure; helper's only callers are in the dead widget |

## Controls

- **Negative control (sub-resource 404 must not raise):** main frame 200 + four 404
  sub-resources (png/js/css/ico), proven delivered by the proxy access log. No overlay, no
  new `[FAIL]`. **Recorded as NO-COVERAGE, not a pass** — the positive control below shows the
  overlay could not have appeared for any input, so the negative result is vacuous on device.
  The `isForMainFrame == false` branch remains unit-pinned and mutation-proven.
- **Positive control (same instrument, main-frame 404):** also produced no overlay → the
  instrument could not have produced a pass, which is what exposed the headline finding.
- **Instrument liveness:** CDP `Page.navigate` to a `payment-cancel` URL drove the app out of
  the payment screen to Wallet, proving the navigation reached Dart.

## Automated backstop

- `flutter test test/features/payment/payment_webview_failure_gate_test.dart` → **5/5 passed**
- `flutter test` (whole UserApp) → **3950 passed, 2 skipped, 0 failed**

## Regression sweep (bounded — this screen + its entry points)

Clean end-to-end wallet→payment load after restoring the environment: gateway page rendered
(`Pay`/`Cancel`), **0** `[FAIL]`/`[ERR]`/`EXCEPTION CAUGHT`/`RenderFlex overflow`. Nothing is
broken by the change — it is inert at runtime.

## Not covered, and why

- ar/RTL strings, landscape+Arabic overflow geometry, spinner-exclusion, tap-through,
  double-tap Retry latch, `NAppBar` back with overlay up: all require the overlay to render.
  **NO-COVERAGE**, not pass.
- Checkout entry path: not driven — it needs a real `Place Order` (DB mutation, forbidden by
  the read-only rule). Covered structurally instead: the single `GetPage` proof above.
- Dark mode: deferred by policy, not checked.

## Environment note (drift from the brief)

- Free `/data` on 5558 measured **1,205,380 KB (~1.15 GB)**, not the ~832 MB briefed. No
  install pressure; install succeeded first try.
- The briefed `svc data disable` + `svc wifi disable` recipe **cannot fail this screen**: the
  gateway page comes from `10.0.2.2:8000` and app assets ride the `adb reverse tcp:80`
  tunnel, neither of which depends on wifi/data. Replaced with a local reverse proxy
  (NEARS-1862 recipe) + CDP-driven main-frame loads.
