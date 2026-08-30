# NEARS-2634 QA progress checkpoint

Device: emulator-5554 (worktree `nears-NEARS-2634-payment-appbar-back-guard`, package
`com.izzes.nears.nears_nears_2634_payment_appbar_back_gua`).

## Environment note
`add_fund_status` business_setting = 0 on the shared dev backend (port 8000) at run start —
verified via DB read + live `/api/v1/config` — hides the Wallet screen's "Add Fund" button
(front-end-only gate; the `add-fund` backend endpoint itself only checks `digital_payment`,
confirmed by reading `Admin/app/Http/Controllers/Api/V1/WalletController.php::add_fund`). Per
the project's own established precedent for this exact situation (nav guide "Refund Request"
NEARS-2592 addendum: front door gated by a `business_settings` flag QA may not flip → drive the
underlying controller method directly over the Dart VM Service `evaluate` RPC instead), reached
the flow via `Get.find<WalletController>().addFundToWallet(1.0, 'paypal')` evaluated live against
the running debug isolate — this calls the EXACT same production method the hidden button would
have called (real backend POST, real PayPal sandbox redirect, real `Get.toNamed` into
`PaymentScreen` with a real `addFundUrl`), so every AC downstream is demonstrated against genuine
app behavior, not a mock. No DB write was made. Flagged as `drift[]`/environment gap, not a
product defect.

## AC1 — PASS
Reached PaymentScreen (AppBar title "Payment") after closing the PayPal InAppBrowserActivity.
Single tap on AppBar "Back" → `FundPaymentDialogWidget` appeared with exact strings
"Cancel Add Fund" / "Do you want to cancel this add fund?". Logs clean (no [FAIL]/[ERR]/Exception
in pid-scoped logcat). Evidence: ac1-cancel-add-fund-dialog.png

## AC2/AC3 — PASS
Single tap on "Cancel Add Fund" → landed exactly one level back on WalletScreen (title "Wallet",
"Wallet Amount", "Wallet History" visible) — not Profile, not an unchanged dialog. Logs clean.
Evidence: ac2-ac3-lands-on-wallet.png

## Rapid double-tap race (finger-bounce speed, the actual race this fix closes) — PASS
Fresh PaymentScreen mount (fresh wallet-add-fund via VM eval as above), then
`adb shell "input tap 120 249; input tap 120 249"` (back-to-back, no delay) on the AppBar back
arrow. Only ONE `FundPaymentDialogWidget` mounted (node count matches the single-tap case exactly,
12 nodes / 3 labelled — no stacked duplicate). A single subsequent tap on "Cancel Add Fund" landed
cleanly on WalletScreen in one step (25 nodes matching the plain Wallet screen dump) — this is the
exact pre-fix defect scenario (2 stacked dialogs, 1st Cancel only unwinds one, 2nd Cancel
over-pops to Profile) and it is now closed: the `_popping` latch absorbed the re-entrant 2nd
AppBar tap. Logs clean both times. Evidence: rapid-double-tap-single-cancel-lands-wallet.png

## Spot-check — non-wallet order-payment path — PASS
Real single-store checkout (The Grill House, Double Bacon Burger x2) with payment method switched
to "Digital Payment (Paypal)" via the checkout screen's own payment-method picker → Place Order →
InAppBrowserActivity (PayPal) → closed via back → PaymentScreen (AppBar "Payment", no
addFundUrl/subscriptionUrl). Single AppBar-back tap → `PaymentFailedDialog` ("Are you agree with
this order fail?" / "Cancel Order" + "Switch to Cash On Delivery"). Single tap "Cancel Order" →
dismissed cleanly, landed on the store's item list (sensible prior screen), no second tap needed.
Logs clean both times. Same shared `onBack`/`_exitApp()` callback as the wallet path, confirming
the fix's guard applies uniformly. Evidence: spotcheck-order-payment-failed-dialog.png

## Regression sweep — PASS, no regressions
1. **Guarded system-back, wallet path:** fresh PaymentScreen mount (wallet add-fund), single
   system BACK key → `FundPaymentDialogWidget` appeared correctly in one interaction. Logs clean.
2. **Barrier-tap dismiss:** tap outside the dialog card (1272,300) → dialog dismissed, back on
   PaymentScreen (guard re-armed). Logs clean.
3. **~500ms double-back-press (baseline, NOT re-litigated per NEARS-2346 owner ruling):** back,
   sleep 0.5s, back → 2nd press landed on the already-settled/interactive dialog and dismissed it
   via normal back semantics — exactly the ruled non-defect behavior, unchanged by this fix. Logs
   clean.
4. **Guarded system-back, order-payment path:** fresh checkout (Razor pay), single system BACK →
   `PaymentFailedDialog` appeared correctly in one interaction. Logs clean.

## RTL sanity (Arabic, `Get.updateLocale('ar','SA')` via VM eval) — PASS
Wallet add-fund flow reached in Arabic. Rapid double-tap (finger-bounce) on the AppBar back arrow
(`رجوع`) → single `FundPaymentDialogWidget` (Arabic: "إلغاء إضافة صندوق" / "هل تريد إلغاء هذا
الصندوق الإضافي؟"), no stacked duplicate (node signature matches the single-dialog case). Single
tap on the Arabic Cancel button → landed one level back, no over-navigation. Logs clean both
times. Locale restored to English afterward. Evidence: rtl-sanity-arabic.png

## All demonstrations complete — verdict PASS. Automated backstop (not re-run, engineer +
code review already verified green): `payment_appbar_back_guard_test.dart` 1/1,
`payment_back_guard_test.dart` 4/4 (pre-existing, unmodified).
