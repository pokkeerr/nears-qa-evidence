# NEARS-2235 QA progress (fix-cycle 0, first pass)

Worktree: /Users/Apple/Projects/nears-NEARS-2235-payment-route-encode
Branch: feat/NEARS-2235-payment-route-encode

## AC1 — Uri.encodeComponent applied; &-bearing value round-trips
**met: true**
Ran `~/Tools/flutter/bin/flutter test test/helper/route_helper_payment_route_encode_test.dart`
in the worktree UserApp dir. Output:
```
00:00 +0: getPaymentRoute encodes subscriptionUrl/addFundUrl an &-bearing subscriptionUrl round-trips to the original value
00:00 +1: getPaymentRoute encodes subscriptionUrl/addFundUrl an &-bearing addFundUrl round-trips to the original value
00:00 +2: getPaymentRoute encodes subscriptionUrl/addFundUrl an &-bearing input creates no phantom sibling params — same count as a plain-URL call
00:00 +3: getPaymentRoute encodes subscriptionUrl/addFundUrl normal (non-&-bearing) URLs are unchanged for existing callers
00:00 +4: getPaymentRoute encodes subscriptionUrl/addFundUrl null subscriptionUrl/addFundUrl still round-trips to the literal 'null' sentinel
00:00 +5: All tests passed!
```
Also re-read the diff directly (`git diff HEAD -- UserApp/lib/helper/route_helper.dart`)
— scoped exactly to `getPaymentRoute`'s `add-fund-url=`/`subscription-url=`
interpolation, matching the ticket description. No other line touched.

## AC2 — no phantom sibling params
**met: true** — same test file, test 3 (`+2` above): asserts
`ampersandCount == plainCount == 15` (id + 14 named params). Green.

## AC3 — live regression on checkout / wallet top-up / subscription
**met: unverifiable — BLOCKED on device pool exhaustion, not a code defect.**

Static/code-path verification performed (all clean, no findings):
- Located and read all 3 caller call sites:
  - `checkout_controller.dart:1326,1378,2118` — call `getPaymentRoute` with
    NO `addFundUrl`/`subscriptionUrl` arg (null-sentinel path only) — unaffected
    by the encode change other than the harmless '`null`' sentinel unchanged
    (pinned by AC1 test 5).
  - `wallet_controller.dart:169` — `addFundUrl: redirectUrl` from
    `POST /api/v1/customer/wallet/add-fund` (`redirect_link` in response).
  - `business_service.dart:97` — `subscriptionUrl: redirectUrl` from the
    business-plan submission response.
- Confirmed the consuming `GetPage(name: payment, ...)` block
  (`route_helper.dart` ~805-862) never manually splits the query string — it
  goes through GetX's own `Uri.parse` + `queryParameters` (percent-decodes),
  matching exactly what `Uri.encodeComponent` at construction expects on the
  decode side. No GetPage/PaymentScreen/PaymentWebViewScreen code needed to
  change and none did (confirmed via diff).
- Ran the existing widget/controller test suites for the 3 surfaces as an
  automated regression backstop (in addition to the 2 unit-test ACs above):
  `flutter test test/helper/route_helper_config_gate_test.dart
  test/features/wallet/wallet_controller_test.dart
  test/features/checkout/checkout_controller_test.dart` → 45/45 green, no
  failures, no `[FAIL]`/`[ERR]` lines.
- Confirmed (DB + code) that the real payment-gateway completion step is
  genuinely QA-inaccessible in this dev env regardless of device: `Modules/Gateways`
  is physically absent (`Admin/modules_statuses.json` marks it enabled but
  `Admin/Modules/` contains only `AI`/`TaxModule`), so every gateway route
  (`payment/<x>/pay`) that `Payment::generate_link` (`Admin/app/Traits/Payment.php`)
  would redirect to is unroutable — matches the ticket's own note. This
  confirms the task's log/widget-tree-inspection substitute would in fact have
  been the ceiling reachable even with a device, for the "complete a real
  gateway" part specifically — but NOT a substitute for the base "does the app
  navigate to PaymentScreen/PaymentWebViewScreen with the correct un-truncated
  URL" smoke, which still needs a live app+device to observe.

**Device attempt (all failed — pool exhausted, not code-related):**
- `emulator-5554`, `emulator-5556`, `emulator-5558` (documented pool) +
  `emulator-5564` (attached, drift — see below) all probed via
  `qa-lock-guard.sh`. None carry a lock file, but ALL 4 are being actively
  driven by foreign, long-running `flutter run --debug` sessions (process
  `ps` elapsed times: 44 min, 8h04m, 8h03m, 7h51m — genuinely live, not
  stale/reclaimable per NEARS-1805).
- Bounded-waited ~9 minutes (two poll cycles, 240s + 300s, well within the
  documented ≤10 min cap) re-probing all 4 devices every 30s. No device
  freed.
- No lock was ever acquired by this QA session (all `qa_lock_acquire` calls
  returned non-zero: REFUSING on a relative source path once, then OCCUPIED
  on all 4 absolute-sourced attempts) — nothing to release on exit.

**drift noted:** profile documents the Android pool as
`emulator-5554/5556/5558` (+ `emulator-5560` broken bridge, excluded).
Live `adb devices` shows `emulator-5554/5556/5558/5564` — no `5560` attached
at all, `5564` present instead. Flagged in envelope `drift[]`.

## Automated backstop
`flutter test test/helper/route_helper_payment_route_encode_test.dart
test/helper/route_helper_config_gate_test.dart
test/features/wallet/wallet_controller_test.dart
test/features/checkout/checkout_controller_test.dart` → **50/50 passed**, 0 failures.

## Verdict
BLOCKED — AC1/AC2 fully demonstrated live (PASS). AC3 could not be
demonstrated live because the entire device pool was occupied by other
live sessions for the whole bounded wait; nothing in the change itself
failed any check performed. No task_bugs, no regression_bugs found.
Recommend re-QA of AC3 alone the moment a pool device frees — the fix
itself is not in question.
