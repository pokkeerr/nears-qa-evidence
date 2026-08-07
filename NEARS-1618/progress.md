# NEARS-1618 QA progress (live)
Device: emulator-5556 | pre-installed build com.izzes.nears vN 3.8.0 (versionCode 3, installed 2026-08-07 09:07:38, provenance UNKNOWN)
Account: robert.taylor@demo.com (user 5) — already-authenticated session; Add Fund gating is config-only, not user-scoped.
Baseline DB: wallet_payments=0, payment_requests=2

- [AC4-a] Wallet screen renders "Add Fund" affordance — OBSERVED (ac4-01-wallet-screen-add-fund.png)
- [AC4-b] Add Fund dialog opens with 2 selectable methods (Paypal, Razor pay) — OBSERVED (ac4-02)
- [AC5-pre] Both radios EMPTY on open, no pre-selection (activePaymentMethodList.length==2 so initState auto-select does not fire) — OBSERVED (ac4-02 / ac5-01)
- [AC5] amount=50, no method -> toast "Please select payment method"; stack pins add_fund_dialogue_widget.dart:225 (3rd branch). Reproduced 4x. — PASS (ac5-02, ac5-03)
- [SWEEP] Bonus banner: NOT shown. Correct — gated on fundBonusList.isNotEmpty AND addFundStatus (lines 20-23), and wallet_bonuses has 0 rows. Brief said "addFundStatus alone" = drift.
- [SWEEP] Checkout: shows Cash on Delivery, NO digital auto-select. But digital section absent entirely — zone 2 (Abu Dhabi) has zones.digital_payment=0, store "Fresh supermarket" is zone 2. Auto-select check therefore VACUOUS, reported as such.
- [SWEEP] Gateway tiles render generic placeholder (gateway_image null) — expected, not filed.
- [BUILD PROVENANCE RESOLVED] runtime stack line 225 == please_select_payment_method on feat/userapp-reskin2; on feat/NEARS-1616 branch line 225 is please_provide_transfer_amount (its select-method line is 229). Installed build therefore matches the checked-out branch, NOT the 1616 branch.
- [DB] final wallet_payments=0, payment_requests=2 — unchanged from baseline. No payment completed.
- [AUTOMATED] phpunit --filter ConfigContractTest: 4/4 OK, 147 assertions.
